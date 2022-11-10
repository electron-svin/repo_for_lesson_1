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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1440
HEIGHT = 720

GRAVITY = 1


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
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
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
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
        self.screen = screen
        self.f2_power = 20
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, balls, type):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
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
        l = self.f2_power + 10
        w = 7
        polygon(screen, self.color, [(self.x, self.y),
                                     (self.x + l * math.cos(self.an), self.y + l * math.sin(self.an)),
                                     (self.x + l * math.cos(self.an) + w * math.sin(self.an),
                                      self.y + l * math.sin(self.an) - w * math.cos(self.an)),
                                     (self.x + w * math.sin(self.an), self.y - w * math.cos(self.an))])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface, x=450, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.live = 1
        self.points = 0
        self.color = RED
        self.vx = 0
        self.vy = 0

    def new_target(self):
        """ Инициализация новой цели. """

        self.x = 20
        self.y = rnd(200, 400)
        self.r = 10
        self.color = RED
        self.live = 1
        self.vx = 5
        self.vy = 0

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
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

    def bomb(self):
        global bombs
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


class Tank:

    def __init__(self, screen, gun):
        self.screen = screen
        self.vx = 4
        self.x = 40
        self.y = 690
        self.r = 30
        self.live = 10
        self.color = BLUE
        self.gun = gun
        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN
        self.fire_key = pygame.K_SPACE
        self.bullet_type = 0
        self.balls = []
        gun.x = self.x
        gun.y = self.y
        self.edge_l = 20
        self.edge_r = 500


    def draw(self):
        polygon(self.screen, self.color, [(self.x - 40, self.y),
                                     (self.x + 40, self.y),
                                     (self.x + 32, self.y + 20),
                                     (self.x - 32, self.y + 20)])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 20)
        self.gun.color = self.color
        self.gun.draw()

    def move(self, keys, fl, balls, type):
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
        if keys[self.fire_key] and not fl:
            self.gun.fire2_start()
            fl = True
        elif not keys[self.fire_key] and fl:
            self.gun.fire2_end(balls, type)
            fl = False
        self.gun.power_up()
        return fl


class Helicopter:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface, x=450, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.live = 1
        self.points = 0
        self.color = RED
        self.vy = 4
        self.vx = 5

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = 0
        self.y = rnd(200, 400)
        self.r = 10
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
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
        if self.y < 400:
            self.x += self.vx
            self.y += self.vy
            if 1 == rnd(0, 7):
                self.vy = -self.vy
        else:
            self.vy = -self.vy
            self.y += self.vy - 2




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
text = pygame.font.Font(None, 24)
targets = []
helicopters = []
bombs = []

clock = pygame.time.Clock()
gun1 = Gun(screen)
tank1 = Tank(screen, gun1)
gun2 = Gun(screen)
tank2 = Tank(screen, gun2)
tank2.x = 1300
tank2.gun.x = 1300
tank2.gun.color = RED
tank2.color = RED
tank2.left_key = pygame.K_a
tank2.right_key = pygame.K_d
tank2.up_key = pygame.K_w
tank2.down_key = pygame.K_s
tank2.fire_key = pygame.K_e
tank2.edge_l = 800
tank2.edge_r = 1420

finished = False
fl1 = False
fl2 = False
for i in range(6):
    targets.append(Target(screen))
for i in range(6):
    helicopters.append(Helicopter(screen))
for i in range(6):
    targets[i].new_target()
    targets[i].x += 200*i
for i in range(6):
    helicopters[i].new_target()
    helicopters[i].x += 200*i
