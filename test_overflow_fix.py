import numpy as np
from ctpbee.indicator.indicator import atr, ewma, get_max_row_size

# 测试get_max_row_size函数在alpha=0.0时的情况
print("Testing get_max_row_size with alpha=0.0...")
try:
    result = get_max_row_size(0.0)
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Failed: {e}")

# 测试ewma函数在period=1时的情况（此时alpha=0.0）
print("\nTesting ewma with period=1...")
data = np.array([1, 2, 3, 4, 5])
try:
    result = ewma(data, 1)
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Failed: {e}")

# 测试atr函数
print("\nTesting atr function...")
high = np.array([10, 11, 12, 13, 14])
low = np.array([9, 10, 11, 12, 13])
close = np.array([9.5, 10.5, 11.5, 12.5, 13.5])
try:
    result = atr(high, low, close, 1)
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Failed: {e}")

# 测试atr函数在正常周期下的情况
print("\nTesting atr function with normal period=14...")
try:
    result = atr(high, low, close, 14)
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Failed: {e}")