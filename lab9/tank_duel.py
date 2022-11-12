import math
from random import choice, randint

import pygame
from pygame.draw import circle, polygon

import numpy as np

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
TANK_COLORS = [YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

List_of_tanks = {}
Health_of_tanks = {}
List_of_guns = {}
Max_number = 0
Current_number = 0


class Tank:
    def __init__(self, num, scr: pygame.Surface, x=400, y=450):
        self.scr = screen
        self.x = x
        self.y = y
        self.color = choice(TANK_COLORS)
        self.vx = 0
        self.health_points = 5
        List_of_tanks.update({num: self})
        Health_of_tanks.update({num: self})

    def tank_draw(self):
        """Draws the body of the tank
        """
        polygon(screen, color=self.color, points=[[self.x - 30, self.y],
                                                  [self.x + 30, self.y],
                                                  [self.x + 30, self.y + 15],
                                                  [self.x - 30, self.y + 15]])
        circle(screen, color=self.color, center=(self.x, self.y), radius=10)

    def tank_control(self):
        """Controls the movement of the tank.
        """
        if pygame.key.get_pressed()[pygame.K_d] and self.x < 770:
            self.x += 3
            return True
        if pygame.key.get_pressed()[pygame.K_a] and self.x > 30:
            self.x -= 3
            return True


class Rocket:
    def __init__(self, x, y, scr: pygame.Surface, shooter, angle=0, length=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.an = angle
        self.len = length
        self.color = choice(GAME_COLORS)
        self.alpha_1 = None
        self.alpha_2 = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.x3 = None
        self.y3 = None
        self.x4 = None
        self.y4 = None
        self.closest_point = None
        self.vx = None
        self.vy = None
        self.shooter = shooter

    def rocket_coordinates(self):
        """Defines coordinates of the angles of the rocket
        """
        self.alpha_1 = self.an + 0.5
        self.alpha_2 = self.an - 0.5
        self.x1 = self.x + math.cos(self.alpha_1) * 5
        self.y1 = self.y + math.sin(self.alpha_1) * 5
        self.x2 = self.x + math.cos(self.alpha_2) * 5
        self.y2 = self.y + math.sin(self.alpha_2) * 5
        self.x3 = self.x2 + math.cos(self.an) * self.len
        self.y3 = self.y2 + math.sin(self.an) * self.len
        self.x4 = self.x1 + math.cos(self.an) * self.len
        self.y4 = self.y1 + math.sin(self.an) * self.len

    def rocket_closest_point(self, obj):
        """Finds the rocket point closest to the center of the target and its
        distance to it.
        Firstly, finds the closest angle.
        Secondly, finds two points of crossing of the sides with common
        closest angle, that we already found, with their normals.
        Thirdly, if the points belong to the sides of the rectangle, than it
        chooses the closest one and returns its distance to the center of the
        target.
        Fourthly, if none of the points belong to the sides, than it returns
        the distance between the closest angle and the center of the target.

        :param obj: round target
        """
        var = []
        coord = [[self.x1, self.y1],
                 [self.x2, self.y2],
                 [self.x3, self.y3],
                 [self.x4, self.y4]]
        distance = []
        for i in range(len(coord)):
            distance.append(((coord[i][0] - obj.x)**2 +
                             (coord[i][1] - obj.y)**2)**0.5)
        c = distance.index(min(distance))
        var.append(min(distance))
        eq_1 = np.array([[(coord[c-1][0] - coord[c][0]) /
                        (coord[c-1][1] - coord[c][1]), 1],
                      [- (coord[c-1][1] - coord[c][1]) /
                       (coord[c-1][0] - coord[c][0]), 1]])
        ans_1 = np.array([obj.y + (coord[c-1][0] - coord[c][0]) /
                         (coord[c-1][1] - coord[c][1]) * obj.x,
                          coord[c][1] - (coord[c-1][1] - coord[c][1]) /
                         (coord[c-1][0] - coord[c][0]) * coord[c][0]])
        solv_1 = list(np.linalg.solve(eq_1, ans_1))
        eq_2 = np.array([[(coord[c][0] - coord[c-len(coord)+1][0]) /
                          (coord[c][1] - coord[c-len(coord)+1][1]), 1],
                        [-(coord[c][1] - coord[c-len(coord)+1][1]) /
                          (coord[c][0] - coord[c-len(coord)+1][0]), 1]])
        ans_2 = np.array([obj.y + (coord[c][0] - coord[c-len(coord)+1][0]) /
                         (coord[c][1] - coord[c-len(coord)+1][1]) * obj.x,
                          coord[c-len(coord)+1][1] -
                         (coord[c][1] - coord[c-len(coord)+1][1]) /
                         (coord[c][0] - coord[c-len(coord)+1][0]) *
                          coord[c - len(coord) + 1][0]])
        solv_2 = list(np.linalg.solve(eq_2, ans_2))
        if coord[c][0] >= solv_1[0] >= coord[c-1][0] or \
                coord[c-1][0] >= solv_1[0] >= coord[c][0]:
            var.append(((solv_1[0] - obj.x)**2 + (solv_1[1] - obj.y)**2)**0.5)
        if coord[c][0] >= solv_2[0] >= coord[c-len(coord)+1][0] or \
                coord[c-len(coord)+1][0] >= solv_2[0] >= coord[c][0]:
            var.append(((solv_2[0] - obj.x)**2 + (solv_2[1] - obj.y)**2)**0.5)
        self.closest_point = min(var)

    def rocket_hit_detection_square(self, obj):
        coord = [[self.x1, self.y1],
                 [self.x2, self.y2],
                 [self.x3, self.y3],
                 [self.x4, self.y4]]

        def equation_x(i, x):
            return coord[i][1] + (coord[i-1][1] - coord[i][1]) / \
                   (coord[i-1][0] - coord[i][0]) * (x - coord[i][0])

        def equation_y(i, y):
            return coord[i][0] + (coord[i-1][0] - coord[i][0]) / \
                   (coord[i-1][1] - coord[i][1]) * (y - coord[i][1])

        for x in [obj.x - obj.a, obj.x + obj.a]:
            for i in range(4):
                if obj.y - obj.a <= equation_x(i, x) <= obj.y + obj.a and \
                        (coord[i][1] <= equation_x(i, x) <= coord[i-1][1] or
                         coord[i][1] >= equation_x(i, x) >= coord[i-1][1]):
                    return True
        for y in [obj.y - obj.a, obj.y + obj.a]:
            for i in range(4):
                if obj.x - obj.a <= equation_y(i, y) <= obj.x + obj.a and \
                        (coord[i][0] <= equation_y(i, y) <= coord[i-1][0] or
                         coord[i][0] >= equation_y(i, y) >= coord[i-1][0]):
                    return True
        return False

    def rocket_hit_detection_tank(self, obj):
        coord = [[self.x1, self.y1],
                 [self.x2, self.y2],
                 [self.x3, self.y3],
                 [self.x4, self.y4]]

        def equation_x(i, x):
            return coord[i][1] + (coord[i - 1][1] - coord[i][1]) / \
                   (coord[i - 1][0] - coord[i][0]) * (x - coord[i][0])

        def equation_y(i, y):
            return coord[i][0] + (coord[i - 1][0] - coord[i][0]) / \
                   (coord[i - 1][1] - coord[i][1]) * (y - coord[i][1])

        for x in [obj.x - 30, obj.x + 30]:
            for i in range(4):
                if obj.y <= equation_x(i, x) <= obj.y + 15 and \
                        (coord[i][1] <= equation_x(i, x) <= coord[i - 1][1] or
                         coord[i][1] >= equation_x(i, x) >= coord[i - 1][1]):
                    return True
        for y in [obj.y, obj.y + 15]:
            for i in range(4):
                if obj.x - 30 <= equation_y(i, y) <= obj.x + 30 and \
                        (coord[i][0] <= equation_y(i, y) <= coord[i - 1][0] or
                         coord[i][0] >= equation_y(i, y) >= coord[i - 1][0]):
                    return True
        var = []
        distance = []
        for i in range(len(coord)):
            distance.append(((coord[i][0] - obj.x) ** 2 +
                             (coord[i][1] - obj.y) ** 2) ** 0.5)
        c = distance.index(min(distance))
        var.append(min(distance))
        eq_1 = np.array([[(coord[c - 1][0] - coord[c][0]) /
                          (coord[c - 1][1] - coord[c][1]), 1],
                         [- (coord[c - 1][1] - coord[c][1]) /
                          (coord[c - 1][0] - coord[c][0]), 1]])
        ans_1 = np.array([obj.y + (coord[c - 1][0] - coord[c][0]) /
                          (coord[c - 1][1] - coord[c][1]) * obj.x,
                          coord[c][1] - (coord[c - 1][1] - coord[c][1]) /
                          (coord[c - 1][0] - coord[c][0]) * coord[c][0]])
        solv_1 = list(np.linalg.solve(eq_1, ans_1))
        eq_2 = np.array([[(coord[c][0] - coord[c - len(coord) + 1][0]) /
                          (coord[c][1] - coord[c - len(coord) + 1][1]), 1],
                         [-(coord[c][1] - coord[c - len(coord) + 1][1]) /
                          (coord[c][0] - coord[c - len(coord) + 1][0]), 1]])
        ans_2 = np.array(
            [obj.y + (coord[c][0] - coord[c - len(coord) + 1][0]) /
             (coord[c][1] - coord[c - len(coord) + 1][1]) * obj.x,
             coord[c - len(coord) + 1][1] -
             (coord[c][1] - coord[c - len(coord) + 1][1]) /
             (coord[c][0] - coord[c - len(coord) + 1][0]) *
             coord[c - len(coord) + 1][0]])
        solv_2 = list(np.linalg.solve(eq_2, ans_2))
        if coord[c][0] >= solv_1[0] >= coord[c - 1][0] or \
                coord[c - 1][0] >= solv_1[0] >= coord[c][0]:
            var.append(
                ((solv_1[0] - obj.x) ** 2 + (solv_1[1] - obj.y) ** 2) ** 0.5)
        if coord[c][0] >= solv_2[0] >= coord[c - len(coord) + 1][0] or \
                coord[c - len(coord) + 1][0] >= solv_2[0] >= coord[c][0]:
            var.append(
                ((solv_2[0] - obj.x) ** 2 + (solv_2[1] - obj.y) ** 2) ** 0.5)
        self.closest_point = min(var)

    def rocket_draw(self):
        """Draws a rectangle of the rocket
        """
        polygon(screen, color=self.color,
                points=[[self.x1, self.y1],
                        [self.x2, self.y2],
                        [self.x3, self.y3],
                        [self.x4, self.y4]])

    def rocket_move(self):
        """Moves the rocket with every frame.
        """
        self.x += self.vx
        self.y += -self.vy

    def rocket_hit_detection(self, obj):
        """Compares the distance between the chosen point
        and the center of the target.

        :param obj: round target
        """
        if self.closest_point > obj.r:
            return False
        else:
            return True

    def rocket_slowing_down(self):
        """Stops the rocket after hitting the right side of the screen
        """
        if (self.x3 >= 800 or self.x4 >= 800) or\
           (self.x3 <= 0 or self.x4 <= 0) or \
           (self.y3 >= 600 or self.y4 >= 600) or \
           (self.y3 <= 0 or self.y4 <= 0):
            self.vx = 0
            self.vy = 0

    def rocket_removal(self):
        """Adds the rocket to the list to deletion
        after some time after its full stop"""
        if rockets_with_time[self] != 0 and \
                current_time - rockets_with_time[r] > 1000:
            rubbish_bin.append(r)


class Ball:
    def __init__(self, x, y, shooter, scr: pygame.Surface):
        """Constructor of the Ball class.
        :param scr: pygame screen
        :param x, y: initial coordinates of the center of the circle
        """
        self.scr = screen
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.shooter = shooter

    def ball_move(self):
        """Moves the circle in certain direction with each frame.
        Velocity on x-axis is permanent.
        Velocity on y-axis changes with each frame (simulates the gravity).
        """
        if self.y < 585:
            self.vy -= 2
        self.x += self.vx
        self.y -= self.vy

    def ball_draw(self):
        """Draws the circle with a certain coordinates of its center.
        """
        pygame.draw.circle(
            self.scr,
            self.color,
            (self.x, self.y),
            self.r)

    def ball_hit_detection(self, obj):
        """Checks the collision with given object.
        :param obj: colliding object
        :return: True, if collides; False, if not.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= \
                (self.r + obj.r) ** 2:
            self.shooter.points += 1
            return True
        else:
            return False

    def ball_hit_detection_square(self, obj):
        """Checks the hitting into the square target.

        :param obj: square target.
        :return: True, if collides; False, if not.
        """
        if obj.x - obj.a <= self.x <= obj.x + obj.a and \
                obj.y - obj.a - self.r <= self.y <= obj.y + obj.a + self.r:
            self.shooter.points += 1
            return True
        elif obj.x - obj.a - self.r <= self.x <= obj.x + obj.a + self.r and \
                obj.y - obj.a <= self.y <= obj.y + obj.a:
            self.shooter.points += 1
            return True
        elif obj.x + obj.a <= self.x <= obj.x + obj.a + self.r and \
                obj.y + obj.a <= self.y <= obj.y + obj.a + self.r and \
                ((self.x - obj.x - obj.a)**2 +
                 (self.y - obj.y - obj.a)**2)**0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x - obj.a >= self.x >= obj.x - obj.a - self.r and \
                obj.y - obj.a >= self.y >= obj.y - obj.a - self.r and \
                ((self.x - obj.x + obj.a)**2 +
                 (self.y - obj.y + obj.a)**2)**0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x + obj.a <= self.x <= obj.x + obj.a + self.r and \
                obj.y - obj.a >= self.y >= obj.y - obj.a - self.r and \
                ((self.x - obj.x - obj.a) ** 2 +
                 (self.y - obj.y + obj.a) ** 2) ** 0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x - obj.a >= self.x >= obj.x - obj.a - self.r and \
                obj.y + obj.a <= self.y <= obj.y + obj.a + self.r and \
                ((self.x - obj.x + obj.a) ** 2 +
                 (self.y - obj.y - obj.a) ** 2) ** 0.5 <= self.r:
            self.shooter.points += 1
            return True
        else:
            return False

    def ball_hit_detection_tank(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= \
                (self.r + 10) ** 2:
            return True
        if obj.x - 30 <= self.x <= obj.x + 30 and \
                obj.y - self.r <= self.y <= obj.y + 15 + self.r:
            self.shooter.points += 1
            return True
        elif obj.x - 30 - self.r <= self.x <= obj.x + 30 + self.r and \
                obj.y <= self.y <= obj.y + 15:
            self.shooter.points += 1
            return True
        elif obj.x + 30 <= self.x <= obj.x + 30 + self.r and \
                obj.y + 15 <= self.y <= obj.y + 15 + self.r and \
                ((self.x - obj.x - 30)**2 +
                 (self.y - obj.y - 15)**2)**0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x - 30 >= self.x >= obj.x - 30 - self.r and \
                obj.y >= self.y >= obj.y - self.r and \
                ((self.x - obj.x + 30)**2 +
                 (self.y - obj.y + 15)**2)**0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x + 30 <= self.x <= obj.x + 30 + self.r and \
                obj.y >= self.y >= obj.y - self.r and \
                ((self.x - obj.x - 30) ** 2 +
                 (self.y - obj.y + 15) ** 2) ** 0.5 <= self.r:
            self.shooter.points += 1
            return True
        elif obj.x - 30 >= self.x >= obj.x - 30 - self.r and \
                obj.y + 15 <= self.y <= obj.y + 15 + self.r and \
                ((self.x - obj.x + 30) ** 2 +
                 (self.y - obj.y - 15) ** 2) ** 0.5 <= self.r:
            self.shooter.points += 1
            return True
        else:
            return False

    def ball_reflection(self):
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
                self.vx = 0
        if self.x <= 15:
            self.vy = 0.5 * self.vy
            if abs(self.vx) >= 0.5 and self.vx < 0:
                self.vx = -0.8 * self.vx
            elif abs(self.vx) < 0.5:
                self.vx = 0

    def ball_removal(self):
        """Adds the circle to the list to deletion
        after some time after its full stop"""
        if balls_with_time[self] != 0 and \
           current_time - balls_with_time[self] > 1000:
            rubbish_bin.append(b)


def cleaning_the_bin():
    """Removes deletion candidates from the list
    of the existing circles and rockets and rubbish bin.
    """
    while rubbish_bin:
        if rubbish_bin[0] in balls_with_time:
            balls_with_time.pop(rubbish_bin[0])
        if rubbish_bin[0] in rockets_with_time:
            rockets_with_time.pop(rubbish_bin[0])
        rubbish_bin.remove(rubbish_bin[0])


class Gun:
    def __init__(self, scr, x, num):
        self.screen = scr
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.sign = 1
        self.points = 0
        List_of_guns.update({num: self})

    def gun_fire2_start(self):
        self.f2_on = 1

    def gun_fire2_end(self, ev, num):
        """Firing the bullet
        Movement direction of the bullet (vx, vy)
        depends on the position of the cursor.
        Speed of the bullet depends on the power of gun.
        """
        global balls_with_time, bullet
        bullet += 1
        if event.button == 1:
            new_ball = Ball(scr=self.screen, x=List_of_tanks[num].x,
                            y=List_of_tanks[num].y, shooter=self)
            self.an = math.atan2((ev.pos[1]-new_ball.y),
                                 (ev.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            balls_with_time.update({new_ball: 0})
        elif event.button == 3:
            new_rocket = Rocket(scr=self.screen, angle=0,
                                x=List_of_tanks[num].x, y=List_of_tanks[num].y,
                                shooter=self)
            self.an = math.atan2((ev.pos[1] - new_rocket.y),
                                 (ev.pos[0] - new_rocket.x))
            new_rocket.an = self.an
            new_rocket.len = self.f2_power
            new_rocket.vx = self.f2_power * math.cos(self.an)
            new_rocket.vy = - self.f2_power * math.sin(self.an)
            rockets_with_time.update({new_rocket: 0})
        self.f2_on = 0
        self.f2_power = 10

    def gun_targeting(self, num):
        """Targeting of the gun.
        Depends on coordinates of the mouse on the screen.
        """
        if pygame.mouse.get_pos()[0] - List_of_tanks[num].x > 0:
            self.an = math.atan((pygame.mouse.get_pos()[1]-450) /
                                (pygame.mouse.get_pos()[0] -
                                 List_of_tanks[num].x))
            self.sign = 1
        elif pygame.mouse.get_pos()[0] - List_of_tanks[num].x < 0:
            self.an = math.atan((pygame.mouse.get_pos()[1] - 450) /
                                (pygame.mouse.get_pos()[0] -
                                 List_of_tanks[num].x))
            self.sign = -1
        elif pygame.mouse.get_pos()[0] - List_of_tanks[num].x == 0 and \
                pygame.mouse.get_pos()[1] - 450 > 0:
            self.an = math.pi / 2
            self.sign = 1
        elif pygame.mouse.get_pos()[0] - List_of_tanks[num].x == 0 and \
                pygame.mouse.get_pos()[1] - 450 < 0:
            self.an = math.pi / 2
            self.sign = -1
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def gun_draw(self, x):
        """Draws a gun in form of slim rectangle, oriented on the cursor.
        Length of rectangle depends on the current power of the gun.
        """
        alpha_1 = self.an + 0.5
        alpha_2 = self.an - 0.5
        x1 = x + self.sign * math.cos(alpha_1) * 5
        y1 = 450 + self.sign * math.sin(alpha_1) * 5
        x2 = x + self.sign * math.cos(alpha_2) * 5
        y2 = 450 + self.sign * math.sin(alpha_2) * 5
        x3 = x2 + self.sign * math.cos(self.an) * self.f2_power
        y3 = y2 + self.sign * math.sin(self.an) * self.f2_power
        x4 = x1 + self.sign * math.cos(self.an) * self.f2_power
        y4 = y1 + self.sign * math.sin(self.an) * self.f2_power
        polygon(screen, color=self.color,
                points=[[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    def gun_power_up(self):
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
        self.x = None
        self.y = None
        self.r = None
        self.vx = None
        self.vy = None
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
                self.x = randint(20, 780)
                self.y = randint(300, 550)
                self.r = randint(2, 50)
                self.vx = randint(1, 10)
                self.vy = randint(1, 10)
                self.color = RED
                self.live = 1

    def target_hit(self, points=1):
        """Add a point to the score after hitting the target.
        """
        self.points += points

    def target_reflection(self):
        """Reflection of the target after hitting the edge of the screen.
        """
        if self.x + self.r >= 800 and self.vx > 0:
            self.vx = -self.vx
        if self.x - self.r <= 0 and self.vx < 0:
            self.vx = -self.vx
        if self.y + self.r >= 600 and self.vy > 0:
            self.vy = -self.vy
        if self.y - self.r <= 0 and self.vy < 0:
            self.vy = -self.vy

    def target_movement(self):
        """Movement of the target with every frame.
        """
        self.x += self.vx
        self.y += self.vy

    def target_draw(self):
        """Draws a new target.
        """
        circle(screen, color=self.color,
               center=(self.x, self.y), radius=self.r)


class TargetSquare:
    def __init__(self):
        self.live = 1
        self.color = BLUE
        self.points = 0
        self.x = None
        self.y = None
        self.a = None
        self.vx = None
        self.vy = None
        self.new_target_square(a=0, b=0, c=Default_font.render(str(0),
                               True, (255, 255, 255)))

    def new_target_square(self, a, b, c):
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
                self.x = randint(20, 780)
                self.y = randint(300, 550)
                self.a = randint(2, 50)
                self.vx = randint(1, 10)
                self.vy = randint(1, 10)
                self.color = BLUE
                self.live = 1

    def square_hit(self, points=1):
        """Add a point to the score after hitting the target.
        """
        self.points += points

    def square_reflection(self):
        """Reflection of the target in the random direction
        after hitting the edge of the screen.
        """
        if self.x + self.a >= 800 and self.vx > 0:
            self.vx = -randint(1, 10)
            self.vy = randint(1, 10) * choice([-1, 1])
        if self.x - self.a <= 0 and self.vx < 0:
            self.vx = randint(1, 10)
            self.vy = randint(1, 10) * choice([-1, 1])
        if self.y + self.a >= 600 and self.vy > 0:
            self.vx = randint(1, 10) * choice([-1, 1])
            self.vy = -randint(1, 10)
        if self.y - self.a <= 0 and self.vy < 0:
            self.vx = randint(1, 10) * choice([-1, 1])
            self.vy = randint(1, 10)

    def square_movement(self):
        """Movement of the target with every frame.
        """
        self.x += self.vx
        self.y += self.vy

    def square_draw(self):
        """Draws a new target.
        """
        polygon(screen, color=self.color,
                points=[[self.x + self.a, self.y + self.a],
                        [self.x - self.a, self.y + self.a],
                        [self.x - self.a, self.y - self.a],
                        [self.x + self.a, self.y - self.a]])


def score_counter():
    """Adds the counter of hits to the upper-left corner of the screen.
    """
    score = Default_font.render('First tank: ' + str(List_of_guns[0].points) + '\nSecond tank: ' + str(List_of_guns[1].points), True, (0, 0, 0))
    screen.blit(score, (10, 10))


def event_checker(ev, num):
    if event.type == pygame.QUIT:
        return True
    if ev.type == pygame.MOUSEBUTTONDOWN and target1.live:
        List_of_guns[num].gun_fire2_start()
    elif ev.type == pygame.MOUSEBUTTONUP and target1.live:
        List_of_guns[num].gun_fire2_end(ev, num)


def number_changer(ev, num):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_c:
        if num == len(List_of_tanks) - 1:
            return 0
        else:
            return num+1
    else:
        return num


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bullet = 0      # Amount of bullets needed to hit the target
balls_with_time = {}        # Circles with their times of full stop
rockets_with_time = {}
rubbish_bin = []
time_of_hitting = 0

clock = pygame.time.Clock()
for i in [0, 1]:
    Tank(scr=screen, num=Max_number)
    Gun(scr=screen, num=Max_number, x=List_of_tanks[Max_number].x)
    Max_number += 1
current_time = 0

Default_font = pygame.font.SysFont('arial', 30)
amount_of_bullets = None

target1 = Target()
target2 = Target()
target_square1 = TargetSquare()
target_square2 = TargetSquare()

finished = False

while not finished:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    screen.fill(WHITE)

    List_of_tanks[Current_number].tank_control()
    List_of_guns[Current_number].gun_targeting(Current_number)
    for i in range(len(List_of_tanks)):
        List_of_tanks[i].tank_draw()
        List_of_guns[i].gun_draw(x=List_of_tanks[i].x)

    target1.target_reflection()
    target2.target_reflection()
    target1.target_movement()
    target2.target_movement()
    target1.target_draw()
    target2.target_draw()

    target_square1.square_reflection()
    target_square2.square_reflection()
    target_square1.square_movement()
    target_square2.square_movement()
    target_square1.square_draw()
    target_square2.square_draw()

    score_counter()

    for r in rockets_with_time.keys():
        r.rocket_draw()
        if r.vx == r.vy == 0 and rockets_with_time[r] == 0:
            rockets_with_time[r] = pygame.time.get_ticks()

    for b in balls_with_time.keys():
        b.ball_draw()
        if b.vx == b.vy == 0 and balls_with_time[b] == 0:
            balls_with_time[b] = pygame.time.get_ticks()

    for event in pygame.event.get():
        finished = event_checker(ev=event, num=Current_number)
        Current_number = number_changer(ev=event, num=Current_number)

    for b in balls_with_time.keys():
        b.ball_removal()
        b.ball_reflection()
        b.ball_move()
        if (b.ball_hit_detection(target1) or b.ball_hit_detection(target2) or
                b.ball_hit_detection_square(target_square1) or
                b.ball_hit_detection_square(target_square2) or
                b.ball_hit_detection_tank(List_of_tanks[1]) or
                b.ball_hit_detection_tank(List_of_tanks[1])) and \
                target1.live:
            amount_of_bullets = Default_font.render('Вы попали в цель за ' +
                                                    str(bullet) + ' выстрелов',
                                                    True, (0, 0, 0))
            bullet = 0
            target1.live = 0
            target2.live = 0
            target_square1.live = 0
            target_square2.live = 0
            time_of_hitting = pygame.time.get_ticks()
            target1.target_hit()

    for r in rockets_with_time.keys():
        r.rocket_removal()
        r.rocket_coordinates()
        r.rocket_slowing_down()
        r.rocket_move()
        r1 = r.rocket_closest_point(target1)
        r2 = r.rocket_closest_point(target2)
        if (r.rocket_hit_detection(obj=target1) or
                r.rocket_hit_detection(obj=target2) or
                r.rocket_hit_detection_square(obj=target_square1) or
                r.rocket_hit_detection_square(obj=target_square2) or
                r.rocket_hit_detection_tank(List_of_tanks[1])) and \
                target1.live:
            amount_of_bullets = Default_font.render('Вы попали в цель за ' +
                                                    str(bullet) + ' выстрелов',
                                                    True, (0, 0, 0))
            bullet = 0
            target1.live = 0
            target2.live = 0
            target_square1.live = 0
            target_square2.live = 0
            time_of_hitting = pygame.time.get_ticks()
            target1.target_hit()

    target1.new_target(a=time_of_hitting,
                       b=target1.live,
                       c=amount_of_bullets)
    target2.new_target(a=time_of_hitting,
                       b=target2.live,
                       c=amount_of_bullets)

    target_square1.new_target_square(a=time_of_hitting,
                                     b=target_square1.live,
                                     c=amount_of_bullets)
    target_square2.new_target_square(a=time_of_hitting,
                                     b=target_square2.live,
                                     c=amount_of_bullets)

    cleaning_the_bin()
    pygame.display.update()
    for i in [0, 1]:
        List_of_guns[i].gun_power_up()
pygame.quit()
