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

    def repaint(self, win, cam1, cam2, cam3) :
        if self.layer == 0 :
            cam = cam1
        elif self.layer == 1 :
            cam = cam2
        else :
            cam = cam3
        if self.x < cam[0] :
            self.x = cam[0] + self.game.game_window[0]
            self.y = cam[1] + random.randint(0,self.game.game_window[1])
        elif self.x > cam[0] + self.game.game_window[0] :
            self.x = cam[0]
            self.y = cam[1] + random.randint(0,self.game.game_window[1])
        if self.y < cam[1] :
            self.x = cam[0] + random.randint(0,self.game.game_window[0])
            self.y = cam[1] + self.game.game_window[1]
        elif self.y > cam[1] + self.game.game_window[1] :
            self.x = cam[0] + random.randint(0,self.game.game_window[0])
            self.y = cam[1]

        pygame.draw.rect(win, (100, random.randint(150,255), random.randint(150,250)), pygame.Rect(self.x - cam[0], self.y - cam[1], 2, 2))

    def ticktack(self) :
        # pokazać z drugiej strony ekranu
        super().ticktack()


