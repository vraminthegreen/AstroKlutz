#!/usr/bin/env python3
import pygame
import os
import math
import random

from Game import Game
from StarObject import StarObject
from Starship import Starship
from InputHandler import InputHandler
from Missile import Missile
from Dust import Dust
from Team import Team
from Pilot import Pilot, FighterPilot, RocketFrigatePilot
from ShipClass import FighterClass, RocketFrigateClass, Stationary, Background


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

background = StarObject(game, Background('background'), 0, 0)
game.add_object(background)

player_class = FighterClass()
player_class.maxV = 5
player_class.rotation_speed = 3
player_class.max_bullets = 15
player_class.maxAcc = 0.5
player = Starship(game, team_green, player_class, Pilot(game), -200, 200)
game.add_object(player)
input_handler.set_focus(player)
game.set_focused(player)

Dust.make_dust(game)

crippled_fighter = FighterClass()
crippled_fighter.maxV = 1.5  # Maximum speed
crippled_fighter.rotation_speed = 0.3
crippled_fighter.max_bullets = 3

enemies = [
    # Starship(game, team_yellow, crippled_fighter, FighterPilot(game), -350, -350 ),
    # Starship(game, team_red, RocketFrigateClass(), RocketFrigatePilot(game), 350, -350 ),
    # Starship(game, team_blue, crippled_fighter, FighterPilot(game), 350, 350 )
]

for enemy in enemies :
    enemy.set_enemy(player)
    game.add_object(enemy)

# Missile.fire(game)

# Create the game and start the game loop
game.game_loop()

