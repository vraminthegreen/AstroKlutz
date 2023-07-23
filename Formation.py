import pygame
import math

from StarObject import StarObject


class Formation :

    GUARD_POS = [(-120,0),(-100,-50),(-100,50),(100,-70),(100,70),(0,-100),(0,100)]
    FOLLOW_POS = [(-120,0),(-100,-50),(-100,50),
        (-150,-30),(-150,30),(-150,-100),(-150,100),
        (-200,-30),(-200,30),(-200,-100),(-200,100),
        (-250,-30),(-250,30),(-250,-100),(-250,100),
        (-300,-30),(-300,30),(-300,-100),(-300,100),
        ]

    def __init__(self, target) :
        self.target = target
        self.followers = []
        self.guards = []
        self.positions = {}

    def add_follower(self, ship) :
        self.followers.append(ship)
        self.reassign_followers()

    def add_guard(self, ship) :
        self.guards.append(ship)
        self.reassign_guards()
        self.reassign_followers()

    def remove(self, ship) :
        if ship in self.followers :
            self.followers.remove(ship)
            self.reassign_followers()
        elif ship in self.guards :
            self.guards.remove(ship)
            self.reassign_guards()
            self.reassign_followers()

    def reassign_guards(self) :
        for i, ship in enumerate(self.guards) :
            if i < len(Formation.GUARD_POS) :
                self.positions[ship] = Formation.GUARD_POS[i]
            else :
                self.positions[ship] = Formation.FOLLOW_POS[i-4] # 3 first positions are common for followers and guards

    def reassign_followers(self) :
        if len(self.guards) > 0 :
            last_guard_pos = self.positions[self.guards[-1]]     
            if last_guard_pos in Formation.FOLLOW_POS :
                index = Formation.FOLLOW_POS.index(last_guard_pos) + 1
            else :
                index = 4
        else :
            index = 0
        for ship in self.followers :
            self.positions[ship] = self.FOLLOW_POS[index]
            index += 1
            if index >= len(self.FOLLOW_POS) : return

    def get_optimal_pos(self, ship) :
        # Assume self.target.dir is in degrees. Convert it to radians.
        #angle_rad = math.radians(self.target.dir)        
        # Create the displacement vector.
        displacement = pygame.Vector2(*self.positions[ship])
        print(f'displacement: {displacement}')
        # Rotate the displacement vector.
        displacement = displacement.rotate(self.target.dir)
        print(f'displacement rotated: {displacement}')
        # Add the rotated displacement to the original position to get the new position.
        new_pos = pygame.Vector2(self.target.x, self.target.y) + displacement
        print(f'new_pos: {new_pos}')
        return new_pos

