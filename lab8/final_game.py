import pygame
from pygame.draw import circle, polygon
from random import randint, sample, choice


def new_squares():
    """Draws from one to three new squares of random color and size
    at the random positions on the screen.
    """
    global x_sq, y_sq, a, a_sq, color_sq
    a_sq = randint(1, 3)
    x_sq = sample(range(100, 1100), a_sq)
    y_sq = sample(range(100, 900), a_sq)
    a = sample(range(10, 50), a_sq)
    color_sq = sample(COLORS, a_sq)
    for i in range(a_sq):
        polygon(screen, color_sq[i], [[x_sq[i] - a[i], y_sq[i] - a[i]],
                                      [x_sq[i] - a[i], y_sq[i] + a[i]],
                                      [x_sq[i] + a[i], y_sq[i] + a[i]],
                                      [x_sq[i] + a[i], y_sq[i] - a[i]]])


def new_circles():
    """Draws from one to three new circles of random color and radius
    at the random positions on the screen.
    """
    global x_cir, y_cir, r, a_cir, color_cir
    a_cir = randint(1, 3)
    x_cir = sample(range(100, 1100), a_cir)
    y_cir = sample(range(100, 900), a_cir)
    r = sample(range(10, 100), a_cir)
    color_cir = sample(COLORS, a_cir)
    for i in range(a_cir):
        circle(screen, color_cir[i], (x_cir[i], y_cir[i]), r[i])


def direction_vec_cir(a_cir):
    """Gives a direction and a value for circles' movement

    :param a_cir: amount of circles
    """
    global x_vec_cir, y_vec_cir
    x_vec_cir = [0 for i in range(a_cir)]
    y_vec_cir = [0 for i in range(a_cir)]
    for i in range(a_cir):
        x_vec_cir[i] = randint(0, 5) * choice([1, -1])
        y_vec_cir[i] = (25 - x_vec_cir[i]**2)**0.5 * choice([1, -1])


def direction_vec_sq(a_sq):
    """Gives a direction and a value for squares' movement

    :param a_sq: amount of squares
    """
    global x_vec_sq, y_vec_sq
    x_vec_sq = [0 for i in range(a_sq)]
    y_vec_sq = [0 for i in range(a_sq)]
    for i in range(a_sq):
        x_vec_sq[i] = randint(0, 5) * choice([1, -1])
        y_vec_sq[i] = (25 - x_vec_sq[i]**2)**0.5 * choice([1, -1])


def squares_moving(x_sq, y_sq,
                   a_sq, x_vec_sq,
                   y_vec_sq, color_sq,
                   a):
    """Changes coordinates of the squares according to
    their speed and direction of movement.

    :param x_sq, y_sq: coordinates of the squares
    :param a: halves of the squares' sides
    :param a_sq: amount of squares
    :param x_vec_sq: x-axis velocity
    :param y_vec_sq: y-axis velocity
    :param color_sq: colors of circles
    """
    for i in range(a_sq):
        x_sq[i] += x_vec_sq[i]
        y_sq[i] += y_vec_sq[i]
        polygon(screen, color_sq[i], [[x_sq[i] - a[i], y_sq[i] - a[i]],
                                      [x_sq[i] - a[i], y_sq[i] + a[i]],
                                      [x_sq[i] + a[i], y_sq[i] + a[i]],
                                      [x_sq[i] + a[i], y_sq[i] - a[i]]])


def circles_moving(x_cir, y_cir,
                   r, a_cir,
                   x_vec_cir, y_vec_cir,
                   color_cir):
    """Changes coordinates of circles according to
    their speed and direction of movement.

    :param x_cir, y_cir: coordinates of the circles
    :param r: radii of the circles
    :param a_cir: amount of circles
    :param x_vec_cir: x-axis velocity
    :param y_vec_cir: y-axis velocity
    :param color_cir: colors of circles
    """
    for i in range(a_cir):
        x_cir[i] += x_vec_cir[i]
        y_cir[i] += y_vec_cir[i]
        circle(screen, color_cir[i], (x_cir[i], y_cir[i]), r[i])


