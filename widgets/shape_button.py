import pygame


class ShapeButton:
    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (148, 80, 52)

        self.text_color = (44, 44, 44)
        self.shape = pygame.Rect(x, y, width, height)
        self.label = label

        self.font = pygame.font.Font("Poppins-Medium.ttf", 10)
        self.text_surface = self.font.render(label, True, self.text_color)

        self.status = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        screen.blit(self.text_surface, (self.x - 6, self.y - 24))

    def check_clicked(self, pos):
        return self.shape.collidepoint(pos)

    def change_status(self):
        self.status = not self.status
        if self.status:
            self.color = (221, 168, 83)
        else:
            self.color = (148, 80, 52)
