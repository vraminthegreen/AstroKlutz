import pygame
import os
import math

from StarObject import StarObject

class Starship ( StarObject ) :

    def __init__(self, game, x, y ):
        StarObject.__init__( self, game, x, y, "starship.png" )
        self.dir = -150

    def command( self, cmd ) :
        if cmd == 'a' :
            self.auto = not self.auto
            return True
        return False



