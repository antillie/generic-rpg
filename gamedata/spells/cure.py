#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defines the cure spell.

class Cure:
    
    def __init__(self):
        
        # Base stats.
        self.name = "Cure"
        self.spelltype = "healing"
        self.cost = 8
        self.element = "light"
        self.casttime = 2
        self.description1 = "Restores HP"
    
    def amount(self, caster):
        
        power = (caster.mind / 2) + (caster.vitality / 4) + caster.healing
        
        if power < 20:
            rate = 1
            pow_floor = 0
            hp_floor = 10
        elif power < 40:
            rate = 1.33
            pow_floor = 20
            hp_floor = 15
        elif power < 125:
            rate = 8.5
            pow_floor = 40
            hp_floor = 30
        elif power < 200:
            rate = 15
            pow_floor = 125
            hp_floor = 40
        elif power < 600:
            rate = 20
            pow_floor = 200
            hp_floor = 45
        else:
            return 65
        
        amount = int(((power - pow_floor) / rate) + hp_floor)
        
        return amount
