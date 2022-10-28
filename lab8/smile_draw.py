import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

color = (255, 255, 255)
screen.fill(color)

# body
circle(screen, (255, 255, 51), (200, 230), 130)
circle(screen, (0, 0, 0), (200, 230), 130, 5)

# eyes
circle(screen, (255, 0, 0), (150, 210), 30)
circle(screen, (255, 0, 0), (250, 210), 25)
circle(screen, (0, 0, 0), (150, 210), 15)
circle(screen, (0, 0, 0), (250, 210), 15)

# mouth
polygon(screen, (0, 0, 0), [(150, 300), (250, 300), (250, 280), (150, 280)])

# eyebrows
polygon(screen, (0, 0, 0), [(90, 135), (90, 145), (180, 200), (180, 190)])
polygon(screen, (0, 0, 0), [(220, 210), (220, 200), (300, 120), (300, 130)])



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()