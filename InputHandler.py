import pygame
import os
import math

from StarObject import StarObject
from ShipClass import Stationary
from Menu import Menu


class InputHandler:

    def __init__(self):
        self.last_key = 0
        self.counter = 0
        self.menu = None

    def set_focus(self, focus) :
        self.focus = focus

    def set_game(self, game):
        self.game = game

    def handle_input(self, mouse_tracking):
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
        if keys[pygame.K_ESCAPE] and self.counter > self.last_key + 20 :
            self.game.pop_focused()
            self.last_key = self.counter

        running = True

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION and mouse_tracking:
                x, y = event.pos
                self.game.mouse_track(x, y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if  event.button == 1 :
                    self.game.click( *pygame.mouse.get_pos() )
                elif event.button == 3 :
                    x, y = pygame.mouse.get_pos()
                    game_coords = self.game.get_xy_display( x, y )
                    # star_object = StarObject(self.game, Stationary('target', 48), game_coords[0], game_coords[1] )
                    # self.game.add_object(star_object)
                    # self.focus.set_order(star_object)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.unicode == ' ':
                    self.focus.command(event.unicode)
            elif event.type == pygame.QUIT:
                running = False

        return running


