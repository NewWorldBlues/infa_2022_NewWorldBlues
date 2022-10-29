import pygame
from pygame.draw import circle
from random import randint


def new_ball():
    """Draws a new circle of random color and radius
    at the random position on the screen.
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def hit_registration(x1, y1,
                     r1, event,
                     points):
    """Checks the hitting into the circle.
    Adds a point for hitting into the circle.

    :param x1, y1: coordinates of the center of the circle
    :param r1: radius of the circle
    :param event: occurred event of click
    :param points: initial score
    """
    if (event.pos[0] - x1)**2 + (event.pos[1] - y1)**2 <= r1**2:
        print('Hit!')
        return points + 1
    else:
        print('Miss!')
        return points


def main_algorithm(finished, frequency, points):
    """Spawns random circles at the screen during every defined period of time.
    With every hitting into the circle prints "Hit!" and adds one point to the
    score.
    With every missing prints "Miss!"
    After closure of the window prints player's score

    :param finished: parameter that shows the closure of screen
    :param frequency: frequency of changing of circles
    :param points: initial score
    """
    while not finished:
        clock.tick(frequency)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                points = hit_registration(x, y, r, event, points)
                break
        new_ball()
        pygame.display.update()
        screen.fill(BLACK)
    print('Your score is:', points)


pygame.init()

screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    RED, BLUE, YELLOW,
    GREEN, MAGENTA, CYAN
]

pygame.display.update()
clock = pygame.time.Clock()
starting_argument = False
FPS = 0.25

main_algorithm(starting_argument, FPS, 0)

pygame.quit()