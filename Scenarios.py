
import bisect
import random

from Targets import TargetAttackMove
from ShipClass import Stationary
from Team import Team
from Starship import Starship
from Pilot import Pilot, FighterPilot, RocketFrigatePilot, ScoutPilot, SciencePilot
from ShipClass import FighterClass, RocketFrigateClass, ScoutClass, ScienceClass
from Group import Group
from Game import Game
from Comic import Comic
from StarObject import StarObject
from InputHandler import InputHandler
from Missile import Missile
from Dust import Dust
from DistantObject import DistantObject
from StationaryObject import StationaryObject
from ShipClass import Stationary, Background
from ComicPage import ComicPage
from AnimatedSprite import AnimatedSprite


#################################################

class Scenario :

    def __init__( self, game, win ) :
        self.win = win
        self.reset_game( game )

    def reset_game( self, game ) :
        self.game = game
        self.game.add_ticktack_receiver(self)
        self.event_times = []
        self.events = {}

    def get_order( self, ship ) :
        return None

    def at_time( self, time, f ) :
        if time in self.events :
            self.events[time].append(f)
        else :
            self.events[time] = [ f ]
        bisect.insort( self.event_times, time )

    def ticktack( self ) :
        while len(self.event_times) > 0 and self.event_times[0] < self.game.get_time() :
            for f in self.events[self.event_times[0]] :
                f()
            del self.events[self.event_times[0]]
            del self.event_times[0]

    def on_stop_request(self) :
        pass

#################################################

class BasicScenario ( Scenario ) :

    def __init__( self, win ) :
        self.input_handler = InputHandler()
        super().__init__( Game(self.input_handler, win), win )
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

class Wormhole ( StationaryObject ) :

    def __init__( self, game, x, y ) :
        super().__init__(game, Stationary(None,96), x, y)
        # self.sprite = AnimatedSprite( "wormhole.png", 6, 6, 96, False )
        self.animation = None
        # self.animate( self.game.get_animation('wormhole'), Wormhole.on_animation_finished )

    def on_animation_finished(self) :
        self.animation = None

    def start_burst(self) :
        print(f'Wormohole> start_burst')
        self.animation = AnimatedSprite( "wormhole.png", 5, 6, random.randint(32,256), False )
        self.animate( self.animation, Wormhole.on_animation_finished, random.uniform(0.5, 3) )

    def ticktack(self) :
        if self.animation == None and random.randint(0,2000) < 1 :
            self.start_burst()
        super().ticktack()

#################################################

class Scenario1 ( Scenario ) :

    def __init__( self, win ) :
        self.input_handler = InputHandler()
        super().__init__( Comic(self, self.input_handler, win), win )
        self.input_handler.set_game( self.game )
        self.background = DistantObject(self.game, Background( 1 ), 0, 0)
        self.game.add_object(self.background)
        Dust.make_dust(self.game, 1)
        self.pages = []
        self.science_ship = None

    def start( self ) :
        self.scene1()
        self.scene2()

    def command( self, command ) :
        if command == ' ' :
            self.game.on_stop_request()

    def scene1( self ) :
        cp = ComicPage(self.game, 'sc1_1', 450, 350, 680)
        self.game.add_object( cp )
        self.pages.append( cp )

        delay = 400

        self.at_time( 150, lambda : cp.add_text(
            """IN A KNOWN SOLAR SYSTEM, WHERE PATHS ARE WELL-CHARTED
            A SCOUTING MISSION EMBARKS TO INVESTIGATE AN ENIGMATIC COSMIC FLASH ...""", 
            400, 100 
            ) )
        self.at_time( 150 + delay, lambda : cp.add_text(
            """AS A CO-PILOT INTERN ON A SCOUT SHIP, YOU ARE PART OF A SMALL FLEET
            COMPOSED OF ONE SCIENTIFIC VESSEL, TWO EXPLORATORY SCOUTS, AND AN ESCORT FIGHTER ...""", 
            320, 160 
            ) )
        self.at_time( 150 + 2*delay, lambda : cp.add_text(
            "YOUR MISSION: TO INVESTIGATE THE OCCURRENCE OF AN ENIGMATIC COSMIC FLASH ...",
            420, 220 
            ) )
        self.at_time( 150 + 3*delay, lambda : cp.add_text(
            "YOUR JOURNEY INTO THE UNKNOWN IS ABOUT TO BEGIN ...",
            370, 270 
            ) )
        self.at_time( 150 + 4*delay, lambda : cp.add_text(
            "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
            650, 480 
            ) )

        self.game.game_loop()

    def scene2( self ) :

        self.reset_game( Game(self.input_handler, self.win) )
        self.input_handler.set_game( self.game )
        self.background = DistantObject(self.game, Background( 1 ), 0, 0)
        self.game.add_object(self.background)
        self.game.add_ticktack_receiver(self)
        self.game.zoom_enabled = False
        self.input_handler.control_enabled = False

        Dust.make_dust(self.game, 1)

        self.team_blue = Team( "Blue", (0,0,255), 2, 0, self )

        self.explorer_group = Group(self.game, self.team_blue)

        sc = Starship(self.game, self.team_blue, ScoutClass(), ScoutPilot(self.game), -400, 190 )
        sc.dir = 45
        sc.maxV = 1.2
        self.game.add_object( sc )
        self.explorer_group.add_ship( sc )
        sc = Starship(self.game, self.team_blue, ScoutClass(), ScoutPilot(self.game), -300, 290 )
        sc.dir = 45
        sc.maxV = 1.2
        self.game.add_object( sc )
        self.explorer_group.add_ship( sc )
        sc = Starship(self.game, self.team_blue, FighterClass(), FighterPilot(self.game), -300, 190 )
        sc.dir = 45
        sc.maxV = 1.2
        self.game.add_object( sc )
        self.explorer_group.add_ship( sc )
        sc = Starship(self.game, self.team_blue, ScienceClass(), SciencePilot(self.game), -400, 290 )
        sc.dir = 45
        sc.maxV = 1.2
        self.science_ship = sc
        self.game.add_object( sc )
        self.explorer_group.add_ship( sc )

        self.game.add_object( self.explorer_group )

        planet = StationaryObject(self.game, Stationary("planet_1", 64), -420, 240)
        self.game.add_object( planet )

        wormhole = Wormhole(self.game, 2000, -2000)
        self.game.add_object( wormhole )

        self.explorer_group.order_guard( 2000, -2000 )

        self.game.paused = False

        self.game.game_loop()

    def ticktack( self ) :
        if self.science_ship != None :
            print(f'science_ship pos: {self.science_ship.get_pos()}')
            self.game.optimal_fieldview.center = self.science_ship.get_pos()
            self.game.optimal_camera = self.science_ship.get_pos()
            self.game.camera[0] = self.game.optimal_camera[0]
            self.game.camera[1] = self.game.optimal_camera[1]
            self.game.zoom_locked = self.game.get_time() + 1000
        super().ticktack()


