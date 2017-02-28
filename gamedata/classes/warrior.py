#!/usr/bin/python
# -*- coding: utf-8 -*-

import skillranks

# Defines the stat growth of the warrior class. Warriors are physical combatants that wear heavy armor and beat things to death with axes.
class Warrior:
    
    def __init__(self):
        
        # Class name.
        self.name = "Warrior"
        self.short = "WAR"
        
        # Skillrank template.
        self.skills = skillranks.SkillRanks()
        
        # Good HP and no MP.
        self.hp_scale = 8
        self.hp_base = 17
        self.hp_altscale = 1
        self.mp_scale = 0
        self.mp_base = 0
        self.has_mp = False
        
        # Strong physical stats but poor magic stats.
        self.strength_scale = 0.5
        self.strength_base = 5
        self.vitality_scale = 0.45
        self.vitality_base = 4
        self.agility_scale = 0.4
        self.agility_base = 4
        self.dexterity_scale = 0.4
        self.dexterity_base = 4
        self.mind_scale = 0.25
        self.mind_base = 2
        self.inteligence_scale = 0.25
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
        if skill == "axe":
            return self.skills.a_minus[level]
        elif skill == "gaxe":
            return self.skills.a_plus[level]
        elif skill == "club":
            return self.skills.b_minus[level]
        elif skill == "dagger":
            return self.skills.b_minus[level]
        elif skill == "h2h":
            return self.skills.d[level]
        elif skill == "polearm":
            return self.skills.b_minus[level]
        elif skill == "scythe":
            return self.skills.b_plus[level]
        elif skill == "staff":
            return self.skills.b[level]
        elif skill == "sword":
            return self.skills.b[level]
        elif skill == "gsword":
            return self.skills.b_plus[level]
        elif skill == "evasion":
            return self.skills.c[level]
        elif skill == "parrying":
            return self.skills.c_minus[level]
        elif skill == "shield":
            return self.skills.c_plus[level]
        else:
            return 0
    
    def spells(self, level, healing, elemental, enchancing, dark, divine):
        return [None]
