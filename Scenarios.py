
import bisect
import random
import pygame

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
from MusicPlayer import MusicPlayer


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
        self.active = True
        self.noises = False
        # self.animate( self.game.get_animation('wormhole'), Wormhole.on_animation_finished )

    def on_animation_finished(self) :
        self.animation = None

    def start_burst(self) :
        print(f'Wormohole> start_burst')
        
        if self.noises :
            zap_sound = pygame.mixer.Sound('assets/audio/electric-zap-made-with-Voicemod-technology.mp3')
            zap_sound.set_volume(random.uniform(0.2,0.8))
            zap_sound.play()

        self.animation = AnimatedSprite( "wormhole.png", 5, 6, random.randint(32,256), False )
        self.animate( self.animation, Wormhole.on_animation_finished, random.uniform(0.5, 3) )

    def mega_burst(self) :

        if self.noises :
            zap_sound = pygame.mixer.Sound('assets/audio/electric-zap-made-with-Voicemod-technology.mp3')
            zap_sound.set_volume(1)
            zap_sound.play()

        self.animation = AnimatedSprite( "wormhole.png", 5, 6, 320, False )
        self.animate( self.animation, Wormhole.on_animation_finished, 1.5 )
        self.active = False


    def ticktack(self) :
        if self.active and self.animation == None and random.randint(0,200) < 1 :
            self.start_burst()
        super().ticktack()

#################################################

