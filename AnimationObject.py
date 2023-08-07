
from StarObject import StarObject
from ShipClass import Stationary
from AnimatedSprite import AnimatedSprite


class AnimationObject ( StarObject ) :

    def __init__(self, game, x, y, animation, size ) :
        super().__init__(game, Stationary(None, size), x, y)
        self.animation = AnimatedSprite( "explosion.png", 8, 6, size, False )
        self.game.add_object( self )
        self.animate( self.animation, AnimationObject.on_animation_finished )

    def on_animation_finished( self ) :
        self.game.remove_object( self )


