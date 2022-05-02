
from pyfirmata import Arduino, SERVO
from time import sleep
import threading

port = 'COM3'
pin10 = 10
pin9 = 9
board = Arduino(port)

board.digital[pin10].mode = SERVO
board.digital[pin9].mode = SERVO

motor1=0
motor2=0
# motor3=0





allmators= {(9,180),(10,180)}
reset ={9,10}


def getmotorAngle(pin):
    if (pin == 9):
        return motor1
    if (pin == 10):
        return motor2

def motorUp(pin, angle):
    global motor1
    global motor2
    before = getmotorAngle(pin)

    value=before - angle
    print(angle,before)
    if(angle>before):
        v= angle-before
        for i in range(before, angle,1):
            rotateServer(pin, i)
            if (pin == 9):
                motor1 = angle
            if (pin == 10):
                motor2 = angle


    if (angle<before):
        v =before - angle
        for i in range(before, angle, -1):
            rotateServer(pin, i)
            if (pin == 9):
                motor1 = angle
            if (pin == 10):
                motor2 = angle

# def motorback(pin, angle):
#     for i in range(angle, 0, -1):
#         rotateServer(pin, i)
#         if (pin == 9):
#             motor1 = angle
#         if (pin == 9):
#             motor2 = angle


def rotateServer(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)



for i in reset:
    rotateServer(i, 0)

for m in allmators:
    motorUp(m[0], 0)
    motorUp(m[0],m[1])
    motorUp(m[0], 20)
    motorUp(m[0], 80)
    motorUp(m[0], 0)
    motorUp(m[0], 150)
    motorUp(m[0], 0)
        # motor1(10, 180)
    # for m in allmators:
    #     # print(m[0],m[1])
    #
    #     motorback(m[0], m[1])
    #     # motor1(10, 180)