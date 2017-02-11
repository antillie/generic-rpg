#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import base
import colors

# Dummy scene for resetting the window size.
class DummyScreen(base.SceneBase):
    
    def __init__(self, sound, cache):
        base.SceneBase.__init__(self)
        self.name = "DummyScreen"
        self.sound = sound
        self.cache = cache
        
    # Returns to the title screen.
    def ProcessInput(self, events, pressed_keys):
        self.SwitchToScene("TitleScene")
        
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws a black screen.
    def Render(self, screen, real_w, real_h):
        screen.fill(colors.black)
        
        
