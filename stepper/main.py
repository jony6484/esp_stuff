import uasyncio as asyncio
from stepper import Stepper, MotorAbsolute
from kinematics import insert_points, FiveBarMech, load_points
# Setup absolute motors
left_motor = MotorAbsolute(Stepper(14, 13, 26, 27, delay_ms=5, mode=0),
                         "left_motor.txt", rev=False)
right_motor = MotorAbsolute(Stepper(25, 33, 15, 32, delay_ms=5, mode=0),
                          "right_motor.txt", rev=True)

async def move_motors(theta_l, theta_r):
    t1 = asyncio.create_task(left_motor.move(theta_l))
    t2 = asyncio.create_task(right_motor.move(theta_r))
    await asyncio.gather(t1, t2)
    
    
mechanism = FiveBarMech(A=(0,0), L1=5, L2=7, L3=7, L4=6.5, L5=1.9, K=5.6)
points= load_points('points.csv')
# points = insert_points(points, 2)
point = points[0]
asyncio.run(move_motors(*mechanism.inverse_kinematics(*point)))
asyncio.sleep_ms(5000) 
def run():
    for point in points:
        asyncio.run(move_motors(*mechanism.inverse_kinematics(*point)))
        asyncio.sleep_ms(1000)

#asyncio.run(main())


