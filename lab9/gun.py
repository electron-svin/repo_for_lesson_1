import math
from random import choice
from random import randint as rnd
from pygame.draw import *

import pygame

FPS = 30

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

WIDTH = 800
HEIGHT = 600

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
        self.r = 10
        self.vx = 0
        self.vy = 0.0
        self.color = choice(GAME_COLORS)
        self.live = 120

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.vx + self.r > WIDTH or self.x + self.vx - self.r < 0:
            self.vx = -self.vx // 2
            if abs(self.vx) <= 1:
                self.vx = 0
        if self.y - self.vy + self.r > HEIGHT:
            self.vy = -self.vy // 2
            if abs(self.vy) == 1:
                self.vy = 0
        self.x += self.vx
        self.y -= self.vy
        self.vy -= GRAVITY
        self.live -= 1

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

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 20
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) // 2
        new_ball.vy = - self.f2_power * math.sin(self.an) // 2
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 20

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - 20 == 0:
                self.an = math.asin(1)
            else:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        l = self.f2_power
        w = 7
        polygon(screen, self.color, [(20, 450),
                                     (20 + l * math.cos(self.an), 450 + l * math.sin(self.an)),
                                     (20 + l * math.cos(self.an) + w * math.sin(self.an),
                                      450 + l * math.sin(self.an) - w * math.cos(self.an)),
                                     (20 + w * math.sin(self.an), 450 - w * math.cos(self.an))])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


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

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(5, 15)
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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
text = pygame.font.Font(None, 24)
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
finished = False
for i in range(2):
    targets.append(Target(screen))
for target in targets:
    target.new_target()
while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    score_text = text.render('score: ' + str(target.points), True, (139, 0, 255))
    screen.blit(score_text, (20, 30))
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    delete_list = []
    for i in range(len(balls)):
        b = balls[i]
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                pygame.display.update()
                screen.fill(WHITE)
                gun.draw()
                for b in balls:
                    b.draw()
                score_text = text.render('score: ' + str(target.points), True, (139, 0, 255))
                screen.blit(score_text, (20, 30))
                score_text = text.render('Вы уничтожили цель за ' + str(bullet) + " выстрелов", True, (0, 214, 120))
                screen.blit(score_text, (250, 250))
                bullet = 0
                pygame.display.update()
                clock.tick(1)
                target.live = 0
                target.hit()
                target.new_target()
        if b.live < 0:
            delete_list.append(i)
    for i in delete_list:
        balls.pop(i)
    gun.power_up()

pygame.quit()
