#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import colors
import utils
import pyganim
import human
import warrior
import monk

# This class represents the player character.
class Hero(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, direction, weapons, width=32, height=48):
        # Call the parent class constructor.
        super(Hero, self).__init__()
        self.direction = direction
        self.weapons = weapons
        
        self.name = "Hero Name"
        self.mclass = "Warrior"
        self.sclass = "Monk"
        
        self.race = human.Human()
        self.job = warrior.Warrior()
        self.subjob = monk.Monk()
        
        # Level.
        self.level = 1
        
        # Equipment.
        self.equipment = {
            "main":self.weapons["bronzeaxe"],
            "off":None,
            "helm":None,
            "body":None,
            "gloves":None,
            "boots":None,
            "ring1":None,
            "ring2":None
        }
        
        # Bonus stats from gear.
        
        # Core stats.
        self.hpbonus = 0
        self.mpbonus = 0
        self.strbonus = 0
        self.vitbonus = 0
        self.agibonus = 0
        self.dexbonus = 0
        self.mndbonus = 0
        self.intbonus = 0
        self.chabonus = 0
        
        # Secondary stats.
        self.defbonus = 0
        self.atkbonus = 0
        self.accbonus = 0
        self.dodgebonus = 0
        self.matkbonus = 0
        self.madefbonus = 0
        self.parrybonus = 0
        self.blockbonus = 0
        self.guardbonus = 0
        self.counterbonus = 0
        
        # Elemental resistances.
        self.fire_res = 0
        self.ice_res = 0
        self.wind_res = 0
        self.earth_res = 0
        self.lightning_res = 0
        self.water_res = 0
        self.holy_res = 0
        self.darkness_res = 0
        
        # Add up the bonus stats from gear.
        for slot, item in self.equipment.items():
            if item != None:
                self.hpbonus = self.hpbonus + item.stat_bonuses["hpbonus"]
                self.mpbonus = self.mpbonus + item.stat_bonuses["mpbonus"]
                self.strbonus = self.strbonus + item.stat_bonuses["strbonus"]
        
        # Main stats.
        race_hp = self.race.hp(self.level)
        class_hp = self.job.hp(self.level)
        subclass_hp = self.subjob.hp(self.level / 2) / 2
        
        self.max_hp = int(race_hp + class_hp + subclass_hp + self.hpbonus)
        self.current_hp = int(race_hp + class_hp + subclass_hp + self.hpbonus)
        
        if self.job.has_mp == False and self.subjob.has_mp == False:
            self.current_mp = 0 + self.mpbonus
            self.max_mp = 0 + self.mpbonus
        else:
            race_mp = self.race.mp(self.level)
            class_mp = self.job.mp(self.level)
            subclass_mp = self.subjob.mp(self.level / 2) / 2
            self.current_mp = int(race_mp + class_mp + subclass_mp + self.mpbonus)
            self.max_mp = int(race_mp + class_mp + subclass_mp + self.mpbonus)
        
        race_str = self.race.stat(self.level, "strength")
        race_vit = self.race.stat(self.level, "vitality")
        race_agi = self.race.stat(self.level, "agility")
        race_dex = self.race.stat(self.level, "dexterity")
        race_mnd = self.race.stat(self.level, "mind")
        race_int = self.race.stat(self.level, "inteligence")
        race_cha = self.race.stat(self.level, "charisma")
        
        class_str = self.job.stat(self.level, "strength")
        class_vit = self.job.stat(self.level, "vitality")
        class_agi = self.job.stat(self.level, "agility")
        class_dex = self.job.stat(self.level, "dexterity")
        class_mnd = self.job.stat(self.level, "mind")
        class_int = self.job.stat(self.level, "inteligence")
        class_cha = self.job.stat(self.level, "charisma")
        
        subclass_str = self.subjob.stat(self.level / 2, "strength") / 2
        subclass_vit = self.subjob.stat(self.level / 2, "vitality") / 2
        subclass_agi = self.subjob.stat(self.level / 2, "agility") / 2
        subclass_dex = self.subjob.stat(self.level / 2, "dexterity") / 2
        subclass_mnd = self.subjob.stat(self.level / 2, "mind") / 2
        subclass_int = self.subjob.stat(self.level / 2, "inteligence") / 2
        subclass_cha = self.subjob.stat(self.level / 2, "charisma") / 2
        
        self.strength = int(race_str + class_str + subclass_str + self.strbonus)
        self.vitality = int(race_vit + class_vit + subclass_vit)
        self.agility = int(race_agi + class_agi + subclass_agi)
        self.dexterity = int(race_dex + class_dex + subclass_dex)
        self.mind = int(race_mnd + class_mnd + subclass_mnd)
        self.inteligence = int(race_int + class_int + subclass_int)
        self.charisma = int(race_cha + class_cha + subclass_cha)
        
        if self.level <= 50:
            self.base_defense = (self.vitality / 2) + 8 + self.level
        elif self.level > 50 and self.level <= 60:
            self.base_defense = (self.vitality / 2) + 8 + self.level + (self.level - 50)
        else:
            self.base_defense = (self.vitality / 2) + 8 + self.level + self.level + 10
        
        self.weaponskill = self.job.skill(self.level, self.equipment["main"].wtype)
        
        if self.weaponskill <= 200:
            self.skillaccuracy = self.weaponskill
        else:
            self.skillaccuracy = (0.857 * (self.weaponskill - 200)) + 200
        
        self.defense = int(self.base_defense) # Add item/armor effects later.
        self.attack = int(8 + self.weaponskill + (self.strength * 0.75)) # Add item/armor effects later.
        self.accuracy = int(self.skillaccuracy + (self.dexterity * 0.75)) # Add item/armor effects later.
        self.dodge = int(self.job.skill(self.level, "evasion") + (self.agility * 0.75))
        self.magic_attack = 0
        self.magic_defense = 0
        self.parry = self.job.skill(self.level, "parrying")
        self.block = self.job.skill(self.level, "shield")
        self.guard = 0
        self.counter = 0
        
        self.tnl = 500
        
        # Status effects.
        self.status_effects = {
            "poison":False,
            "silence":False,
            "blind":False,
            "petrify":False,
            "imp":False,
            "zombie":False
        }
        
        # Battle screen info.
        self.battle_line_x = 0
        self.attack_flag = False
        self.attack_starting = True
        self.attack_ending = False
        
        # Start with a transparant surface the size of our sprite and make a rect for it.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        self.rect = self.image.get_rect()
        # Quack quack!
        
        # Set the standing still images.
        self.front_standing = cache.get_char_sprite("character.png", 0, 0, 32, 48)
        self.back_standing = cache.get_char_sprite("character.png", 0, 144, 32, 48)
        self.left_standing = cache.get_char_sprite("character.png", 0, 48, 32, 48)
        self.right_standing = cache.get_char_sprite("character.png", 0, 96, 32, 48)
        
        # Draw the starting image.
        if self.direction == "up":
            self.image.blit(self.back_standing, (0, 0))
        elif self.direction == "down":
            self.image.blit(self.front_standing, (0, 0))
        elif self.direction == "left":
            self.image.blit(self.left_standing, (0, 0))
        elif self.direction == "right":
            self.image.blit(self.right_standing, (0, 0))
        else:
            raise Exception("You must pass in a valid direction for the character to be facing.")
        
        # Set the walking animation speed. (in seconds)
        anim_speed = 0.15
        
        # Define the still images to use for each frame of the animation.
        # Format: Image file, top left corner of the part of the file that we want (in x, y format), character width, character height.
        goingUpImages = [
            (cache.get_char_sprite("character.png", 0, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 144, width, height), anim_speed)
        ]
        goingDownImages = [
            (cache.get_char_sprite("character.png", 0, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 0, width, height), anim_speed)
        ]
        goingLeftImages = [
            (cache.get_char_sprite("character.png", 0, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 48, width, height), anim_speed)
        ]
        goingRightImages = [
            (cache.get_char_sprite("character.png", 0, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 96, width, height), anim_speed)
        ]
        
        # Create a dictionary to hold the animation objects.
        self.animObjs = {}
        self.animObjs["front_walk"] = pyganim.PygAnimation(goingDownImages)
        self.animObjs["back_walk"] = pyganim.PygAnimation(goingUpImages)
        self.animObjs["left_walk"] = pyganim.PygAnimation(goingLeftImages)
        self.animObjs["right_walk"] = pyganim.PygAnimation(goingRightImages)
        
        # Create the conductor object that will do the actual animation.
        self.moveConductor = pyganim.PygConductor(self.animObjs)
    
    # Displays the walking animation on the screen.
    def update_image(self, direction):
        if direction == None:
            if self.direction == "up":
                self.image.fill(colors.black)
                self.image.blit(self.back_standing, (0, 0))
            elif self.direction == "down":
                self.image.fill(colors.black)
                self.image.blit(self.front_standing, (0, 0))
            elif self.direction == "left":
                self.image.fill(colors.black)
                self.image.blit(self.left_standing, (0, 0))
            elif self.direction == "right":
                self.image.fill(colors.black)
                self.image.blit(self.right_standing, (0, 0))
        else:
            self.direction = direction
            if self.direction == "up":
                self.image.fill(colors.black)
                self.animObjs["back_walk"].blit(self.image, (0, 0))
            elif self.direction == "down":
                self.image.fill(colors.black)
                self.animObjs["front_walk"].blit(self.image, (0, 0))
            elif self.direction == "left":
                self.image.fill(colors.black)
                self.animObjs["left_walk"].blit(self.image, (0, 0))
            elif self.direction == "right":
                self.image.fill(colors.black)
                self.animObjs["right_walk"].blit(self.image, (0, 0))
    
    # Displays a standing image.
    def update_standing_image(self, direction):
        self.direction = direction
        if self.direction == "up":
            self.image.fill(colors.black)
            self.image.blit(self.back_standing, (0, 0))
        elif self.direction == "down":
            self.image.fill(colors.black)
            self.image.blit(self.front_standing, (0, 0))
        elif self.direction == "left":
            self.image.fill(colors.black)
            self.image.blit(self.left_standing, (0, 0))
        elif self.direction == "right":
            self.image.fill(colors.black)
            self.image.blit(self.right_standing, (0, 0))
        else:
            raise Exception("You must pass in a valid direction for the character to be facing.")
