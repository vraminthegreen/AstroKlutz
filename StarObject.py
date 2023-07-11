import pygame
import os
import math

class StarObject :

    def __init__(self, game, x, y, icon_name):
        self.game = game
        self.x = x
        self.y = y
        self.dir = 0  # Direction in degrees
        self.v = pygame.Vector2(0, 0)  # Velocity vector
        self.maxV = 2  # Maximum speed
        self.maxAcc = 0.01 # thrusters power
        self.chaseDecelerate = True
        self.auto = True
        self.order = None
        self.load_icon(icon_name)


    def load_icon(self, icon_name):
        # Load and resize the icon
        self.icon = pygame.image.load(os.path.join('.', icon_name))

        orig_width, orig_height = self.icon.get_size()

        # Determine the aspect ratio
        aspect_ratio = orig_width / orig_height

        # Calculate new dimensions
        if aspect_ratio >= 1:  # Width is greater than height
            new_width = self.get_size()
            new_height = int(self.get_size() / aspect_ratio)
        else:  # Height is greater than width
            new_height = self.get_size()
            new_width = int(self.get_size() * aspect_ratio)

        # Resize the image with anti-aliasing
        self.icon = pygame.transform.smoothscale(self.icon, (new_width, new_height))
        self.icon = self.icon.convert_alpha()

    def get_size( self ) :
        return 64

    def get_icon( self ) :
        return self.icon

    def repaint(self, win):
        rotated_icon = pygame.transform.rotate(self.get_icon(), self.dir)
        new_rect = rotated_icon.get_rect(center=(self.x, self.y))
        win.blit(rotated_icon, new_rect.topleft)

    def ticktack(self):
        if self.auto and self.order :
            self.chase( *self.order.get_pos() )
        self.x += self.v.x
        self.y += self.v.y

    def get_pos(self) :
        return (self.x, self.y)

    def distance_to(self, other) :
        point1 = pygame.math.Vector2(self.x, self.y)
        point2 = pygame.math.Vector2(other.x, other.y)
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

    def chase(self, tx, ty):
        target_vector = pygame.Vector2(tx, -ty) - pygame.Vector2(self.x, -self.y)
        direction_to_target = math.degrees(math.atan2(target_vector.y, target_vector.x))
        difference_in_direction = (direction_to_target - self.dir) % 360

        # Adjust for the shortest rotation direction
        if difference_in_direction > 180:
            difference_in_direction -= 360

        # Determine whether to rotate left or right
        if difference_in_direction > 0:
            self.rotate(1)
        elif difference_in_direction < 0:
            self.rotate(-1)

        # Determine whether to accelerate or decelerate
        distance_to_target = target_vector.length()
        if distance_to_target > 40 :  # Accelerate if far from the target
            if abs(difference_in_direction) < 90 :
                self.accelerate()
        elif self.chaseDecelerate :  # Decelerate if close to the target
            self.decelerate()


