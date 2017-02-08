#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("scenes")
sys.path.append("/..")
import pygame
import os
import virtualscreen
import cache
import sound
import base
import colors

sound = sound.JukeBox()

class GameScene(base.SceneBase):
    # The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
    def __init__(self, song="plesantcreekloop.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        # Stop whatever music is playing, if any.
        sound.stop_music()
        # Play the town theme for now.
        sound.play_music(self.song)
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        pass
    
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Filling a 1024x576 screen requires 16x9 64x64 pixel tiles.
        x_count = 16
        y_count = 9
        
        for y in range(y_count):
            for x in range(x_count):
                canvas.canvas.blit(cache.get_image("landscaping/mountain_landscape.png"), (x * 64, y * 64), (448, 128, 64, 64))
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
