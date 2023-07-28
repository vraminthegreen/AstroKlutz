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
from DistantObject import DistantObject
from Group import Group
from Scenarios import BasicScenario


# Initialize Pygame
pygame.init()

input_handler = InputHandler()
game = Game(input_handler)
input_handler.set_game( game )
# Create a starship and an input handler

scenario = BasicScenario(game)


team_red = Team( "Red", (255,0,0), 1, 1, scenario )
team_blue = Team( "Blue", (0,0,255), 2, 1, scenario )
team_green = Team( "Green", (0,255,0), 3, 0, scenario )
team_yellow = Team( "Yellow", (255,255,0), 4, 1, scenario )

background = DistantObject(game, Background('background'), 0, 0)
game.add_object(background)

player_class = FighterClass()
player_class.maxV = 3
player_class.rotation_speed = 2
player_class.max_bullets = 5
player_class.maxAcc = 0.5
player = None
# player = Starship(game, team_green, player_class, FighterPilot(game), -200, 200)
# player.auto = False
# game.add_object(player)
# game.set_focused(player)

Dust.make_dust(game, 1)

crippled_fighter = FighterClass()
#crippled_fighter.maxV = 1.5  # Maximum speed
#crippled_fighter.rotation_speed = 0.3
#crippled_fighter.max_bullets = 3

enemies = [
    Starship(game, team_yellow, crippled_fighter, FighterPilot(game), -350, -350 ),
    Starship(game, team_red, RocketFrigateClass(), RocketFrigatePilot(game), 350, -350 ),
    Starship(game, team_blue, crippled_fighter, FighterPilot(game), 350, 350 ),
]

# enemies[2].debug = True



friends = [
    Starship(game, team_green, FighterClass(), FighterPilot(game), -130, 230 ),
    Starship(game, team_green, FighterClass(), FighterPilot(game), -100, 230 ),
    Starship(game, team_green, FighterClass(), FighterPilot(game), -70, 230 ),
    Starship(game, team_green, FighterClass(), FighterPilot(game), -40, 230 ),
]

for enemy in enemies :
    # if player != None :
    #     enemy.set_enemy(player)
    # else :
    #     enemy.set_enemy(friends[random.randint(0,len(friends)-1)])
    game.add_object(enemy)


group = Group.new(game, friends[0])

for friend in friends :
    game.add_object(friend)
    group.add_ship(friend)

# Missile.fire(game)

# Create the game and start the game loop
game.game_loop()

