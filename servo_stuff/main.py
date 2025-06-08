from stepper import Stepper

in1 = 16
in2 = 17
in3 = 5
in4 = 18
delay = 2
mode = 1 # 0 for half step, 1 for full step

def main() -> None:
    left = Stepper(14, 13, 26, 27, delay, mode)
    left.step(100)
    left.step(100,-1)
    left.angle(180)
    left.angle(360,-1)
    
main()