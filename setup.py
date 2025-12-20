import io
import re
import sys

from pathlib import Path

from setuptools import setup

with io.open("ctpbee/__init__.py", "rt", encoding="utf8") as f:
    context = f.read()
    patterns = [
        r'__version__\s*=\s*["\']([^"\']+)["\']',  # 标准格式
        r'__version__\s*:\s*["\']([^"\']+)["\']',  # 可能使用冒号
        r'version\s*=\s*["\']([^"\']+)["\']',  # 可能没有下划线
    ]

    for pattern in patterns:
        match = re.search(pattern, context)
        if match:
            version = match.group(1)
            break

if sys.version_info < (3, 6):
    raise RuntimeError(
        "当前ctpbee只支持python36以及更高版本/ ctpbee only support python36 or higher "
    )

# libraries
install_requires = [
    "pytz",
    "blinker",
    "requests",
    "simplejson",
    "lxml",
    "jinja2",
    "redis",
    "click",
    "cologer>=2.0",
    "ctpbee_api>=0.40",
    "numpy",
    "pandas",
    "ctpbee_kline",
]

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    install_requires.append("dataclasses")

pkgs = [
    "ctpbee",
    "ctpbee.context",
    "ctpbee.exceptions",
    "ctpbee.data_handle",
    "ctpbee.interface",
    "ctpbee.interface.ctp",
    "ctpbee.interface.local",
    "ctpbee.interface.looper",
    "ctpbee.interface.ctp_mini",
    "ctpbee.jsond",
    "ctpbee.looper",
    "ctpbee.indicator",
]

setup(
    name="ctpbee",
    version=version,
    description="Easy ctp trade and market support",
    author="somewheve",
    author_email="somewheve@gmail.com",
    url="https://github.com/ctpbee/ctpbee",
    license="MIT",
    long_description_content_type="text/markdown",
    packages=pkgs,
    install_requires=install_requires,
    platforms=["Windows", "Linux", "Mac OS-X"],
    package_dir={"ctpbee": "ctpbee"},
    zip_safe=False,
    include_package_data=True,
    data_files=[],
    package_data={"ctpbee": ["api/ctp/*", "*.html"]},
    ext_modules=[],
    entry_points={"console_scripts": ["bee = ctpbee.cmdline:cli"]},
)
