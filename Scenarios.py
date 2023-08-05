

from Targets import TargetAttackMove
from ShipClass import Stationary
from Team import Team
from Starship import Starship
from Pilot import Pilot, FighterPilot, RocketFrigatePilot
from ShipClass import FighterClass, RocketFrigateClass
from Group import Group
from Game import Game
from Comic import Comic
from StarObject import StarObject
from InputHandler import InputHandler
from Missile import Missile
from Dust import Dust
from DistantObject import DistantObject
from ShipClass import Stationary, Background


#################################################

class Scenario :

    def __init__( self ) :
        self.game = game

    def get_order( self, ship ) :
        return None

#################################################

class BasicScenario ( Scenario ) :

    def __init__( self ) :
        self.input_handler = InputHandler()
        self.game = Game(self.input_handler)
        self.input_handler.set_game( self.game )
        self.background = DistantObject(self.game, Background(), 0, 0)
        self.game.add_object(self.background)
        Dust.make_dust(self.game, 1)

    def get_order( self, ship ) :
        order = TargetAttackMove( self.game, ship, Stationary('protect', 32), ship.x, ship.y, None, 500 )
        order.weak = True
        print(f'New weak order for {ship.name} -> guard ({ship.x},{ship.y})')
        return order

    def start( self ) :
        self.friends = []
        self.enemies = []
        self.team_red = Team( "Red", (255,0,0), 1, 1, self )
        self.team_blue = Team( "Blue", (0,0,255), 2, 0, self )
        self.team_green = Team( "Green", (0,255,0), 3, 0, self )
        self.team_yellow = Team( "Yellow", (255,255,0), 4, 1, self )

        top = -320
        spac = 72

        self.friend_group_fighters = Group(self.game, self.team_blue)
        self.game.add_object(self.friend_group_fighters)
        self.friend_group_frigates = Group(self.game, self.team_blue)
        self.game.add_object(self.friend_group_frigates)
        self.enemy_group = Group(self.game, self.team_red)
        self.game.add_object(self.enemy_group)

        for i in range(0,10) :
            sb = Starship(self.game, self.team_blue, FighterClass(), FighterPilot(self.game), -400, top + spac*i )
            sr = Starship(self.game, self.team_red, FighterClass(), FighterPilot(self.game), 400, top + spac*i )
            self.game.add_object(sb)
            self.friend_group_fighters.add_ship( sb )
            self.game.add_object(sr)
            self.enemy_group.add_ship( sr )
            sr.dir = 180
            sb = Starship(self.game, self.team_blue, FighterClass(), FighterPilot(self.game), -350, top + spac*i )
            sr = Starship(self.game, self.team_red, FighterClass(), FighterPilot(self.game), 350, top + spac*i )
            self.game.add_object(sb)
            self.friend_group_fighters.add_ship( sb )
            self.game.add_object(sr)
            self.enemy_group.add_ship( sr )
            sr.dir = 180
            sb = Starship(self.game, self.team_blue, RocketFrigateClass(), RocketFrigatePilot(self.game), -470, top + spac*i )
            sr = Starship(self.game, self.team_red, RocketFrigateClass(), RocketFrigatePilot(self.game), 470, top + spac*i )
            self.game.add_object(sb)
            self.friend_group_frigates.add_ship( sb )
            self.game.add_object(sr)
            self.enemy_group.add_ship( sr )
            sr.dir = 180

        self.enemy_group.order_guard( -350, 0 )
        self.friend_group_fighters.order_guard( 350, 0 )
        self.friend_group_frigates.order_guard( 350, 0 )
        self.enemy_group.order_guard( 350, 0 )
        self.friend_group_fighters.order_guard( -350, 0 )
        self.friend_group_frigates.order_guard( -350, 0 )

        self.game.game_loop()

#################################################

class Scenario1 ( Scenario ) :

    def __init__( self ) :
        self.input_handler = InputHandler()
        self.game = Comic(self.input_handler)
        self.input_handler.set_game( self.game )
        self.background = DistantObject(self.game, Background(), 0, 0)
        self.game.add_object(self.background)
        Dust.make_dust(self.game, 1)

    def start( self ) :
        self.game.game_loop()


