#!/usr/bin/python
# -*- coding: utf-8 -*-

import hero
import npc

# This class holds all data about the current game session. Story progress, characters, inventory, ect...
class GameData:

    def __init__(self, cache, current_w, current_h):
        # Scene transition data. Used to move between scenes and to allow the context dependent scenes know which scene called them.
        self.next_scene = "TitleScene"
        self.previous_scene = ""
        self.reset_display = False
        self.cache = cache
        
        # Make the screen size avilable to all scenes for screen resize purposes.
        self.current_w = current_w
        self.current_h = current_h
        
        # Define all the characters in the game. The NPCs will probably need to be moved into their own module later.
        self.hero = hero.Hero(self.cache, "down")
        self.npc = npc.npc(self.cache, "down")
        
        # Make the party's position on the world map avilable to all scenes so we always know where to put the party when going to the world map.
        self.worldpos_x = 0
        self.worldpos_y = 0
        
        # Make the background for the battle scene easily changable by the calling scene.
        self.battlebackground = "forestbackground.png"
        
        # Define a couple of variables to control what mobs should be spawned in a battle. Either a specific mob (boss fight) or a random selection of mobs according to an area.
        self.battle_monsters = None
        self.battle_area = None
        
        # Create a flag so the battlescene will know when to reset itself for a fresh battle.
        self.battle_reset = True
        
        # When drawing the party use the party slot list. That way we can change party order visually without having to rework the scene.
        self.party_slots = [self.hero, None, None, None]
