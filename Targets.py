
import pygame

from StarObject import StarObject
from ShipClass import Stationary
from Pilot import FighterPilot

#################################################

class TargetMove ( StarObject ) :

    def __init__(self, game, owner, object_class, x, y, menu_item):
        super().__init__(game, object_class, x, y)
        self.owner = owner
        self.menu_item = menu_item

    def is_completed(self) :
        target_vector =  pygame.Vector2(self.x, self.y) - pygame.Vector2(self.owner.x, self.owner.y)
        distance_to_target = target_vector.length()
        # print(f'distance_to_target: {distance_to_target}')
        return distance_to_target < 25

    def get_vmax(self) :
        return self.owner.maxV

    def logic(self) :
        self.owner.chase( *self.get_pos() )

    def on_terminate(self) :
        pass

#################################################

class TargetEscape ( TargetMove ) :

    def __init__(self, game, owner, object_class, x, y, menu_item):
        super().__init__(game, owner, object_class, x, y, menu_item)
        self.chase_pos = None

    def is_completed(self) :
        if self.chase_pos == None :
            return False
        target_vector =  pygame.Vector2(self.chase_pos[0], self.chase_pos[1]) - pygame.Vector2(self.owner.x, self.owner.y)
        distance_to_target = target_vector.length()
        return distance_to_target < 25

    def logic(self) :
        if self.chase_pos == None or self.game.get_time() % 200 == 0 :
            vector = pygame.Vector2(self.owner.x - self.x, self.owner.y - self.y)
            # Normalize the vector (make its length 1)
            vector.normalize_ip()
            # Scale it to the desired length (1000)
            vector.scale_to_length(5000)
            # Adding it to the original position to get the extended position
            self.chase_pos = (self.x + vector.x, self.y + vector.y)
        self.owner.chase( *self.chase_pos )

#################################################

class TargetAttackMove ( TargetMove ) :

    def __init__(self, game, owner, object_class, x, y, menu_item):
        super().__init__(game, owner, object_class, x, y, menu_item)

    def get_vmax(self) :
        return 0.5 * self.owner.maxV

    def logic(self) :
        self.owner.chase( *self.get_pos() )
        if self.owner.ping_animation == None :
            if self.game.get_time() % 120 == 0 :
                self.owner.ping_animation = 100
            return
        if self.owner.enemy != None :
            self.owner.ping_animation = None
            return
        self.owner.ping_animation -= 2
        if self.owner.ping_animation < 0 : 
            self.owner.ping_animation = None
            objs = self.game.get_objects_in_range(self.owner.x, self.owner.y, self.owner.detectors_range)
            for obj in objs :
                if self.owner.is_hostile(obj) :
                    print("FOUND ENEMY")
                    order = TargetAttack(self.game, self.owner, Stationary('target', 40), self.menu_item, obj )
                    self.owner.push_order( order )

#################################################

class TargetAttack ( TargetMove ) :

    def __init__(self, game, owner, object_class, menu_item, enemy):
        super().__init__(game, owner, object_class, enemy.x, enemy.y, menu_item)
        self.enemy = enemy
        self.owner.set_enemy(enemy)
        self.owner.pilot.set_enemy(enemy)

    def get_vmax(self) :
        return self.owner.maxV

    def is_completed(self) :
        return self.enemy.dead

    def logic(self) :
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.owner.pilot.ticktack()

    def on_terminate(self) :
        self.owner.set_enemy(None)
        self.owner.pilot.set_enemy(None)

#################################################

