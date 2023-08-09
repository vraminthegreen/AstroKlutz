
import math

from StarObject import StarObject
from ShipClass import Stationary
from AnimatedSprite import AnimatedSprite


class DirectionObject ( StarObject ) :

    def __init__(self, game, src_object, trg_object ) :
        super().__init__(game, Stationary(None, 48), src_object.x, src_object.y)
        self.src_object = src_object
        self.trg_object = trg_object
        self.animation = AnimatedSprite( "arrow.png", 10, 10, 48, False )
        self.game.add_object( self )
        self.recalc_pos()
        self.start_animation()
        self.animation_count = 5

    def ticktack(self) :
    	self.recalc_pos()
    	super().ticktack()

    def recalc_pos(self) :
    	self.dir = self.src_object.get_display_direction_to(self.trg_object)
    	distance = self.src_object.size + 30 + math.sin(self.game.get_time()/10) * 20
    	(self.x, self.y) = self.src_object.get_displaced_pos(self.dir, distance)

    def start_animation(self) :
        self.animate( self.animation, DirectionObject.on_animation_finished )

    def on_animation_finished( self ) :
    	self.animation_count -= 1
    	if self.animation_count > 0 :
    		self.start_animation()
    	else :
        	self.game.remove_object( self )


