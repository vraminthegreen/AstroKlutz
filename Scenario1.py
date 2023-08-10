
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
from DirectionObject import DirectionObject
from Scenarios import Scenario, Wormhole
from Scenario2 import Scenario2
from Group import Group


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
        self.liora = None

    def start( self ) :
        self.scene1()
        self.scene2()
        self.scene6()

    def ticktack( self ) :
        if self.scene_no == 2 :
            self.ticktack2()
        elif self.scene_no == 6 :
            self.ticktack6()
        elif self.scene_no == 10 :
            self.ticktack10()
        super().ticktack()        

    def on_key_pressed( self, key ) :
        if key == ' ' :
            self.fire_next_dlg_event()
            return True
        return False

    def scene1( self ) :
        print("SCENE1 start")
        self.scene_no = 1
        MusicPlayer.skip_to_song('alexander-nakarada-twin-explorers.mp3')

        cp = ComicPage(self.game, 'sc1_1', 450, 350, 680)
        self.game.add_object( cp )

        delay = 400

        self.dlg_at_time( self.game.get_time() + 100, lambda : cp.add_text(
            """IN A KNOWN SOLAR SYSTEM, WHERE PATHS ARE WELL-CHARTED
            A SCOUTING MISSION EMBARKS TO INVESTIGATE AN ENIGMATIC COSMIC FLASH ...""", 
            (700, 100 )
            ) )
        self.dlg_at_time( self.game.get_time() + delay, lambda : cp.add_text(
            """AS A CO-PILOT INTERN ON A SCOUT SHIP, YOU ARE PART OF A SMALL FLEET
            COMPOSED OF ONE SCIENTIFIC VESSEL, TWO EXPLORATORY SCOUTS, AND AN ESCORT FIGHTER ...""", 
            (620, 160 )
            ) )
        self.dlg_at_time( self.game.get_time() + 2*delay, lambda : cp.add_text(
            "YOUR MISSION: TO INVESTIGATE THE OCCURRENCE OF AN ENIGMATIC COSMIC FLASH ...",
            (720, 220 )
            ) )
        self.dlg_at_time( self.game.get_time() + 3*delay, lambda : cp.add_text(
            "YOUR JOURNEY INTO THE UNKNOWN IS ABOUT TO BEGIN ...",
            (750, 270 )
            ) )
        self.dlg_at_time( self.game.get_time() + 4*delay, lambda : cp.add_text(
            "USE THE [SPACE] KEY TO ADVANCE TO THE NEXT DIALOGUE OR SCENE AT ANY TIME.",
            (900, 580 )
            ) )
        self.dlg_at_time( self.game.get_time() + 10000, self.game.on_stop_request )

        self.game.game_loop()

    def scene2( self ) :
        print("SCENE2 start")        
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
        self.game.set_team(self.team_blue, Group(self.game, self.team_blue, 0))

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

        self.at_time( self.game.get_time() + 600, self.liora_in )
        self.at_time( self.game.get_time() + 650, lambda: 
            self.agent_says( self.liora, "HELLO, PILOT.\nI'M DR. LIORA CALYX, YOUR CHIEF SCIENCE OFFICER." ) )
        self.at_time( self.game.get_time() + 950, lambda: 
            self.agent_says( self.liora, "WE'RE HEADED TOWARDS THIS COSMIC FLASH,\nAN ANOMALY UNLIKE ANYTHING WE'VE SEEN." ) )
        self.at_time( self.game.get_time() + 1250, lambda: 
            self.agent_says( self.liora, "I'LL BE GUIDING YOU THROUGH THE SCIENTIFIC ASPECTS OF OUR MISSION." ) )
        self.at_time( self.game.get_time() + 1550, lambda: 
            self.agent_says( self.liora, "STAY ALERT AND TRUST IN OUR COLLECTIVE EXPERTISE." ) )
        self.at_time( self.game.get_time() + 1800, self.liora_out )

        self.game.game_loop()

    def ticktack2( self ) :
        self.game.set_camera(self.science_ship.get_pos())
        if self.game.get_time() == self.start_chatter_time :
            chatter_sound = pygame.mixer.Sound('assets/audio/military-radio-communication-high-quality-sound-effect-made-with-Voicemod-technology.mp3')
            chatter_sound.set_volume(0.3)
            chatter_sound.play()
        if self.game.get_time() % 50 == 0 :
            if self.science_ship.disp_distance_to( self.wormhole ) < 700 :
                self.wormhole.noises = True
            if self.science_ship.disp_distance_to( self.wormhole ) < 50 :
                if self.wormhole.active :
                    self.wormhole.mega_burst()
                else :
                    self.scene3()

    def scene3(self) :
        print("SCENE3 start")        
        self.scene_no = 3
        MusicPlayer.skip_to_song('darren-curtis-ignite-the-fire.mp3')        
        cp3 = ComicPage(self.game, 'sc1_2', 450, 350, 680)
        self.game.add_object( cp3 )


        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp3.add_speech(
                "PREPARE FOR ANALYSIS, CREW.\nTHAT FLASH IS UNLIKE ANYTHING WE'VE SEEN.",
                (550,250),
                (400,400)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene4 )

    def scene4(self):
        print("SCENE4 start")
        self.scene_no = 4

        cp4 = ComicPage(self.game, 'sc1_3', 490, 390, 630)
        self.game.add_object( cp4 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp4.add_text(
                "AS THE FLEET NEARS THE PHENOMENON, TENSION MOUNTS.\nSOMETHING DOESN'T FEEL RIGHT.",
                (470,100)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene5 )


    def scene5(self):
        print("SCENE5 start")        
        self.scene_no = 5

        explosion_sound = pygame.mixer.Sound('assets/audio/big-explosion-sound-effect-made-with-Voicemod-technology.mp3')
        explosion_sound.play()

        cp5 = ComicPage(self.game, 'sc1_4', 440, 360, 700)
        self.game.add_object( cp5 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp5.add_text(
                "IN AN INSTANT, CHAOS ERUPTS.\nTHE FLASH MATERIALIZES, ANNIHILATING ALL BUT ONE SHIP.",
                (490,50)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.game.on_stop_request )

    def scene6(self) :
        print("SCENE6 start")        
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
        self.game.set_team(self.team_blue, Group(self.game, self.team_blue, 0))


        self.player_ship = Starship(self.game, self.team_blue, ScoutClass(), ScoutPilot(self.game), -1000, 1000 )
        self.game.add_object( self.player_ship )

        self.planet = StationaryObject(self.game, Stationary("planet_7", 48), 1000, -1000)
        self.planet.layer = 1
        self.game.add_object( self.planet )

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
        print("SCENE7 start")        
        self.scene_no = 7

        cp7 = ComicPage(self.game, 'sc1_5', 440, 360, 700)
        self.open_pages.append( cp7 )

        self.game.add_object( cp7 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp7.add_speech(
                "ALL HANDS, BRACE FOR IMPACT!\nYOU, THE CO-PILOT, TAKE THE CONTROLS!",
                (290,450),
                (500,600)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene8 )


    def scene8(self):
        print("SCENE8 start")        
        self.scene_no = 8

        cp8 = ComicPage(self.game, 'sc1_6', 460, 370, 700)
        self.open_pages.append( cp8 )

        self.game.add_object( cp8 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp8.add_text(
                "ALONE AND UNPREPARED, THE CO-PILOT MUST NOW GUIDE THE SHIP HOME.",
                (490,50),
            ) )

        self.dlg_at_time( self.game.get_time() + 300,
            lambda :
            cp8.add_text(
"""USE THE ARROW KEYS TO NAVIGATE YOUR SHIP.
THE UP KEY ACCELERATES, THE DOWN KEY DECELERATES.
USE THE LEFT AND RIGHT KEYS TO STEER YOUR SHIP.
QUICK, STEADY MOVEMENTS WILL KEEP YOU ON COURSE.""",
                (950,150)
            ) )

        self.dlg_at_time( self.game.get_time() + 600,
            lambda :
            cp8.add_text(
                "NOW, IT'S TIME TO TAKE CONTROL AND STEER THE SHIP TO SAFETY.",
                (960,260)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene9 )


    def scene9(self):
        print("SCENE9 start")        
        self.scene_no = 9

        cp9 = ComicPage(self.game, 'sc1_7', 470, 360, 680)
        self.open_pages.append( cp9 )
        self.game.add_object( cp9 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp9.add_text(
                "A JOURNEY BEGINS, A MYSTERY UNFOLDS. WHAT WAS THE FLASH? AND WHAT LIES AHEAD?",
                (490,650),
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene10 )

    def scene10( self ) :
        print("SCENE10 start")        
        self.scene_no = 10
        for page in self.open_pages :
            page.on_stop_request()
        self.game.set_focused(self.player_ship)
        self.game.zoom_locked = None
        self.input_handler.control_enabled = True
        self.at_time( self.game.get_time() + 3000, self.scene10_liora_planet )
        self.at_time( self.game.get_time() + 6000, self.scene10_liora_wormhole )

    def scene10_liora_planet(self) :
        if 'planet7' in Scenario.flags :
            return
        if self.player_ship.disp_distance_to( self.planet ) < 200 or self.player_ship.disp_distance_to( self.wormhole ) < 200 :
            self.at_time( self.game.get_time() + 500, self.scene10_liora_planet )
            return
        self.at_time( self.game.get_time(), self.liora_in )
        self.at_time( self.game.get_time() + 50, lambda: 
            self.agent_says( self.liora, 
                f"ATTENTION, PILOT.\nOUR SCANNERS HAVE PICKED UP A POTENTIAL PLANETARY SIGNATURE"))
        self.at_time( self.game.get_time() + 100, lambda: DirectionObject(self.game, self.player_ship, self.planet))
        self.at_time( self.game.get_time() + 200, lambda: 
            self.agent_says( self.liora, 
                "I SUGGEST WE ADJUST OUR COURSE AND INVESTIGATE.\nTHIS COULD BE WHAT WE'RE LOOKING FOR." ) )
        self.at_time( self.game.get_time() + 600, self.liora_out )
        self.at_time( self.game.get_time() + 3000, self.scene10_liora_planet )

    def scene10_liora_wormhole(self) :
        if 'wormhole7' in Scenario.flags :
            return
        if self.player_ship.disp_distance_to( self.planet ) < 200 or self.player_ship.disp_distance_to( self.wormhole ) < 200 :
            self.at_time( self.game.get_time() + 500, self.scene10_liora_wormhole )
            return   
        print(f"scene10_liora_wormhole: distance to planet: {self.player_ship.disp_distance_to( self.planet )}, distance to wormhole: {self.player_ship.disp_distance_to( self.wormhole )}")         
        self.at_time( self.game.get_time(), self.liora_in )
        self.at_time( self.game.get_time() + 50, lambda: self.agent_says( self.liora, f"ATTENTION, PILOT."))
        self.at_time( self.game.get_time() + 200, lambda: self.agent_says( self.liora, f"OUR SENSORS HAVE JUST DETECTED AN ENERGY SIGNATURE\nREMINISCENT OF THE RIFT WE ENCOUNTERED EARLIER."))
        self.at_time( self.game.get_time() + 200, lambda: DirectionObject(self.game, self.player_ship, self.wormhole))
        self.at_time( self.game.get_time() + 350, lambda: 
            self.agent_says( self.liora, "THIS COULD BE OUR WAY BACK.\nI RECOMMEND WE APPROACH WITH CAUTION AND INVESTIGATE FURTHER." ) )
        self.at_time( self.game.get_time() + 600, self.liora_out )
        self.at_time( self.game.get_time() + 4500, self.scene10_liora_wormhole )

    def ticktack10( self ) :
        if self.game.get_time() % 50 == 0 :
            # print(f'distance to planet: {self.player_ship.disp_distance_to( self.planet )}')
            # print(f'    player_ship: {self.player_ship.get_pos()}')
            # print(f'    planet: {self.planet.get_pos()}')
            if (not 'planet7' in Scenario.flags) and self.player_ship.disp_distance_to( self.planet ) < 50 :
                self.scene11()
            if (not 'wormhole7' in Scenario.flags) and self.player_ship.disp_distance_to( self.wormhole ) < 200 :
                self.scene13()
            if ('wormhole7' in Scenario.flags) and self.player_ship.disp_distance_to( self.wormhole ) < 50 :
                self.game.on_stop_request()
                Scenario2(win).start()

    def scene11( self ) :
        print("SCENE11 start")        
        self.scene_no = 11
        self.game.pop_focused()
        self.player_ship.v = pygame.Vector2(0, 0)
        Scenario.flags.add('planet7')
        self.game.zoom_locked = self.game.get_time() + 100000
        self.input_handler.control_enabled = False
        cp11 = ComicPage(self.game, 'sc2_1', 470, 360, 680)
        self.open_pages.append( cp11 )
        self.game.add_object( cp11 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp11.add_text(
                "IN AN UNCHARTED STAR SYSTEM, THE SCOUT SHIP'S SENSORS DETECT A PROMISING SIGNAL.",
                (490,50),
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene12 )


    def scene12( self ) :
        print("SCENE12 start")        
        self.scene_no = 12
        self.game.zoom_locked = self.game.get_time() + 100000
        self.input_handler.control_enabled = False
        cp12 = ComicPage(self.game, 'sc2_2', 480, 370, 670)
        self.open_pages.append( cp12 )
        self.game.add_object( cp12 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp12.add_speech(
                "THE ATMOSPHERE COMPOSITION,\nGRAVITY... IT'S ALL WITHIN LIVABLE RANGE.",
                (280,120),
                (320,170)
            ) )

        self.dlg_at_time( self.game.get_time() + 300, 
            lambda : 
            cp12.add_speech(
                "AND THERE'S MORE...\nTHESE READINGS INDICATE RICH DEPOSITS OF RESOURCES.",
                (580,60),
                (460,170)
            ) )

        self.dlg_at_time( self.game.get_time() + 500, 
            lambda : 
            cp12.add_speech(
                "WE NEED TO RELAY THIS INFORMATION HOME.\nBUT FIRST, WE MUST FIND A WAY BACK.",
                (250,670),
                (470,580)
            ) )

        self.dlg_at_time( self.game.get_time() + 700, 
            lambda : 
            cp12.add_speech(
                "AGREED. THIS DISCOVERY IS MONUMENTAL,\nBUT WE'RE STILL LOST IN THIS SYSTEM.",
                (680,400),
                (710,450)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene10 )


    def scene13( self ) :
        print("SCENE13 start")        
        self.scene_no = 13
        Scenario.flags.add('wormhole7')
        self.game.pop_focused()
        self.player_ship.v = pygame.Vector2(0, 0)
        self.game.zoom_locked = self.game.get_time() + 100000
        self.input_handler.control_enabled = False
        cp13 = ComicPage(self.game, 'sc2_3', 480, 370, 670)
        self.open_pages.append( cp13 )
        self.game.add_object( cp13 )
        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp13.add_text(
                "AS THE SHIP JOURNEYS ONWARD,\nA BEACON OF HOPE EMERGES FROM THE COSMIC DEPTHS.",
                (430,70),
            ) )
        self.dlg_at_time( self.game.get_time() + 300, 
            lambda : 
            cp13.add_speech(
                "CAPTAIN, SENSORS ARE PICKING UP A STRONG ENERGY SOURCE.\nIT... IT LOOKS LIKE ANOTHER PORTAL!",
                (500,350),
                (660,570)
            ) )
        self.dlg_at_time( self.game.get_time() + 500, 
            lambda : 
            cp13.add_speech(
                "BUT THIS ONE... IT'S DIFFERENT. MORE STABLE.",
                (350,470),
                (160,680)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene14 )

    def scene14( self ) :
        print("SCENE14 start")        
        self.scene_no = 14
        cp14 = ComicPage(self.game, 'sc2_4', 480, 360, 680)
        self.open_pages.append( cp14 )
        self.game.add_object( cp14 )

        self.dlg_at_time( self.game.get_time() + 100, 
            lambda : 
            cp14.add_speech(
                "THE ENERGY SIGNATURES MATCH\nTHOSE OF THE RIFT THAT BROUGHT US HERE.\nBUT THEY'RE MORE CONSISTENT.\nTHIS MIGHT BE OUR WAY OUT.",
                (220,70),
                (450,100)
            ) )

        self.dlg_at_time( self.game.get_time() + 300, 
            lambda : 
            cp14.add_speech(
                "WE CAN'T JUMP IN BLINDLY AGAIN.\nWE NEED TO ANALYZE AND ENSURE IT'S SAFE.",
                (900,50),
                (720,100)
            ) )

        self.dlg_at_time( self.game.get_time() + 500,
            lambda : 
            cp14.add_speech(
                "REGARDLESS, IT'S OUR BEST CHANCE.\nLET'S PREP FOR THE JUMP.",
                (370,480),
                (330,410)
            ) )

        self.dlg_at_time( self.game.get_time() + 10000, self.scene10 )



