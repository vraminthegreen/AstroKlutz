
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

#################################################

class Scenario :

    flags = set()

    def __init__( self, game, win ) :
        self.win = win
        self.game = None
        self.reset_game( game )

    def reset_game( self, game ) :
        if self.game != None :
            Dust.remove_dust(self.game)
        self.game = game
        self.game.add_ticktack_receiver(self)
        self.event_times = []
        self.events = {}
        self.dlg_events = {}
        self.dlg_event_times = []
        self.agents = {}
        self.agent = None
        self.current_agent = None

    def get_order( self, ship ) :
        return None

    def at_time( self, time, f ) :
        if time in self.events :
            self.events[time].append(f)
        else :
            self.events[time] = [ f ]
            bisect.insort( self.event_times, time )

    def dlg_at_time( self, time, f ) :
        if time in self.dlg_events :
            self.dlg_events[time].append(f)
        else :
            self.dlg_events[time] = [ f ]
            bisect.insort( self.dlg_event_times, time )

    def ticktack( self ) :
        while len(self.event_times) > 0 and self.event_times[0] < self.game.get_time() :
            self.fire_next_event()
        while len(self.dlg_event_times) > 0 and self.dlg_event_times[0] < self.game.get_time() :
            self.fire_next_dlg_event()

    def fire_next_event( self ) :
        if len(self.events) == 0 :
            return False
        events = self.events[self.event_times[0]]
        del self.events[self.event_times[0]]
        del self.event_times[0]
        for f in events :
            f()
        return True

    def fire_next_dlg_event( self ) :
        if len(self.dlg_events) == 0 :
            return False
        events = self.dlg_events[self.dlg_event_times[0]]
        del self.dlg_events[self.dlg_event_times[0]]
        del self.dlg_event_times[0]
        for f in events :
            f()
        return True

    def on_stop_request(self) :
        pass

    def liora_in( self ) :
        self.agent_in('liora')

    def agent_says( self, text ) :
        if self.agent == None :
            return
        self.agent.reset_texts()
        walkie_talkie_sound = pygame.mixer.Sound('assets/audio/walkie-talkie-sound-effect-made-with-Voicemod-technology.mp3')
        walkie_talkie_sound.play()
        self.agent.add_speech( text, (random.randint(750,850),random.randint(530,680)), (1160, 600) )

    def liora_out( self ) :
        self.agent_out()

    def agent_in(self, agent) :
        if self.current_agent == agent :
            return
        else :
            self.agent_out()
        self.current_agent = agent
        #if not agent in self.agents :
        #self.agents[agent] = ComicPage(self.game, 'portrait_' + agent, 1200, 610, 196)
        self.agent = ComicPage(self.game, 'portrait_' + agent, 1200, 610, 196)
        # if self.agent != self.agents[agent] :
        #     self.agent_out()
        walkie_talkie_sound = pygame.mixer.Sound('assets/audio/walkie-talkie-beep-made-with-Voicemod-technology.mp3')
        walkie_talkie_sound.play()
        # self.agent = self.agents[agent]
        self.game.add_object(self.agent)

    def agent_out( self ) :
        if self.agent != None :
            walkie_talkie_sound = pygame.mixer.Sound('assets/audio/walkie-talkie-beep-made-with-Voicemod-technology.mp3')
            walkie_talkie_sound.play()
            self.agent.on_stop_request()
            self.agent = None
            self.current_agent = None

    def agent_dialog(self, args) :
        time = self.game.get_time() + int(args['time_rel'])
        self.at_time(time, lambda: self.agent_in(args['agent']))
        SPEECH_DELAY = 250
        SPEECH_DELAY = 50
        obj = args.get('obj')
        if obj != None :
            self.at_time(time, lambda : self.game.set_focused(obj))
            pos = obj.get_pos()
        else :
            pos = args.get('pos')
        if pos != None :
            self.at_time(time, lambda: self.game.set_optimal_camera(pos))
        time += 50
        for line in args['text'] :
            self.at_time(time, lambda line=line: self.agent_says(line.upper()))
            time += SPEECH_DELAY
        self.at_time(time, self.agent_out)
        if obj != None :
            self.at_time(time, self.game.pop_focused )
        return time


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
        self.animation = None

    def start_burst(self, size = None) :
        if size == None :
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



