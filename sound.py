#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
import sys

# Cache sound objects so we aren't initializing the same sound over and over.
_sound_library = {}

# Sound class that handles all audio output.
class JukeBox:
    # Default volume levels.
    music_volume = 0.2
    fx_volume = 0.3
    
    def __init__(self):
        self.music_playing = False
        if getattr(sys, 'frozen', False):
            # frozen
            self.root = os.path.dirname(sys.executable)
        else:
            # unfrozen
            self.root = os.path.dirname(os.path.realpath(__file__))
    
    def play_music(self, song):
        if self.music_playing == False:
            
            if song == "forest.mp3":
                self.music_volume = 0.8
            else:
                self.music_volume = 0.2
            
            song_path = self.root + "/sound/music/" + song
            song_path = song_path.replace("/", os.sep).replace("\\", os.sep)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_playing = True
        
    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def play_sound(self, sound):
        
        if sound == "menu_change.wav":
            self.fx_volume = 1.0
        else:
            self.fx_volume = 0.3
        
        # Cache sound effect objects so we don't have to generate them every time a sound is played.
        global _sound_library
        sound_fx = _sound_library.get(sound)
        if sound_fx == None:
            path = self.root + "/sound/" + sound
            canonicalized_path = path.replace("/", os.sep).replace("\\", os.sep)
            sound_fx = pygame.mixer.Sound(canonicalized_path)
            sound_fx.set_volume(self.fx_volume)
            _sound_library[sound] = sound_fx
        sound_fx.play()
