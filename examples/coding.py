from ctpbee_analyzer import cost


@cost
def print_time():
    a = list(range(10000000))


@cost
def letsgo():
    p = list(range(100000000))


if __name__ == "__main__":
    print_time()
    letsgo()
