import pygame
import os
import math

from AnimatedSprite import AnimatedSprite
from Dust import Dust

class Game:

    def __init__(self, input_handler, win):
        self.win = win
        self.objects = [[],[],[],[],[]]
        self.ticktack_receivers = []
        self.mouse_tracking = []
        self.input_handler = input_handler
        self.game_window = (1024,768)
        self.game_window = (1280,720)
        self.window_center = pygame.math.Vector2(self.game_window[0]//2, self.game_window[1]//2)
        self.clock = pygame.time.Clock()
        self.focused = []
        self.time = 0
        self.initial_zoom = 0.00001
        self.zoom = self.initial_zoom
        self.zoom_speed = 15
        self.zoom_locked = None
        self.zoom_enabled = True
        self.stop_time = None
        self.camera = [ 0, 0 ]
        self.animations = {
            'explosion' : AnimatedSprite( "explosion.png", 8, 6, 96, False ),
            'spark' : AnimatedSprite( "spark.png", 4, 4, 16, False ),
            'shield' : AnimatedSprite( "shield.png", 5, 5, 96, True ),
        }
        self.paused = True
        self.key_handlers = {}
        self.font = pygame.font.Font('assets/Komika-Display/Komika_display.ttf', 16)
        self.drag_rect = None
        self.reset_fieldview()

    def reset_fieldview( self ) :
        max_width = self.game_window[0]
        max_height = self.game_window[1]
        self.optimal_fieldview = pygame.Rect(-max_width//2,-max_height//2,max_width,max_height)
        self.target_zoom = 1

    def add_object(self, obj):
        self.objects[obj.Z].append( obj )

    def add_ticktack_receiver(self, receiver) :
        self.ticktack_receivers.append(receiver)

    def add_command_receiver(self, receiver) :
        self.command_receivers.append(receiver)

    def remove_object(self, obj):
        if obj in self.objects[obj.Z] :
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
        if focused == None :
            raise ValueError("focused can't be None")
        self.focused.insert( 0, focused )

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

    def move_to_contain( self, rect1, rect2 ) :
        "move rect1 so that it contains rect2"
        if rect1.right < rect2.right :
            rect1.move_ip(rect2.right - rect1.right, 0)
        elif rect2.left < rect1.left :
            rect1.move_ip(rect2.left - rect1.left, 0)
        if rect2.top < rect1.top :
            rect1.move_ip(0, rect2.top - rect1.top) 
        elif rect1.bottom < rect2.bottom :
            rect1.move_ip(0, rect2.bottom - rect1.bottom)
        return rect1

    def compute_optimal_fieldview( self ) :
        if self.zoom_locked != None and self.zoom_locked > self.get_time() :
            return
        max_width = self.game_window[0]
        max_height = self.game_window[1]
        important_objects = [obj for obj in self.objects[0] if obj.is_important]
        if len(important_objects)==0 :
            print(f'compute_optimal_fieldview: NO IMPORTANT OBJECTS')
            self.reset_fieldview()
            return
        all_ships_fieldview = important_objects[0].get_rect()
        for obj in important_objects[1:] :
            all_ships_fieldview = all_ships_fieldview.union(obj.get_rect())
        all_fit = True
        if all_ships_fieldview.width <= max_width and all_ships_fieldview.height <= max_height :
            if self.target_zoom != 1 :
                self.toggle_zoom({'force':True})
                self.optimal_fieldview = all_ships_fieldview
        elif all_ships_fieldview.width > 2 * max_width or all_ships_fieldview.height >= 2 * max_height :
            all_fit = False
            if self.target_zoom != 1 :
                self.toggle_zoom({'force':True})
                self.optimal_fieldview.inflate_ip(-max_width, -max_height)
        elif self.target_zoom == 1 :
            self.optimal_fieldview.inflate_ip(max_width,max_height)
            max_widht = 2 * self.game_window[0]
            max_height = 2 * self.game_window[1]
            self.toggle_zoom({'force':True})
        else :
            max_width = 2 * self.game_window[0]
            max_height = 2 * self.game_window[1]
        focused_rect = all_ships_fieldview # guard
        if len(self.focused) > 0 :
            focused_rect = self.focused[0].get_rect().inflate(200,200)
            fv = all_ships_fieldview.union(focused_rect)
            if all_fit :
                if fv.width <= max_width and fv.height <= max_height :
                    all_ships_fieldview = fv
            else :
                if fv.width <= max_width and fv.height <= max_height :
                    all_ships_fieldview = fv
                else :
                    all_ships_fieldview = focused_rect
        if not self.optimal_fieldview.contains(all_ships_fieldview) :
            self.optimal_fieldview = self.move_to_contain(self.optimal_fieldview, all_ships_fieldview)
        self.optimal_fieldview.inflate_ip(
            self.game_window[0] / self.target_zoom - self.optimal_fieldview.width,
            self.game_window[1] / self.target_zoom - self.optimal_fieldview.height )
        assert self.optimal_fieldview.width == self.game_window[0] / self.target_zoom
        assert self.optimal_fieldview.height == self.game_window[1] / self.target_zoom

    def get_optimal_camera( self ) :
        return self.optimal_fieldview.center

    def compute_pans(self) :
        self.pan1 = (
            self.camera[0]-self.game_window[0]/2/self.zoom,
            self.camera[1]-self.game_window[1]/2/self.zoom )
        self.pan2 = (
            self.camera[0]/2.5/self.zoom-self.game_window[0]/2/2.5/self.zoom,
            self.camera[1]/2.5/self.zoom-self.game_window[1]/2/2.5/self.zoom)
        self.pan3 = (self.camera[0]/5-self.game_window[0]/2/self.zoom,self.camera[1]/5-self.game_window[1]/2/self.zoom)

    def pan_camera(self) :
        optimal_camera = self.get_optimal_camera()
        d = (optimal_camera[0]-self.camera[0], optimal_camera[1]-self.camera[1])
        recompute_pans = abs(d[0])>=1 or abs(d[1])>=1
        if not recompute_pans :
            return
        if abs(d[0]>10) or abs(d[1]>10) :
            self.camera[0] = self.approach_value(self.camera[0],optimal_camera[0],15)
            self.camera[1] = self.approach_value(self.camera[1],optimal_camera[1],15)
        else :
            d = ( max(1,d[0]/10) if d[0]>=0 else min(-1,d[0]/10),
                  max(1,d[1]/10) if d[1]>=0 else min(-1,d[1]/10) )
            self.camera[0] += d[0]
            self.camera[1] += d[1]
        if recompute_pans :
            self.compute_pans()

    def toggle_zoom(self, args) :
        if not self.zoom_enabled :
            return
        if args.get('force', False) or self.zoom == self.target_zoom :
            Dust.remove_dust(self)
            self.target_zoom = 1.5 - self.target_zoom
            Dust.make_dust(self, self.target_zoom)
        if args.get('lock',False) :
            self.zoom_locked = self.get_time() + 5000

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

    def get_screen_distance_from_center( self, x, y ) :
        p1 = pygame.math.Vector2(*self.get_display_xy( x, y ))
        return self.window_center.distance_to(p1)

    def get_screen_centerism( self, x, y ) :
        v = self.get_screen_distance_from_center(x,y)
        t = min(self.game_window[0]//2, self.game_window[1]//2)
        if v > t : return 0
        return (t-v) / t

    def get_xy_display( self, x, y, layer = 0 ) :
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

    def compute_bounding_rect_old(self) :
        important_objects = [obj for obj in self.objects[0] if obj.is_important]

        if not important_objects:
            return None  # Return None if there are no important objects

        # Initialize the bounding rectangle with the first object's rectangle
        bounding_rect = important_objects[0].get_rect()

        # Expand the bounding rectangle to include all other important objects
        for obj in important_objects[1:]:
            bounding_rect.union_ip(obj.get_rect())

        print(f'important_objects: {len(important_objects)}, bounding_rect: {bounding_rect}')
        return bounding_rect

    def game_loop( self ):
        self.running = True
        while self.running:
            self.time += 1


            if self.stop_time != None and self.stop_time <= self.time :
                self.running = False

            self.clock.tick(60)  # Limit the game loop to 60 frames per second

            self.compute_optimal_fieldview()

            self.zoom = Game.approach_value(self.zoom, self.target_zoom, self.zoom_speed)

            self.win.fill((0, 0, 0))
            if self.input_handler.handle_input(len(self.mouse_tracking)>0) == False :
                self.running = False


            # world_surface = pygame.Surface((self.game_window[0]/self.zoom,self.game_window[1]/self.zoom))  # The surface that represents the game world

            self.compute_pans()

            #if not self.paused :
                # self.pan_camera(bounding_rect)
            self.pan_camera()

            for receiver in self.ticktack_receivers :
                receiver.ticktack()

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
            if self.drag_rect != None :
                pygame.draw.rect(self.win, (0,180,255), self.drag_rect, 1)

            # Resize world_surface to achieve a zoom effect
            # zoomed_surface = pygame.transform.smoothscale(world_surface, self.game_window)

            # Then draw zoomed_surface onto self.win
            # self.win.blit(zoomed_surface, (0, 0))

            pygame.display.flip()


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

    def on_key_pressed(self, key) :
        handler = self.key_handlers.get( key )
        if handler != None :
            handler.on_key_pressed( key )

    def register_key_handler(self, key, handler) :
        self.key_handlers[ key ] = handler

    def on_stop_request(self) :
        self.zoom_locked = self.get_time() + 1000
        for ol in self.objects :
            for o in ol :
                o.on_stop_request()
        for o in self.ticktack_receivers :
            o.on_stop_request()
        Dust.remove_dust(self)
        self.stop_time = self.get_time() + 50
        self.zoom = 1
        self.target_zoom = self.initial_zoom
        self.zoom_speed = 15

    def get_font( self ) :
        return self.font

    def set_camera(self, pos) :
        self.set_optimal_camera( pos )
        self.camera[0] = self.optimal_camera[0]
        self.camera[1] = self.optimal_camera[1]

    def set_optimal_camera(self, pos) :
        self.optimal_fieldview.center = pos
        self.optimal_camera = pos
        self.zoom_locked = self.get_time() + 1000

    def drag_start(self, pos) :
        self.drag_p1 = pos

    def drag_continue(self, pos) :
        self.drag_p2 = pos
        top_left_x = min(self.drag_p1[0], self.drag_p2[0])
        top_left_y = min(self.drag_p1[1], self.drag_p2[1])
        width = abs(self.drag_p1[0] - self.drag_p2[0])
        height = abs(self.drag_p1[1] - self.drag_p2[1])
        self.drag_rect = pygame.Rect(top_left_x, top_left_y, width, height)

    def drag_stop(self, pos) :
        self.drag_p1 = None
        self.drag_p2 = None
        self.drag_rect = None

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



