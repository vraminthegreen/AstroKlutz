import pygame
import os
import math

from StarObject import StarObject
from Bullet import Bullet
from AnimatedSprite import AnimatedSprite

class Starship ( StarObject ) :

    def __init__(self, game, x, y ):
        StarObject.__init__( self, game, x, y, "starship.png" )
        self.dir = -150
        self.max_bullets = 5
        self.bullets = []
        self.enemy = None
        self.enemy_chase_mode = 1
        self.explosionAnimation = AnimatedSprite( "explosion.png", 8, 6, self.get_size() * 2 )
        self.dead = False

    def command( self, cmd ) :
        if cmd == 'a' :
            self.auto = not self.auto
            return True
        elif cmd == ' ' :
            self.fire()
            return True
        return False

    def fire( self ) :
        if len(self.bullets) < self.max_bullets :
            bullet = Bullet( self.game, self, self.x, self.y, self.dir, self.v )
            self.bullets.append( bullet )
            self.game.add_object( bullet )

    def remove_object( self, obj ) :
        self.bullets.remove( obj )
        self.game.remove_object( obj )

    def set_enemy( self, enemy ) :
        self.enemy = enemy

    def ticktack(self):
        if self.enemy != None :
            if self.enemy_chase_mode == 1 :
                self.chase( * self.enemy.get_pos_in_front(-200) )
            else :
                self.chase( * self.enemy.get_pos() )
            if self.enemy.is_in_field(self.x, self.y, self.dir - (180+25), self.dir - (180-25), 0, 300) :
                self.enemy_chase_mode = 2
            elif not self.enemy.is_in_field(self.x, self.y, self.dir - (180+45), self.dir - (180-45), 0, 300) :
                self.enemy_chase_mode = 1
            if self.game.get_time() % 10 == 0 and self.is_in_field( self.enemy.x, self.enemy.y, self.dir - 30, self.dir + 30, 0, 250) :
                self.fire()
        super().ticktack()

    def hit(self, hitter):
        if self.dead : return
        self.icon = None
        self.dead = True
        self.animate( self.explosionAnimation, Starship.onExploded )

    def onExploded( self ) :
        self.game.remove_object( self )


    # def repaint(self, win):
    #     if self.enemy != None :
    #         (xx,yy) = self.enemy.get_pos_in_front(-100)
    #         pygame.draw.rect(win, (255, 255, 255), pygame.Rect(xx, yy, 5, 5))
    #     super().repaint(win)


