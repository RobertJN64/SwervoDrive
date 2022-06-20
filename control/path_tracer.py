import pygame
import json
import math

#region pygame
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, pos, color=(255,0,0), size=30):
    largeText = pygame.font.SysFont("Consolas", size)
    TextSurf, TextRect = text_objects(str(text), largeText, color)
    TextRect.center = pos
    screen.blit(TextSurf, TextRect)
#endregion


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    done = False
    active = False
    counter = 0
    counter_reset = 5
    locations = []
    while not done:
        screen.fill((200,200,200))

        if active:
            if counter == 0:
                x, y = pygame.mouse.get_pos()
                locations.append((x,y))
                counter = counter_reset
            else:
                counter -= 1

        for item in locations:
            pygame.draw.circle(screen, (200,0,0), item, 5)

        message_display(screen, 'FPS: ' + str(round(clock.get_fps(), 1)), (300, 25),
                        color=(0, 0, 0), size=15)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYUP and event.key == pygame.key.key_code('space'):
                active = not active
            if event.type == pygame.KEYUP and event.key == pygame.key.key_code('c'):
                locations = []

            if event.type == pygame.KEYUP and event.key == pygame.key.key_code('return') and len(locations) > 1:
                out_json = []
                speed = 100

                last_angle = 0
                lx, ly = locations[0]
                for (x, y) in locations[1:]:
                    if lx == x and ly == y:
                        continue
                    duration = ((lx - x) ** 2 + (ly - y) ** 2) ** 0.5 / 100
                    if duration < 0.1:
                        continue
                    angle = (math.degrees(math.atan2(lx-x, y-ly))+180)%360
                    if abs(angle - last_angle) > 45:
                        out_json.append({'speed': 10, 'duration': 0.5, 'direction': angle})
                    out_json.append({'speed': speed, 'duration': duration, 'direction': angle})
                    lx = x
                    ly = y
                    last_angle = angle

                with open('path.json', 'w+') as f:
                    json.dump(out_json, f, indent=4)

                print("Path saved!")





if __name__ == '__main__':
    main()

