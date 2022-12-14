import math
from random import choice, randint

import pygame
from pygame.draw import circle, polygon

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


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """Constructor of the Ball class.
        :param screen: pygame screen
        :param x, y: initial coordinates of the center of the circle
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Moves the circle in certain direction with each frame.
        Velocity on x-axis is permanent.
        Velocity on y-axis changes with each frame (simulates the gravity).
        """
        if self.y < 585:
            self.vy -= 2
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """Draws the circle with a certain coordinates of its center.
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)

    def hit_detection(self, obj):
        """Checks the collision with given object.
        :param obj: colliding object
        :return: True, if collides; False, if not
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= \
                (self.r + obj.r) ** 2:
            return True
        else:
            return False

    def reflection(self):
        """Reflects and slows down the circle after hitting
        right or lower border of the screen
        """
        if self.y >= 585:
            if abs(self.vx) >= 0.5:
                self.vx = 0.5 * self.vx
            elif abs(self.vx) < 0.5:
                self.vx = 0
            if abs(self.vy) >= 1 and self.vy < 0:
                self.vy = -0.5 * self.vy
            elif abs(self.vy) < 1:
                self.vy = 0
                self.y = 585
        if self.x >= 785:
            self.vy = 0.5 * self.vy
            if abs(self.vx) >= 0.5 and self.vx > 0:
                self.vx = -0.8 * self.vx
            elif abs(self.vx) < 0.5:
                self.vx = 1

    def removal(self):
        """Adds the circle to the list to deletion
        after some time after its full stop"""
        if balls_with_time[b] != 0 and \
           current_time - balls_with_time[b] > 1000:
            balls_backrooms.append(b)


def cleaning_the_bin():
    """Removes deletion candidates from the list
    of the existing circles and rubbish bin
    """
    while balls_backrooms:
        balls_with_time.pop(balls_backrooms[0])
        balls_backrooms.remove(balls_backrooms[0])


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Firing the bullet
        Movement direction of the bullet (vx, vy)
        depends on the position of the cursor.
        Speed of the bullet depends on the power of gun.
        """
        global balls_with_time, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1]-new_ball.y),
                             (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls_with_time.update({new_ball: 0})
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event):
        """Targeting of the gun.
        Depends on coordinates of the mouse on the screen.
        """
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Draws a gun in form of slim rectangle, oriented on the cursor.
        Length of rectangle depends on the current power of the gun.
        """
        alpha_1 = self.an + 0.5
        alpha_2 = self.an - 0.5
        x1 = 40 + math.cos(alpha_1) * 5
        y1 = 450 + math.sin(alpha_1) * 5
        x2 = 40 + math.cos(alpha_2) * 5
        y2 = 450 + math.sin(alpha_2) * 5
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        x4 = x1 + math.cos(self.an) * self.f2_power
        y4 = y1 + math.sin(self.an) * self.f2_power
        polygon(screen, color=self.color,
                points=[[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    def power_up(self):
        """Increases the power of the gun by reaching the max power value
        """
        if self.f2_on and target1.live:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.live = 1
        self.color = RED
        self.points = 0
        self.new_target(a=0, b=0, c=Default_font.render(str(0), True,
                                                        (255, 255, 255)))

    def new_target(self, a, b, c):
        """After hitting the target with a bullet prints the message
         on the screen during the period of cooldown.
         After the period of cooldown defines a new target
         """
        if not b:
            if 3000 > current_time - a and a != 0:
                screen.blit(c, (250, 300))
                self.x = 1000
                self.y = 1000
                self.vx = 0
                self.vy = 0
            else:
                self.x = randint(600, 780)
                self.y = randint(300, 550)
                self.r = randint(2, 50)
                self.vx = randint(1, 10)
                self.vy = randint(1, 10)
                self.color = RED
                self.live = 1

    def hit(self, points=1):
        """Add a point to the score after hitting the target.
        """
        self.points += points

    def reflection(self):
        """Reflection of the target after hitting the edge of the screen.
        """
        if self.x + self.r >= 800 or self.x - self.r <= 400:
            self.vx = -self.vx
        if self.y + self.r >= 600 or self.y - self.r <= 0:
            self.vy = -self.vy

    def movement(self):
        """Movement of the target with every frame.
        """
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        """Draws a new target.
        """
        circle(screen, color=self.color,
               center=(self.x, self.y), radius=self.r)


def score_counter():
    """Adds the counter of hits to the upper-left corner of the screen.
    """
    score = Default_font.render(str(target1.points), True, (0, 0, 0))
    screen.blit(score, (10, 10))

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bullet = 0      # Amount of bullets needed to hit the target
balls_with_time = {}        # Circles with their times of full stop
balls_backrooms = []        # Rubbish bin
time_of_hitting = 0

clock = pygame.time.Clock()
gun = Gun(screen)
gun.color = GREY
current_time = 0

Default_font = pygame.font.SysFont(None, 30)
amount_of_balls = None

target1 = Target()
target2 = Target()

finished = False

while not finished:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    screen.fill(WHITE)
    gun.draw()

    target1.reflection()
    target2.reflection()
    target1.movement()
    target2.movement()
    target1.draw()
    target2.draw()

    score_counter()

    for b in balls_with_time.keys():
        b.draw()
        if b.vx == b.vy == 0 and balls_with_time[b] == 0:
            balls_with_time[b] = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and target1.live:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION and target1.live:
            gun.targeting(event)

    for b in balls_with_time.keys():
        b.removal()
        b.reflection()
        b.move()
        if b.hit_detection(target1) or b.hit_detection(target2) and \
                target1.live:
            amount_of_balls = Default_font.render('???? ???????????? ?? ???????? ???? ' +
                                                  str(bullet) + ' ??????????????????',
                                                  True, (0, 0, 0))
            bullet = 0
            target1.live = 0
            target2.live = 0
            time_of_hitting = pygame.time.get_ticks()
            target1.hit()
    target1.new_target(a=time_of_hitting,
                       b=target1.live,
                       c=amount_of_balls)
    target2.new_target(a=time_of_hitting,
                       b=target2.live,
                       c=amount_of_balls)

    cleaning_the_bin()
    pygame.display.update()
    gun.power_up()
pygame.quit()