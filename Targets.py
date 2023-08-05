
import pygame
import random

from StarObject import StarObject
from ShipClass import Stationary
from Pilot import FighterPilot
from Formation import Formation

#################################################

class Target ( StarObject ) :

    def on_activate(self) :
        pass

    def on_deactivate(self) :
        pass

    def on_completed(self) :
        pass

    def on_deleted(self) :
        pass

    def is_completed(self) :
        return False

    def get_vmax(self) :
        return 0

    def logic(self) :
        pass


#################################################

class TargetMove ( Target ) :

    def __init__(self, game, owner, object_class, x, y, menu_item):
        super().__init__(game, object_class, x, y)
        self.owner = owner
        self.menu_item = menu_item
        self.visible = False
        self.completed = False  
        self.weak = False      

    def on_activate(self) :
        pass

    def on_deactivate(self) :
        pass

    def is_completed(self) :        
        if self.completed == True :
            return True
        target_vector =  pygame.Vector2(self.x, self.y) - pygame.Vector2(self.owner.x, self.owner.y)
        distance_to_target = target_vector.length()
        # print(f'distance_to_target: {distance_to_target}')
        self.completed = distance_to_target < 35
        if self.completed :
            print("TargetMove completed")
        return self.completed

    def get_vmax(self) :
        return self.owner.maxV

    def logic(self) :
        self.owner.chase( *self.get_pos() )

    def on_completed(self) :
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

    def __init__(self, game, owner, object_class, x, y, menu_item, guarding_time = 0 ):
        super().__init__(game, owner, object_class, x, y, menu_item)
        self.chase_pos = self.get_pos()
        self.guarding_time = guarding_time
        print(f'New TargetAttackMove: {self}')

    def get_vmax(self) :
        return 0.5 * self.owner.maxV

    def logic(self) :
        if self.chase_pos != None :
            self.owner.chase( *self.chase_pos, False )
        if self.owner.enemy != None :
            self.owner.ping_animation = None
        if self.owner.ping_animation == None and self.owner.enemy == None:
            if self.game.get_time() % 120 == 0 :
                if self.owner.debug :
                    print(f'{self.owner.name} TargetAttackMove.logic - start ping')
                self.owner.ping_animation = 100
        if self.owner.ping_animation != None :
            self.owner.ping_animation -= 2
            if self.owner.ping_animation < 0 : 
                self.owner.ping_animation = None
                if random.randint(0,10) <= 3 : 
                    if self.owner.debug :
                        print(f'{self.owner.name} TargetAttackMove.logic - execute ping')                    
                    objs = self.game.get_objects_in_range(self.owner.x, self.owner.y, self.owner.detectors_range)
                    for obj in objs :
                        if self.owner.is_hostile(obj) :
                            print(f"{self.owner.name} FOUND ENEMY {obj.name}")
                            order = TargetAttack(self.game, self.owner, Stationary('target', 40), self.menu_item, obj )
                            self.owner.push_order( order )
                            self.completed = False
        if self.completed and self.guarding_time > 0 :
            if self.owner.debug and self.guarding_time % 100 == 0:
                print(f'{self.owner.name} TargetAttackMove.logic - guarding {self.guarding_time}')
            self.guarding_time -= 1

    def is_completed(self) :
        res = super().is_completed()
        if res and self.guarding_time > 0 : 
            if self.guarding_time % 100 == 0 :
                print(f'{self.owner.name} GUARDING ({self.guarding_time})  ({self}) ...')
            return
        if res :
            self.owner.ping_animation = None
            print(f'{self.owner.name} GUARDING completed')
        return res


#################################################

class TargetPatrolMove ( TargetAttackMove ) :

    def on_completed(self) :
        self.owner.append_order(self)


#################################################

class TargetAttack ( TargetMove ) :

    def __init__(self, game, owner, object_class, menu_item, enemy):
        super().__init__(game, owner, object_class, enemy.x, enemy.y, menu_item)
        self.enemy = enemy

    def on_activate(self) :
        self.owner.set_enemy(self.enemy)
        self.owner.pilot.set_enemy(self.enemy)

    def on_deactivate(self) :
        self.owner.set_enemy(None)
        self.owner.pilot.set_enemy(None)

    def get_vmax(self) :
        return self.owner.maxV

    def is_completed(self) :
        return self.enemy.dead

    def logic(self) :
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.owner.pilot.ticktack()

    def on_completed(self) :
        self.owner.set_enemy(None)
        self.owner.pilot.set_enemy(None)

#################################################

class TargetFollow ( TargetAttackMove ) :

    def __init__(self, game, owner, object_class, menu_item, target, guard):
        super().__init__(game, owner, object_class, target.x, target.y, menu_item)
        self.target = target
        self.guard = guard
        self.chase_pos = None
        # self.owner.set_enemy(enemy)
        # self.owner.pilot.set_enemy(enemy)

    def on_activate(self) :
        if self.target.formation == None :
            self.target.formation = Formation(self.target)
        if self.guard :
            self.target.formation.add_guard(self.owner)
        else :
            self.target.formation.add_follower(self.owner)        

    def on_deactivate(self) :
        self.target.formation.remove(self.owner)

    def get_vmax(self) :
        if self.guard :
            return 0.5 * self.owner.maxV
        else :
            return self.owner.maxV

    def is_completed(self) :
        return self.target.dead

    def logic(self) :
        self.x = self.target.x
        self.y = self.target.y
        if self.chase_pos == None or self.game.get_time() % 200 == 0 :
            self.chase_pos = self.target.formation.get_optimal_pos( self.owner )
            if self.chase_pos == None :
                print("TargetFollow: formation position not found")
                self.owner.pop_order()
        if self.guard :
            super().logic()
        elif self.chase_pos != None :
            self.owner.chase( *self.chase_pos, False )

    def on_completed(self) :
        self.target.formation.remove(self.owner)

