import pygame
import math


class Dial:
    def __init__(self, x, y, radius, a, b, label, size):
        self.x = x
        self.y = y
        self.radius = radius

        self.color = (61, 61, 61)
        self.color_rect = (240, 160, 75)
        self.text_color = (44, 44, 44)
        self.label = label
        self.size = size

        self.angle = 270
        self.prev_angle = 270
        self.dragging = False

        self.x_hand = self.x - 3
        self.y_hand = self.y - self.radius + 5

        self.a = a
        self.b = b

        self.hand = pygame.Rect(self.x_hand, self.y_hand, 6, self.radius / 8 * 3)

        self.font = pygame.font.Font("Poppins-Medium.ttf", size)
        self.text_surface = self.font.render(label, True, self.text_color)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(screen, self.color_rect, (self.x_hand, self.y_hand, 3, 3))
        screen.blit(self.text_surface, (self.x - self.radius + 3, self.y - self.radius - self.size - 5))

    def check_clicked(self, pos):
        mouse_x = pos[0]
        mouse_y = pos[1]
        return (mouse_x - self.x)**2 + (mouse_y - self.y)**2 < self.radius**2

    def calculate_angle(self, mouse_x, mouse_y):
        hand_angle = math.degrees(math.atan2(self.y - mouse_y, self.x - mouse_x))
        return hand_angle

    def drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        curr_angle = self.calculate_angle(mouse_x, mouse_y)
        self.angle += self.calculate_angle(mouse_x, mouse_y) - self.prev_angle
        self.prev_angle = curr_angle

        self.x_hand = self.x
        self.y_hand = self.y

        self.x_hand = self.x + math.cos(math.radians(self.angle)) * (self.radius - 5)
        self.y_hand = self.y + math.sin(math.radians(self.angle)) * (self.radius - 5)

        self.hand = pygame.Rect(self.x_hand, self.y_hand, 6, self.radius / 8 * 3)

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def get_value(self):
        return self.angle * self.a + self.b
