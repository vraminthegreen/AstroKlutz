
import pygame

from StarObject import StarObject

#################################################

class TargetMove ( StarObject ) :

    def __init__(self, game, object_class, x, y, menu_item):
    	StarObject.__init__(self, game, object_class, x, y)
    	self.menu_item = menu_item

    def is_completed(self, starship) :
    	target_vector =  pygame.Vector2(self.x, self.y) - pygame.Vector2(starship.x, starship.y)
    	distance_to_target = target_vector.length()
    	# print(f'distance_to_target: {distance_to_target}')
    	return distance_to_target < 25

    def get_vmax(self, starship) :
    	return starship.maxV
 
#################################################

class TargetAttack ( TargetMove ) :

    def get_vmax(self, starship) :
    	return 0.5 * starship.maxV

#################################################
