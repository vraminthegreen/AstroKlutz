#!/usr/bin/env python3
import pygame
import os
import math

from Game import Game
from Starship import Starship
from InputHandler import InputHandler


# Initialize Pygame
pygame.init()

input_handler = InputHandler()
game = Game(input_handler)
# Create a starship and an input handler
starship = Starship(400, 300, 'starship.png')
game.add_object(starship)
input_handler.set_focus(starship)

# Create the game and start the game loop
game.game_loop()

