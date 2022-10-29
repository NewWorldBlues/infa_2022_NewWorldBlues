import pygame
from pygame.draw import circle
from random import randint, sample


def new_balls():
    """Draws from one to three new circles of random color and radius
    at the random positions on the screen.
    """
    global x, y, r, amount_of_circles
    amount_of_circles = randint(1, 3)
    x = sample(range(100, 1100), amount_of_circles)
    y = sample(range(100, 900), amount_of_circles)
    r = sample(range(10, 100), amount_of_circles)
    color = sample(COLORS, amount_of_circles)
    for i in range(amount_of_circles):
        circle(screen, color[i], (x[i], y[i]), r[i])


def hit_registration(x1, y1,
                     r1, event,
                     points):
    """Checks the hitting into the circles.
    Adds a point for hitting into the circles.

    :param x1, y1: coordinates of the centers of the circles
    :param r1: radii of the circles
    :param event: occurred event of click
    :param points: initial score
    """
    for i in range(amount_of_circles):
        if (event.pos[0] - x1[i])**2 + (event.pos[1] - y1[i])**2 <= r1[i]**2:
            print('Hit!')
            points += 1
    return points


def main_algorithm(finished, frequency, points):
    """Spawns random circles at the screen during every defined period of time.
    With every hitting into the circle prints "Hit!" and adds one point to the
    score.
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

        new_balls()
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
FPS = 2

main_algorithm(starting_argument, FPS, 0)

pygame.quit()
