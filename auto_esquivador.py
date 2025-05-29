import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

pygame.quit()



































