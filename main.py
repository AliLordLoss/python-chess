import pygame
import os
from board import Board
from loader import load


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)
screen = pygame.display.set_mode((840, 680))
icon = pygame.image.load(os.path.join('assets', 'KingW.png'))
pygame.display.set_icon(icon)
pygame.display.set_caption('Chess')
game_board = Board()

while True:
    load(screen, game_board, my_font)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        game_board.game_manager(event.pos)

    pygame.display.update()
