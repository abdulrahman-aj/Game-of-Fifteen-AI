from constants import *


class Tile:
    BORDER = 10
    COLOR = (255, 255, 255)
    font = None
    length = None
    TEXT_COLOR = (64, 64, 64)

    @classmethod
    def set(cls, font, length):
        cls.font = font
        cls.length = length

    def __init__(self, x, y, value):
        assert Tile.font != None and Tile.length != None
        self.x = x
        self.y = y
        self.value = value

    def show(self, screen):
        text = Tile.font.render(f"{self.value}", True, Tile.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.x + Tile.length // 2, self.y + Tile.length // 2)

        pygame.draw.rect(
            screen,
            BLACK,
            pygame.Rect((self.x, self.y), (Tile.length, Tile.length))
        )
        
        pygame.draw.rect(
            screen,
            Tile.COLOR,
            pygame.Rect(
                (self.x + Tile.BORDER, self.y + Tile.BORDER),
                (Tile.length - 2 * Tile.BORDER, Tile.length - 2 * Tile.BORDER)
            )
        )

        screen.blit(text, text_rect)
