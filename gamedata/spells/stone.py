#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defines the stone spell.

class Stone:
    
    def __init__(self):
        
        # Base stats.
        self.name = "Stone"
        self.spelltype = "elemental"
        self.cost = 4
        self.element = "earth"
        self.casttime = 0.5
        self.description1 = "Deals earth elemental damage."
    
    def amount(self, caster, target):
        
        dint = caster.inteligence - target.inteligence
        
        if dint < 50:
            damage = 10 + (dint * 2)
        elif dint < 100:
            damage = 110 + (dint * 1)
        elif dint >= 100:
            damage = 160
        
        if damage < 0:
            damage = 0
        
        return damage
