import pygame
import os
import math
import random

from StarObject import StarObject
from ShipClass import BulletClass


class Bullet ( StarObject ) :

    def __init__(self, game, owner, x, y, dir, v ):
        StarObject.__init__( self, game, BulletClass(), x, y )
        self.dir = dir

        # Convert the ship's direction to radians
        dir_rad = math.radians(dir)

        # Create a unit vector in the direction of the ship's orientation
        bullet_dir = pygame.Vector2(math.cos(dir_rad), -math.sin(dir_rad))
        bullet_speed = 3
        # Multiply the bullet's direction vector by its speed to get its velocity
        bullet_v = bullet_dir * bullet_speed  # Assuming bullet_speed is 3

        # Add the ship's velocity to the bullet's velocity
        bullet_v += v

        self.v = bullet_v
        self.x += 10 * self.v.x
        self.y += 10 * self.v.y
        self.owner = owner
        self.team = self.owner.team
        self.fuel = self.object_class.fuel

    def repaint( self, win ) :
        if self.animationFrame != None :
            super().repaint( win )
        else :
            center = self.game.get_display_xy(self.x, self.y, 0)
            pygame.draw.rect(win, (255, 255, 255), pygame.Rect(center[0], center[1], 2, 2))

    def hit(self, target) :
        self.fuel = 0
        target.hit( self )
        self.v = pygame.Vector2(0, 0)  # Velocity vector
        self.animate( self.game.get_animation('spark'), Bullet.onExploded )

    def ticktack(self) :
        if self.fuel > 0 :
            self.fuel -= 1
            if self.fuel == 0 :
                self.owner.remove_object( self )
                return
            elif random.randint(0, 99) <= 30 :
                collisions = self.game.get_collisions( pygame.Rect(self.x, self.y, 3, 3) )
                for obj in collisions :
                    if obj.is_hostile( self ) :
                        self.hit( obj )
                        break
        super().ticktack()

    def onExploded( self ) :
        self.owner.remove_object( self )


