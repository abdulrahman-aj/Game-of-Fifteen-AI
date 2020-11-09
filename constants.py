import pygame
pygame.init()

FPS                     = 100
SIZE = WIDTH, HEIGHT    = 700, 500
BLACK                   = (  0,   0,   0)
WHITE                   = (255, 255, 255)
GAME_OVER_COLOR         = (255, 247, 122)
THINKING_COLOR          = (  0, 255, 255)

fonts = [
    pygame.font.SysFont('freesansbold', 30),
    pygame.font.SysFont('freesansbold', 50),
    pygame.font.SysFont('freesansbold', 90)
]