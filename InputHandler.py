import pygame
import os
import math

from StarObject import StarObject

class InputHandler:

    def __init__(self):
        pass

    def set_focus(self, focus) :
        self.focus = focus

    def set_game(self, game):
        self.game = game

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

        running = True

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                star_object = StarObject(self.game, x, y, 'target.png')
                self.game.add_object(star_object)
                self.focus.set_order(star_object)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.unicode == ' ':
                    self.focus.command(event.unicode)
            elif event.type == pygame.QUIT:
                running = False

        return running


