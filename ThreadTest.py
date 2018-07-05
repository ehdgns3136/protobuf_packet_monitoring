from threading import Thread
from time import sleep
def test1():
    while True:
        print('hello')
        sleep(1)

thread = Thread(target = test1)
thread.start()
while True:
    print('hello2')
    sleep(1)