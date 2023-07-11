import pygame
import os
import math

class Game:
    def __init__(self, input_handler):
        self.objects = []
        self.input_handler = input_handler
        self.win = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.focused = None

    def add_object(self, obj):
        if self.focused == None :
            self.focused = obj
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def get_focused( self ) :
        return self.focused

    def game_loop(self):
        running = True
        while running:
            self.clock.tick(60)  # Limit the game loop to 60 frames per second

            self.win.fill((0, 0, 0))
            if self.input_handler.handle_input() == False :
                running = False
            for obj in self.objects:
                obj.ticktack()
                obj.repaint(self.win)
            pygame.display.flip()

        pygame.quit()


