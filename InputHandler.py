import pygame
import os
import math

from StarObject import StarObject
from ShipClass import Stationary

class InputHandler:

    def __init__(self):
        self.last_key = 0
        self.counter = 0

    def set_focus(self, focus) :
        self.focus = focus

    def set_game(self, game):
        self.game = game

    def handle_input(self):
        print(f'handle_input {self.counter} {self.last_key + 20} ')
        if self.counter > self.last_key + 20 :
            print("carency passed")
        self.counter += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.focus.rotateRight()
        if keys[pygame.K_RIGHT]:
            self.focus.rotateLeft()
        if keys[pygame.K_UP]:
            self.focus.accelerate()
        if keys[pygame.K_DOWN]:
            self.focus.decelerate()
        if keys[pygame.K_z] and self.counter > self.last_key + 20 :
            self.game.toggle_zoom()
            self.last_key = self.counter
        if keys[pygame.K_p] and self.counter > self.last_key + 20 :
            self.game.toggle_pause()
            self.last_key = self.counter

        running = True

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                star_object = StarObject(self.game, Stationary('target', 48), x, y )
                self.game.add_object(star_object)
                self.focus.set_order(star_object)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.unicode == ' ':
                    self.focus.command(event.unicode)
            elif event.type == pygame.QUIT:
                running = False

        return running


