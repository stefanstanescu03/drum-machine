import pygame


class Button:
    def __init__(self, x, y, width, height, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (212, 201, 190)
        self.id = id

        self.inside_color = (148, 80, 52)
        self.shape = pygame.Rect(x, y, width, height)

        self.status = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        pygame.draw.rect(screen, self.inside_color,
                         (self.x + 10, self.y + 5, self.width / 5 * 3, self.height / 5))

    def check_clicked(self, pos):
        return self.shape.collidepoint(pos)

    def change_status(self):
        self.status = not self.status
        if self.status:
            self.inside_color = (221, 168, 83)
        else:
            self.inside_color = (148, 80, 52)

