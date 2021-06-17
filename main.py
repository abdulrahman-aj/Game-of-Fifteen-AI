#!/usr/bin/env python3
from board import Board
from constants import *
from ext.fifteen_solver import solve
import pygame
import sys

pygame.init()


def pressed(prev_keys, current_keys, key_pressed):
    """To avoid a single click affecting multiple frames."""
    if not prev_keys:
        return current_keys[key_pressed]

    return not prev_keys[key_pressed] and current_keys[key_pressed]


def main():
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    board = None
    prev_keys = None
    game_over = None
    ai_moves = None
    player_moves = None
    shortest_path = None
    goal_list = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        screen.fill(BLACK)

        if not board:
            board = menu(screen)
            if board:
                prev_keys = None
                game_over = False
                ai_moves = 0
                player_moves = 0
                shortest_path = None
                goal_list = [x + 1 for x in range(board.N * board.N - 1)] + [0]
        else:
            board.show(screen)

            current_keys = pygame.key.get_pressed()

            # Render AI moves counter
            ai_moves_text = fonts[1].render(f"AI moves: {ai_moves}", True, WHITE)
            ai_moves_rect = ai_moves_text.get_rect()
            ai_moves_rect.center = (WIDTH - 120, HEIGHT // 2 - 100)
            screen.blit(ai_moves_text, ai_moves_rect)
            
            # Render player moves counter
            player_moves_text = fonts[1].render(f"Player: {player_moves}", True, WHITE)
            player_moves_rect = player_moves_text.get_rect()
            player_moves_rect.center = (WIDTH - 120, HEIGHT // 2 - 50)
            screen.blit(player_moves_text, player_moves_rect)
            
            # Render game Over Rectangle
            if game_over:
                win_text = fonts[1].render(f"YOU WIN!!!", True, GAME_OVER_COLOR)
                win_rect = win_text.get_rect()
                win_rect.center = (WIDTH - 120, 50)
                screen.blit(win_text, win_rect)

            # Check if goal
            if board.tiles_as_list() == goal_list:
                game_over = True

            if pressed(prev_keys, current_keys, pygame.K_ESCAPE):
                # Main menu on Esc
                board = None

            elif pressed(prev_keys, current_keys, pygame.K_RETURN):
                # AI Move

                if shortest_path is None:
                    # Render AI thinking rect
                    ai_thinking_text = fonts[1].render(f"thinking...", True, THINKING_COLOR)
                    ai_thinking_rect = ai_thinking_text.get_rect()
                    ai_thinking_rect.center = (WIDTH - 125, HEIGHT - 50)
                    screen.blit(ai_thinking_text, ai_thinking_rect)
                    pygame.display.flip()
                    shortest_path = solve(board.tiles_as_str())
                
                if len(shortest_path) != 0:
                    board.apply_move(shortest_path[0])
                    shortest_path = shortest_path[1:]
                    if not game_over:
                        ai_moves += 1
            else:
                # Player move
                direction = None
                if pressed(prev_keys, current_keys, pygame.K_LEFT):
                    direction = "r"
                elif pressed(prev_keys, current_keys, pygame.K_RIGHT):
                    direction = "l"
                elif pressed(prev_keys, current_keys, pygame.K_UP):
                    direction = "d"
                elif pressed(prev_keys, current_keys, pygame.K_DOWN):
                    direction = "u"

                if direction:
                    increment = board.apply_move(direction)
                    
                    if not game_over and increment:
                        player_moves += 1
                    
                    if shortest_path == "":
                        shortest_path = None
                    elif shortest_path:
                        if shortest_path[0] == direction:
                            shortest_path = shortest_path[1:]
                        else:
                            shortest_path = None

            prev_keys = current_keys

        pygame.display.flip()
        clock.tick(FPS)


def menu(screen):
    """Renders main menu."""

    # Render title
    title_text = fonts[2].render("N X N Puzzle", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.center = (WIDTH // 2, 100)
    screen.blit(title_text, title_rect)

    # Render instructions
    instructions = [
        "Press Esc for main menu.",
        "Use arrows to make moves.",
        "Press Enter/Return for AI move."
    ]

    for index, instruction in enumerate(instructions):
        text = fonts[0].render(instruction, True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 230 + index * 30)
        screen.blit(text, text_rect)

    # Render 3X3 button
    center_3 = (WIDTH // 3, HEIGHT - 120)
    text_3 = fonts[1].render("3 X 3", True, BLACK)
    text_rect_3 = text_3.get_rect()
    text_rect_3.center = center_3
    bg_rect_3 = pygame.Rect((0, 0), (150, 60))
    bg_rect_3.center = center_3
    pygame.draw.rect(screen, WHITE, bg_rect_3)
    screen.blit(text_3, text_rect_3)

    # Render 4X4 button
    center_4 = (WIDTH - WIDTH // 3, HEIGHT - 120)
    text_4 = fonts[1].render("4 X 4", True, BLACK)
    text_rect_4 = text_4.get_rect()
    text_rect_4.center = center_4
    bg_rect_4 = pygame.Rect((0, 0), (150, 60))
    bg_rect_4.center = center_4
    pygame.draw.rect(screen, WHITE, bg_rect_4)
    screen.blit(text_4, text_rect_4)

    # On mouse click:
    if pygame.mouse.get_pressed()[0]:
        coordinates = pygame.mouse.get_pos()
        if bg_rect_3.collidepoint(coordinates):
            return Board(3, fonts[2])
        elif bg_rect_4.collidepoint(coordinates):
            return Board(4, fonts[1])

    return None


if __name__ == "__main__":
    main()
