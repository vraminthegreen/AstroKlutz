import pygame
import os
import math
import random

from StarObject import StarObject
from Bullet import Bullet
from Game import Game
from IconRepository import IconRepository


class Starship ( StarObject ) :

    def __init__(self, game, team, object_class, pilot, x, y ):
        StarObject.__init__( self, game, object_class, x, y )
        self.team = team
        self.pilot = pilot
        self.pilot.set_starship( self )
        self.icon = IconRepository.get_icon( self.object_class.icon_name, self.get_size(), self.team )
        self.dir = -150
        self.bullets = []
        self.enemy = None
        self.dead = False
        self.shield_active = False

    def command( self, cmd ) :
        if cmd == 'a' :
            if self.auto != None and self.order != None:
                self.game.remove_object(self.order)
                self.order = None
            self.auto = not self.auto
            return True
        elif cmd == ' ' :
            self.fire()
            return True
        return False

    def fire( self ) :
        if len(self.bullets) < self.object_class.max_bullets :
            bullet = Bullet( self.game, self, self.x, self.y, self.dir, self.v )
            self.bullets.append( bullet )
            self.game.add_object( bullet )

    def remove_object( self, obj ) :
        self.bullets.remove( obj )
        self.game.remove_object( obj )

    def set_enemy( self, enemy ) :
        self.enemy = enemy
        self.pilot.set_enemy( enemy )

    def ticktack(self):
        self.pilot.ticktack()
        super().ticktack()

    def hit(self, hitter):
        if self.dead or self.shield_active : return
        ddiff = ( hitter.dir - self.dir - 180 ) % 360
        if ddiff < 0 : ddiff = -ddiff
        aa = Game.is_acute_angle( hitter.dir, self.dir )
        if aa :
            print("belly hit")
        else :
            print("shield hit")
        if ( aa and random.randint(0, 99) < (100-self.object_class.rear_shield) ) or ( random.randint(0,99) < (100-self.object_class.front_shield) ) :
            self.icon = None
            self.dead = True
            self.animate( self.game.get_animation('explosion'), Starship.onExploded )
        else :
            self.shield_active = True
            self.animate( self.game.get_animation('shield'), Starship.onShieldEnded )

    def onExploded( self ) :
        self.game.remove_object( self )

    def onShieldEnded( self ) :
        self.shield_active = False


    # def repaint(self, win):
    #     if self.enemy != None :
    #         (xx,yy) = self.enemy.get_pos_in_front(-100)
    #         pygame.draw.rect(win, (255, 255, 255), pygame.Rect(xx, yy, 5, 5))
    #     super().repaint(win)


