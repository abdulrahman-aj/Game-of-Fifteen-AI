from ext.fifteen_solver import get_solvable
from constants import *
from random import shuffle
from tile import Tile
import pygame

class Board:
    BORDER = 15
    BORDER_COLOR = (20, 40, 60)
    COLOR = (75, 0, 130)
    LENGTH = int(0.9 * HEIGHT)
    SEP = 3
    BOTTOM_OFFSET           = 25
    X = (WIDTH - LENGTH) // 2 - 110
    Y = HEIGHT - LENGTH - BOTTOM_OFFSET
    
    def __init__(self, N, font):
        self.N = N
        
        tile_length = (Board.LENGTH - 2 * Board.BORDER - (N - 1) * Board.SEP) // N
        Tile.set(font, tile_length)
        
        shift = (Board.LENGTH - 2 * Board.BORDER - N * tile_length - (N - 1) * Board.SEP) // 2
        
        temp = []
        for x in get_solvable(N).split():
            temp.append(int(x) if x != "0" else None)
        
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
        
    def apply_move(self, dir: str):
        """
        Accepts ('u', 'r', 'd', 'l') as a parameter.
        Where to move the empty tile.
        """
        
        dir = dir.lower()
        r = self.zero_index // self.N
        c = self.zero_index % self.N
        dr, dc = (0, 0)
        
        if dir == "u":
            dr -= 1
        elif dir == "d":
            dr += 1
        elif dir == "l":
            dc -= 1
        elif dir == "r":
            dc += 1
        else:
            raise Exception("Invalid Direction")

        swap_r = r + dr
        swap_c = c + dc

        if swap_r < 0 or swap_r >= self.N or swap_c < 0 or swap_c >= self.N:
            return False

        swap_index = swap_r * self.N + swap_c
        self.tiles[self.zero_index] = self.tiles[swap_index]
        self.tiles[swap_index] = None
        self.tiles[self.zero_index].x -= dc * (Tile.length + Board.SEP)
        self.tiles[self.zero_index].y -= dr * (Tile.length + Board.SEP)
        self.zero_index = swap_index
        return True
    
    def tiles_as_list(self):
        return [x.value if x else 0 for x in self.tiles]

    def tiles_as_str(self):
        return " ".join([str(x) for x in self.tiles_as_list()])
        # return " ".join([str(x.value) if x else "0" for x in self.tiles])