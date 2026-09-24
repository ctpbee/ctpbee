# agentic.md — ctpbee fork: architecture, conventions, and local changes

Working notes for AI agents and developers on this local editable checkout of
[ctpbee](https://github.com/ctpbee/ctpbee). **Violating the conventions below
silently corrupts tick data or breaks hot-path throughput.**

## What this fork feeds

This checkout is the market-data engine of the local "hive" stack:

- `hive_recorder` (in the `hive` repo) embeds a `CtpbeeApi` extension and
  streams every tick to the hive gRPC server;
- `ctpbee.date.trade_dates` is the source of the futures trading calendar
  (via `hive/extral_update/update_trading_date.py` → hft DB `trading_date`
  table, and as the recorder's in-process gate `_is_trading_time`);
- `.ctpbee/contract/*.json` feeds `hive_tool`'s `contracts` table
  (pricetick / multiplier for slippage and PnL).

Changes here are **upstreamable by design**: minimal diffs, behavior-preserving,
English comments explaining motivation and equivalence.

## Architecture map

```
C++ CTP callbacks (interface/<broker>/md_api.py, td_api.py)
  └─ onRtnDepthMarketData → build TickData → Event → blinker signal
       common_signals.tick_signal            (module-level, tick/bar/timer)
       app.app_signal.<event>_signal         (per-app: order/trade/...)
  └─ Recorder (record.py, the data center)
       process_tick_event (@call decorator, helpers.py)
       ├─ LocalPositionManager.update_tick (data_handle/local_position.py,
       │    one dict lookup; PositionHolding recomputes pnl only when the
       │    price / position signature changed — see changelog 2026-08-21b)
       ├─ app.tools[*].on_tick(tick)
       └─ app._extensions → CtpbeeApi subclasses (e.g. hive_recorder)
```

| Module | Role |
|---|---|
| `app.py` | `CtpBee` container: config, extensions, tools, engine lifecycle |
| `interface/ctp`, `ctp_rohon`, `ctp_mini` | Broker adapters (MD = market data, TD = trading). The three `md_api.py` copies share the same tick-parsing shape — keep them in sync |
| `constant.py` | `Entity` data objects (`TickData`/`OrderData`/...) under `@frozen` attribute protection; `Event` |
| `record.py` | `Recorder`: latest tick/order/trade per symbol, local position manager, fan-out to tools + extensions |
| `signals.py` | blinker signals; common (tick/bar/timer) vs per-app |
| `helpers.py` | `call` decorator (event → extension dispatch), shared utilities, `build_tick_datetime` |
| `func.py` | `Hickey` 7×24 process manager (`auth_time` session gating; hive_recorder shifts open times by −300 s), legacy `get_current_trade_day` (hive uses its own calendar) |
| `date.py` | Hardcoded `trade_dates` list (1990 → **2026-12-31**, see risks) |

## Hot-path optimization (2026-08-21, this branch)

Per-tick Python-side fixed cost: **~412 µs → ~3.4 µs** (~120×). Two changes:

1. **`build_tick_datetime()` in `helpers.py`** replaces the per-tick
   `datetime.strptime` in all three interfaces:
   - caches the `(year, month, day)` tuple per `ActionDay` (constant within a
     session; cache grows a few entries per day, keyed by `date.today()` for
     the fallback so midnight rolls over automatically);
   - direct `datetime(...)` construction (~0.3 µs vs ~3.7 µs);
   - **millisecond quantization to 100 ms is preserved deliberately**
     (`int(UpdateMillisec / 100)` legacy semantics: 550 ms → `".5"` → 500 ms).
     Changing to full ms precision is a downstream contract decision
     (dedup keys, minute-bar boundaries), not a free fix;
   - DCE branch (`use_today=True`): ActionDay is the trading day on DCE, so
     local today + UpdateTime is used (upstream issue #165);
   - empty/invalid ActionDay falls back to today — the old code raised
     `ValueError` here, the only intentional behavior delta.
2. **`constant.py`**:
   - `__set_attr__` (the `@frozen` guard) now reads the caller function name
     via `sys._getframe(1).f_code.co_name` instead of
     `inspect.getframeinfo(...)`: identical semantics (same frame's function
     name, same underscore-prefix allow rule, same error message),
     ~14 µs → <1 µs per attribute write;
   - `Entity.__init__` writes constructor kwargs with one
     `self.__dict__.update(mapping)` instead of ~40 `setattr` calls —
     equivalent because the guard always allowed `__init__` writes straight
     into `__dict__`; protection after construction is unchanged.

Benchmarks (Windows, Python 3.13): datetime parse 3.7 → 0.3 µs (11×);
`TickData` construction 408 → 3.1 µs (130×).

### Verified equivalence

`tests/test_hotpath_optimization.py` (run `python tests/test_hotpath_optimization.py`,
no DB / no broker needed): 10/10 checks. The legacy `strptime` implementation
is inlined as the oracle: 100 ms quantization matrix (0/49/50/99/100/550/999),
DCE branch, cache isolation across ActionDays, `@frozen` allow/deny by caller
name, TickData 40-field construction + `__post_init__` `local_symbol` +
`_to_dict`. Import smoke covers all three interfaces (no circular imports).

## Backtest hot path (2026-09-22, this branch)

The 2026-08-21 sweep only covered the **live** market-data path. The looper
(`PATTERN="looper"`) had two per-bar fixed costs on top of that, and they were
bigger by two orders of magnitude:

1. **`VessData.last_bar()` in `looper/data.py`** attempted
   `from data_api import Tick, Kline` **once per replayed bar/tick**. `data_api`
   is an optional package that was never open-sourced (see the `todo` in
   `app.add_basic_info`), so in practice the import always fails — and a
   **failed import is not cached in `sys.modules`**: every attempt walks the
   whole `PathFinder` chain, joining and `stat`-ing each `sys.path` entry.
   cProfile on origin/dev: **9.1 `nt.stat` per replayed bar** (179,823 calls for
   19,800 bars), 76% of the profiled time in `nt.stat` alone and ~93% inside
   `importlib._bootstrap._find_and_load`. The probe result is now cached on
   first use (`data_api_types()`, empty tuple when unavailable, so the
   `isinstance` call site needs no branch).
2. **Trade-day resolution at the end of `LocalLooper.__call__`** linearly
   scanned the 8800-entry `trade_dates` list 1-2 times per tick plus a
   `strptime` — 40-46 µs (day session) / 49-60 µs (night session) per bar.
   Extracted as `trade_day_of()` on top of new O(1) primitives in `date.py`
   (`is_trade_date` / `trade_date_index` over a lazily built `{date: index}`
   map) and memoized per `(calendar day, night session)`, so a whole backtest
   resolves each day at most twice. The date conversion inside is pure
   arithmetic — `date(*map(int, s.split("-")))` — because `date.fromisoformat`
   is 3.7+ while `setup.py` declares 3.6 support (it even installs the
   `dataclasses` backport for 3.6); on 3.6 the night/holiday branch would have
   raised `AttributeError` for every night bar.

Benchmarks (Windows, Python 3.11.16, synthetic minute bars, best of 2-3 reps;
the isolated rows are printed by `tests/test_backtest_hotpath.py` itself, the
end-to-end rows by timing `CtpBee.start()` over a synthetic replay — the
per-call numbers are syscall/cache dependent, so treat them as ranges):

| dataset | origin/dev | + probe cache | + trade-day O(1) |
|---|---|---|---|
| 72,600 bars, 1 contract | 90.7-93.0 s (1.25-1.28 ms/bar) | 4.27 s (59 µs/bar) — 21× | **1.13-1.17 s (16 µs/bar) — ~80×** |
| same, no-op strategy instead of a counting one | 80.8-81.9 s (1.12 ms/bar) | — | **1.11-1.14 s (15.5 µs/bar) — 72×** |
| 139,800 bars, 2 contracts | 177 s | — | **3 s** — 59× |
| trade-day block, isolated | 37.6-45.5 µs (day) / 48.7-60.0 µs (night) | — | 0.11-0.14 µs (≈300-500×) |
| `data_api` probe, isolated | 1.1-1.8 ms/bar | 0.037 µs (cached) | ≤1 probe per process |

**Wall-clock numbers scale with background load.** The rows above come from a
single earlier session; re-measuring the 72,600-bar row on the same machine at
~30 % concurrent CPU gave origin/dev 109.5-138.5 s and this branch 1.36-1.47 s
(19-20 µs/bar), i.e. absolute time drifts up to ~50 % while the paired ratio
stays 77-101×. Quote the rows as ranges; the load-independent claim is the
mechanism — one failing `import` and one 8800-entry linear scan taken out of
the per-bar loop, each measured in isolation.

### Verified equivalence

`tests/test_backtest_hotpath.py` (32 checks) inlines **both** pre-optimization
implementations as oracles and verifies on three levels: exhaustive unit
equivalence (all 8800 calendar dates × 5 session buckets, and every natural day
2025-01-01…2027-01-04 × 5 buckets, comparing return values **and** exception
type+message — 925 exception cases included), observability of the caches (a
`meta_path` counter shows 1 path search per 5000 replayed bars vs 1 per bar
before), and an **end-to-end differential backtest**: the same two-contract,
multi-settlement, long+short run executed by the new code and by the restored
old code, asserting identical `daily_life`, identical trade blotter (uuid order
ids excluded) and identical final balance.

Known pre-existing edges the suite locks instead of fixing: a night bar on the
last calendar day (`2026-12-31`) raises `IndexError`, a non-trading day whose
predecessor is also non-trading raises `ValueError`, and sending an order on the
**first** bar of a backtest raises `AttributeError` because `LocalLooper.datetime`
is only assigned after the bar is dispatched.

## Conventions and known edges (read before touching)

- **`@frozen` rule**: only callers whose function name starts with `_` may
  write `Entity` attributes. Do not weaken the guard; bulk `__init__` writes
  are equivalent precisely because `__init__` was always allowed.
- **DCE timestamps use the local machine date** (`date.today()`) — assumes a
  Beijing-time host. Same class of assumption exists in hive-side code.
- **CTP "no price" sentinels pass through raw** (bid/ask ≈ DBL_MAX on
  limit-locked markets) — normalize downstream if a consumer cares.
- **`date.py` calendar expires 2026-12-31**: after that date the recorder's
  `_is_trading_time`, `update_trading_date.py`, and the `TradingCalendar`
  fallback silently stop recognizing trading days. Replace the calendar source
  (hft `trading_date` table is the intended single source of truth) or bump
  the list before 2027.
- **Keep the three `md_api.py` copies in sync**; shared helpers
  (`build_tick_datetime`) prevent drift for the parsing path.
- **No optional-dependency `import` inside per-tick / per-bar loops.** A
  *failing* import is never cached in `sys.modules`, so it re-walks `sys.path`
  with a `stat` per entry on every iteration (9 `nt.stat` per replayed bar,
  ~80% of backtest wall time until 2026-09-22). Probe once and cache the
  outcome.
- **`trade_dates` lookups must go through `date.is_trade_date` /
  `date.trade_date_index`**, not `x in trade_dates` / `trade_dates.index(x)`:
  the list has 8800 entries and any per-tick linear scan shows up immediately in
  profiles.
- **Per-bar / per-tick code may only use APIs available in the oldest
  interpreter `setup.py` claims (3.6 — it even installs the `dataclasses`
  backport for it).** `date.fromisoformat` / `datetime.fromisoformat` are 3.7+
  and would raise `AttributeError` on every night-session bar; build the date
  arithmetically instead — `date(*map(int, s.split("-")))`.
  `tests/test_backtest_hotpath.py` D4 guards this at source level.

## Test infrastructure (hard rule: every change must land with passing tests)

All suites are standalone scripts (no pytest dependency, no CTP callback, no
real Redis): `python tests/<name>.py` exits non-zero on failure.

| Suite | Checks | Covers |
|---|---|---|
| `test_hotpath_optimization.py` | 10 | `build_tick_datetime` equivalence vs legacy strptime oracle, frozen guard semantics, TickData bulk init |
| `test_position_hotpath.py` | 4 | local-position skip-on-unchanged (3000-step randomized oracle, staleness guard, skip observability) |
| `test_dispatcher.py` | 11 | Dispatcher relay hardening (queue isolation, failure containment, LRU, overflow drop) |
| `test_tool_register.py` | 15 | standalone tool_register primitive (order/dedup/unregister, isolation, key isolation, snapshot) + Tool integration |
| `test_config_env.py` | 8 | `Config.from_envvars` (override, typed parsing, fallback, strict mode, prefix) |
| `test_backtest_hotpath.py` | 32 | looper hot path vs inlined pre-optimization oracles: O(1) calendar primitives + `trade_day_of` exhaustive over all 8800 calendar dates and all natural days 2025-2026 (values **and** exception type/message), cache observability (memo hits, single `data_api` probe), optional-dependency branch still converting `data_api` entities, end-to-end differential backtest (new vs old code path: identical daily settlements, trade blotter and balance) |
| `test_upper_layers.py` | 66 | end-to-end upper-layer simulation with a FakeApp + isolated global signals: constant data objects & frozen protection, Recorder event flow (tick/order/trade/position/account/contract/last, INSTRUMENT_INDEPEND, active-order bookkeeping, init-once), local position deep cases (SHFE vs non-SHFE close priority, frozen spill, order splitting, yesterday conversion), DDDR/UDDR serialization round-trips, Hickey session windows / trade-day derivation, CtpbeeApi `__call__`/`route`/`register`/`subscribe`, Config loaders |

161 checks in total across the 8 suites.

Behavioral quirks locked by characterization (see suite comments):
`PositionData.local_position_id` uses `str(enum)` (`ag2612.SHFE.Direction.LONG`);
`OrderData`/`CancelRequest` both accept string and enum exchanges (the
CancelRequest enum-only trap was fixed via `_exchange_code`, changelog
2026-08-21i);
`main_contract_mapping` keys strip digits from the whole local_symbol
(`ag2612.SHFE` → `AG.SHFE`). Formerly `DDDR.encode→parse` was not
self-consistent — fixed (see changelog 2026-08-21g).

## Changelog

| Date | Change |
|---|---|
| 2026-08-21 | Hot-path optimization: `build_tick_datetime` (+ActionDay cache) shared by ctp/ctp_rohon/ctp_mini; `@frozen` guard via `sys._getframe`; `Entity.__init__` bulk init. Equivalence suite `tests/test_hotpath_optimization.py` (10 checks) + benchmarks. No public API change; only behavior delta: empty ActionDay now falls back to today instead of raising. |
| 2026-08-21b | Position hot path (`data_handle/local_position.py`): `update_tick`/`update_bar` skip pnl recompute when inputs are unchanged — pnl is a pure function of `(last_price, pre_settlement, positions, avg prices, size)`; the signature is compared against **current** attributes so external mutations (trade/position callbacks, yesterday-holding conversion) always trigger a recompute on the next tick (no stale pnl). `LocalPositionManager.update_tick/update_bar` use a single dict lookup. Benchmarks (both-side positions): recompute 0.31 µs → skip 0.10 µs (3×; ~60-80% of real ticks carry an unchanged price). Equivalence suite `tests/test_position_hotpath.py` (4 checks: 3000-step random trade/tick oracle, staleness guard, skip observability, changing-price correctness). |
| 2026-08-21c | Dispatcher (`stream.py`, `Mode.DISPATCHER` Redis relay) reliability hardening — wire protocol and callback signatures unchanged: ① `on_tick` only enqueues (hot path); serialization + publish run on a background thread, bounded queue (100k) drops oldest on overflow with a running counter; ② all publications go through `_publish`, which throttles warnings and never raises — a Redis outage can no longer propagate into the CTP callback chain; ③ the upstream listen loop reconnects on a fixed 5 s backoff and isolates per-message failures (`_handle_upstream`) so one bad order no longer kills the listener thread; ④ `order_key_map` is a bounded LRU (10k; evicted ids fall back to the pre-existing default index 0); ⑤ `send_order` returning empty no longer pollutes the map; ⑥ `UDDR` parse failures are logged (throttled) instead of silently swallowed; ⑦ added `close()` for best-effort thread shutdown. Suite `tests/test_dispatcher.py` (11 checks, FakeRedis injection, no real Redis needed). |
| 2026-08-21d | `tool_register` extracted into a **standalone stdlib-only primitive** (`ctpbee/tool_register.py`) so other libraries can use it without importing the ctpbee app machinery — ctpbee's own `Tool` is now just its first consumer. The decorator accepts any hashable key (string / enum / None, not just `ToolRegisterType`); hooks receive the decorated method's **return value** (existing contract, now documented). Fixed in the process: `functools.wraps` preserved; snapshot iteration (register/unregister during a fire no longer raises `Set changed size`, takes effect next round); per-hook exception isolation with throttled logging (a bad hook can no longer propagate into the tick dispatch chain); ordered + deduplicated hook lists (sets previously gave nondeterministic order); lazy `_linked` creation (never-subscribed objects cost one `getattr`; underscore-named creation keeps frozen `Entity` hosts writable); `add_func` raises a clear `ValueError` on unknown types (was `None.add` AttributeError); `remove_func` added for symmetry; **base `Tool.on_tick/on_order/on_trade/on_position/on_account` are now decorated**, so `subscribe()` works out of the box (previously the mechanism never fired unless the user decorated their own subclass — a silent dead-end). New public helpers `register_tool_hook(obj, key, func)` / `unregister_tool_hook(obj, key, func)` exported from `ctpbee`; `from ctpbee.func import tool_register` keeps working via re-export. Suite `tests/test_tool_register.py` (15 checks: standalone plain-class usage, order/dedup/unregister, exception isolation, key isolation, snapshot semantics, zero-subscription path, wraps, Tool integration incl. base activation and explicit errors). |
| 2026-08-21e | `Config.from_envvars(prefix="CTPBEE_", silent=True)`: reads config from prefixed env vars — values JSON-parsed (bool/int/float/list/dict; `CONNECT_INFO` as a JSON string), unparseable values fall back to the raw string, keys must be uppercase after prefix stripping (consistent with `from_mapping`), `silent=False` raises on non-conforming entries. Recommended precedence: `from_json` then `from_envvars` so env overrides the file. Suite `tests/test_config_env.py` (8 checks). |
| 2026-08-21f | Comprehensive upper-layer simulation suite `tests/test_upper_layers.py` (61 checks, no CTP / no real Redis — FakeApp + isolated global signals). Covers the full Recorder event flow, local-position deep cases (close priority by exchange, frozen spill, SHFE order splitting, yesterday conversion), DDDR/UDDR serialization round-trips, Hickey session windows, trade-day derivation, CtpbeeApi dispatch (`__call__`, `route`, `register`, `subscribe`) and Config loaders. Established the standing rule: **every change lands with passing tests** (109 checks across 6 suites total). Characterization-locked upstream quirks are listed in the test-infrastructure section above. |
| 2026-08-21g | Fixed `DDDR.encode→parse` self-inconsistency (the long-standing `fixme`): `loads` restores `dumps`-produced payloads directly as entity objects, so `__parse__` now adopts the object as-is and only falls back to the key-sniffing reconstruction when the inner data is a plain dict (legacy hand-built payloads keep working). Round-trip checks for TickData/OrderData/TradeData/ContractData added to `test_upper_layers.py` (now 65 checks; 113 total across 6 suites). |
| 2026-08-21h | Replaced the five duplicated try/except exchange fallbacks in `constant.py` `__post_init__` methods with a single module helper `_exchange_code()` using the `getattr(exchange, "value", exchange)` idiom — enum takes `.value`, a plain string falls back to itself. Identical semantics (both paths already characterization-tested: string via A2, enum via A3), no exception machinery, one line per site. `CancelRequest` remains enum-only (documented quirk); switching it to `_exchange_code` as well would also fix the `create_cancel_request()` trap if desired. |
| 2026-08-21i | `CancelRequest.__post_init__` now uses `_exchange_code` — accepts string **and** enum exchanges, defusing the trap where `OrderData.create_cancel_request()` crashes on a string-exchange OrderData (`AttributeError: 'str' object has no attribute 'value'`). Test `test_upper_layers.py` A7 locks the string path (66 checks; 114 total across 6 suites). |
| 2026-08-21j | Examples medium-severity fixes (high-severity items intentionally left: test credentials in config.json and expired contract codes are user-maintained): ① `spread_arbitrage.calculate_spread` now appends exactly one spread per time-aligned minute (timestamp alignment + same-minute dedup via `_last_pair_dt`) instead of re-zipping the entire two-leg window on every bar (O(window) churn per bar; positional, not temporal, pairing); ② `atr_strategy.on_contract` enriches `instrument_set` with the `local_symbol` form — the `INSTRUMENT_INDEPEND` filter compares `event.data.local_symbol`, so a bare contract name silently dropped every tick; ③ `openctp_client` order gating: at most one action per 20 ticks (was: FOK order on nearly every tick) with local net-position tracking from `on_trade`. Suite `tests/test_examples_strategies.py` (15 checks; 129 total across 7 suites). |
| 2026-08-21k | User-facing HTML documentation `docs/index.html` (single file, terminal aesthetic, no build step): quickstart, config reference incl. `from_envvars`, architecture/event-flow diagram, strategy callbacks, order-action semantics (documents the `buy_close`=平多头 naming trap), standalone `tool_register`, looper backtest, performance characteristics, user caveats (calendar horizon 2026-12-31, 100 ms timestamp quantization, DCE local-date host assumption, CTP no-price sentinels, INSTRUMENT_INDEPEND local_symbol form), test suites. Entries added to root `README.md` and `examples/readme.md`. HTML tag balance verified; 7 suites still green (129 checks). |
| 2026-08-21l | Docs expanded per review: ① new "Tools usage" section (write a Tool subclass, with_tools/add_tool/get_tool, subscribe/remove_func via CtpbeeApi or the tool object, kline injection, plus the standalone primitive); ② full config.json demo; ③ examples showcase (login/ATR, run_arb spread, kline, looper backtest, openctp, strategy library); ④ bilingual zh/en with a sidebar toggle persisted in localStorage; ⑤ new "Data structures" section (TickData cumulative-volume semantics, OrderData/TradeData status machine and Δpos = direction × volume, PositionData yd/frozen/pn semantics, requests/enums). Section count 12; tag balance verified; suites still green. |
| 2026-09-22a | Backtest (looper) hot path: ① `VessData.last_bar` no longer runs `from data_api import Tick, Kline` once per replayed bar — the optional `data_api` package is unpublished, so that import always failed, and failed imports are not cached in `sys.modules` (each attempt re-walks `sys.path` with a `stat` per entry: cProfile on origin/dev shows 9.1 `nt.stat` per replayed bar — 179,823 calls for a 19,800-bar run, 76% of profiled time in `nt.stat` and ~93% inside `_find_and_load`). Probe now happens at most once and the result is cached (`data_api_types()`, empty tuple when unavailable); the `data_api → to_bumblebee()` branch keeps its semantics (`isinstance(nx, Tick) or isinstance(nx, Kline)` → the equivalent single `isinstance(nx, (Tick, Kline))`), including non-ImportError propagation and "a raising data_api is not cached as unavailable". ② `LocalLooper.__call__`'s trailing trade-day block (1-2 linear scans of the 8800-entry `trade_dates` + a `strptime` per tick, 40-60 µs) extracted as `trade_day_of()` over new O(1) primitives `date.is_trade_date` / `date.trade_date_index` (lazily built `{date: index}` map, so live-only processes pay nothing at import) and memoized per `(calendar day, night session)`. `get_day_from` uses the same primitive. Net effect on synthetic minute bars: 90.7-93.0 s → **1.13-1.17 s** (≈80×, 1.28 ms → 16 µs per bar; 72× with a no-op strategy instead of a counting one — 80.8-81.9 s → 1.11-1.14 s) for 72,600 bars, 177 s → **3 s** (59×) for a 139,800-bar two-contract run. Re-measured on the same host under ~30 % concurrent CPU: 109.5-138.5 s → 1.36-1.47 s, paired ratio 77-101× (see the benchmark note on load dependence). Behavior-preserving: both pre-optimization implementations are inlined as oracles in `tests/test_backtest_hotpath.py` (32 checks: exhaustive value+exception equivalence, cache observability, end-to-end differential backtest); the 2026-08-21d/2026-08-21j first-bar `LocalLooper.datetime` `AttributeError`, the calendar-horizon `IndexError` and the holiday `ValueError` are locked as characterization, not changed. Review follow-up (Copilot): the extracted date conversion is now `date(*map(int, s.split("-")))` instead of 3.7+ `date.fromisoformat` — `setup.py` declares 3.6 support, and on 3.6 the night/holiday branch would have raised `AttributeError` for every night bar; check D4 now guards the hot path at source level (still 32 checks). Suites: 161 checks across 8, all green. |