#################################################

class TargetEnemyEscape ( TargetMove ) :

    def __init__(self, game, owner, object_class, menu_item, enemy):
        super().__init__(game, owner, object_class, enemy.x, enemy.y, menu_item)
        self.enemy = enemy
        self.chase_pos = None
        self.next_zigzag = -1

    def is_completed(self) :
        return self.owner.distance_to(self.enemy) > 5000 or self.enemy.dead

    def logic(self) :
        self.x = self.enemy.x
        self.y = self.enemy.y
        if self.game.get_time() > self.next_zigzag :
            print(f'{self.owner.name} TargetEnemyEscape zigzag')
            segment_len = random.randint(20,200)
            self.next_zigzag = self.game.get_time() + segment_len
            vector = pygame.Vector2(self.owner.x - self.enemy.x, self.owner.y - self.enemy.y)
            # Normalize the vector (make its length 1)
            vector.normalize_ip()
            vector = vector.rotate(random.randint(-60,60))
            # Scale it to the desired length (1000)
            vector.scale_to_length(5000)
            # Adding it to the original position to get the extended position
            self.chase_pos = (self.owner.x + vector.x, self.owner.y + vector.y)
        if self.game.get_time() % 50 == 0 :
            print(f'{self.owner.name} TargetEnemyEscape chase ({self.owner.x},{self.owner.y}) -> {self.chase_pos}')
        self.owner.chase( *self.chase_pos, False )

#################################################

class TargetGroup( Target ) :

    def __init__(self, game, stationary, owner, x, y, menu_item):
        super().__init__(game, stationary, x, y)
        self.owner = owner
        self.menu_item = menu_item
        self.visible = False
        self.completed = False
        self.suborders = {}
        self.weak = False

    def on_activate(self) :
        self.issue_orders()

    def make_order_for_ship( self, ship, x, y ) :
        return None

    def issue_orders(self) :
        center = self.owner.get_pos()
        target = pygame.Vector2(self.x,self.y)
        self.suborders = {}
        for ship in self.owner.ships :
            ship.add_on_dead_listener( self )
            offset = pygame.Vector2(ship.x - center[0], ship.y - center[1])
            ship_target = target + offset
            ship_order = self.make_order_for_ship( ship, *ship_target )
            if ship_order != None :
                ship.append_order( ship_order )
                self.suborders[ship] = ship_order

    def add_ship(self, ship) :
        ship.add_on_dead_listener( self )
        ship_order = TargetMove(self.game, ship, Stationary('move',32), self.x, self.y, self.menu_item)
        ship.append_order( ship_order )
        self.suborders[ship] = ship_order

    def remove_ship(self, ship) :
        ship.remove_on_read_listener( self )
        if ship in self.suborders :
            del self.suborders[ship]

    def on_dead(self, ship) :
        if ship in self.suborders :
            del self.suborders[ship]

    def on_deleted(self) :
        for ship, order in self.suborders.items() :
            ship.remove_order(order)

    def is_completed(self) :
        if self.completed == True :
            return True
        for ship, order in self.suborders.items() :
            if not order.is_completed() : 
                return False
        self.completed = True
        return True

#################################################

class TargetGroupMove( TargetGroup ) :

    def __init__(self, game, owner, x, y, menu_item):
        super().__init__(game, Stationary('mmove',32), owner, x, y, menu_item )

    def make_order_for_ship( self, ship, x, y ) :
        ship_order = TargetMove(self.game, ship, Stationary('move',32), x, y, self.menu_item)
        return ship_order


#################################################

class TargetGroupAttackMove( TargetGroup ) :

    def __init__(self, game, owner, x, y, menu_item, guarding_time = 0 ):
        super().__init__(game, 
            Stationary('mtarget',32) if guarding_time == 0 else Stationary('mprotect',32), 
            owner, x, y, menu_item )
        self.guarding_time = guarding_time

    def make_order_for_ship( self, ship, x, y ) :
        ship_order = TargetAttackMove(self.game, ship, 
            Stationary('target',32) if self.guarding_time == 0 else Stationary('protect',32), 
            x, y, self.menu_item, self.guarding_time)
        return ship_order

#################################################

class TargetGroupPatrolMove( TargetGroup ) :

    def __init__(self, game, owner, x, y, menu_item):
        super().__init__(game, Stationary('mpatrol',32), owner, x, y, menu_item )
        self.guarding_time = 0

    def make_order_for_ship( self, ship, x, y ) :
        ship_order = TargetAttackMove(self.game, ship, Stationary('patrol',32), x, y, self.menu_item, self.guarding_time)
        return ship_order

    def on_completed(self) :
        self.completed = False
        self.owner.append_order(self)
        if self.owner.get_order() == self : # single order
            self.owner.guarding_time = 500

#################################################

class TargetGroupEnemyEscape( TargetGroup ) :

    def __init__(self, game, owner, menu_item, target ) :
        super().__init__(game, Stationary('mescape',32), owner, target.x, target.y, menu_item )
        self.target = target

    def make_order_for_ship( self, ship, x, y ) :
        ship_order = TargetEnemyEscape(self.game, ship, Stationary('escape', 24), self.menu_item, self.target)
        return ship_order

