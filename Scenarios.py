
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
from AnimationObject import AnimationObject


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
            self.fire_next_event()

    def fire_next_event( self ) :
        if len(self.events) == 0 :
            return False
        for f in self.events[self.event_times[0]] :
            f()
        del self.events[self.event_times[0]]
        del self.event_times[0]
        return True

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
        self.stable = False
        self.current_frame_idx = None
        self.target_frame_idx = None
        self.animationOverlay = True
        # self.animate( self.game.get_animation('wormhole'), Wormhole.on_animation_finished )

    def on_animation_finished(self) :
        print("WORMHOLE on_animation_finished")
        self.animation = None

    def start_burst(self) :
        print(f'Wormohole> start_burst')
        
        size = random.uniform(0,1)

        if self.noises :
            zap_sound = pygame.mixer.Sound('assets/audio/electric-zap-made-with-Voicemod-technology.mp3')
            zap_sound.set_volume(0.2 + size*(0.8-0.2))
            zap_sound.play()

        self.animation = AnimatedSprite( "wormhole.png", 5, 6, int(32 + size*(256-32)), False )
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
        if self.active and not self.stable and self.animation == None and random.randint(0,200) < 1 :
            self.start_burst()
        elif self.stable and self.game.get_time() % 3 == 0:
            if self.animation == None :
                self.animation = AnimatedSprite( "wormhole.png", 5, 6, 64, False )
            if self.current_frame_idx == None :
                self.current_frame_idx = 0
            if self.target_frame_idx == None or self.target_frame_idx == self.current_frame_idx :
                self.target_frame_idx = random.randint(0,self.animation.get_frame_count()-1)
            self.animationFrame = self.animation.get_frame(self.current_frame_idx)
            if self.current_frame_idx < self.target_frame_idx :
                self.current_frame_idx += 1
            else :
                self.current_frame_idx -= 1
            if random.randint(0,100) < 10 :
                vip = self.game.get_screen_centerism( *self.get_pos() )
                if vip > 0 :
                    zap_sound = pygame.mixer.Sound('assets/audio/electric-zap-made-with-Voicemod-technology.mp3')
                    zap_sound.set_volume(vip/2)
                    zap_sound.play()
        super().ticktack()

    def animateNextFrame( self ) :
        self.animationFrame = self.animationOngoing.get_frame(self.animationFrameNo)
        self.animationFrameNo = int(( self.game.get_time() - self.animationStart ) // self.animationSpeed)
        if self.animationFrame == None :
            self.animationOngoing = None
            self.animationAfter(self)

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
        self.open_pages = []

    def start( self ) :
        # self.scene1()
        # self.scene2()
        self.scene6()

    def ticktack( self ) :
        if self.scene_no == 2 :
            self.ticktack2()
        elif self.scene_no == 6 :
            self.ticktack6()
        super().ticktack()        

    def on_key_pressed( self, key ) :
        if key == ' ' :
            if self.fire_next_event() :
                return True
            if self.scene_no == 1 :
                self.game.on_stop_request()
            elif self.scene_no == 3 :
                self.scene4()
            elif self.scene_no == 4 :
                self.scene5()
            elif self.scene_no == 5 :
                self.game.on_stop_request()
            elif self.scene_no == 7 :
                self.scene8()
            elif self.scene_no == 8 :
                self.scene9()
            elif self.scene_no == 9 :
                self.scene10()
            return True
        return False

    def scene1( self ) :
        self.scene_no = 1
        MusicPlayer.skip_to_song('alexander-nakarada-twin-explorers.mp3')

        cp = ComicPage(self.game, 'sc1_1', 450, 350, 680)
        self.game.add_object( cp )

        delay = 400

        self.at_time( 100, lambda : cp.add_text(
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
        self.wormhole_pos = (800,-800)
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

    def ticktack2( self ) :
        self.game.set_camera(self.science_ship.get_pos())
        if self.game.get_time() == self.start_chatter_time :
            chatter_sound = pygame.mixer.Sound('assets/audio/military-radio-communication-high-quality-sound-effect-made-with-Voicemod-technology.mp3')
            chatter_sound.set_volume(0.3)
            chatter_sound.play()
        if self.game.get_time() % 50 == 0 :
            if self.science_ship.distance_to_xy( *self.wormhole_pos ) < 700 :
                self.wormhole.noises = True
            if self.science_ship.distance_to_xy( *self.wormhole_pos ) < 50 :
                if self.wormhole.active :
                    self.wormhole.mega_burst()
                else :
                    self.scene3()

    def scene3(self) :
        self.scene_no = 3
        MusicPlayer.skip_to_song('darren-curtis-ignite-the-fire.mp3')        
        cp3 = ComicPage(self.game, 'sc1_2', 450, 350, 680)
        self.game.add_object( cp3 )


        self.at_time( self.game.get_time() + 100, 
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

        self.at_time( self.game.get_time() + 100, 
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

        self.at_time( self.game.get_time() + 100, 
            lambda : 
            cp5.add_text(
                "IN AN INSTANT, CHAOS ERUPTS.\nTHE FLASH MATERIALIZES, ANNIHILATING ALL BUT ONE SHIP.",
                (490,50)
            ) )

        self.at_time( self.game.get_time() + 1000,
            lambda :
            cp5.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (550, 690 )
                ) )

    def scene6(self) :
        self.scene_no = 6
        MusicPlayer.skip_to_song("darren-curtis-the-ascension.mp3")

        self.reset_game( Game(self.input_handler, self.win) )
        self.input_handler.set_game( self.game )
        self.game.register_key_handler(' ', self)
        self.background = DistantObject(self.game, Background( 2 ), 0, 0)
        self.game.add_object(self.background)
        self.game.add_ticktack_receiver(self)
        # self.game.register_key_handler(' ', self)
        self.game.zoom_enabled = False
        self.input_handler.control_enabled = False
        self.wormhole_pos = (-1000,1000)
        self.target_position = (-500,500)
        self.game.set_camera(self.wormhole_pos)
        #self.wormhole_pos = (400,-400)

        Dust.make_dust(self.game, 1)

        self.team_blue = Team( "Blue", (0,0,255), 2, 0, self )

        self.player_ship = Starship(self.game, self.team_blue, ScoutClass(), ScoutPilot(self.game), -1000, 1000 )
        self.game.add_object( self.player_ship )

        planet = StationaryObject(self.game, Stationary("planet_7", 48), 1000, -1000)
        planet.layer = 1
        self.game.add_object( planet )

        self.wormhole = Wormhole(self.game, *self.wormhole_pos)
        self.game.add_object( self.wormhole )
        self.wormhole.stable = True

        self.game.paused = False

        self.start_time = self.game.get_time()
        self.ps_rotation_speed = 5
        self.starting_sequence_length = 500
        self.explosion_probability = 3

        self.game.game_loop()
   
    def ticktack6( self ) :
        self.player_ship.dir = ( self.player_ship.dir + self.ps_rotation_speed ) % 360
        self.ps_rotation_speed = self.game.approach_value( self.ps_rotation_speed, 0, self.starting_sequence_length )
        self.player_ship.x = self.game.approach_value( self.player_ship.x, self.target_position[0], self.starting_sequence_length)
        self.player_ship.y = self.game.approach_value( self.player_ship.y, self.target_position[1], self.starting_sequence_length)
        self.game.set_camera( self.player_ship.get_pos() )
        self.explosion_probability = self.game.approach_value( self.explosion_probability, 0, self.starting_sequence_length )
        if self.game.get_time() < self.starting_sequence_length and random.randint(0,100) < self.explosion_probability :
            p = random.uniform(0,1)
            size = 16 + int(p * (96-16))
            AnimationObject( 
                self.game, 
                *self.player_ship.get_pos(), 
                self.game.get_animation('explosion'),
                size )
            explosion_sound = pygame.mixer.Sound('assets/audio/explosion-roblox-made-with-Voicemod-technology.mp3')
            explosion_sound.set_volume( p/2 )
            explosion_sound.play()
        if self.game.get_time() > self.starting_sequence_length :
            self.scene7()

    def scene7(self):
        self.scene_no = 7

        cp7 = ComicPage(self.game, 'sc1_5', 440, 360, 700)
        self.open_pages.append( cp7 )

        self.game.add_object( cp7 )

        self.at_time( self.game.get_time() + 100, 
            lambda : 
            cp7.add_speech(
                "ALL HANDS, BRACE FOR IMPACT!\nYOU, THE CO-PILOT, TAKE THE CONTROLS!",
                (290,450),
                (500,600)
            ) )

        self.at_time( self.game.get_time() + 1000,
            lambda :
            cp7.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (550, 690 )
                ) )


    def scene8(self):
        self.scene_no = 8

        cp8 = ComicPage(self.game, 'sc1_6', 460, 370, 700)
        self.open_pages.append( cp8 )

        self.game.add_object( cp8 )

        self.at_time( self.game.get_time() + 100, 
            lambda : 
            cp8.add_text(
                "ALONE AND UNPREPARED, THE CO-PILOT MUST NOW GUIDE THE SHIP HOME.",
                (490,50),
            ) )

        self.at_time( self.game.get_time() + 300,
            lambda :
            cp8.add_text(
"""USE THE ARROW KEYS TO NAVIGATE YOUR SHIP.
THE UP KEY ACCELERATES, THE DOWN KEY DECELERATES.
USE THE LEFT AND RIGHT KEYS TO STEER YOUR SHIP.
QUICK, STEADY MOVEMENTS WILL KEEP YOU ON COURSE.""",
                (950,150)
            ) )

        self.at_time( self.game.get_time() + 600,
            lambda :
            cp8.add_text(
                "NOW, IT'S TIME TO TAKE CONTROL AND STEER THE SHIP TO SAFETY.",
                (960,260)
            ) )

    def scene9(self):
        self.scene_no = 9

        cp9 = ComicPage(self.game, 'sc1_7', 470, 360, 680)
        self.open_pages.append( cp9 )
        self.game.add_object( cp9 )

        self.at_time( self.game.get_time() + 100, 
            lambda : 
            cp9.add_text(
                "A JOURNEY BEGINS, A MYSTERY UNFOLDS. WHAT WAS THE FLASH? AND WHAT LIES AHEAD?",
                (490,650),
            ) )

        self.at_time( self.game.get_time() + 1000,
            lambda :
            cp9.add_text(
                "WHEN YOU'RE READY, PRESS SPACE TO CONTINUE.",
                (550, 690 )
                ) )

    def scene10( self ) :
        for page in self.open_pages :
            page.on_stop_request()
        self.game.set_focused(self.player_ship)
        self.game.zoom_locked = None
        self.input_handler.control_enabled = True




