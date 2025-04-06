import pygame


class LineDelimiter:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

        self.shape = pygame.Rect(x, y, 2, height)
        self.color = (44, 44, 44)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)