import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
color = (200, 200, 200)
screen.fill(color)
pygame.display.flip()

circle(screen, center=(200, 200), radius=100, color='yellow')
circle(screen, center=(200, 200), radius=100, color='black', width=1)
circle(screen, center=(150, 180), radius=20, color='red')
circle(screen, center=(150, 180), radius=20, color='black', width=1)
circle(screen, center=(150, 180), radius=9, color='black')
circle(screen, center=(250, 180), radius=15, color='red')
circle(screen, center=(250, 180), radius=7, color='black')
circle(screen, center=(250, 180), radius=15, color='black', width=1)
x1 = 100
y1 = 100
x2 = 200
y2 = 200
polygon(screen, color='black', points=[(180, 180), (187, 173), (107, 103), (100, 110)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()