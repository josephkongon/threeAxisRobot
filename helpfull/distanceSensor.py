

from signal import signal,SIGTERM,SIGHUP
from time import sleep
from gpiozero import DistanceSensor

sensor = DistanceSensor(ech0=13,trigger=12)

def safe_exit(signum, fram):
    exit(1)

signal(SIGTERM,safe_exit())
signal(SIGHUP,safe_exit())

try:
    while True:
        print("Distance :" + "{:1,2f}".format(sensor.value)+" m")
        sleep((0.1))
except:
    pass
finally:
    sensor.close()

##############################################

# import time
# from pyfirmata import Arduino
# from pymata4 import pymata4
#
# triggerPin= 12
# echo_pin= 13
#
# board = pymata4.Pymata4()
#
# def callReturn(data):
#     print("distace: ",data)
#
# board.set_pin_mode_sonar(triggerPin,echo_pin,callReturn)
#
# while True:
#     try:
#         time.sleep(1)
#         board.sonar_read(triggerPin)
#     except Exception:
#         board.shutdown()

