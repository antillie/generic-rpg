#!/usr/bin/python
# -*- coding: utf-8 -*-

import hero
import npc

# This class holds all data about the current game session. Story progress, characters, inventory, ect...
class GameData:

    def __init__(self, cache):
        # Scene transition data. Used to move between scenes and to allow the context dependent scenes know which scene called them.
        self.next_scene = "TitleScene"
        self.previous_scene = ""
        self.reset_display = False
        self.cache = cache
        
        self.hero = hero.Hero(self.cache, "down")
        
        self.npc = npc.npc(self.cache, "down")
