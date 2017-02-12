#!/usr/bin/python
# -*- coding: utf-8 -*-

# Template class for scenes. Things like the title screen, loading screen, towns, world map, dungeons, menus, ect...
class SceneBase():
        
    def ProcessInput(self, events, pressed_keys):
        raise Exception("process input function not overridden")

    def Update(self):
        raise Exception("update function not overridden")

    def Render(self, screen):
        raise Exception("render function not overridden")
