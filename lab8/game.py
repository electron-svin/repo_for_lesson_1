import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 2
screen = pygame.display.set_mode((1200, 900))

# Colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    global x, y, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click(mouse_event):
    print(x, y, r)
    mouse_x = mouse_event.pos[0]
    mouse_y = mouse_event.pos[1]
    return (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2


pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            if click(event):
                score += 1
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print("-----End of the game-----")
print("Score:", score)