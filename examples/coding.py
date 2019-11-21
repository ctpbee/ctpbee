from blinker import signal

a = signal("hello")


def hello(gg):
    print("bb")
    print(gg)


def gg(ds):
    print(ds)


a.connect(hello)
a.connect(gg)
print(a.receivers)
