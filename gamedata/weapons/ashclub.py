#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defines the ash club weapon.

class AshClub:
    
    def __init__(self):
        
        # Base stats.
        self.damage = 4
        self.delay = 264
        self.amount = 0
        self.wtype = "club"
        self.twohander = False
        self.description1 = "Damage: 4, Delay: 264"
        self.description2 = "No stat bonuses."
        self.description3 = "All."
        
        # Attribute bonuses.
        
        self.stat_bonuses = {
            # Core stats.
            "hpbonus":0,
            "mpbonus":0,
            "strbonus":0,
            "vitbonus":0,
            "agibonus":0,
            "dexbonus":0,
            "mndbonus":0,
            "intbonus":0,
            "chabonus":0,
            # Secondary stats.
            "defbonus":0,
            "atkbonus":0,
            "accbonus":0,
            "dodgebonus":0,
            "matkbonus":0,
            "madefbonus":0,
            "parrybonus":0,
            "blockbonus":0,
            "guardbonus":0,
            "counterbonus":0,
            # Elemental resistances.
            "fire_res":0,
            "ice_res":0,
            "wind_res":0,
            "earth_res":0,
            "lightning_res":0,
            "water_res":0,
            "holy_res":0,
            "darkness_res":0
        }
