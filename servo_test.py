from servosix.servosix import ServoSix
#from time import sleep

ss = ServoSix(servo_min = 200, servo_max = 1200)
while True:
    angle = int(input("Angle: "))
    ss.set_servo(1, angle)
    ss.set_servo(2, angle)
    ss.set_servo(3, angle)
    ss.set_servo(4, angle)

