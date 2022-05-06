import RPi.GPIO as GPIO
from time import sleep


#TODO - set pins
fwd_pin = 4 #in1
rev_pin = 17 #in2
spd_pin = 27 #en

GPIO.setmode(GPIO.BCM)

GPIO.setup(fwd_pin,GPIO.OUT)
GPIO.setup(rev_pin,GPIO.OUT)
GPIO.setup(spd_pin,GPIO.OUT)

GPIO.output(fwd_pin,GPIO.LOW)
GPIO.output(rev_pin,GPIO.LOW)

pwm = GPIO.PWM(spd_pin,1000) #1000 is freq
pwm.start(50) #on 50% of time

print("Init finished.")

def stop():
    GPIO.output(fwd_pin, GPIO.LOW)
    GPIO.output(rev_pin, GPIO.LOW)
    print("Motor stopped.")

def forward():
    GPIO.output(rev_pin, GPIO.LOW)
    GPIO.output(fwd_pin, GPIO.HIGH)
    print("Motor forward")

def reverse():
    GPIO.output(fwd_pin, GPIO.LOW)
    GPIO.output(rev_pin, GPIO.HIGH)
    print("Motor reverse")

def speed(spd):
    global pwm
    pwm.ChangeDutyCycle(spd)
    print("Motor to spd: ", spd)

print("Starting Control Sequence:")
forward()
sleep(5)
# speed(25)
# sleep(1)
# speed(75)
# sleep(1)
# speed(50)
# reverse()
# sleep(1)
stop()

GPIO.cleanup()
print("Exited cleanly...")
