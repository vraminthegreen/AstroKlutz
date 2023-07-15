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
        self.order = None
        self.animationOngoing = None
        self.animationFrame = None
        # copy the prototype
        self.size = self.object_class.size
        self.can_be_hit = self.object_class.can_be_hit
        self.resistance = self.object_class.resistance
        self.maxAcc = self.object_class.maxAcc
        self.maxV = self.object_class.maxV
        self.rotation_speed = self.object_class.rotation_speed
        self.chaseDecelerate = self.object_class.chaseDecelerate
        self.layer = self.object_class.layer
        #
        if self.object_class.icon_name != None :
            self.icon = IconRepository.get_icon(self.object_class.icon_name, self.get_size())
            if self.size == None :
                self.size = max(*self.icon.get_size())
        else :
            self.icon = None

    def get_size( self ) :
        return self.size

    def can_be_hit( self ) :
        return self.can_be_hit

    def get_icon( self ) :
        if self.animationFrame != None :
            return self.animationFrame
        else :
            return self.icon

    def repaint(self, win, pan1, pan2, pan3):
        if self.layer == 0 :
            co = pan1
        elif self.layer == 1 :
            co = pan2
        else :
            co = pan3
        if self.icon != None and self.animationFrame != None and self.animationOverlay :
            rotated_icon = pygame.transform.rotate(self.icon, self.dir)
            new_rect = rotated_icon.get_rect(center=(self.x - co[0], self.y - co[1]))
            win.blit(rotated_icon, new_rect.topleft)
        ico = self.get_icon()
        if ico == None :
            return
        rotated_icon = pygame.transform.rotate(ico, self.dir)
        new_rect = rotated_icon.get_rect(center=(self.x - co[0], self.y - co[1]))
        win.blit(rotated_icon, new_rect.topleft)

    def ticktack(self):
        if self.auto and self.order :
            self.chase( *self.order.get_pos() )
        if self.animationOngoing != None :
            self.animateNextFrame()        
        self.x += self.v.x
        self.y += self.v.y
        self.v *= self.resistance

    def get_pos(self) :
        return (self.x, self.y)

    def get_rect(self) :
        width = self.get_size()
        height = width
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)

    def get_collision_rect(self) :
        width = self.get_size() / 2
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
        if self.order :
            self.game.remove_object( self.order )
        self.order = order
        self.auto = True

    def accelerate(self):
        acceleration_vector = pygame.Vector2(self.maxAcc, 0).rotate(-self.dir)
        self.v += acceleration_vector
        if self.v.length() > self.maxV:
            self.v.scale_to_length(self.maxV)

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

    def chase(self, tx, ty):
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
        if distance_to_target > 60 :  # Accelerate if far from the target
            if abs(difference_in_direction) < 90 :
                self.accelerate()
        elif self.chaseDecelerate :  # Decelerate if close to the target
            self.decelerate()

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
            self.animationAfter( self )


