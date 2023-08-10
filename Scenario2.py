
from Scenarios import Scenario, Wormhole
from InputHandler import InputHandler
from Game import Game
from DistantObject import DistantObject
from ShipClass import Background, ScoutClass, ScienceClass, FighterClass, Stationary
from StationaryObject import StationaryObject
from Dust import Dust
from MusicPlayer import MusicPlayer
from Team import Team
from Starship import Starship
from Pilot import ScoutPilot, FighterPilot, SciencePilot


class Scenario2 ( Scenario ) :

    def __init__( self, win ) :
        self.input_handler = InputHandler()
        super().__init__( Game(self.input_handler, win), win )
        self.input_handler.set_game( self.game )
        self.game.register_key_handler(' ', self)
        self.background = DistantObject(self.game, Background( 1 ), 0, 0)
        self.game.add_object(self.background)
        Dust.make_dust(self.game, 1)
        self.scene_no = 1
        self.open_pages = []
        self.liora = None

    def start( self ) :
        self.scene1()

    def scene1( self ) :
        print("SCENE1 start")        
        self.scene_no = 1
        MusicPlayer.skip_song()
        self.game.zoom_enabled = False
        self.input_handler.control_enabled = False
        self.wormhole_pos = (1000,-1000)
        self.wormhole = Wormhole(self.game, *self.wormhole_pos)
        self.game.add_object( self.wormhole )

        self.wormhole.stable = False
        self.wormhole.noises = True
        #self.wormhole_pos = (400,-400)

        Dust.make_dust(self.game, 1)

        self.team_green = Team( "Green", (0,255,0), 3, 0, self )
        self.team_blue = Team( "Blue", (0,0,255), 2, 0, self )

        self.player_ship = Starship(self.game, self.team_blue, ScoutClass(), ScoutPilot(self.game), 900, -900 )
        self.player_ship.dir = 135
        self.game.add_object( self.player_ship )

        sc = Starship(self.game, self.team_green, ScoutClass(), ScoutPilot(self.game), 800, -800 )
        sc.dir = 45
        self.scout_ship = sc
        self.game.add_object( sc )
        sc = Starship(self.game, self.team_green, FighterClass(), FighterPilot(self.game), 850, -750 )
        sc.dir = 45
        self.fighter_ship = sc
        self.game.add_object( sc )
        sc = Starship(self.game, self.team_green, ScienceClass(), SciencePilot(self.game), 700, -700 )
        sc.dir = 45
        self.science_ship = sc
        self.game.add_object( sc )

        planet = StationaryObject(self.game, Stationary("planet_1", 64), -420, 240)
        planet.layer = 1
        self.game.add_object( planet )
        self.game.set_camera( self.player_ship.get_pos() )

        self.wormhole.start_burst(1)

        self.game.paused = False

        time = self.agent_dialog( {
                'agent' : 'elena',
                'text' : [ 
                    'This is Captain Elena Voss of the SS Orionis.', 
                    "We had assumed you were lost in that cosmic flash.\nIt's good to see you back, Pilot."
                ],
                'obj' : self.science_ship,
                'time_rel' : 100
        } )

        time = self.agent_dialog( {
                'agent' : 'jack',
                'text' : [ 
                    "Lt. Jack Holt:\nIt's a miracle you made it back!\nWe had written you off.", 
                ],
                'obj' : self.fighter_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "Dr. Liora Calyx:\nThe ship's diagnostics indicate that\nthere's no structural damage, which is astounding.",
                    "It's as if the rift had a protective bubble."
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'ronan',
                'text' : [ 
                    "We've been studying the portal's residual effects,\nbut coming through it provides a perspective we haven't had.",\
                    "Can you share the data from your ship's instruments?"
                ],
                'obj' : self.scout_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'alex',
                'text' : [ 
                    "Of course, Commander Blake. I'll upload the data logs.",
                    "And thank you, Captain Voss. It's good to be back."
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'elena',
                'text' : [ 
                    "We'll analyze your data and decide our next course of action.",
                    "For now, follow our lead. We're heading back to the planet.",
                    "All vessels, set a course for home."
                ],
                'obj' : self.science_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'jack',
                'text' : [ 
                    "You heard the Captain. Escorts, form up and follow the SS Orionis.", 
                ],
                'obj' : self.fighter_ship,
                'time_rel' : time + 50
        })
        
        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "Once we're on the planet,\nwe should present our findings to the Scientific Council.",
                    "They'll be eager to hear about our journey and the alternate system."
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'alex',
                'text' : [ 
                    "Agreed, Dr. Calyx.\nIt will be crucial to share our experiences and data.",
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "Once we're on the planet,\nwe should present our findings to the Scientific Council.",
                    "They'll be eager to hear about our journey and the alternate system."
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })
        
        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "Drag your mouse cursor over both scout ships\nand the fighter to select them.",
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "Now, press Control-1 to create a group with them.\nYou can activate this group later by simply pressing the number key\nthat corresponds to the group's number, from 1 to 9.",
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        time = self.agent_dialog( {
                'agent' : 'liora',
                'text' : [ 
                    "With your group selected,\nright-click on the science vessel to command them to escort it.",
                ],
                'obj' : self.player_ship,
                'time_rel' : time + 50
        })

        self.at_time( self.game.get_time() + time + 50, lambda: self.input_handler.set_control_enabled( True ) )


        self.game.game_loop()

