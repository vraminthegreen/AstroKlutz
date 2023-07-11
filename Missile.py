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
        self.exploding = None
        self.currentIcon = None
        self.fuel = 700

    def ticktack( self ) :
        if self.exploding != None :
            self.exploding += 1
        else :
            self.fuel -= 1
            if self.fuel == 0 :
                self.exploding = 0
            elif self.order != None and self.distance_to(self.order) < self.get_size() :
                self.exploding = 0
        if self.exploding != None :
            self.currentIcon = self.explosionAnimation.get_frame(self.exploding)
            if self.currentIcon == None :
                self.game.remove_object( self )
                Missile.fire( self.game )
                return
        super().ticktack()


    def get_size( self ) :
        return 48

    def get_icon( self ) :
        if self.currentIcon :
            return self.currentIcon
        else :
            return super().get_icon()

    @staticmethod
    def fire( game ) :
        missile = Missile(game, random.choice( [50, 750 ] ), random.choice( [50,550] ) )
        missile.set_order(game.get_focused())
        game.add_object(missile)



