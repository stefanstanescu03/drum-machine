import pygame


class ActionButton:
    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (234, 209, 150)

        self.inside_color = (148, 80, 52)
        self.text_color = (44, 44, 44)
        self.shape = pygame.Rect(x, y, width, height)
        self.label = label

        self.font = pygame.font.Font("Poppins-Medium.ttf", 15)
        self.text_surface = self.font.render(label, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        pygame.draw.rect(screen, self.inside_color,
                         (self.x + 10, self.y + 5, self.width / 5 * 3, self.height / 5))
        screen.blit(self.text_surface, (self.x + 5, self.y - 20))

    def check_clicked(self, pos):
        return self.shape.collidepoint(pos)
