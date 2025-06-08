import uasyncio as asyncio
from machine import Pin
import os

class MotorAbsolute:
    def __init__(self, motor, file_name, rev=False):
        self.motor = motor
        self.file_name = file_name
        self.d = -1 if rev else 1
        self.motor.reset()
        self.angle = self.read_angle()

    def write_angle(self, angle):
        with open(self.file_name, "w") as file:
            file.write(str(angle))

    def read_angle(self):
        try:
            with open(self.file_name, 'r') as file:
                return float(file.read())
        except (OSError, ValueError):
            # If file doesn't exist or is invalid, start at 0
            self.write_angle(0)
            return 0.0

    async def move(self, new_angle):
        delta = new_angle - self.angle
        if delta != 0:
            direction = -1 if delta > 0 else 1
            await self.motor.angle(abs(delta), self.d * direction)
            self.angle = new_angle
            self.write_angle(new_angle)


class Stepper:
    FULL_ROTATION = int(4075.7728395061727 / 8)  # 28BYJ-48 motor

    HALF_STEP = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]

    FULL_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, pin1, pin2, pin3, pin4, delay_ms=10, mode=1):
        self.mode = self.FULL_STEP if mode == 1 else self.HALF_STEP
        self.pins = [Pin(pin, Pin.OUT) for pin in (pin1, pin2, pin3, pin4)]
        self.delay = delay_ms
        self.reset()

    async def step(self, count, direction=1):
        """Async rotate stepper motor by step count"""
        if count < 0:
            direction = -1
            count = -count
        sequence = self.mode[::direction]

        for _ in range(count):
            for bits in sequence:
                for pin, val in zip(self.pins, bits):
                    pin(val)
                await asyncio.sleep_ms(self.delay)
        self.reset()

    async def angle(self, degrees, direction=1):
        """Async rotate by degrees"""
        steps = int(self.FULL_ROTATION * degrees / 360)
        await self.step(steps, direction)

    def reset(self):
        for pin in self.pins:
            pin(0)
