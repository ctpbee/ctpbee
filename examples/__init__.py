from threading import Thread
from time import sleep

def run_consumer():
    while True:
        print("I am ready to go")
        sleep(1)


def send_message():

    print("send")

p = Thread(target=run_consumer)
p.start()
send_message()



