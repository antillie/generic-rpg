#!/usr/bin/python
# -*- coding: utf-8 -*-

import hero
import sidekick
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
        self.sidekick = sidekick.Sidekick(self.cache, "down")
        self.npc = npc.npc(self.cache, "down")
        
        # Make the party's position on the world map avilable to all scenes so we always know where to put the party when going to the world map.
        self.worldpos_x = 0
        self.worldpos_y = 0
        
        # Make the background for the battle scene easily changable by the calling scene.
        self.battlebackground = "forestbackground.png"
        
        # Define a couple of variables to control what mobs should be spawned in a battle. Either a list of specific mobs (boss fight) or a random selection of mobs according to an area.
        self.battle_monsters = [None]
        self.battle_area = None
        
        # Create a flag so the battlescene will know when to reset itself for a fresh battle.
        self.battle_reset = True
        
        # When drawing the party use the party slot list. That way we can change party order visually without having to rework the scene.
        self.party_slots = [self.hero, self.sidekick, None, None]
        
        # Status screen selection choice.
        self.status_selection = 0
        
        # Party GP.
        self.gp = 50
        
        # Party inventory.
        self.inventory = {
        
        # Potions; restore HP.
        "Potion":"6",
        "Hi-Potion":"0",
        "Mega-Potion":"0",
        "X-Potion":"0",
        
        # Ethers; restore MP.
        "Ether":"2",
        "Hi-Ether":"0",
        "Mega-Ether":"0",
        "X-Ether":"0",
        
        # HP/MP restorers.
        "Minor Elixer":"0", # Restores 30%
        "Elixer":"0", # Restores to full
        
        # Status effect removers.
        "Antidote":"2", # Poison
        "Echo Screen":"0", # Silence
        "Eye Drops":"0", # Blind
        "Gold Needle":"0", # Petrify
        "Green Cherry":"0", # Imp
        "Holy Water":"0", # Zombie
        "Phoenix Feather":"0", # KO
                    
        # Party wide recovery items.
        "Tent":"3", # Out of battle, cheap, common.
        "Megalixer":"0", # In battle, rare.
        
        # Battle items.
        "Smoke Bomb":"0",
        "Warp Stone":"0",
        "Fire Edge":"0",
        "Ice Edge":"0",
        "Wind Edge":"0",
        "Earth Edge":"0",
        "Lightning Edge":"0",
        "Water Edge":"0",
        "Holy Edge":"0",
        "Darkness Edge":"0",
        "Shuriken":"0"
        
        }
