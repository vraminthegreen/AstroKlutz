import pygame
import os
import math
import random

from StarObject import StarObject
from ShipClass import DustClass


class Dust ( StarObject ) :

    def __init__(self, game, x, y ):
        StarObject.__init__( self, game, DustClass(), x, y )
        self.layer = random.randint(0,1)

    def repaint( self, win ) :
        rect = self.game.get_visible_rectangle( self.layer )
        if self.x < rect.left :
            self.x = rect.right
            self.y = random.randint(rect.top, rect.bottom)
        elif self.x >= rect.right :
            self.x = rect.left
            self.y = random.randint(rect.top, rect.bottom)
        if self.y >= rect.bottom :
            self.x = random.randint(rect.left, rect.right)
            self.y = rect.top
        elif self.y < rect.top :
            self.x = random.randint(rect.left, rect.right)
            self.y = rect.bottom
        center = self.game.get_display_xy(self.x, self.y, self.layer)

        pygame.draw.rect(win, (100, random.randint(150,255), random.randint(150,250)), pygame.Rect(center[0], center[1], 2, 2))

    def ticktack(self) :
        # pokazać z drugiej strony ekranu
        super().ticktack()


