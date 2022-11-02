import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1440, 720))

# Colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball(balls):
    fl = True
    while fl:
        x = randint(100, 1340)
        y = randint(100, 600)
        r = randint(30, 50)
        fl = False
        for i in range(len(balls)):
            if (balls[i][0] - x) ** 2 + (balls[i][1] - y) ** 2 <= (balls[i][2] + r) ** 2:
                fl = True
    color = COLORS[randint(0, 5)]
    v_x = randint(5, 10) * (randint(0, 1) * 2 - 1)
    v_y = randint(5, 10) * (randint(0, 1) * 2 - 1)
    circle(screen, color, (x, y), r)
    return [x, y, r, color, v_x, v_y]


def new_square(balls):
    fl = True
    while fl:
        x = randint(100, 1340)
        y = randint(100, 600)
        r = randint(30, 50)
        fl = False
        for i in range(len(balls)):
            if (balls[i][0] - x) ** 2 + (balls[i][1] - y) ** 2 <= (balls[i][2] + r) ** 2:
                fl = True
    color = COLORS[randint(0, 5)]
    v_x = randint(5, 10) * (randint(0, 1) * 2 - 1)
    v_y = randint(5, 10) * (randint(0, 1) * 2 - 1)
    return [x, y, r, color, v_x, v_y]


def draw_ball(ball):
    circle(screen, ball[3], (ball[0], ball[1]), ball[2])


def draw_square(square):
    x = square[0]
    y = square[1]
    r = square[2]
    color = square[3]
    polygon(screen, color, [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)])

def click(mouse_event, ball):
    mouse_x = mouse_event.pos[0]
    mouse_y = mouse_event.pos[1]
    return (mouse_x - ball[0])**2 + (mouse_y - ball[1])**2 <= ball[2]**2


def popb(ball, fl, balls):
    if not fl:
        ball[0] += ball[4]
        ball[1] += ball[5]
        draw_ball(ball)
    else:
        ball = new_ball(balls)
        ball[4] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        ball[5] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        fl = False
    return ball


def col_b(i, balls, boom):
    for j in range(len(balls)):
        if i != j and not(j in boom) and not(i in boom):
            if (balls[i][0] - balls[j][0]) ** 2 + (balls[i][1] - balls[j][1]) ** 2 <= (balls[i][2] + balls[j][2]) ** 2:
                balls[i][4], balls[j][4] = balls[j][4], balls[i][4]
                balls[i][5], balls[j][5] = balls[j][5], balls[i][5]
                boom.append(j)
                boom.append(j)
                break
    return balls, boom


def col(ball):
    while ball[0] + ball[4] - 1440 > -ball[2] or ball[0] + ball[4] < ball[2] or ball[1] + ball[5] - 720 > -ball[2] or ball[1] + ball[5] < ball[2]:
        ball[4] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        ball[5] = randint(5, 10) * (randint(0, 1) * 2 - 1)
    return ball


pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0
square = new_square([])
draw_square(square)
n = 3
balls = []
for i in range(n):
    ball = new_ball(balls)
    balls.append(ball)
squares = []
for i in range(n):
    square = new_square(balls + squares)
    squares.append(square)
fls = [False]*n*2
ball = balls[0]
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            for i in range(n):
                fl = click(event, balls[i])
                if fl:
                    score += 1
                fls[i] = fl
    for i in range(n):
        balls[i] = popb(balls[i], fls[i], balls)
    fls = [False]*n
    boom = []
    for i in range(n):
        balls, boom = col_b(i, balls, boom)
        balls[i] = col(balls[i])
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print("-----End of the game-----")
print("Score:", score)