import sys
from tmc.TMC_2209_StepperDriver import *
import time
import uasyncio as asyncio

def setup_motor(pin_step, pin_dir, pin_en, rx, tx):
    # use your pins for pin_step, pin_dir, pin_en here
    motor = TMC_2209(pin_step=pin_step, pin_dir=pin_dir, pin_en=pin_en, rx=rx, tx=tx)
    print("Connected to motor")
    motor.setDirection_reg(False)
    motor.setVSense(True)
    motor.setCurrent(1000)
    motor.setIScaleAnalog(True)
    motor.setInterpolation(True)
    motor.setSpreadCycle(False)
    motor.setMicrosteppingResolution(2)
    motor.setInternalRSense(False)
    motor.setAcceleration(2000)
    motor.setMaxSpeed(500)
    motor.setMotorEnabled(True)
    return motor

def connect_motors():
    motor_l = setup_motor(5, 18, 19, 16, 17)
    motor_r = setup_motor(25, 26, 27, 32, 33)
    return motor_l, motor_r

# Coroutine for moving both motors
async def move_both(motor_l, motor_r, left_steps, right_steps):
    # Move left 1000 steps, right 2000 steps
    await asyncio.gather(
        motor_l.async_runToPositionSteps(left_steps),
        motor_r.async_runToPositionSteps(right_steps)
    )
    print("Both motors completed their move.")

time.sleep(0.1)
motor_l, motor_r = connect_motors()
#asyncio.run(move_both(motor_l, motor_r, 20, 30))