
from pyfirmata import Arduino, SERVO
from time import sleep
import threading

port = 'COM3'
pin10 = 10
pin9 = 7
pin11 = 11
board = Arduino(port)

# board.digital[pin10].mode = SERVO
board.digital[pin9].mode = SERVO
board.digital[pin11].mode = SERVO

motor1=0
motor2=0
motor3=0
# motor3=0





allmators= {7}
reset ={8,9,10}


def getmotorAngle(pin):
    if (pin == 10):
        return motor3
    if (pin == 7):
        return motor1
    if (pin == 11):
        return motor2

def motorUp(pin, angle):
    global motor1
    global motor2
    global motor3
    before = getmotorAngle(pin)

    # value=before - angle
    print(angle,before)
    if(angle>before):
        v= angle-before
        for i in range(before, angle,1):
            rotateServer(pin, i)
            if (pin == 7):
                motor1 = angle
            if (pin == 11):
                motor2 = angle
            if (pin == 8):
                motor3 = angle


    if (angle<before):
        v =before - angle
        for i in range(before, angle, -1):
            rotateServer(pin, i)
            if (pin == 7):
                motor1 = angle
            if (pin == 11):
                motor2 = angle
            if (pin == 8):
                motor3 = angle
# def motorback(pin, angle):
#     for i in range(angle, 0, -1):
#         rotateServer(pin, i)
#         if (pin == 9):
#             motor1 = angle
#         if (pin == 9):
#             motor2 = angle


def rotateServer(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.00383)
    return

def smallmotorUp(pin, angle):
    global motor1
    global motor2
    global motor3
    before = getmotorAngle(pin)

    # value=before - angle
    print(angle,before)
    if(angle>before):
        v= angle-before
        for i in range(before, angle,1):
            smallrotateServer(pin, i)
            if (pin == 7):
                motor1 = angle
            if (pin == 11):
                motor2 = angle
    if (angle<before):
        v =before - angle
        for i in range(before, angle, -1):
            smallrotateServer(pin, i)
            if (pin == 7):
                motor1 = angle
            if (pin == 11):
                motor2 = angle

# def motorback(pin, angle):
#     for i in range(angle, 0, -1):
#         rotateServer(pin, i)
#         if (pin == 9):
#             motor1 = angle
#         if (pin == 9):
#             motor2 = angle


def smallrotateServer(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.00133)
    return

for i in reset:
    rotateServer(i, 0)
while(True):
    for m in allmators:

        t=threading.Thread(smallmotorUp(7, 90))
        t.start()

        t = threading.Thread(smallmotorUp(7, 0))

        t.start()

        # sleep(2)
        # smallmotorUp(7, 0)
        sleep(2)
        r= threading.Thread(motorUp(11,90))
        r.start()
        r.join()
        sleep(2)
        r= threading.Thread(motorUp(11,0))
        r.start()
        r.join()
        sleep(2)
    # motorUp(m,80)
    # motorUp(m, 10)
    # motorUp(m, 40)
    # motorUp(m[0], 50)
    # motorUp(m[0], 0)
    # motorUp(m[0], 30)
    # motorUp(m[0], 0)
        # motor1(10, 180)
    # for m in allmators:
    #     # print(m[0],m[1])
    #
    #     motorback(m[0], m[1])
    #     # motor1(10, 180)