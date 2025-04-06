import pygame


class NumbersStrip:
    def __init__(self, x, y, width, height, total):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.total = total

        self.shape = pygame.Rect(x, y, width, height)
        self.text_color = (44, 44, 44)
        self.color = (233, 118, 43)

        self.font = pygame.font.Font("Poppins-Medium.ttf", 20)
        self.text_surfaces = []
        for i in range(1, total):
            if i < 10:
                self.text_surfaces.append(self.font.render("0" + str(i), True, self.text_color))
            else:
                self.text_surfaces.append(self.font.render(str(i), True, self.text_color))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        padding = 70
        for i, text in enumerate(self.text_surfaces):
            screen.blit(text, (self.x + 15 + i * padding, self.y - 1))
