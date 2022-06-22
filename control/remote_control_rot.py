import pygame
import math
import requests

#region init
pygame.init()
joysticks = []

zero_speed = False
spin_left = False
spin_right = False
reorient_wheel = False

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
#endregion

lastAxis0 = 0
lastAxis1 = 0
lastAxis2 = 0
lastAxis3 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                lastAxis0 = event.value
            elif event.axis == 1:
                lastAxis1 = event.value
            elif event.axis == 2:
                lastAxis2 = event.value
            elif event.axis == 3:
                lastAxis3 = event.value
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                zero_speed = True
            if event.button == 9:
                spin_left = True
            if event.button == 10:
                spin_right = True
            if event.button == 0:
                reorient_wheel = True
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 1:
                zero_speed = False
            if event.button == 9:
                spin_left = False
            if event.button == 10:
                spin_right = False
            if event.button == 0:
                reorient_wheel = False


    magnitude = min(math.sqrt((lastAxis0 ** 2) + (lastAxis1 ** 2)) * 100, 100)
    angle = math.degrees(math.atan2(lastAxis1, lastAxis0 + 0.0000000000001))
    angle += 90
    angle = angle%360

    rotation = math.degrees(math.atan2(lastAxis3, lastAxis2 + 0.0000000000001))
    magnitude_2 = min(math.sqrt((lastAxis3 ** 2) + (lastAxis2 ** 2)) * 30, 30)
    rotation += 90
    rotation = rotation%360

    if 45 < rotation < 135:
        rotation_magnitude = magnitude_2
    elif 225 < rotation < 315:
        rotation_magnitude = -magnitude_2
    else:
        rotation_magnitude = 0


    if spin_right:
        print("Spin right")
        requests.get('http://192.168.4.1/drive_cmd/spinright')
    elif spin_left:
        print("Spin left")
        requests.get('http://192.168.4.1/drive_cmd/spinleft')
    elif reorient_wheel:
        print("Lock wheels to 0")
        requests.get('http://192.168.4.1/setspeeddir?speed=1&direction=0')
    else:
        if zero_speed:
            magnitude = 10
        print("Target: ", magnitude, angle)
        rurl = ('http://192.168.4.1/setspeeddirrot?speed=' + str(int(magnitude)) +
                         '&direction=' + str(int(angle)) +
                         '&rotation=' + str(int(rotation_magnitude)))
        print(rurl)
        r = requests.get(rurl)
        #print(r.text)
