#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os

# Cache sound objects so we aren't initializing the same sound over and over.
_sound_library = {}
class JukeBox:
    # Sound class that handles all audio output.
    
    # Default volume levels.
    music_volume = 0.2
    fx_volume = 1.0
    
    def __init__(self):
        self.music_playing = False
    
    def play_music(self, song):
        if self.music_playing == False:
            song_path = os.path.dirname(os.path.realpath(__file__)) + "/sound/music/" + song
            song_path = song_path.replace('/', os.sep).replace('\\', os.sep)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_playing = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def play_sound(self, sound):
        # Cache sound effect objects so we don't have to generate them every time a sound is played.
        global _sound_library
        sound_fx = _sound_library.get(sound)
        if sound_fx == None:
            path = os.path.dirname(os.path.realpath(__file__)) + "/sound/" + sound
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound_fx = pygame.mixer.Sound(canonicalized_path)
            _sound_library[sound] = sound_fx
        sound_fx.set_volume(self.fx_volume)
        sound_fx.play()
