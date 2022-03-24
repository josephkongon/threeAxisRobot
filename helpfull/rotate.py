from pyfirmata import Arduino, SERVO
from time import sleep
import threading

port = 'COM3'
pin10 = 10
pin9 = 9
board = Arduino(port)

board.digital[pin10].mode = SERVO
board.digital[pin9].mode = SERVO


def motor1(pin, angel):
    for i in range(0, angel):
        rotateServer(pin, i)

    for i in range(angel, 0, -1):
        rotateServer(pin, i)


def rotateServer(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.00015)

def threadsFuntion(pin,agl):
    t1 = threading.Thread(target=motor1, args=(pin, agl))

    t1.start()
    t1.join()

if __name__ == "__main__":

    while True:
        threadsFuntion(9,90)
        threadsFuntion(10, 180)
