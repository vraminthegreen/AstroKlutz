import pygame
import os
import math


class InputHandler:
    def __init__(self):
        pass

    def set_focus(self, focus) :
        self.focus = focus

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.focus.rotate(1)
        if keys[pygame.K_RIGHT]:
            self.focus.rotate(-1)
        if keys[pygame.K_UP]:
            self.focus.accelerate()
        if keys[pygame.K_DOWN]:
            self.focus.decelerate()


