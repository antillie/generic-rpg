#!/usr/bin/python
# -*- coding: utf-8 -*-

import skillranks

# Defines the stat growth of the monk class. Monks are physical combatants that favor raw HP over armor and beat things with their fists.
class Monk:
    
    def __init__(self):
        
        # Class name.
        self.name = "Monk"
        self.short = "MNK"
        
        # Skillrank template.
        self.skills = skillranks.SkillRanks()
        
        # Great HP and no MP.
        self.hp_scale = 9
        self.hp_base = 19
        self.hp_altscale = 1
        self.mp_scale = 0
        self.mp_base = 0
        self.has_mp = False
        
        # Strong physical stats but poor magic stats.
        self.strength_scale = 0.4
        self.strength_base = 4
        self.vitality_scale = 0.5
        self.vitality_base = 5
        self.agility_scale = 0.25
        self.agility_base = 2
        self.dexterity_scale = 0.45
        self.dexterity_base = 4
        self.mind_scale = 0.35
        self.mind_base = 3
        self.inteligence_scale = 0.2
        self.inteligence_base = 2
        self.charisma_scale = 0.3
        self.charisma_base = 3
    
    def hp(self, level):
        scale = level - 10
        if scale < 0:
            scale = 0
        
        alt_scale = level - 30
        if alt_scale < 0:
            alt_scale = 0
        
        hp = (self.hp_scale * (level - 1)) + self.hp_base + (self.hp_altscale * alt_scale)
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
        
    def skill(self, level, skill):
        if skill == "club":
            return self.skills.c_plus[level]
        elif skill == "h2h":
            return self.skills.a_plus[level]
        elif skill == "staff":
            return self.skills.b[level]
        elif skill == "evasion":
            return self.skills.b_plus[level]
        elif skill == "guard":
            return self.skills.a_minus[level]
        elif skill == "parrying":
            return self.skills.e[level]
        elif skill == "counter":
            return 10
        else:
            return 0
    
    def spells(self, level, healing, elemental, enchancing, dark, divine):
        return [None]
