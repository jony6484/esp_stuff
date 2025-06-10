import sys
from tmc.TMC_2209_StepperDriver import *
import time
import uasyncio as asyncio

MICROSTEPPING = 2
ANGLE_2_STEPS_RATIO = 360 / (200 * MICROSTEPPING)

def setup_motor(pin_step, pin_dir, pin_en, rx, tx):
    # use your pins for pin_step, pin_dir, pin_en here
    motor = TMC_2209(pin_step=pin_step, pin_dir=pin_dir, pin_en=pin_en, rx=rx, tx=tx)
    print("Connected to motor")
    motor.setVSense(True)
    motor.setCurrent(1000)
    motor.setIScaleAnalog(True)
    motor.setInterpolation(True)
    motor.setSpreadCycle(False)
    motor.setMicrosteppingResolution(MICROSTEPPING)
    motor.setInternalRSense(False)
    motor.setAcceleration(500)
    motor.setMaxSpeed(80)
    motor.setMotorEnabled(True)
    return motor

def connect_motors():
    motor_l = setup_motor(5, 18, 19, 16, 17)
    motor_l.setDirection_reg(0)
    motor_r = setup_motor(25, 26, 27, 32, 33)
    motor_l.setDirection_reg(1)
    return motor_l, motor_r

def a2s(angle):
    return int(angle / ANGLE_2_STEPS_RATIO)

def stop_and_home_left(ch):
    motor_l.stop()
    motor_l.setCurrentPosition(a2s(208.0))
    
def stop_and_home_right(ch): 
    motor_r.stop()
    motor_r.setCurrentPosition(a2s(-30.0))

def home_motors():  
   # home left motor    
    motor_r.setMotorEnabled(False)
    motor_l.setMotorEnabled(True)
    motor_l.setStallguard_Callback(21, 15, stop_and_home_left)
    motor_l.runToPositionSteps(800)
    time.sleep(1.0)
    motor_l.runToPositionSteps(a2s(70.0))
    print("Left homed")
    # home right motor     
    motor_r.setMotorEnabled(True)
    motor_r.setStallguard_Callback(35, 15, stop_and_home_right)
    motor_r.runToPositionSteps(-800)
    time.sleep(1.0)
    motor_r.runToPositionSteps(a2s(70.0))
    print("Right homed")
    motor_l.runToPositionSteps(a2s(110.0))

# Coroutine for moving both motors
async def move_both(motor_l, motor_r, left_steps, right_steps):
    # Move left 1000 steps, right 2000 steps
    await asyncio.gather(
        motor_l.async_runToPositionSteps(left_steps),
        motor_r.async_runToPositionSteps(right_steps)
    )

    
time.sleep(0.1)
motor_l, motor_r = connect_motors()
home_motors()

#asyncio.run(move_both(motor_l, motor_r, 20, 30))