from servosix.servosix import ServoSix
from time import sleep

ss = ServoSix()
ss.set_servo(1, 10)
sleep(1)
ss.set_servo(1, 90)
sleep(1)
ss.set_servo(1, 170)

