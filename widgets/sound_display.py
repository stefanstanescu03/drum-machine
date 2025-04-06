import pygame


class SoundDisplay:
    def __init__(self, sound, label, x, y, width, height):
        self.sound = sound
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rectangle_color = (44, 44, 44)
        self.text_color = (233, 118, 43)
        self.inside_color = (148, 80, 52)

        self.shape = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font("Poppins-Medium.ttf", 20)
        self.text_surface = self.font.render(label, True, self.text_color)

        self.status = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.shape)
        screen.blit(self.text_surface, (self.x + 5, self.y))
        pygame.draw.rect(screen, self.inside_color,
                         (self.x + self.width - self.height / 2 - 5, self.y + self.height / 4,
                          self.height / 2, self.height / 2))

    def play_sample(self):
        self.sound.get_sound().play()

    def check_clicked(self, pos):
        return self.shape.collidepoint(pos)

    def change_status(self):
        self.status = not self.status
        if self.status:
            self.inside_color = (221, 168, 83)
        else:
            self.inside_color = (148, 80, 52)
