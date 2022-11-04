import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1440, 720))
text = pygame.font.Font(None, 36)

# Colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


# make new ball
def new_ball(balls):
    '''
    :param balls: list of object to check no intersections
    :return: list of balls, where ball is list:
    par[0] = x, par[1] = y, par[2] = r, par[3] = color, par[4] = velocity_x, par[5] = velocity_y
    '''
    fl = True
    x = randint(100, 1340)
    y = randint(100, 600)
    r = randint(30, 50)
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


# make new squares
def new_square(squares):
    '''
    :param squares: list of object to check no intersections
    :return: list of squares, where ball is list:
    par[0] = x, par[1] = y, par[2] = r, par[3] = color, par[4] = velocity_x, par[5] = velocity_y,
    par[6] = acceleration_x, par[7] = acceleration_y
    '''
    fl = True
    x = randint(100, 1340)
    y = randint(100, 600)
    r = randint(30, 50)
    while fl:
        x = randint(100, 1340)
        y = randint(100, 600)
        r = randint(30, 50)
        fl = False
        for i in range(len(squares)):
            if (squares[i][0] - x) ** 2 + (squares[i][1] - y) ** 2 <= (squares[i][2] + r) ** 2:
                fl = True
    color = COLORS[randint(0, 5)]
    v_x = randint(5, 10) * (randint(0, 1) * 2 - 1)
    v_y = randint(5, 10) * (randint(0, 1) * 2 - 1)
    a_x = randint(-3, 3)
    a_y = randint(-3, 3)
    return [x, y, r, color, v_x, v_y, a_x, a_y]


# draw ball
def draw_ball(ball):
    '''
    :param ball: ball
    :return: none
    '''
    circle(screen, ball[3], (ball[0], ball[1]), ball[2])


# draw square
def draw_square(square):
    '''
    :param square: square
    :return: none
    '''
    x = square[0]
    y = square[1]
    r = square[2]
    color = square[3]
    polygon(screen, color, [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)])


# object check hit
def click(mouse_event, object):
    """
    :param mouse_event: mouse event
    :param object: object to check hit
    :return: True if hit object else False
    """
    mouse_x = mouse_event.pos[0]
    mouse_y = mouse_event.pos[1]
    return (mouse_x - object[0]) ** 2 + (mouse_y - object[1]) ** 2 <= object[2] ** 2


# draw ball or delete ball which is hit and make new object instead
def show_ball(ball, fl, balls):
    """
    :param ball: ball
    :param fl: True if ball is hit else False
    :param balls: list of balls
    :return: old ball if it is not hit else new ball
    """
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


# draw square or delete square which is hit and make new object instead
def show_square(square, fl, squares):
    """
    :param square: square
    :param fl: True if square is hit else False
    :param squares: list of squares
    :return: old square if it is not hit else new square
    """
    if not fl:
        square[0] += square[4]
        square[1] += square[5]
        square[4] += square[6] * int(randint(1, 3) == 1)
        square[5] += square[7] * int(randint(1, 3) == 1)
        if square[4] ** 2 + square[5] ** 2 >= 200:
            square[4] = randint(5, 10) * (randint(0, 1) * 2 - 1)
            square[5] = randint(5, 10) * (randint(0, 1) * 2 - 1)
            square[6] = randint(-3, 3)
            square[7] = randint(-3, 3)
        draw_square(square)
    else:
        square = new_square(squares)
        square[4] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        square[5] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        fl = False
    return square


# balls hit check and scores
def click_balls(n_b, balls, event, score):
    """
    :param balls: list of balls
    :param n_b: length of balls
    :param event: mouse event
    :param score: score
    :return: list with True and False, True if hit balls else False and new score
    """
    fl_b = [False] * n_b
    for i in range(n_b):
        fl = click(event, balls[i])
        if fl:
            score += 1
        fl_b[i] = fl
    return fl_b, score


# squares hit check and scores
def click_squares(n_s, squares, event, score):
    '''
    :param n_s: length of squares
    :param squares: list of squares
    :param event: mouse event
    :param score: score
    :return: list with True and False, True if hit balls else False and new score
    '''
    fl_s = [False] * n_s
    for i in range(n_s):
        fl = click(event, squares[i])
        if fl:
            score += 2
        fl_s[i] = fl
    return fl_s, score


# collisions object with other object
def collisions_obect(i, objects, boom):
    '''
    :param i: index of object which is checked
    :param objects: list of object
    :param boom: list of index of object which has collision
    :return: new list of objects and list of index with object which has collision
    '''
    for j in range(len(objects)):
        if i != j and not (j in boom) and not (i in boom):
            if (objects[i][0] - objects[j][0]) ** 2 + (objects[i][1] - objects[j][1]) ** 2 <= (objects[i][2] + objects[j][2]) ** 2:
                objects[i][4], objects[j][4] = objects[j][4], objects[i][4]
                objects[i][5], objects[j][5] = objects[j][5], objects[i][5]
                objects[i][0] = objects[i][0] + objects[i][4]
                objects[i][1] = objects[i][1] + objects[i][5]
                objects[j][0] = objects[j][0] + objects[j][4]
                objects[j][1] = objects[j][1] + objects[j][5]
                boom.append(j)
                boom.append(j)
                break
    return objects, boom


# check collisions with walls and make new velocity if it needs
def collisions_walls(ball):
    '''
    :param ball: ball
    :return: new ball with new velocity if it needs
    '''
    while ball[0] + ball[4] - 1440 > -ball[2] or ball[0] + ball[4] < ball[2] or ball[1] + ball[5] - 720 > -ball[2] or\
            ball[1] + ball[5] < ball[2]:
        ball[4] = randint(5, 10) * (randint(0, 1) * 2 - 1)
        ball[5] = randint(5, 10) * (randint(0, 1) * 2 - 1)
    return ball


n_b = 3  # number of balls
n_s = 3  # number of squares
score = 0  # counter score

# make primary list of balls
balls = []
for i in range(n_b):
    ball = new_ball(balls)
    balls.append(ball)

# make primary list of balls
squares = []
for i in range(n_s):
    square = new_square(balls + squares)
    squares.append(square)

# make primary list of hit conditions
fl_s = [False] * n_s
fl_b = [False] * n_b

# main

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # check hit
            fl_b, score = click_balls(n_b, balls, event, score)
            fl_s, score = click_squares(n_s, squares, event, score)

    objects = balls + squares

    # collisions object with other object
    boom = []  # list object, which have collision with other object
    for i in range(n_s + n_b):
        objects, boom = collisions_obect(i, objects, boom)

    # collisions object with walls
    for i in range(n_b):
        balls[i] = collisions_walls(balls[i])
    for i in range(n_s):
        squares[i] = collisions_walls(squares[i])

    # show object or delete object which is hit and make new object instead
    for i in range(n_b):
        balls[i] = show_ball(balls[i], fl_b[i], balls)
    fl_b = [False] * n_b
    for i in range(n_s):
        squares[i] = show_square(squares[i], fl_s[i], balls)
    fl_s = [False] * n_s

    # print score and rules
    score_text = text.render('score: ' + str(score), True, (180, 0, 0))
    screen.blit(score_text, (20, 30))
    instruction_text = text.render('click on balls - 1 point, click on squares - 2 points', True, (153, 255, 153))
    screen.blit(instruction_text, (150, 30))

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print(" ----End of the game----")
print("Score:", score)
