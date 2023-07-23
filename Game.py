import pygame
import os
import math

from AnimatedSprite import AnimatedSprite
from Dust import Dust

class Game:

    def __init__(self, input_handler):
        self.objects = [[],[],[],[],[]]
        self.mouse_tracking = []
        self.input_handler = input_handler
        self.game_window = (1024,768)
        self.win = pygame.display.set_mode(self.game_window)
        self.clock = pygame.time.Clock()
        self.focused = []
        self.time = 0
        self.zoom = 0.5
        self.target_zoom = 1
        self.camera = [ 0, 0 ]
        self.animations = {
            'explosion' : AnimatedSprite( "explosion.png", 8, 6, 96, False ),
            'spark' : AnimatedSprite( "spark.png", 4, 4, 16, False ),
            'shield' : AnimatedSprite( "shield.png", 5, 5, 96, True ),
        }
        self.paused = True

    def add_object(self, obj):
        self.objects[obj.Z].append( obj )

    def remove_object(self, obj):
        self.objects[obj.Z].remove(obj)
        if obj in self.focused :
            self.focused.remove( obj )

    def get_focused( self ) :
        if len(self.focused) > 0 : 
            return self.focused[0]
        else :
            return None

    def set_focused(self, focused) :
        self.focused = [ focused ]

    def push_focused(self, focused) :
        self.focused.insert(0,focused)
        print(f'push focused, focused len: {len(self.focused)}')

    def pop_focused( self ) :
        if len(self.focused) > 0 :
            removed = self.focused.pop(0)
            removed.on_focus_lost()

    def get_collisions(self, pygame_rect ):
        collisions = []
        for obj in self.objects[0]:
            if obj.can_be_hit and obj.get_collision_rect().colliderect(pygame_rect):
                collisions.append(obj)
        return collisions

    def get_selections(self, pygame_rect ):
        selections = []
        for obj in self.objects[0]:
            if obj.can_be_hit and obj.get_collision_rect(1).colliderect(pygame_rect):
                selections.append(obj)
        return selections

    def get_objects_in_range(self, x, y, range) :
        res = []
        for obj in self.objects[0] :
            if obj.can_be_hit and obj.distance_to_xy(x, y) <= range :
                res.append( obj )
        return res

    def get_time( self ) :
        return self.time

    def get_visible_rectangle( self, layer, zoom = None ) :
        if zoom == None :
            zz = self.zoom
        else :
            zz = zoom
        if layer == 0 :
            z = 1
        elif layer == 1 :
            z = 2.5
        else :
            z = 5
        width = self.game_window[0] * z / zz
        height = self.game_window[1] * z / zz
        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.camera
        return rect

    def compute_pans(self) :
        self.pan1 = (
            self.camera[0]-self.game_window[0]/2/self.zoom,
            self.camera[1]-self.game_window[1]/2/self.zoom )
        self.pan2 = (
            self.camera[0]/2.5/self.zoom-self.game_window[0]/2/2.5/self.zoom,
            self.camera[1]/2.5/self.zoom-self.game_window[1]/2/2.5/self.zoom)
        self.pan3 = (self.camera[0]/5-self.game_window[0]/2/self.zoom,self.camera[1]/5-self.game_window[1]/2/self.zoom)

    def pan_camera(self, bounding_rect) :
        rect = self.get_visible_rectangle( 0, self.target_zoom )
        srect = rect.inflate( -200, -200 )

        # if not rect.collidepoint( self.focused.x, self.focused.y ) :
        #     print(f'--------------------------')
        #     print(f'visible_rectangle> left: {rect.left}, right: {rect.right}, top: {rect.top}, bottom: {rect.bottom}')
        #     print(f'focused: ({self.focused.x},{self.focused.y}) ')
        #     fd = self.get_display_xy( self.focused.x, self.focused.y, 0 )
        #     print(f'focused-display: ({fd[0]},{fd[1]}) ')            
        #     print(f'camera: ({self.camera[0]},{self.camera[1]})')
        #     print(f'pan1: ({self.pan1[0]},{self.pan1[1]})')
        #     print(f'zoom: {self.zoom}')

        recompute_pans = False
        if len(self.focused) > 0 :
            if self.focused[0].x < srect.left :
                self.camera[0] = self.focused[0].x - 100 + self.game_window[0]/2/self.zoom
                recompute_pans = True
            elif self.focused[0].x > srect.right :
                self.camera[0] = self.focused[0].x + 100 - self.game_window[0]/2/self.zoom
                recompute_pans = True
            if self.focused[0].y < srect.top :
                self.camera[1] = self.focused[0].y - 100 + self.game_window[1]/2/self.zoom
                recompute_pans = True
            elif self.focused[0].y > srect.bottom :
                self.camera[1] = self.focused[0].y + 100 - self.game_window[1]/2/self.zoom
                recompute_pans = True
        if not recompute_pans :
            if bounding_rect.left < rect.left :
                self.camera[0] -= max((rect.left-bounding_rect.left)/20,1)
                recompute_pans = True
            elif bounding_rect.right > rect.right :
                self.camera[0] += max((bounding_rect.right-rect.right)/20,1)
                recompute_pans = True
            if bounding_rect.top < rect.top :
                self.camera[1] -= max((rect.top-bounding_rect.top)/20,1)
                recompute_pans = True
            elif bounding_rect.bottom > rect.bottom :
                self.camera[1] += max((rect.bottom-bounding_rect.bottom)/20,1)
                recompute_pans = True
        if recompute_pans :
            # print(f'camera after: ({self.camera[0]},{self.camera[1]})')
            # print(f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self.compute_pans()


    def toggle_zoom(self) :
        if(self.zoom == self.target_zoom) :
            Dust.remove_dust(self)
            self.target_zoom = 1.5 - self.target_zoom
            Dust.make_dust(self, self.target_zoom)

    def toggle_pause(self) :
        print('Toggle pause')
        self.paused = not self.paused

    def get_display_xy( self, x, y, layer = 0 ) :
        "given game coords, give display coords"
        if layer == 0 :
            xy_rel_camera = ( x - self.camera[0], y - self.camera[1] )
            xy_from_layer = xy_rel_camera
            xy_from_zoom = ( self.zoom * xy_from_layer[0], self.zoom * xy_from_layer[1] )
            return (self.game_window[0] / 2 + xy_from_zoom[0], self.game_window[1] / 2 + xy_from_zoom[1])
        elif layer == 1 :
            xy_rel_camera = ( x - self.camera[0], y - self.camera[1] )
            xy_from_layer = ( xy_rel_camera[0] / 2.5, xy_rel_camera[1] / 2.5 )
            xy_from_zoom = ( self.zoom * xy_from_layer[0], self.zoom * xy_from_layer[1] )
            return (self.game_window[0] / 2 + xy_from_zoom[0], self.game_window[1] / 2 + xy_from_zoom[1])
        else :
            return (self.zoom*(x - self.pan3[0]), self.zoom*(y - self.pan3[1]))

    def get_xy_display( self, x, y ) :
        "given display coords, give game coords (in layer 0)"
        return (
            x - self.game_window[0] / 2 / self.zoom + self.camera[0],
            y - self.game_window[1] / 2 / self.zoom + self.camera[1] 
        )

    def get_display_rect( self, rect, layer ) :
        (left, top) = self.get_display_xy( rect.left, rect.top, layer )
        if layer == 0 :
            layer_factor = 1
        elif layer == 1 :
            layer_factor = 2.5
        else :
            layer_factor = 5
        width = rect.width * self.zoom / layer_factor
        height = rect.height * self.zoom / layer_factor
        return pygame.Rect( left, top, width, height )

    def compute_bounding_rect(self) :
        important_objects = [obj for obj in self.objects[0] if obj.is_important]

        if not important_objects:
            return None  # Return None if there are no important objects

        # Initialize the bounding rectangle with the first object's rectangle
        bounding_rect = important_objects[0].get_rect()

        # Expand the bounding rectangle to include all other important objects
        for obj in important_objects[1:]:
            bounding_rect.union_ip(obj.get_rect())

        return bounding_rect

    def game_loop( self ):
        running = True
        while running:
            self.time += 1
            self.clock.tick(60)  # Limit the game loop to 60 frames per second

            bounding_rect = self.compute_bounding_rect()

            if self.zoom == self.target_zoom :

                if self.zoom == 1 :
                    br = self.get_visible_rectangle(0)
                    if bounding_rect.width > br.width or bounding_rect.height > br.height :
                        self.toggle_zoom()
                elif self.zoom == 0.5 :
                    br = self.get_visible_rectangle(0, 1)
                    if bounding_rect.width < br.width and bounding_rect.height < br.height :
                        self.toggle_zoom()

            self.zoom = Game.approach_value(self.zoom, self.target_zoom, 15)

            # self.win.fill((0, 0, 0))
            if self.input_handler.handle_input(len(self.mouse_tracking)>0) == False :
                running = False


            # world_surface = pygame.Surface((self.game_window[0]/self.zoom,self.game_window[1]/self.zoom))  # The surface that represents the game world

            self.compute_pans()

            self.pan_camera(bounding_rect)

            for z_list in reversed(self.objects) :
                for obj in z_list :
                    if not self.paused or not obj.affected_by_pause :
                        obj.ticktack()

            for z_list in reversed(self.objects) :
                for obj in z_list :
                    if obj.visible :
                        obj.repaint( self.win ) # span1, pan2, pan3)
                    # obj.repaint(world_surface, pan1, pan2, pan3 )
            focus_painted = False
            for obj in self.focused :
                if obj.focus_visible and not focus_painted :
                    self.draw_select(obj, (0,255,0))
                    focus_painted = True
                if obj.visible :
                    obj.repaint_focused( self.win )

            # Resize world_surface to achieve a zoom effect
            # zoomed_surface = pygame.transform.smoothscale(world_surface, self.game_window)

            # Then draw zoomed_surface onto self.win
            # self.win.blit(zoomed_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()

    def draw_select(self, obj, color):
        # Get the object's rectangle and create a larger rectangle
        obj_rect = self.get_display_rect( obj.get_rect(), 0 )
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

    def set_mouse_tracking(self, obj, tracking_enabled) :
        if tracking_enabled :
            self.mouse_tracking.append( obj )
        else :
            self.mouse_tracking.remove( obj )

    def mouse_track( self, x, y ) :
        dc = self.get_xy_display( x, y )
        for obj in self.mouse_tracking :
            if obj.get_collision_rect().collidepoint( *dc ) :
                obj.mouse_track( dc, (x,y) )

    def click( self, x, y ) :
        if len(self.focused) > 0 :
            print(f'focused click')
            gxy = self.get_xy_display( x, y )
            if self.focused[0].click( *gxy ) :
                return
            print(f'focused click ignored')
        print(f'unfocused click')
        game_coords = self.get_xy_display( x, y )
        objects_here = self.get_selections(pygame.Rect(*game_coords,1,1))
        objects_selectable = [ obj for obj in objects_here if obj.is_selectable ]
        if len(objects_selectable) > 0 :
            self.set_focused( objects_selectable[0] )

    @staticmethod
    def is_acute_angle(dir1, dir2):
        # Calculate the difference between the two directions
        diff = abs(dir1 - dir2) % 360
        # Adjust for the case where the angle crosses the 0/360 boundary
        if diff > 180:
            diff = 360 - diff
        # Check if the angle is acute
        return diff < 90

    @staticmethod
    def approach_value(value, target, delay) :
        speed = max(0.002,abs(value - target) / delay)
        if value < target :
            return min( target, value + min(speed, target - value) )
        elif value > target :
            return max( target, value - min(speed, value - target) )
        else :
            return value



