import pygame
from pygame.draw import circle
from random import randint


def new_ball():
    """Draws a new circle of random color and radius
    at the random position on the screen.
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def quit_detector(event):
    """Detects clicks on the mouse button or quitting the game.
    Returns True, if the event is quitting,
    and False, if the event is click.

    :param event: occurred event of click or quitting
    """
    if event.type == pygame.QUIT:
        return True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        print('Click!')
        return False


def main_algorithm(finished, frequency):
    """Spawns random circles at the screen during every defined period of time.
    With every click function prints 'Click!' in the console.

    :param finished: parameter that shows the closure of screen
    :param frequency: frequency of changing of circles
    """
    while not finished:
        clock.tick(frequency)
        for event in pygame.event.get():
            finished = quit_detector(event)
        new_ball()
        pygame.display.update()
        screen.fill(BLACK)


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

main_algorithm(starting_argument, FPS)

pygame.quit()
