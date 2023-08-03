#!/usr/bin/env python3
import pygame
import os
import math
import random

from Game import Game
from StarObject import StarObject
from InputHandler import InputHandler
from Missile import Missile
from Dust import Dust
from DistantObject import DistantObject
from Scenarios import BasicScenario
from ShipClass import Stationary, Background

# Initialize Pygame
pygame.init()

input_handler = InputHandler()
game = Game(input_handler)
input_handler.set_game( game )

scenario = BasicScenario(game)

background = DistantObject(game, Background(), 0, 0)
game.add_object(background)

Dust.make_dust(game, 1)

scenario.start()
# Missile.fire(game)

# Create the game and start the game loop
game.game_loop()

