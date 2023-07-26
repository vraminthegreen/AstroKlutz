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

    def set_game(self, game):
        self.game = game

    def handle_input(self, mouse_tracking):
        self.counter += 1
        keys = pygame.key.get_pressed()
        if self.game.get_focused() != None :
            if keys[pygame.K_LEFT]:
                self.game.get_focused().rotateRight()
            if keys[pygame.K_RIGHT]:
                self.game.get_focused().rotateLeft()
            if keys[pygame.K_UP]:
                self.game.get_focused().accelerate()
            if keys[pygame.K_DOWN]:
                self.game.get_focused().decelerate()
        if keys[pygame.K_z] :
            if self.counter > self.last_key + 20 :
                self.game.toggle_zoom()
                self.last_key = self.counter
        # if keys[pygame.K_p] :
        #     if self.counter > self.last_key + 20 :
        #         self.game.toggle_pause()
        #         self.last_key = self.counter
        if keys[pygame.K_ESCAPE] :
            if self.counter > self.last_key + 20 :
                self.game.pop_focused()
                self.last_key = self.counter
        if keys[pygame.K_BACKSPACE] :
            if self.game.get_focused() != None and self.counter > self.last_key + 20 :
                self.game.get_focused().command_delete()
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
                if event.unicode.isdigit() :
                    self.game.on_key_pressed(event.unicode)
                elif event.unicode.isalnum() or event.unicode == ' ':
                    if event.unicode == 'p' :
                        self.game.toggle_pause()
                    elif self.game.get_focused() != None :
                        self.game.get_focused().command(event.unicode)
            elif event.type == pygame.QUIT:
                running = False

        return running


