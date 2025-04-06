import pygame

class DigitalDisplay:
    def __init__(self, x, y, width, height, text):
        self.rectangle_color = (44, 44, 44)
        self.text_color = (247, 55, 79)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.shape = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font("digital-7.ttf", 60)
        self.text_surface = self.font.render(text, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.shape)
        screen.blit(self.text_surface, (self.x, self.y))

    def set_text(self, text):
        self.text_surface = self.font.render(text, True, self.text_color)