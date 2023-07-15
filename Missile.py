import pygame
import os
import math
import random

from StarObject import StarObject
from ShipClass import MissileClass
from Pilot import MissilePilot


class Missile ( StarObject ) :

    def __init__(self, game, missile_class, pilot, x, y ):
        StarObject.__init__( self, game, missile_class, x, y )
        self.pilot = pilot
        self.pilot.set_starship( self )
        self.fuel = self.object_class.fuel
        self.dead = False

    def ticktack( self ) :
        self.pilot.ticktack()
        super().ticktack()

    def explode( self ) :
        self.animate( self.game.get_animation('explosion'), Missile.onExploded )

    def onExploded( self ) :
        self.game.remove_object( self )
        Missile.fire( self.game )

    def get_size( self ) :
        return self.object_class.size

    def hit( self, hitter ) :
        if self.dead : return
        self.dead = True
        self.animate( self.game.get_animation('explosion'), Missile.onExploded )

    @staticmethod
    def fire( game ) :
        missile = Missile(game, MissileClass(), MissilePilot(game), random.choice( [50, 750 ] ), random.choice( [50,550] ) )
        missile.set_order(game.get_focused())
        game.add_object(missile)



