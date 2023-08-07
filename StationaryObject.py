
import pygame
import random

from StarObject import StarObject
from IconRepository import IconRepository
from ShipClass import Background


class StationaryObject ( StarObject ) :

    def __init__(self, game, object_class, x, y) :
        self.icon_name = None
        super().__init__(game, object_class, x, y)
        self._Z = 1
        self.zoom = None


