import os
import random
import pygame


class MusicPlayer:
    # Define a custom event
    SONG_END = pygame.USEREVENT + 1
    SONG_SKIP = pygame.USEREVENT + 2
    # SONG_FADEOUT_END = pygame.USEREVENT + 3

    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.songs = self.get_songs()
        self.current_song = 0
        self.selected_song = None

    def get_songs(self):
        # List all files in the directory
        files = os.listdir(self.music_dir)

        # Filter out non-mp3 files
        songs = [file for file in files if file.endswith('.mp3')]

        # Return the list of song names
        return songs

    def start_playlist(self):
        # Shuffle the playlist
        random.shuffle(self.songs)

        # Set the end event on the music player
        pygame.mixer.music.set_endevent(MusicPlayer.SONG_END)

        # Start playing the first song
        self.play_song()

    def play_song(self):
        print(f'Playing song: {self.songs[self.current_song]}')
        pygame.mixer.music.load(os.path.join(self.music_dir, self.songs[self.current_song]))
        pygame.mixer.music.play()

    def next_song(self):
        if self.selected_song != None :
            self.current_song = self.selected_song
            self.selected_song = None
        else :
            self.current_song += 1
        if self.current_song >= len(self.songs):
            self.current_song = 0
        self.play_song()

    def skip_next(self):
        print("MUSIC SKIP NEXT")
        # Fade out over 2000 milliseconds (2 seconds)
        pygame.mixer.music.fadeout(1000)

    def skip_to(self, song_name) :
        if song_name in self.songs :
            self.selected_song = self.songs.index(song_name)
            pygame.mixer.music.fadeout(1000)
        else :
            self.skip_next()

    def on_event(self, event) :
        if event.type == MusicPlayer.SONG_END :
            self.next_song()
            return True
        elif event.type == MusicPlayer.SONG_SKIP :
            print(f"MediaPlayer: SONG_SKIP, message: {event.message}")
            if event.message == None :
                self.skip_next()
            else :
                self.skip_to(event.message)
            return True
        else :
            return False

    @staticmethod
    def skip_song() :
        new_event = pygame.event.Event(MusicPlayer.SONG_SKIP, message=None)
        pygame.event.post(new_event)

    @staticmethod
    def skip_to_song(song_name) :
        new_event = pygame.event.Event(MusicPlayer.SONG_SKIP, message=song_name)
        pygame.event.post(new_event)


