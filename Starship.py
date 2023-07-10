import pygame
import os
import math

class Starship:
    def __init__(self, x, y, icon_name):
        self.x = x
        self.y = y
        self.dir = 0  # Direction in degrees
        self.v = 0  # Current speed
        self.maxV = 1  # Maximum speed

        # Load and resize the icon
        self.icon = pygame.image.load(os.path.join('.', icon_name))
        self.icon = pygame.transform.scale(self.icon, (32, 32)).convert_alpha()

    def accelerate(self):
        if self.v < self.maxV:
            self.v += 0.01

    def decelerate(self):
        if self.v > 0:
            self.v -= 0.01

    def rotate(self, rotation):
        self.dir += rotation
        self.dir %= 360

    def repaint(self, win):
        rotated_icon = pygame.transform.rotate(self.icon, self.dir)
        new_rect = rotated_icon.get_rect(center=(self.x, 600-self.y))
        win.blit(rotated_icon, new_rect.topleft)

    def ticktack(self):
        self.x += self.v * math.cos(math.radians(self.dir))
        self.y += self.v * math.sin(math.radians(self.dir))