points1 = 0
points2 = 0
win = 0
type1 = 0
type2 = 0
score_text = text.render('Правила', True, (139, 0, 255))
screen.blit(score_text, (20, 30))
score_text = text.render('Для первого игрока: стрелки вверх-вниз за пушку, стрелки вправо-влево за движение, SPACE - выстрел, C - сменить типи снаряда', True, (139, 0, 255))
screen.blit(score_text, (20, 50))
score_text = text.render('Для второго игрока: W-S за пушку, A-D за движение, E - выстрел, Q - сменить типи снаряда', True, (139, 0, 255))
screen.blit(score_text, (20, 70))
score_text = text.render('Для победы уничтожьте противника или наберите 50 очков, за попадания в противника - 5 очков, за попадание в мишень 1', True, (139, 0, 255))
screen.blit(score_text, (20, 90))
score_text = text.render('Нажмите на крестик, чтобы начать игру', True, (139, 0, 255))
screen.blit(score_text, (20, 110))
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
screen.fill(WHITE)
finished = False
k1 = 0
k2 = 0
while not finished:
    if points1 == 50 or tank2.live < 1:
        win = 1
        break
    if points2 == 50 or tank1.live < 1:
        win = 2
        break
    screen.fill(WHITE)
    tank1.draw()
    tank2.draw()
    if k1 == 0 and pygame.key.get_pressed()[pygame.K_c]:
        type1 = (type1 + 1) % 2
        k1 = 30
    if k1 > 0:
        k1 -= 1
    if k2 == 0 and pygame.key.get_pressed()[pygame.K_q]:
        type2 = (type2 + 1) % 2
        k2 = 30
    if k2 > 0:
        k2 -= 1
    for target in targets:
        target.move()
    line(screen, BLACK,
                [0, 710],
                [1440, 710])
    for target in targets:
        target.draw()
        if 0 == rnd(0, 120):
            target.bomb()
    for i in range(len(bombs)):
        b = bombs[i]
        b.draw()
    for helicopter in helicopters:
        helicopter.draw()
        helicopter.move()
    for b in tank1.balls + tank2.balls:
        b.draw()
    score_text = text.render('score: ' + str(points1), True, (139, 0, 255))
    screen.blit(score_text, (20, 30))
    score_text = text.render('live: ' + str(tank1.live), True, (139, 0, 255))
    screen.blit(score_text, (20, 50))
    score_text = text.render('score: ' + str(points2), True, (139, 0, 255))
    screen.blit(score_text, (1350, 30))
    score_text = text.render('live: ' + str(tank2.live), True, (139, 0, 255))
    screen.blit(score_text, (1350, 50))
    pygame.display.update()

    clock.tick(FPS)
    fl1 = tank1.move(pygame.key.get_pressed(), fl1, tank1.balls, type1)
    fl2 = tank2.move(pygame.key.get_pressed(), fl2, tank2.balls, type2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    delete_list = []
    for i in range(len(tank1.balls)):
        b = tank1.balls[i]
        b.move()
        for target in targets + helicopters:
            if b.hittest(target) and target.live:
                target.live = 0
                points1 += 1
                target.new_target()
        if b.live < 0:
            delete_list.append(i)
    for target in targets + helicopters:
        if target.x + target.vx + target.r > WIDTH or target.x + target.vx - target.r < 0:
            target.new_target()
    for i in delete_list:
        tank1.balls.pop(i)

    delete_list = []
    for i in range(len(tank2.balls)):
        b = tank2.balls[i]
        b.move()
        for target in targets + helicopters:
            if b.hittest(target) and target.live:
                target.live = 0
                points2 += 1
                target.new_target()
        if b.live < 0:
            delete_list.append(i)
    for target in targets + helicopters:
        if target.x + target.vx + target.r > WIDTH or target.x + target.vx - target.r < 0:
            target.new_target()
    for i in delete_list:
        tank2.balls.pop(i)


    delete_list = []
    for i in range(len(bombs)):
        b = bombs[i]
        b.move()
        if b.hittest(tank1):
            tank1.live -= 1
            delete_list.append(i)
        if b.live < 0:
            delete_list.append(i)
    for i in delete_list:
        bombs.pop(i)

    delete_list = []
    for i in range(len(tank2.balls)):
        b = tank2.balls[i]
        if b.hittest(tank1):
            tank1.live -= 1
            points2 += 5
            delete_list.append(i)
        if b.live < 0:
            delete_list.append(i)
    for i in delete_list:
        tank2.balls.pop(i)

    delete_list = []
    for i in range(len(tank1.balls)):
        b = tank1.balls[i]
        if b.hittest(tank2):
            tank2.live -= 1
            points1 += 5
            delete_list.append(i)
        if b.live < 0:
            delete_list.append(i)
    for i in delete_list:
        tank1.balls.pop(i)

    delete_list = []
    for i in range(len(bombs)):
        b = bombs[i]
        if b.hittest(tank2):
            tank2.live -= 1
            delete_list.append(i)
        if b.live < 0:
            delete_list.append(i)
    for i in delete_list:
        bombs.pop(i)
pygame.display.update()
screen.fill(WHITE)
score_text = text.render('Player ' + str(win) + ' win', True, (139, 0, 255))
screen.blit(score_text, (720, 360))
finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()

pygame.quit()
