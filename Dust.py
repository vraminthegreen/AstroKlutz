import pygame
import os
import math
import random

from StarObject import StarObject
from ShipClass import DustClass


class Dust ( StarObject ) :

    existing_dust = []

    def __init__(self, game, zoom ):
        layer = random.randint(0,1)
        rect = game.get_visible_rectangle( layer, zoom )
        x = random.randint(rect.left, rect.right)
        y = random.randint(rect.top, rect.bottom)
        StarObject.__init__( self, game, DustClass(), x, y )
        self.layer = layer
        self.size = random.randint(1,4)
        self.new_color()
        self.color_tempo = random.randint(1,20)
        self.brightness = 0
        self.target_brightness = 1
        self.remove_timer = None
        self.Z = 1

    def repaint( self, win ) :
        rect = self.game.get_visible_rectangle( self.layer, self.game.target_zoom )
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

        col = (
            self.color[0] * self.brightness,
            self.color[1] * self.brightness,
            self.color[2] * self.brightness)

        pygame.draw.rect(win, col, pygame.Rect(center[0], center[1], self.size, self.size))

    def new_color(self) :
        self.color = (100, random.randint(150,255), random.randint(200,250))

    def ticktack(self) :
        if self.brightness < self.target_brightness :
            self.brightness = min(self.brightness + 0.03, 1)
        elif self.brightness > self.target_brightness :
            self.brightness = max(self.brightness - 0.03, 0)
        if self.remove_timer != None :
            if self.remove_timer <= 0 :
                self.game.remove_object( self )
                return
            else :
                self.remove_timer -= 1
        if self.game.get_time() % self.color_tempo == 0 :
            self.new_color()
        super().ticktack()

    def remove(self) :
        if self.remove_timer == None :
            self.remove_timer = 30;
            self.target_brightness = 0

    @staticmethod
    def remove_dust(game) :
        print(f'existing_dust: {len(Dust.existing_dust)}')
        for dust in Dust.existing_dust :
            dust.remove();
        print(f'object count (before): {len(game.objects)}')
        Dust.existing_dust = []

    @staticmethod
    def make_dust(game, zoom) :
        for i in range(0,50) :
            Dust.existing_dust.append( Dust(game, zoom) )
        for dust in Dust.existing_dust :
            game.add_object( dust )
        print(f'object count (after): {len(game.objects)}')