def squares_ref(x_sq, y_sq,
                a, a_sq,
                x_vec_sq, y_vec_sq):
    """Reflection of the squares after elastic collision
    with the edge of the screen.

    :param x_sq, y_sq: coordinates of the squares
    :param a: halves of the squares' sides
    :param a_sq: amount of squares
    :param x_vec_sq: x-axis velocity
    :param y_vec_sq: y-axis velocity
    """
    for i in range(a_sq):
        if x_sq[i] + a[i] >= 1200 or x_sq[i] - a[i] <= 0:
            x_vec_sq[i] = -x_vec_sq[i]
        if y_sq[i] + a[i] >= 900 or y_sq[i] - a[i] <= 0:
            y_vec_sq[i] = -y_vec_sq[i]


def circles_ref(x_cir, y_cir,
                r, a_cir,
                x_vec_cir, y_vec_cir):
    """Reflection of the circles after hitting the edge of the screen
    to the random direction.

    :param x_cir, y_cir: coordinates of the circles
    :param r: radii of the circles
    :param a_cir: amount of circles
    :param x_vec_cir: x-axis velocity
    :param y_vec_cir: y-axis velocity
    """
    for i in range(a_cir):
        if x_cir[i] + r[i] >= 1200:
            x_vec_cir[i] = -1 * randint(0, 5)
            y_vec_cir[i] = (25 - x_vec_cir[i]**2)**0.5 * choice([1, -1])
        if x_cir[i] - r[i] <= 0:
            x_vec_cir[i] = randint(0, 5)
            y_vec_cir[i] = (25 - x_vec_cir[i] ** 2) ** 0.5 * choice([1, -1])
        if y_cir[i] + r[i] >= 900:
            x_vec_cir[i] = randint(0, 5) * choice([-1, 1])
            y_vec_cir[i] = -1 * (25 - x_vec_cir[i] ** 2) ** 0.5
        if y_cir[i] - r[i] <= 0:
            x_vec_cir[i] = randint(0, 5) * choice([-1, 1])
            y_vec_cir[i] = (25 - x_vec_cir[i] ** 2) ** 0.5


def sq_hit_reg(x_sq, y_sq,
               a, event):
    """Checks the hitting into the squares.
    Adds a point for hitting into the squares.

    :param x_sq, y_sq: coordinates of the centers of the circles
    :param a: halves of the squares' sides
    :param event: occurred event of click
    """
    delta_points_sq = 0
    for i in range(a_sq):
        if (x_sq[i] + a[i] >= event.pos[0] >= x_sq[i] - a[i] and
                y_sq[i] + a[i] >= event.pos[1] >= y_sq[i] - a[i]):
            print('Hit!')
            delta_points_sq += 1
    return delta_points_sq


def cir_hit_reg(x_cir, y_cir,
                r, event):
    """Checks the hitting into the circles.
    Adds a point for hitting into the circles.

    :param x_cir, y_cir: coordinates of the centers of the circles
    :param r: radii of the circles
    :param event: occurred event of click
    """
    delta_points_cir = 0
    for i in range(a_cir):
        if (event.pos[0] - x_cir[i])**2 + \
           (event.pos[1] - y_cir[i])**2 <= r[i] ** 2:
            print('Hit!')
            delta_points_cir += 1
    return delta_points_cir


def main_algorithm(finished, frequency):
    """Spawns random circles and squares at the screen with random velocities.
    With every hitting into the figures prints "Hit!", adds one point to the
    score and respawns figures with random velocities.
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
                delta_points_sq = sq_hit_reg(x_sq, y_sq, a, event)
                delta_points_cir = cir_hit_reg(x_cir, y_cir, r, event)
                points = points + delta_points_sq + delta_points_cir
                if delta_points_sq or delta_points_cir:
                    new_squares()
                    new_circles()
                    direction_vec_sq(a_sq)
                    direction_vec_cir(a_cir)
        squares_ref(x_sq, y_sq, a, a_sq, x_vec_sq, y_vec_sq)
        circles_ref(x_cir, y_cir, r, a_cir, x_vec_cir, y_vec_cir)
        squares_moving(x_sq, y_sq, a_sq, x_vec_sq, y_vec_sq, color_sq, a)
        circles_moving(x_cir, y_cir, r, a_cir, x_vec_cir, y_vec_cir, color_cir)
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

new_squares()
new_circles()
direction_vec_sq(a_sq)
direction_vec_cir(a_cir)

main_algorithm(starting_argument, FPS)

pygame.quit()
