from constants import *
from random import shuffle
from tile import Tile
import pygame
import random

class Board:
    BORDER          = 15
    BORDER_COLOR    = (20, 40, 60)
    COLOR           = (75, 0, 130)
    LENGTH          = int(0.9 * HEIGHT)
    SEP             = 3
    BOTTOM_OFFSET   = 25
    X               = (WIDTH - LENGTH) // 2 - 110
    Y               = HEIGHT - LENGTH - BOTTOM_OFFSET

    @staticmethod
    def solvable(n, p):
        inv = 0
        for i in range(n * n):
            for j in range(i + 1, n * n):
                if p[i] and p[j] and p[i] > p[j]:
                    inv += 1
    
        if n % 2 == 1:
            return inv % 2 == 0
        else:
            row = p.index(0) // n
            return row % 2 != inv % 2

    @staticmethod
    def get_solvable(n):
        board = [i for i in range(n * n)]
        for i in range(10):
            random.shuffle(board)
        while not Board.solvable(n, board):
            random.shuffle(board)
        return board

    def __init__(self, N, font):
        self.N = N

        tile_length = (Board.LENGTH - 2 * Board.BORDER - (N - 1) * Board.SEP) // N
        Tile.set(font, tile_length)

        shift = (Board.LENGTH - 2 * Board.BORDER - N * tile_length - (N - 1) * Board.SEP) // 2

        temp = []
        for x in Board.get_solvable(N):
            temp.append(x if x != 0 else None)

        self.tiles = []
        for index, value in enumerate(temp):
            if not value:
                self.zero_index = index
                self.tiles.append(None)
            else:
                r = index // N
                c = index % N
                x = Board.X + Board.BORDER + c * (tile_length + Board.SEP) + shift
                y = Board.Y + Board.BORDER + r * (tile_length + Board.SEP) + shift
                self.tiles.append(Tile(x, y, value))    

    def show(self, screen):
        pygame.draw.rect(
            screen,
            Board.BORDER_COLOR,
            pygame.Rect((Board.X, Board.Y), (Board.LENGTH, Board.LENGTH))
        )

        for tile in self.tiles:
            if tile:
                tile.show(screen)

    def apply_move(self, direction: str):
        """
        Accepts ('u', 'r', 'd', 'l') as a parameter.
        Where to move the empty tile.
        """

        direction = direction.lower()
        row = self.zero_index // self.N
        col = self.zero_index % self.N
        drow, dcol = (0, 0)
        
        if direction == "u":
            drow = -1
        elif direction == "d":
            drow = +1
        elif direction == "l":
            dcol = -1
        elif direction == "r":
            dcol = +1
        else:
            raise Exception("Invalid Direction")

        swap_row = row + drow
        swap_col = col + dcol

        if swap_row < 0 or swap_row >= self.N or swap_col < 0 or swap_col >= self.N:
            return False

        swap_index = swap_row * self.N + swap_col

        self.tiles[self.zero_index] = self.tiles[swap_index]
        self.tiles[swap_index] = None
        self.tiles[self.zero_index].x -= dcol * (Tile.length + Board.SEP)
        self.tiles[self.zero_index].y -= drow * (Tile.length + Board.SEP)
        self.zero_index = swap_index

        return True
    
    def tiles_as_list(self):
        return [x.value if x else 0 for x in self.tiles]

    def tiles_as_str(self):
        return " ".join([str(x) for x in self.tiles_as_list()])
