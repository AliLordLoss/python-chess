import pygame
import os


assets = {
    'black_board': pygame.image.load(os.path.join('assets', 'black_board.jpg')),
    'blue_board': pygame.image.load(os.path.join('assets', 'blue_board.jpg')),
    'gray_board': pygame.image.load(os.path.join('assets', 'gray_board.jpg')),
    'PawnB': pygame.image.load(os.path.join('assets', 'PawnB.png')),
    'QueenB': pygame.image.load(os.path.join('assets', 'QueenB.png')),
    'RookB': pygame.image.load(os.path.join('assets', 'RookB.png')),
    'KnightB': pygame.image.load(os.path.join('assets', 'KnightB.png')),
    'BishopB': pygame.image.load(os.path.join('assets', 'BishopB.png')),
    'KingB': pygame.image.load(os.path.join('assets', 'KingB.png')),
    'PawnW': pygame.image.load(os.path.join('assets', 'PawnW.png')),
    'QueenW': pygame.image.load(os.path.join('assets', 'QueenW.png')),
    'RookW': pygame.image.load(os.path.join('assets', 'RookW.png')),
    'KnightW': pygame.image.load(os.path.join('assets', 'KnightW.png')),
    'BishopW': pygame.image.load(os.path.join('assets', 'BishopW.png')),
    'KingW': pygame.image.load(os.path.join('assets', 'KingW.png')),
    'restart': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'restart.png')), (160, 160)),
}


def load(surface, game, font):
    surface.fill((192, 192, 192))
    surface.blit(assets['black_board'], (0, 0))
    surface.blit(assets['restart'], (680, 60))
    pygame.draw.rect(surface, (150, 150, 150), (680, 340, 80, 380), 3)
    pygame.draw.rect(surface, (150, 150, 150), (760, 340, 80, 380), 3)
    time = font.render(game.get_elapsed_time(), False, (0, 0, 0))
    surface.blit(time, (760 - (font.size("00:00")[0] // 2), 10))
    black = font.render('Black', False, (0, 0, 0))
    white = font.render('White', False, (255, 255, 255))
    surface.blit(black, (720 - (font.size('Black')[0] // 2), 280))
    surface.blit(white, (800 - (font.size('White')[0] // 2), 280))
    x = 680
    y = 300
    for dead in game.black_dead:
        surface.blit(assets[dead], (x, y))
        y += 22
    x = 760
    y = 300
    for dead in game.white_dead:
        surface.blit(assets[dead], (x, y))
        y += 22
    if game.is_checked():
        s = pygame.Surface((80, 80))
        s.set_alpha(200)
        s.fill((255, 150, 150))
        if game.turn:
            surface.blit(s, (20 + game.white_king[1] * 80, 20 + game.white_king[0] * 80))
        else:
            surface.blit(s, (20 + game.white_king[1] * 80, 20 + game.black_king[0] * 80))
    for i in range(8):
        for j in range(8):
            if game.board[i][j] != '':
                surface.blit(assets[game.board[i][j]], (20 + (j * 80), 20 + (i * 80)))
            if (i, j) in game.choices:
                pygame.draw.circle(surface, (255, 255, 0), (60 + (j * 80), 60 + (i * 80)), 20, 20)
    if game.pawn_at_end is not None:
        m, n = game.pawn_at_end
        s = pygame.Surface((680, 680))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))
        pieces = [
            'Queen' + game.board[m][n][-1],
            'Rook' + game.board[m][n][-1],
            'Bishop' + game.board[m][n][-1],
            'Knight' + game.board[m][n][-1],
        ]
        for i in range(4):
            surface.blit(pygame.transform.scale(assets[pieces[i]], (160, 160)), (20 + (i * 160), 260))
    if game.is_checkmated():
        s = pygame.Surface((840, 680))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))
        if game.turn:
            msg = "Black"
        else:
            msg = "White"
        msg += " has won!"
        restart = pygame.transform.scale(assets['restart'], (80, 80))
        surface.blit(font.render(msg, False, (0, 200, 200)), (340 - (font.size(msg)[0] // 2), 250))
        surface.blit(restart, (300, 300))
