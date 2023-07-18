import pygame
import os
import math

from AnimatedSprite import AnimatedSprite

class Game:
    def __init__(self, input_handler):
        self.objects = []
        self.input_handler = input_handler
        self.game_window = (1024,768)
        self.win = pygame.display.set_mode(self.game_window)
        self.clock = pygame.time.Clock()
        self.focused = None
        self.time = 0
        self.zoom = 1
        self.target_zoom = 1
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

    def set_focused(self, focused) :
        self.focused = focused

    def get_collisions(self, pygame_rect ):
        collisions = []
        for obj in self.objects:
            if obj.can_be_hit and obj.get_collision_rect().colliderect(pygame_rect):
                collisions.append(obj)
        return collisions

    def get_time( self ) :
        return self.time

    def pan_camera(self) :
        if self.focused == None :
            return
        left = self.camera[0] - self.game_window[0]/2 + 100
        right = self.camera[0] + self.game_window[0]/2 - 100
        top = self.camera[1] + self.game_window[1]/2 - 100
        bottom = self.camera[1] - self.game_window[1]/2 + 100

        if self.focused.x < left :
            self.camera[0] = self.focused.x + self.game_window[0]/2 - 100
        elif self.focused.x > right :
            self.camera[0] = self.focused.x - self.game_window[0]/2 + 100
        if self.focused.y < bottom :
            self.camera[1] = self.focused.y + self.game_window[1]/2 - 100
        elif self.focused.y > top :
            self.camera[1] = self.focused.y - self.game_window[1]/2 + 100

    def toggle_zoom(self) :
        if(self.zoom == self.target_zoom) :
            self.target_zoom = 1.5 - self.target_zoom


    def get_display_xy( self, x, y, layer ) :
        if layer == 0 :
            co = self.pan1
        elif layer == 1 :
            co = self.pan2
        else :
            co = self.pan3
        return (x - co[0], y - co[1])

    def get_visible_rectangle( self, layer ) :
        if layer == 0 :
            co = self.pan1
            z = 1
        elif layer == 1 :
            co = self.pan2
            z = 2.5
        else :
            co = self.pan3
            z = 5
        return pygame.Rect(co[0], co[1], self.game_window[0] * z, self.game_window[1] * z)

    def game_loop( self ):
        running = True
        self.camera = [0,0]
        while running:
            self.time += 1
            self.clock.tick(60)  # Limit the game loop to 60 frames per second
            zoom_speed = max(0.002,abs(self.zoom - self.target_zoom) / 10)

            if self.zoom < self.target_zoom:
                self.zoom += min(zoom_speed, self.target_zoom - self.zoom)
            elif self.zoom > self.target_zoom:
                self.zoom -= min(zoom_speed, self.zoom - self.target_zoom)

            self.pan_camera()

            # self.win.fill((0, 0, 0))
            if self.input_handler.handle_input() == False :
                running = False

            # world_surface = pygame.Surface((self.game_window[0]/self.zoom,self.game_window[1]/self.zoom))  # The surface that represents the game world

            self.pan1 = (self.camera[0]-self.game_window[0]/2,self.camera[1]-self.game_window[1]/2)
            self.pan2 = (self.camera[0]/2.5-self.game_window[0]/2,self.camera[1]/2.5-self.game_window[1]/2)
            self.pan3 = (self.camera[0]/5-self.game_window[0]/2,self.camera[1]/5-self.game_window[1]/2)
            for obj in self.objects:
                obj.ticktack()
                obj.repaint( self.win ) # span1, pan2, pan3)
                # obj.repaint(world_surface, pan1, pan2, pan3 )
            if self.focused != None :
                self.draw_select(self.focused, (0,255,0))


            # Resize world_surface to achieve a zoom effect
            # zoomed_surface = pygame.transform.smoothscale(world_surface, self.game_window)

            # Then draw zoomed_surface onto self.win
            # self.win.blit(zoomed_surface, (0, 0))

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



