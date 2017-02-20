#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defines the stat growth of human characters. Humans are a balanced race with no glaring strengths or weaknesses.
class Human:
    
    def __init__(self):
        
        # Middle of the road HP/MP.
        self.hp_scale = 6
        self.hp_base = 14
        self.hp_altscale = 0
        self.mp_scale = 3
        self.mp_base = 10
        
        # Balanced base stats.
        self.strength_scale = 0.35
        self.strength_base = 3
        self.vitality_scale = 0.35
        self.vitality_base = 3
        self.agility_scale = 0.35
        self.agility_base = 3
        self.dexterity_scale = 0.35
        self.dexterity_base = 3
        self.mind_scale = 0.35
        self.mind_base = 3
        self.inteligence_scale = 0.35
        self.inteligence_base = 3
        self.charisma_scale = 0.35
        self.charisma_base = 3
    
    def hp(self, level):
        scale = level - 10
        if scale < 0:
            scale = 0
        
        alt_scale = level - 30
        if alt_scale < 0:
            alt_scale = 0
        
        hp = (self.hp_scale * (level - 1)) + (self.hp_base + (2 * scale)) + (self.hp_altscale * alt_scale)
        return hp
    
    def mp(self, level):
        mp = (self.mp_scale * (level - 1)) + self.mp_base
        return mp
    
    def stat(self, level, stat):
        if stat == "strength":
            strength = int(self.strength_scale * (level - 1) + self.strength_base)
            return strength
        elif stat == "vitality":
            vitality = int(self.vitality_scale * (level - 1) + self.vitality_base)
            return vitality
        elif stat == "agility":
            agility = int(self.agility_scale * (level - 1) + self.agility_base)
            return agility
        elif stat == "dexterity":
            dexterity = int(self.dexterity_scale * (level - 1) + self.dexterity_base)
            return dexterity
        elif stat == "mind":
            mind = int(self.mind_scale * (level - 1) + self.mind_base)
            return mind
        elif stat == "inteligence":
            inteligence = int(self.vitality_scale * (level - 1) + self.inteligence_base)
            return inteligence
        elif stat == "charisma":
            charisma = int(self.charisma_scale * (level - 1) + self.charisma_base)
            return charisma
