#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defines the bronze axe weapon.

class BronzeAxe:
    
    def __init__(self):
        
        # Base stats.
        self.damage = 8
        self.delay = 276
        self.amount = 0
        self.wtype = "axe"
        self.twohander = False
        self.description1 = "Damage: 8, Delay: 276"
        self.description2 = "No stat bonuses."
        self.description3 = "WAR, DRK"
        
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
            "firebonus":0,
            "icebonus":0,
            "windbonus":0,
            "earthbonus":0,
            "lightningbonus":0,
            "waterbonus":0,
            "holybonus":0,
            "darknessbonus":0
        }
        
        
