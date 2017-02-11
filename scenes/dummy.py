#!/usr/bin/python
# -*- coding: utf-8 -*-

import base

# Dummy scene for resetting the window size.
class DummyScreen(base.SceneBase):
    
    def __init__(self, sound, cache, transition):
        base.SceneBase.__init__(self)
        self.name = "DummyScreen"
        self.sound = sound
        self.cache = cache
        
    # Returns to the title screen.
    def ProcessInput(self, events, pressed_keys):
        self.SwitchToScene("TitleScene")
        
    # Nothing to do.
    def Update(self):
        pass
    
    # Don't bother drawing anything.
    def Render(self, screen, real_w, real_h):
        pass
