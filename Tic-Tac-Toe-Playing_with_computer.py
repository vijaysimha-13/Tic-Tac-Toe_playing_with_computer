import pygame
import time
import random


from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_SPACE,
    K_ESCAPE,
    QUIT,
)


def result(d, n):
    # d represents a dictionary that contains 9 keys (Tic-Tac-Toe board positions)
    # n stands for total number of moves made (out of 9) till that time
    game_state = 'Playing'
    for k in range(3):
        # conditions for row or column wise win for Player
        if ((d[(3 * k) + 1], d[(3 * k) + 2], d[(3 * k) + 3]).count('p') == 3) or ((d[k + 1], d[k + 4],
                                                                                   d[k + 7]).count('p') == 3):
            game_state = 'Player Won'
            return "Yay!, You won"
            break

        # conditions for row or column wise win for Computer
        if ((d[(3 * k) + 1], d[(3 * k) + 2], d[(3 * k) + 3]).count('c') == 3) or ((d[k + 1], d[k + 4],
                                                                                   d[k + 7]).count('c') == 3):
            game_state = 'Computer Won'
            return "You Lost :("
            break

    # conditions for case where the game ends in a diagonal-win manner
    if (d[1] == d[5] == d[9]) or (d[3] == d[5] == d[7]):

        if d[5] == 'p':                            # Player win case
            game_state = 'Player Won'
            return 'Yay!, You won'
        elif d[5] == 'c':                          # Computer win case
            game_state = 'Computer Won'
            return 'You Lost :('

    # condition for draw case
    if game_state == 'Playing' and n == 9:
        return "Oops!, It's a Draw ^_^"


def computer_move(d, m):
    # m represents number of moves
    empty_positions_list = []
    game_ended = False

    for k in range(1, 10):
        if d[k] == '':
            empty_positions_list += [k]
            d[k] = 'c'
            computer_win_chance = result(d, m+1)
            if computer_win_chance:
                game_ended = True
                break
            if not computer_win_chance:
                d[k] = ''
        if game_ended:
            break

    if not game_ended:
        # empty_positions_list consists of elements where each element is a vacant position in the Tic-Tac-Toe board
        for k in empty_positions_list:
            d[k] = 'p'
            player_win_chance = result(d, m+1)
            if player_win_chance:
                d[k] = 'c'
                game_ended = True
                break
            if not player_win_chance:
                d[k] = ''

    if (not game_ended) and (m > 0):
        q = random.choice(empty_positions_list)    # computer making a random move
        d[q] = 'c'


pygame.init()


BLACK = (0, 0, 0)
GRAY = (119, 136, 153)
LIGHTSEAGREEN = (32, 178, 170)

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
cell_width = SCREEN_WIDTH // 3
cell_height = SCREEN_HEIGHT // 3

pygame.display.set_caption('Tic-Tac-Toe')
game_icon = pygame.image.load('tic-tac-toe.png')
pygame.display.set_icon(game_icon)

CROSS_MARK = pygame.image.load('cross.png')
CROSS_MARK = pygame.transform.scale(CROSS_MARK, (cell_width - 20, cell_height - 20))
O_MARK = pygame.image.load('o.png')
O_MARK = pygame.transform.scale(O_MARK, (cell_width - 20, cell_height - 20))

game_status = 'intro'
font = pygame.font.SysFont('LoveGlitch.ttf', 30)

# This positions_list consists of elements that represent Tic-Tac-Toe board positions on screen in terms of
# cell width and cell height
positions_list = [(0, 0), (cell_width, 0), (2 * cell_width, 0),
                  (0, cell_height), (cell_width, cell_height), (2 * cell_width, cell_height),
                  (0, 2 * cell_height), (cell_width, 2 * cell_height), (2 * cell_width, 2 * cell_height)]

positions_dict = {}
moves = 0
game_result = False    # This result keeps track on the game result from beginning
res = False            # This res stands for final game result
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                game_status = 'playing'
                # Initializing positions_dict and moves, every time player starts the game
                positions_dict = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}
                moves = 0

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(9):
                    # checking on which cell did the player click the mouse left button
                    if (positions_list[i][0] < mouse_pos[0] < (positions_list[i][0] +
                                                               cell_width)) and (positions_list[i][1] < mouse_pos[1]
                                                                                 < (positions_list[i][1] +
                                                                                    cell_height)):
                        if positions_dict[i + 1] == '':
                            positions_dict[i + 1] = 'p'
                            moves += 1
                        break

                game_result = result(positions_dict, moves)
                if not game_result:
                    computer_move(positions_dict, moves)
                    moves += 1

        elif event.type == QUIT:
            running = False

    screen.fill(BLACK)

    if game_status == 'intro':
        start_text = font.render('PUSH SPACE TO START THE GAME', True, GRAY)
        start_text_rect = start_text.get_rect()
        start_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(start_text, start_text_rect)

    elif game_status == 'end':
        end_text = font.render(res, True, LIGHTSEAGREEN)
        end_text_rect = end_text.get_rect()
        end_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        play_again_text = font.render('PRESS SPACE TO PLAY AGAIN', True, GRAY)
        play_again_text_rect = play_again_text.get_rect()
        play_again_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

        screen.blit(end_text, end_text_rect)
        screen.blit(play_again_text, play_again_text_rect)

    elif game_status == 'playing':
        for i in range(2):
            pygame.draw.line(screen, GRAY, ((i + 1) * cell_width, 0), ((i + 1) * cell_width, SCREEN_HEIGHT))
        for j in range(2):
            pygame.draw.line(screen, GRAY, (0, (j + 1) * cell_height), (SCREEN_WIDTH, (j + 1) * cell_height))

        for key in positions_dict:
            if positions_dict[key] != '':
                if positions_dict[key] == 'p':
                    screen.blit(CROSS_MARK, (positions_list[key - 1][0] + 10, positions_list[key - 1][1] + 10))
                elif positions_dict[key] == 'c':
                    screen.blit(O_MARK, (positions_list[key - 1][0] + 10, positions_list[key - 1][1] + 10))

        game_result = result(positions_dict, moves)
        if game_result:
            game_status = 'end'

    pygame.display.flip()
    
    if game_result:
        time.sleep(1)
        res = game_result
        game_result = False
