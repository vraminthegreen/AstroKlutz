#!/usr/bin/env python3
import pygame
import os
import math

from Game import Game
from Starship import Starship
from InputHandler import InputHandler
from Missile import Missile


# Initialize Pygame
pygame.init()

input_handler = InputHandler()
game = Game(input_handler)
input_handler.set_game( game )
# Create a starship and an input handler
starship = Starship(game, 750, 50)
game.add_object(starship)
input_handler.set_focus(starship)
missile = Missile(game, 50, 550)
missile.set_order(starship)
game.add_object(missile)

# Create the game and start the game loop
game.game_loop()

