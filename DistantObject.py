
import pygame
import random

from StarObject import StarObject
from IconRepository import IconRepository
from ShipClass import Background


class DistantObject ( StarObject ) :

    def __init__(self, game, object_class, x, y) :
        self.icon_name = None
        super().__init__(game, object_class, x, y)
        self._Z = 2
        if self.icon_name == None :
            self.icon_name = f'background{random.randint(1,4)}'
        self.zoom = None
        self.initialize_icon()

    def reset_icon(self) :
        self.scaled_icon = None

    def initialize_icon(self) :
        # Scale the icon
        self.ico = IconRepository.load_icon(self.icon_name)
        if self.ico == None :
            self.scaled_icon = None
            print(f'DistantObject#{self}: initialize_icon FAILED')
            return
        self.update_scaled_icon()

    def update_scaled_icon(self) :
        if self.zoom == self.game.zoom or self.ico == None:
            return
        scale_x, scale_y = self.ico.get_size()
        scale_x *= 2
        scale_y *= 2
        self.object_width = int(scale_x * pow(self.game.zoom,0.2))
        self.object_height = int(scale_y * pow(self.game.zoom,0.2))
        self.scaled_icon = pygame.transform.scale(self.ico, (self.object_width, self.object_height))
        self.zoom = self.game.zoom

    def any_distant_visible(self) :
        for obj in self.game.objects[self.Z] :
            if obj.is_visible() :
                return True
        print(f'DistantObject#{self}: NO distant visible (suspicious objects: {len(self.game.objects[self.Z])})')
        return False

    def is_visible(self) :
        print(f'DistantObject#{self}: is_visible? scaled_icon: {self.scaled_icon}')
        return self.scaled_icon != None

    def make_new_distant(self) :
        print(f'DistanObject#{self}: make new')
        (new_x,new_y) = self.game.get_xy_display(self.game.game_window[0]/2, self.game.game_window[1]/2)
        new_x /= 5
        new_y /= 5
        # TODO: rescale according to layer
        # TODO: move behind the frame
        background = DistantObject(self.game, Background(), new_x, new_y)
        self.game.add_object(background)
        print(f'DistantObject#{self}: make new DONE ({new_x},{new_y})')

    def distance_to_midscreen(self) :
        center = self.game.get_display_xy(self.x, self.y, self.layer)
        # print(f'DistanObject#{self}: make new DONE ({new_x},{new_y})')
        midscreen = ( self.game.game_window[0]/2, self.game.game_window[1]/2 )
        # Create vectors for the two points
        vec_center = pygame.Vector2(center)
        vec_midscreen = pygame.Vector2(midscreen)
        # Calculate the distance between the two points
        return vec_center.distance_to(vec_midscreen)

    def ticktack(self) :
        self.update_scaled_icon()
        distance = self.distance_to_midscreen()

        assert distance != None

        if self.scaled_icon != None and distance > 1 * max( self.object_width, self.object_height ) :
            self.reset_icon()
            # if not self.any_distant_visible() :
            #     self.make_new_distant()

        elif self.scaled_icon == None and distance < 0.8 * max( self.object_width, self.object_height ) :
            self.initialize_icon()

    def repaint(self, win):

        if self.scaled_icon == None :
            return
        new_rect = self.scaled_icon.get_rect( center = self.game.get_display_xy(self.x, self.y, self.layer) )
        win.blit(self.scaled_icon, new_rect.topleft)


