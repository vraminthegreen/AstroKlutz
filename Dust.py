import pygame
import os
import math
import random

from StarObject import StarObject
from ShipClass import DustClass


class Dust ( StarObject ) :

    existing_dust = []

    def __init__(self, game ):
        layer = random.randint(0,1)
        rect = game.get_visible_rectangle( layer )
        x = random.randint(rect.left, rect.right)
        y = random.randint(rect.top, rect.bottom)
        StarObject.__init__( self, game, DustClass(), x, y )
        self.layer = layer
        self.size = random.randint(1,4)

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

        pygame.draw.rect(win, (100, random.randint(150,255), random.randint(150,250)), pygame.Rect(center[0], center[1], self.size, self.size))

    def ticktack(self) :
        # pokazać z drugiej strony ekranu
        super().ticktack()

    @staticmethod
    def make_dust(game) :
        print(f'existing_dust: {len(Dust.existing_dust)}')
        for dust in Dust.existing_dust :
            game.remove_object( dust )
        print(f'object count (before): {len(game.objects)}')
        Dust.existing_dust = []
        for i in range(0,50) :
            Dust.existing_dust.append( Dust(game) )
        for dust in Dust.existing_dust :
            game.add_object( dust )
        print(f'object count (after): {len(game.objects)}')




