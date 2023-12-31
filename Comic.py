
import sys
import math
import pygame

from Game import Game

class Comic ( Game ) :

    def __init__(self, owner, input_handler, win):
        super().__init__(input_handler, win)
        self.owner = owner
        self.zoom_locked = sys.maxsize # infinity
        self.zoom = 0.0001
        self.zoom_speed = 10000
        self.rad = 4000

    def get_optimal_camera( self ) :
        self.rad = self.approach_value(self.rad, 1000, 10000)
        return ( 
            self.rad * math.sin(self.get_time() / 1500),
            self.rad * math.cos(self.get_time() / 1500) )

