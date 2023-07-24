
import pygame

from StarObject import StarObject
from ShipClass import ObjectClass



class Group( StarObject ) :

    def __init__(self, game) :
        super().__init__(game, ObjectClass(), 0, 0)
        self.visible = False
        self.focus_visible = True
        self.ships = []
        self.bounding_rect = pygame.Rect(0,0,0,0)

    def add_ship(self,ship) :
        self.ships.append(ship)
        if len(self.ships) == 1 :
            self.bounding_rect = ship.get_rect()
        else :
            self.bounding_rect.union_ip(ship.get_rect())
        self.visible = True
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def remove_ship(self,ship) :
        self.ships.remove(ship)
        if len(self.ships) == 0 :
            self.visible = False
            return
        self.update_bounding_rect()

    def update_bounding_rect(self) :
        self.bounding_rect = self.ships[0].get_rect()
        for aship in self.ships[1:] :
            self.bounding_rect.union_ip(aship)
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def get_rect(self) :
        return self.bounding_rect

