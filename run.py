#!/usr/bin/env python3
import pygame
import os
import math

from Game import Game
from Starship import Starship
from InputHandler import InputHandler
from Missile import Missile
from Team import Team


# Initialize Pygame
pygame.init()

input_handler = InputHandler()
game = Game(input_handler)
input_handler.set_game( game )
# Create a starship and an input handler
team_red = Team( "red", (255,0,0), 1 )
team_blue = Team( "blue", (0,0,255), 2 )
team_green = Team( "green", (0,255,0), 3 )
team_yellow = Team( "yellow", (255,255,0), 4 )

player = Starship(game, team_green, 750, 50)
game.add_object(player)
input_handler.set_focus(player)
enemy = Starship(game, team_yellow, 50, 550 )
enemy.set_enemy(player)
game.add_object(enemy)
Missile.fire(game)

# Create the game and start the game loop
game.game_loop()

