import pygame
import os
import math
import random

from StarObject import StarObject
from AnimatedSprite import AnimatedSprite

class Missile ( StarObject ) :

    def __init__(self, game, x, y ):
        StarObject.__init__( self, game, x, y, "missile.png" )
        self.maxV = 1  # Maximum speed
        self.maxAcc = 0.03 # thrusters power
        self.chaseDecelerate = True
        self.explosionAnimation = AnimatedSprite( "explosion.png", 8, 6, self.get_size() * 2 )
        self.fuel = 700

    def ticktack( self ) :
        if self.fuel > 0 :
            self.fuel -= 1
            if self.fuel == 0 or ( self.order != None and self.distance_to(self.order) < self.get_size() ):
                self.fuel = 0
                self.animate( self.explosionAnimation, Missile.onExploded )
        super().ticktack()

    def onExploded( self ) :
        self.game.remove_object( self )
        Missile.fire( self.game )

    def get_size( self ) :
        return 48

    @staticmethod
    def fire( game ) :
        missile = Missile(game, random.choice( [50, 750 ] ), random.choice( [50,550] ) )
        missile.set_order(game.get_focused())
        game.add_object(missile)



