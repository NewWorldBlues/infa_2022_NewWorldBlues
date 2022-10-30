import pygame
from pygame.draw import circle
from random import randint, sample, choice


def new_balls():
    """Draws from one to three new circles of random color and radius
    at the random positions on the screen.
    """
    global x, y, r, amount_of_circles, color
    amount_of_circles = randint(1, 5)
    x = sample(range(100, 1100), amount_of_circles)
    y = sample(range(100, 900), amount_of_circles)
    r = sample(range(10, 100), amount_of_circles)
    color = sample(COLORS, amount_of_circles)
    for i in range(amount_of_circles):
        circle(screen, color[i], (x[i], y[i]), r[i])


def direction_vec(amount_of_circles):
    """Gives a direction and a value for circles' movement

    :param amount_of_circles: amount of circles
    """
    global x_vec, y_vec
    x_vec = [0 for i in range(amount_of_circles)]
    y_vec = [0 for i in range(amount_of_circles)]
    for i in range(amount_of_circles):
        x_vec[i] = randint(0, 5) * choice([1, -1])
        y_vec[i] = (25 - x_vec[i]**2)**0.5 * choice([1, -1])


def balls_moving(x, y,
                 r, amount_of_circles,
                 x_vec, y_vec,
                 color):
    """Changes coordinates of circles according to
    their speed and direction of movement.

    :param x, y: coordinates of the circles
    :param r: radii of the circles
    :param amount_of_circles: amount of circles
    :param x_vec: x-axis velocity
    :param y_vec: y-axis velocity
    :param color: colors of circles
    """
    for i in range(amount_of_circles):
        x[i] += x_vec[i]
        y[i] += y_vec[i]
        circle(screen, color[i], (x[i], y[i]), r[i])


def reflection(x, y,
               r, amount_of_circles,
               x_vec, y_vec):
    """Reflection of the circles after hitting the edge of the screen

    :param x, y: coordinates of the circles
    :param r: radii of the circles
    :param amount_of_circles: amount of circles
    :param x_vec: x-axis velocity
    :param y_vec: y-axis velocity
    """
    for i in range(amount_of_circles):
        if x[i] + r[i] >= 1200:
            x_vec[i] = -1 * randint(0, 5)
            y_vec[i] = (25 - x_vec[i]**2)**0.5 * choice([1, -1])
        if x[i] - r[i] <= 0:
            x_vec[i] = randint(0, 5)
            y_vec[i] = (25 - x_vec[i] ** 2) ** 0.5 * choice([1, -1])
        if y[i] + r[i] >= 900:
            x_vec[i] = randint(0, 5) * choice([-1, 1])
            y_vec[i] = -1 * (25 - x_vec[i] ** 2) ** 0.5
        if y[i] - r[i] <= 0:
            x_vec[i] = randint(0, 5) * choice([-1, 1])
            y_vec[i] = (25 - x_vec[i] ** 2) ** 0.5


def hit_registration(x1, y1,
                     r1, event):
    """Checks the hitting into the circles.
    Adds a point for hitting into the circles.

    :param x1, y1: coordinates of the centers of the circles
    :param r1: radii of the circles
    :param event: occurred event of click
    """
    delta_points = 0
    for i in range(amount_of_circles):
        if (event.pos[0] - x1[i])**2 + (event.pos[1] - y1[i])**2 <= r1[i]**2:
            print('Hit!')
            delta_points += 1
    return delta_points


def main_algorithm(finished, frequency):
    """Spawns random circles at the screen with random velocities.
    With every hitting into the circle prints "Hit!", adds one point to the
    score and respawns circles with random velocities.
    After closure of the window prints player's score

    :param finished: parameter that shows the closure of screen
    :param frequency: frequency of changing of circles
    """
    points = 0
    while not finished:
        clock.tick(frequency)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                delta_points = hit_registration(x, y, r, event)
                points += delta_points
                if delta_points:
                    new_balls()
                    direction_vec(amount_of_circles)
        reflection(x, y, r, amount_of_circles, x_vec, y_vec)
        balls_moving(x, y, r, amount_of_circles, x_vec, y_vec, color)
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
FPS = 60

new_balls()
direction_vec(amount_of_circles)

main_algorithm(starting_argument, FPS)

pygame.quit()
