#!/usr/bin/python
# -*- coding: utf-8 -*-

import skillranks

# Defines the stat growth of the white mage class. White mages are casters that specalize in healing and defensive magic.
class WhiteMage:
    
    def __init__(self):
        
        # Class name.
        self.name = "White Mage"
        self.short = "WHM"
        
        # Skillrank template.
        self.skills = skillranks.SkillRanks()
        
        # Poor HP and good MP.
        self.hp_scale = 5
        self.hp_base = 13
        self.hp_altscale = 0
        self.mp_scale = 4
        self.mp_base = 12
        self.has_mp = True
        
        # Good stats for healing spells, somewhat poor everywhere else.
        self.strength_scale = 0.35
        self.strength_base = 3
        self.vitality_scale = 0.35
        self.vitality_base = 3
        self.agility_scale = 0.3
        self.agility_base = 3
        self.dexterity_scale = 0.25
        self.dexterity_base = 2
        self.mind_scale = 0.5
        self.mind_base = 5
        self.inteligence_scale = 0.3
        self.inteligence_base = 3
        self.charisma_scale = 0.4
        self.charisma_base = 4
    
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
            return self.skills.b_plus[level]
        elif skill == "staff":
            return self.skills.c_plus[level]
        elif skill == "evasion":
            return self.skills.e[level]
        elif skill == "shield":
            return self.skills.d[level]
        elif skill == "healing":
            return self.skills.a_plus[level]
        elif skill == "divine":
            return self.skills.a_minus[level]
        elif skill == "enhancing":
            return self.skills.c_plus[level]
        elif skill == "enfeebling":
            return self.skills.c_minus[level]
        else:
            return 0
    
    def spells(self, level, healing, elemental, enchancing, dark, divine):
        
        spell_list = []
        
        if level >= 1:
            spell_list.append(healing["cure"])
        
        return spell_list
