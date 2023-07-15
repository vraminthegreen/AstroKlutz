import pygame
import os
import math
import random

from StarObject import StarObject


class Missile ( StarObject ) :

    def __init__(self, game, x, y ):
        StarObject.__init__( self, game, x, y, "missile" )
        self.maxV = 1  # Maximum speed
        self.maxAcc = 0.03 # thrusters power
        self.chaseDecelerate = True
        self.fuel = 700
        self.dead = False

    def ticktack( self ) :
        if self.fuel > 0 :
            self.fuel -= 1
            order_hit = self.order != None and self.distance_to(self.order) < self.get_size()
            if self.fuel == 0 or order_hit :
                self.fuel = 0
                if order_hit :
                    self.order.hit( self )
                self.animate( self.game.get_animation('explosion'), Missile.onExploded )
        super().ticktack()

    def onExploded( self ) :
        self.game.remove_object( self )
        Missile.fire( self.game )

    def get_size( self ) :
        return 48

    def hit( self, hitter ) :
        if self.dead : return
        self.dead = True
        self.animate( self.game.get_animation('explosion'), Missile.onExploded )

    @staticmethod
    def fire( game ) :
        missile = Missile(game, random.choice( [50, 750 ] ), random.choice( [50,550] ) )
        missile.set_order(game.get_focused())
        game.add_object(missile)



