import time
from servo import Servo
from kinematics import *
from time import sleep
import machine

L1 = 5.0
L2 = 7.0
L3 = 7.0
L4 = 6.6
L5 = 2.2
K = 5.5
A = (0.0, 0.0)
B = (L5, 0.0)

x0 = 3.5
y0 = 14.5

dir_pin = machine.Pin(12,machine.Pin.OUT)
step_pin = machine.Pin(14,machine.Pin.OUT)
def move_stepper(direct,steps, delay, accel):
	dir_pin.value(direct)
	steps = abs(steps)
	for i in range(steps):
		step_pin.value(1)
		time.sleep_us(delay)
		step_pin.value(0)
		time.sleep_us(delay)
def stop_stepper():
    step_pin.value(0)
