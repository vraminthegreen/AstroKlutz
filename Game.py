import pygame
import os
import math

from AnimatedSprite import AnimatedSprite

class Game:
    def __init__(self, input_handler):
        self.objects = []
        self.input_handler = input_handler
        self.win = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.focused = None
        self.time = 0
        self.animations = {
            'explosion' : AnimatedSprite( "explosion.png", 8, 6, 96, False ),
            'spark' : AnimatedSprite( "spark.png", 4, 4, 16, False ),
            'shield' : AnimatedSprite( "shield.png", 5, 5, 96, True ),
        }

    def add_object(self, obj):
        if self.focused == None :
            self.focused = obj
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        if obj==self.focused :
            self.focused = None

    def get_focused( self ) :
        return self.focused

    def get_collisions(self, pygame_rect ):
        collisions = []
        for obj in self.objects:
            if obj.can_be_hit and obj.get_collision_rect().colliderect(pygame_rect):
                collisions.append(obj)
        return collisions

    def get_time( self ) :
        return self.time

    def game_loop(self):
        running = True
        while running:
            self.time += 1
            self.clock.tick(60)  # Limit the game loop to 60 frames per second

            self.win.fill((0, 0, 0))
            if self.input_handler.handle_input() == False :
                running = False
            for obj in self.objects:
                obj.ticktack()
                obj.repaint(self.win)
            if self.focused != None :
                self.draw_select(self.focused, (0,255,0))

            pygame.display.flip()

        pygame.quit()

    def draw_select(self, obj, color):
        # Get the object's rectangle and create a larger rectangle
        obj_rect = obj.get_rect()
        select_rect = obj_rect.inflate(10, 10)  # Increase size by 5 pixels in each direction
        # Compute the transparency based on the current time
        transparency = int((math.sin(self.get_time()/15) + 1) / 2 * 255)  # Scale to range 0-255
        # Create a surface with the same size as the selection rectangle
        select_surface = pygame.Surface((select_rect.width, select_rect.height), pygame.SRCALPHA)
        # Draw the selection rectangle on the selection surface
        corner_length = min(select_rect.width, select_rect.height) // 3  # Adjust as needed
        # for i in range(2):
        #     for j in range(2):
        #         start_pos = (i * (select_rect.width - corner_length), j * (select_rect.height - corner_length))
        #         end_pos = (start_pos[0] + corner_length * i, start_pos[1] + corner_length * j)
        #         pygame.draw.line(select_surface, (*color, transparency), start_pos, end_pos, 1)
        pygame.draw.rect(select_surface, (*color, transparency), pygame.Rect(0, 0, *select_rect.size), 1)
        # Draw the selection surface on the window at the position of the selection rectangle
        self.win.blit(select_surface, select_rect.topleft)

    def get_animation(self, animation_name) :
        return self.animations[animation_name]

    @staticmethod
    def is_acute_angle(dir1, dir2):
        # Calculate the difference between the two directions
        diff = abs(dir1 - dir2) % 360
        # Adjust for the case where the angle crosses the 0/360 boundary
        if diff > 180:
            diff = 360 - diff
        # Check if the angle is acute
        return diff < 90