class Scenario1 ( Scenario ) :

    def __init__( self, win ) :
        self.input_handler = InputHandler()
        super().__init__( Comic(self, self.input_handler, win), win )
        self.input_handler.set_game( self.game )
        self.game.register_key_handler(' ', self)
        self.background = DistantObject(self.game, Background( 1 ), 0, 0)
        self.game.add_object(self.background)
        Dust.make_dust(self.game, 1)
        self.science_ship = None
        self.scene_no = 1

    def start( self ) :
        self.scene1()
        self.scene2()

    def on_key_pressed( self, key ) :
        if key == ' ' :
            if self.scene_no == 1 :
                self.game.on_stop_request()
            elif self.scene_no == 3 :
                self.scene4()
            elif self.scene_no == 4 :
                self.scene5()
            return True
        return False

    def scene1( self ) :
        self.scene_no = 1
        cp = ComicPage(self.game, 'sc1_1', 450, 350, 680)
        self.game.add_object( cp )

        delay = 400

        self.at_time( 150, lambda : cp.add_text(
            """IN A KNOWN SOLAR SYSTEM, WHERE PATHS ARE WELL-CHARTED
            A SCOUTING MISSION EMBARKS TO INVESTIGATE AN ENIGMATIC COSMIC FLASH ...""", 
            (700, 100 )
            ) )
        self.at_time( 150 + delay, lambda : cp.add_text(
            """AS A CO-PILOT INTERN ON A SCOUT SHIP, YOU ARE PART OF A SMALL FLEET
            COMPOSED OF ONE SCIENTIFIC VESSEL, TWO EXPLORATORY SCOUTS, AND AN ESCORT FIGHTER ...""", 
            (620, 160 )
            ) )
        self.at_time( 150 + 2*delay, lambda : cp.add_text(
            "YOUR MISSION: TO INVESTIGATE THE OCCURRENCE OF AN ENIGMATIC COSMIC FLASH ...",
            (720, 220 )
            ) )
        self.at_time( 150 + 3*delay, lambda : cp.add_text(
            "YOUR JOURNEY INTO THE UNKNOWN IS ABOUT TO BEGIN ...",
            (750, 270 )
            ) )
        self.at_time( 150 + 4*delay, lambda : cp.add_text(
            "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
            (900, 580 )
            ) )

        self.game.game_loop()

    def scene2( self ) :
        self.scene_no = 2
        MusicPlayer.skip_to_song('hayden-folker-going-home.mp3')

        self.reset_game( Game(self.input_handler, self.win) )
        self.input_handler.set_game( self.game )
        self.background = DistantObject(self.game, Background( 1 ), 0, 0)
        self.game.add_object(self.background)
        self.game.add_ticktack_receiver(self)
        self.game.register_key_handler(' ', self)
        self.game.zoom_enabled = False
        self.input_handler.control_enabled = False
        self.wormhole_pos = (1000,-1000)
        #self.wormhole_pos = (400,-400)

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
        planet.layer = 1
        self.game.add_object( planet )

        self.wormhole = Wormhole(self.game, *self.wormhole_pos)
        self.game.add_object( self.wormhole )

        self.explorer_group.order_guard( *self.wormhole_pos )

        self.game.paused = False
        self.start_chatter_time = self.game.get_time() + 500

        self.game.game_loop()

    def ticktack( self ) :
        if self.scene_no == 2 :
            self.game.optimal_fieldview.center = self.science_ship.get_pos()
            self.game.optimal_camera = self.science_ship.get_pos()
            self.game.camera[0] = self.game.optimal_camera[0]
            self.game.camera[1] = self.game.optimal_camera[1]
            self.game.zoom_locked = self.game.get_time() + 1000
            if self.game.get_time() == self.start_chatter_time :
                # Load the sound effect
                print("START CHATTER")
                chatter_sound = pygame.mixer.Sound('assets/audio/military-radio-communication-high-quality-sound-effect-made-with-Voicemod-technology.mp3')
                chatter_sound.set_volume(0.5)
                # Play the sound effect
                chatter_sound.play()
            if self.game.get_time() % 50 == 0 :
                if self.science_ship.distance_to_xy( *self.wormhole_pos ) < 500 :
                    self.wormhole.noises = True
                if self.science_ship.distance_to_xy( *self.wormhole_pos ) < 50 :
                    if self.wormhole.active :
                        self.wormhole.mega_burst()
                    else :
                        self.scene3()
        super().ticktack()

    def scene3(self) :
        self.scene_no = 3
        MusicPlayer.skip_to_song('darren-curtis-ignite-the-fire.mp3')        
        cp3 = ComicPage(self.game, 'sc1_2', 450, 350, 680)
        self.game.add_object( cp3 )


        self.at_time( self.game.get_time() + 150, 
            lambda : 
            cp3.add_speech(
                "PREPARE FOR ANALYSIS, CREW.\nTHAT FLASH IS UNLIKE ANYTHING WE'VE SEEN.",
                (550,250),
                (400,400)
            ) )

        self.at_time( self.game.get_time() + 1000,
            lambda :
            cp3.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (450, 680 )
                ) )

    def scene4(self):
        self.scene_no = 4

        cp4 = ComicPage(self.game, 'sc1_3', 490, 390, 630)
        self.game.add_object( cp4 )

        self.at_time( self.game.get_time() + 150, 
            lambda : 
            cp4.add_text(
                "AS THE FLEET NEARS THE PHENOMENON, TENSION MOUNTS.\nSOMETHING DOESN'T FEEL RIGHT.",
                (470,100)
            ) )

        self.at_time( self.game.get_time() + 1000,
            lambda :
            cp4.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (450, 680 )
                ) )

    def scene5(self):
        self.scene_no = 5

        explosion_sound = pygame.mixer.Sound('assets/audio/big-explosion-sound-effect-made-with-Voicemod-technology.mp3')
        explosion_sound.play()

        cp5 = ComicPage(self.game, 'sc1_4', 440, 360, 700)
        self.game.add_object( cp5 )

        self.at_time( self.game.get_time() + 150, 
            lambda : 
            cp5.add_text(
                "IN AN INSTANT, CHAOS ERUPTS.\nTHE FLASH MATERIALIZES, ANNIHILATING ALL BUT ONE SHIP.",
                (490,50)
            ) )

        self.at_time( self.game.get_time() + 200,
            lambda :
            cp5.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (550, 690 )
                ) )


        


