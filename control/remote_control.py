import pygame
import math
import requests

#region init
pygame.init()
joysticks = []

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

    magnitude = math.sqrt((lastAxis0 ** 2) + (lastAxis1 ** 2))
    angle = math.degrees(math.atan2(lastAxis1, lastAxis0 + 0.0000000000001))
    angle += 90
    angle = angle%360

    rotation = math.degrees(math.atan2(lastAxis3, lastAxis2 + 0.0000000000001))
    rotation += 90
    rotation = rotation%360

    print("Target: ", magnitude, angle)
    requests.get('http://192.168.4.1/setspeeddir?speed=' + str(magnitude) + '?direction=' + str(angle))
