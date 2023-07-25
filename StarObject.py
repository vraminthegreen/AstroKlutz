import pygame
import os
import math

from IconRepository import IconRepository


class StarObject :

    def __init__(self, game, object_class, x, y):
        self.game = game
        self.object_class = object_class
        self.x = x
        self.y = y
        self.dir = 0  # Direction in degrees
        self.v = pygame.Vector2(0, 0)  # Velocity vector
        self.auto = True
        self.orders = []
        self.animationOngoing = None
        self.animationFrame = None
        # copy the prototype
        self.size = self.object_class.size
        self.minimized_size = self.object_class.minimized_size
        self.can_be_hit = self.object_class.can_be_hit
        self.resistance = self.object_class.resistance
        self.maxAcc = self.object_class.maxAcc
        self.maxV = self.object_class.maxV
        self.rotation_speed = self.object_class.rotation_speed
        self.chaseDecelerate = self.object_class.chaseDecelerate
        self.layer = self.object_class.layer
        self.detectors_range = self.object_class.detectors_range
        #
        if self.object_class.icon_name != None :
            self.icon = IconRepository.get_icon(self.object_class.icon_name, self.get_size())
            if self.size == None :
                self.size = max(*self.icon.get_size())
        else :
            self.icon = None
        self.is_important = False
        self.affected_by_pause = False
        self.is_selectable = False
        self.focus_visible = False
        self.visible = True
        self.Z = 0

    def get_size( self ) :
        return self.size

    def can_be_hit( self ) :
        return self.can_be_hit

    def get_icon( self ) :
        if self.animationFrame != None :
            return self.animationFrame
        else :
            return self.icon

    def repaint(self, win):
        if self.icon != None and self.animationFrame != None and self.animationOverlay :
            # Scale the icon
            scale_x, scale_y = self.icon.get_size()
            scale_x = int(scale_x * self.game.zoom)
            scale_y = int(scale_y * self.game.zoom)
            scaled_icon = pygame.transform.scale(self.icon, (scale_x, scale_y))
            
            # Rotate the scaled icon
            rotated_icon = pygame.transform.rotate(scaled_icon, self.dir)
            
            new_rect = rotated_icon.get_rect( center = self.game.get_display_xy(self.x, self.y, self.layer) )
            win.blit(rotated_icon, new_rect.topleft)

        ico = self.get_icon()
        if ico == None :
            return

        # Scale the icon
        scale_x, scale_y = ico.get_size()
        scale_x = int(scale_x * self.game.zoom)
        scale_y = int(scale_y * self.game.zoom)
        scaled_icon = pygame.transform.scale(ico, (scale_x, scale_y))

        # Rotate the scaled icon
        rotated_icon = pygame.transform.rotate(scaled_icon, self.dir)

        new_rect = rotated_icon.get_rect( center = self.game.get_display_xy(self.x, self.y, self.layer) )
        win.blit(rotated_icon, new_rect.topleft)

    def repaint_focused(self, win) :
        o1dxy = self.game.get_display_xy(self.x, self.y)
        for order in self.orders :            
            # Create vectors for the orders
            o2dxy = self.game.get_display_xy(order.x, order.y)
            vec1 = pygame.Vector2(*o1dxy)
            vec2 = pygame.Vector2(*o2dxy)
            # Calculate the direction vector from order1 to order2
            dir_vec = (vec2 - vec1).normalize()
            # Calculate the start and end points of the line
            start_pos = vec1 + dir_vec * 30
            end_pos = vec2 - dir_vec * 30
            pygame.draw.line(win, (35, 209, 155), start_pos, end_pos)
            o1dxy = o2dxy

        for order in self.orders :
            order.repaint( win )

    def ticktack(self):
        if self.auto and len(self.orders)>0 :
            if self.orders[0].is_completed() :
                self.pop_order()
        if self.animationOngoing != None :
            self.animateNextFrame()        
        self.x += self.v.x
        self.y += self.v.y
        self.v *= self.resistance

    def set_pos(self, x, y) :
        self.x = x
        self.y = y

    def get_pos(self) :
        return (self.x, self.y)

    def get_rect(self) :
        width = self.get_size()
        height = width
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)

    def get_collision_rect(self, range = 0.5) :
        width = self.get_size() * range
        height = width
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)

    def get_pos_in_front(self, distance) :
        # Przeliczamy kierunek na radiany
        dir_rad = math.radians(self.dir)
        # Obliczamy nową pozycję
        new_x = self.x + distance * math.cos(dir_rad)
        new_y = self.y - distance * math.sin(dir_rad)  # Odejmujemy, ponieważ os Y w Pygame jest skierowana w dół
        return (new_x, new_y)

    def get_displaced_pos(self, dir, distance) :
        displacement = pygame.Vector2(self.size, 0).rotate(-dir)
        pos = pygame.Vector2(self.x, self.y) + displacement
        return (pos.x, pos.y)

    def distance_to(self, other) :
        point1 = pygame.math.Vector2(self.x, self.y)
        point2 = pygame.math.Vector2(other.x, other.y)
        distance = point1.distance_to(point2)
        return distance

    def distance_to_xy(self, x, y) :
        point1 = pygame.math.Vector2(self.x, self.y)
        point2 = pygame.math.Vector2(x, y)
        distance = point1.distance_to(point2)
        return distance

    def set_order(self, order) :
        for order in self.orders :
            self.game.remove_object( self.order )
        self.orders = [ order ]
        order.on_activate()
        self.auto = True

    def append_order(self, order) :
        self.game.add_object( order )
        self.orders.append(order)
        if len(self.orders) == 1 :
            order.on_activate()
        self.auto = True

    def push_order(self, order) :
        self.game.add_object( order )
        if len(self.orders) > 0 :
            self.orders[0].on_deactivate()
        self.orders.insert(0, order)
        order.on_activate()
        self.auto = True

    def pop_order(self) :
        order = self.orders.pop( 0 )
        order.on_completed()
        self.game.remove_object( order )
        if len(self.orders) == 0 :
            self.auto = False
        else :
            self.orders[0].on_activate()

    def accelerate(self):
        acceleration_vector = pygame.Vector2(self.maxAcc, 0).rotate(-self.dir)
        self.v += acceleration_vector
        current_vmax = self.get_current_vmax();
        if self.v.length() > current_vmax:
            self.v.scale_to_length(current_vmax)

    def decelerate(self):
        if self.v.length() > 0:
            deceleration_vector = pygame.Vector2(-self.maxAcc, 0).rotate(-self.v.angle_to(pygame.Vector2(1, 0)))
            self.v += deceleration_vector

            # Gradually rotate the starship towards the direction of movement
            desired_dir = self.v.angle_to(pygame.Vector2(1, 0))
            rotation_dir = (desired_dir - self.dir) % 360
            if rotation_dir > 180:
                rotation_dir -= 360  # Adjust for the shortest rotation direction
            rotation_dir = max(min(rotation_dir, 1), -1)  # Limit rotation to 1 degree per tick
            self.dir += rotation_dir

            if self.v.length() < 0.1:
                self.v = pygame.Vector2(0, 0)

    def rotate(self, rotation):
        self.dir += rotation
        self.dir %= 360

    def rotateRight(self) :
        self.rotate(self.rotation_speed)

    def rotateLeft(self) :
        self.rotate(-self.rotation_speed)

    def chase(self, tx, ty, decelerate = None):
        target_vector = pygame.Vector2(tx, -ty) - pygame.Vector2(self.x, -self.y)
        direction_to_target = math.degrees(math.atan2(target_vector.y, target_vector.x))
        difference_in_direction = (direction_to_target - self.dir) % 360

        # Adjust for the shortest rotation direction
        if difference_in_direction > 180:
            difference_in_direction -= 360

        # Determine whether to rotate left or right
        if difference_in_direction > 0:
            self.rotateRight()
        elif difference_in_direction < 0:
            self.rotateLeft()

        # Determine whether to accelerate or decelerate
        distance_to_target = target_vector.length()

        if decelerate == None :
            thedecelerate = self.chaseDecelerate
        else :
            thedecelerate = decelerate
        if distance_to_target > 40 :  # Accelerate if far from the target
            if abs(difference_in_direction) < 90 :
                self.accelerate()
        elif thedecelerate and self.v.length() > distance_to_target / 40  :  # Decelerate if close to the target
            self.decelerate()
        return distance_to_target < 20

    def is_in_field(self, ox, oy, dir_a, dir_b, dist_min, dist_max):
        target_vector = pygame.Vector2(ox, oy) - pygame.Vector2(self.x, self.y)
        # Calculate the direction to the target point
        direction_to_target = math.degrees(math.atan2(-target_vector.y, target_vector.x)) % 360
        # Calculate the distance to the target point
        distance_to_target = target_vector.length()
        # Check if the direction and distance are within the provided ranges
        direction_in_range = (dir_a <= direction_to_target <= dir_b) or \
                             (dir_a <= direction_to_target + 360 <= dir_b) or \
                             (dir_a <= direction_to_target - 360 <= dir_b)
        distance_in_range = dist_min <= distance_to_target <= dist_max
        return direction_in_range and distance_in_range

    def animate(self, animation, after) :
        self.animationOngoing = animation
        self.animationAfter = after;
        self.animationFrameNo = 0
        self.animationOverlay = animation.get_overlay()

    def animateNextFrame( self ) :
        self.animationFrame = self.animationOngoing.get_frame(self.animationFrameNo)
        self.animationFrameNo += 1
        if self.animationFrame == None :
            self.animationOngoing = None
            self.animationAfter(self)

    def click(self, x, y) :
        return False

    def command_delete(self) :
        order = self.orders.pop( -1 )
        self.game.remove_object( order )
        if len(self.orders) == 0 :
            order.on_deactivate()
            self.auto = False

    def on_focus_lost(self) :
        return False

    def get_current_vmax(self) :
        if len(self.orders) > 0 :
            return self.orders[0].get_vmax()
        else :
            return self.maxV

