

from Targets import TargetAttackMove
from ShipClass import Stationary



#################################################

class Scenario :

    def __init__( self, game ) :
        self.game = game

    def get_order( self, ship ) :
        return None

#################################################

class BasicScenario ( Scenario ) :

    def get_order( self, ship ) :
        order = TargetAttackMove( self.game, ship, Stationary('protect', 32), ship.x, ship.y, None, 500 )
        order.weak = True
        print(f'New weak order for {ship.name} -> guard ({ship.x},{ship.y})')
        return order

#################################################
