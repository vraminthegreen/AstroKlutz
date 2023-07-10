import pygame
import os
import math

class Starship:
    def __init__(self, x, y, icon_name):
        self.x = x
        self.y = y
        self.dir = 0  # Direction in degrees
        self.v = pygame.Vector2(0, 0)  # Velocity vector
        self.maxV = 1  # Maximum speed

        # Load and resize the icon
        self.icon = pygame.image.load(os.path.join('.', icon_name))
        self.icon = pygame.transform.scale(self.icon, (32, 32)).convert_alpha()

    def accelerate(self):
        acceleration_vector = pygame.Vector2(0.01, 0).rotate(-self.dir)
        self.v += acceleration_vector
        if self.v.length() > self.maxV:
            self.v.scale_to_length(self.maxV)

    def decelerate(self):
        if self.v.length() > 0:
            deceleration_vector = pygame.Vector2(-0.01, 0).rotate(-self.v.angle_to(pygame.Vector2(1, 0)))
            self.v += deceleration_vector

            # Gradually rotate the starship towards the direction of movement
            desired_dir = self.v.angle_to(pygame.Vector2(1, 0))
            rotation_dir = (desired_dir - self.dir) % 360
            if rotation_dir > 180:
                rotation_dir -= 360  # Adjust for the shortest rotation direction
            rotation_dir = max(min(rotation_dir, 1), -1)  # Limit rotation to 1 degree per tick
            self.dir += rotation_dir

            if self.v.length() < 0.1:
                self.v = pygame.Vector2(0, 0)

    def rotate(self, rotation):
        self.dir += rotation
        self.dir %= 360

    def repaint(self, win):
        rotated_icon = pygame.transform.rotate(self.icon, self.dir)
        new_rect = rotated_icon.get_rect(center=(self.x, self.y))
        win.blit(rotated_icon, new_rect.topleft)

    def ticktack(self):
        self.x += self.v.x
        self.y += self.v.y


