#!/usr/bin/env python3
import pygame
import os
import math
import random

from Scenario1 import Scenario1
from Scenario2 import Scenario2
from MusicPlayer import MusicPlayer
from InputHandler import InputHandler

pygame.init()
pygame.font.init()
pygame.mixer.init()

win = pygame.display.set_mode( (1280,720) )

# Create a music player for a certain directory
music_player = MusicPlayer('./assets/music')
# Start the playlist
music_player.start_playlist()

InputHandler.set_event_handler(MusicPlayer.SONG_END, music_player)
InputHandler.set_event_handler(MusicPlayer.SONG_SKIP, music_player)

# BasicScenario().start()

Scenario2(win).start()

pygame.quit()
