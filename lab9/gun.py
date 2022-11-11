import math
from random import choice
from random import randint as rnd
from pygame.draw import *

import pygame

FPS = 30

GREY = 0x696969
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

WIDTH = 1440
HEIGHT = 720

GRAVITY = 1


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ ball class constructor

        Args:
        x - initial horizontal position of the ball
        y - initial vertical position of the ball
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 2
        self.vx = 0
        self.vy = 0.0
        self.color = GREY
        self.live = 120
        self.type = 1

    def move(self):
        """Move the ball after a unit of time.

        The method describes the movement of the ball in one redraw frame. That is, it updates the values
        self.x and self.y, taking into account the speeds self.vx and self.vy, the force of gravity acting on the ball,
        and walls along the edges of the window (window size 1440x720).
        """
        if self.type == 1:
            self.r += 0.5
        if self.x + self.vx + self.r > WIDTH or self.x + self.vx - self.r < 0:
            self.live = 1
        if self.y - self.vy + self.r > HEIGHT - 10:
            self.live = 1
        self.x += self.vx
        self.y -= self.vy
        self.vy -= GRAVITY
        self.live -= 1

    def draw(self):
        """Draw balls

        :return: none
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            int(self.r)
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            int(self.r), 1
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.live = 0
            return True
        return False


class Gun:
    def __init__(self, screen):
        """Gun class constructor

        :param screen: pygame screen
        """
        self.screen = screen
        self.f2_power = 20
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def fire2_end(self, balls, type):
        """Ball shot.

        Occurs when the mouse button is released.
        The initial values of the ball velocity components vx and vy depend on the position of the mouse.
        """
        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.x = self.x
        new_ball.y = self.y
        new_ball.vx = int(self.f2_power * math.cos(self.an) / 1.5)
        new_ball.vy = -int(self.f2_power * math.sin(self.an) / 1.5)
        new_ball.type = type
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 20

    def draw(self):
        """Draw gun

        :return: none
        """
        l = self.f2_power + 10
        w = 7
        polygon(screen, self.color, [(self.x, self.y),
                                     (self.x + l * math.cos(self.an), self.y + l * math.sin(self.an)),
                                     (self.x + l * math.cos(self.an) + w * math.sin(self.an),
                                      self.y + l * math.sin(self.an) - w * math.cos(self.an)),
                                     (self.x + w * math.sin(self.an), self.y - w * math.cos(self.an))])

    def power_up(self):
        """Gun power up"""
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1


class Target:

    def __init__(self, screen: pygame.Surface, x=450, y=450):
        """Target class constructor

        :param screen: pygame screen
        :param x: position of target
        :param y: position of target
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.live = 1
        self.points = 0
        self.color = MAGENTA
        self.vx = 0
        self.vy = 0

    def new_target(self):
        """ Initializing a new target. """

        self.x = 20
        self.y = rnd(200, 400)
        self.r = 10
        self.live = 1
        self.vx = 5
        self.vy = 0

    def hit(self, points=1):
        """Ball hitting the target."""
        self.points += points

    def draw(self):
        """Draw target"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )

    def move(self):
        """Move target. One of the velocity projections is always zero.
        Randomly changes every 10 frames.
        """
        if self.y < 400:
            self.x += self.vx
            self.y += self.vy
            if 0 == rnd(0, 10):
                if self.vx == 0:
                    self.vx = 5
                    self.vy = 0
                else:
                    self.vx = 0
                    self.vy = rnd(-7, 7)
        else:
            self.vy = -self.vy
            self.y += self.vy - 2

    def bomb(self, bombs):
        """ Make new bomb
        :param bombs: current list of bombs
        :return: new list of bombs
        """
        new_ball = Ball(self.screen)
        new_ball.r += 5
        x = self.x
        y = self.y
        new_ball.x = x
        new_ball.y = y
        new_ball.type = 0
        vx = self.vx
        new_ball.vx = vx
        new_ball.vy = 0
        bombs.append(new_ball)
        return bombs


class Tank:

    def __init__(self, screen, gun):
        """Target class constructor

        :param screen: pygame screen
        :param gun: tank's gun
        """
        self.screen = screen
        self.vx = 4
        self.x = 40
        self.y = 690
        self.r = 30
        self.live = 10
        self.color = BLUE
        self.gun = gun
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.fire_key = pygame.K_e
        self.change_key = pygame.K_q
        self.bullet_type = 0
        self.balls = []
        self.edge_l = 20
        self.edge_r = 500
        self.point = 0
        self.type = 0
        self.k = 0
        self.fl = False
        gun.x = self.x
        gun.y = self.y

    def draw(self):
        """Draw tank and its gun
        :return: none
        """
        polygon(self.screen, self.color, [(self.x - 40, self.y),
                                          (self.x + 40, self.y),
                                          (self.x + 32, self.y + 20),
                                          (self.x - 32, self.y + 20)])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 20)
        self.gun.color = self.color
        self.gun.draw()

    def move(self, keys):
        """Move tank and its gun"""
        if keys[self.left_key]:
            if self.x + self.vx > self.edge_l:
                self.x -= self.vx
                self.gun.x -= self.vx
        if keys[self.right_key]:
            if self.x + self.vx < self.edge_r:
                self.x += self.vx
                self.gun.x += self.vx
        if keys[self.up_key]:
            self.gun.an -= math.asin(1) / 30
        if keys[self.down_key]:
            self.gun.an += math.asin(1) / 30
        if keys[self.fire_key] and not self.fl:
            self.gun.f2_on = 1
            self.fl = True
        elif not keys[self.fire_key] and self.fl:
            self.gun.fire2_end(self.balls, self.type)
            self.fl = False
        if self.k == 0 and pygame.key.get_pressed()[self.change_key]:
            self.type = (self.type + 1) % 2
            self.k = 30
        if self.k > 0:
            self.k -= 1
        self.gun.power_up()

    def object_hit(self, objects):
        """Check hit balls
        :param objects: list of object to check hit
        :return: none
        """
        delete_list = []
        for i in range(len(self.balls)):
            b = self.balls[i]
            b.move()
            for target in objects:
                if b.hittest(target) and target.live:
                    target.live = 0
                    self.point += 1
                    target.new_target()
            if b.live < 0:
                delete_list.append(i)
        for target in objects:
            if target.x + target.vx + target.r > WIDTH or target.x + target.vx - target.r < 0:
                target.new_target()
        for i in delete_list:
            self.balls.pop(i)

    def explosion(self, bombs):
        """They will check the collision of the target bomb with the tank. The tank loses one life on hit.
        :param bombs: current list of bombs
        :return: none
        """
        delete_list = []
        for i in range(len(bombs)):
            b = bombs[i]
            if b.hittest(self):
                self.live -= 1
                delete_list.append(i)
            if b.live < 0:
                delete_list.append(i)
        for i in delete_list:
            bombs.pop(i)

    def bomb_enemy(self, enemy):
        """Checks to hit the enemy, the tank gets five points,
        the enemy loses one life on hit.
        :param bombs: enemy
        :return: none
        """
        delete_list = []
        for i in range(len(self.balls)):
            b = self.balls[i]
            if b.hittest(enemy):
                enemy.live -= 1
                self.point += 5
                delete_list.append(i)
            if b.live < 0:
                delete_list.append(i)
        for i in delete_list:
            self.balls.pop(i)


class Helicopter:

    def __init__(self, screen: pygame.Surface, x=450, y=450):
        """Target class constructor
        :param screen:
        :param x: position of helicopter
        :param y: position of helicopter
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.live = 1
        self.points = 0
        self.color = GREEN
        self.vy = 4
        self.vx = 5

    def new_target(self):
        """ Initializing a new helicopter. """
        self.x = 0
        self.y = rnd(200, 400)
        self.r = 10
        self.live = 1

    def hit(self, points=1):
        """Ball hitting the helicopter."""
        self.points += points

    def draw(self):
        """draw helicopter"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )

    def move(self):
        """Move helicopter, randomly changes every four times"""
        if self.y < 400:
            self.x += self.vx
            self.y += self.vy
            if 1 == rnd(0, 7):
                self.vy = -self.vy
        else:
            self.vy = -self.vy
            self.y += self.vy - 2


def text_start(text):
    """draw start text"""
    txt = text.render('Правила', True, (139, 0, 255))
    screen.blit(txt, (20, 30))
    txt = text.render(
        'Для первого игрока: стрелки вверх-вниз за пушку, стрелки вправо-влево за движение, SPACE - выстрел, C - сменить типи снаряда',
        True, (139, 0, 255))
    screen.blit(txt, (20, 50))
    txt = text.render('Для второго игрока: W-S за пушку, A-D за движение, E - выстрел, Q - сменить типи снаряда',
                      True, (139, 0, 255))
    screen.blit(txt, (20, 70))
    txt = text.render(
        'Для победы уничтожьте противника или наберите 50 очков, за попадания в противника - 5 очков, за попадание в мишень 1',
        True, (139, 0, 255))
    screen.blit(txt, (20, 90))
    txt = text.render('Нажмите на крестик, чтобы начать игру', True, (139, 0, 255))
    screen.blit(txt, (20, 110))
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        pygame.display.update()
    screen.fill(WHITE)


def text_score(text, tank1, tank2):
    """draw score text"""
    txt = text.render('score: ' + str(tank1.point), True, (139, 0, 255))
    screen.blit(txt, (20, 30))
    txt = text.render('live: ' + str(tank1.live), True, (139, 0, 255))
    screen.blit(txt, (20, 50))
    txt = text.render('score: ' + str(tank2.point), True, (139, 0, 255))
    screen.blit(txt, (1350, 30))
    txt = text.render('live: ' + str(tank2.live), True, (139, 0, 255))
    screen.blit(txt, (1350, 50))
    pygame.display.update()


# pygame start

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
text = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

# lists for targets, helicopters and bombs
targets = []
helicopters = []
bombs = []

# make tank1
gun1 = Gun(screen)
tank1 = Tank(screen, gun1)

# make tank2
gun2 = Gun(screen)
tank2 = Tank(screen, gun2)
tank2.x = 1300
tank2.gun.x = 1300
tank2.gun.color = RED
tank2.color = RED
tank2.left_key = pygame.K_LEFT
tank2.right_key = pygame.K_RIGHT
tank2.up_key = pygame.K_DOWN
tank2.down_key = pygame.K_UP
tank2.fire_key = pygame.K_SPACE
tank2.change_key = pygame.K_c
tank2.edge_l = 800
tank2.edge_r = 1420

# make Targets
for i in range(6):
    targets.append(Target(screen))
for i in range(6):
    targets[i].new_target()
    targets[i].x += 200 * i

# make Helicopters
for i in range(6):
    helicopters.append(Helicopter(screen))
for i in range(6):
    helicopters[i].new_target()
    helicopters[i].x += 200 * i

text_start(text)
finished = False
win = 0

# main of game
while not finished:

    # points comparison
    if tank1.point == 50 or tank2.live < 1:
        win = 1
        break
    if tank2.point == 50 or tank1.live < 1:
        win = 2
        break

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    screen.fill(WHITE)
    line(screen, BLACK,
         [0, 710],
         [1440, 710])
    # draw and move

    tank1.draw()
    tank2.draw()

    for helicopter in helicopters:
        helicopter.draw()
        helicopter.move()

    for target in targets:
        target.draw()
        target.move()
        if 0 == rnd(0, 120):
            bombs = target.bomb(bombs)

    for i in range(len(bombs)):
        b = bombs[i]
        b.move()
        b.draw()

    for b in tank1.balls + tank2.balls:
        b.draw()

    # print text score
    text_score(text, tank1, tank2)

    # tanks move
    tank1.move(pygame.key.get_pressed())
    tank2.move(pygame.key.get_pressed())

    # tanks hit objects
    tank1.object_hit(targets + helicopters)
    tank2.object_hit(targets + helicopters)

    # bombs hit tanks
    tank1.explosion(bombs)
    tank2.explosion(bombs)

    # tank1 and tank2 hit each other
    tank1.bomb_enemy(tank2)
    tank2.bomb_enemy(tank1)

pygame.display.update()
screen.fill(WHITE)

# end text
if win != 0:
    score_text = text.render('Player ' + str(win) + ' win', True, (139, 0, 255))
    screen.blit(score_text, (700, 360))
    finished = False
else:
    score_text = text.render('Draw', True, (139, 0, 255))
    screen.blit(score_text, (700, 360))
    finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()

pygame.quit()
