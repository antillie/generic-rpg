#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import colors
import utils
import pyganim
import human
import warrior
import monk

# This class represents a party member.
class Sidekick(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, direction, width=32, height=48):
        # Call the parent class constructor.
        super(Sidekick, self).__init__()
        self.direction = direction
        
        self.name = "Party Member"
        self.mclass = "Monk"
        self.sclass = "Warrior"
        
        self.race = human.Human()
        self.job = monk.Monk()
        self.subjob = warrior.Warrior()
        
        # Level.
        self.level = 1
        self.tnl = 500
        
        # Stats.
        race_hp = self.race.hp(self.level)
        class_hp = self.job.hp(self.level)
        subclass_hp = self.subjob.hp(self.level / 2) / 2
        
        self.max_hp = race_hp + class_hp + subclass_hp
        self.current_hp = race_hp + class_hp + subclass_hp
        
        if self.job.has_mp == False and self.subjob.has_mp == False:
            self.current_mp = 0
            self.max_mp = 0
        else:
            race_mp = self.race.mp(self.level)
            class_mp = self.job.mp(self.level)
            subclass_mp = self.subjob.mp(self.level / 2) / 2
            self.current_mp = race_mp + class_mp + subclass_mp
            self.max_mp = race_mp + class_mp + subclass_mp
        
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
        
        self.strength = race_str + class_str + subclass_str
        self.vitality = race_vit + class_vit + subclass_vit
        self.agility = race_agi + class_agi + subclass_agi
        self.dexterity = race_dex + class_dex + subclass_dex
        self.mind = race_mnd + class_mnd + subclass_mnd
        self.inteligence = race_int + class_int + subclass_int
        self.charisma = race_cha + class_cha + subclass_cha
        
        if self.level <= 50:
            self.base_defense = (self.vitality / 2) + 8 + self.level
        elif self.level > 50 and self.level <= 60:
            self.base_defense = (self.vitality / 2) + 8 + self.level + (self.level - 50)
        else:
            self.base_defense = (self.vitality / 2) + 8 + self.level + self.level + 10
        
        self.defense = self.base_defense # Add item/armor effects later.
        self.attack = 22
        self.accuracy = 10
        self.dodge = 4
        self.magic_attack = 2
        self.magic_defense = 3
        self.parry = 0
        self.block = 0
        self.guard = 15
        self.counter = 10
        
        self.fire_res = 0
        self.ice_res = 0
        self.wind_res = 0
        self.earth_res = 0
        self.lightning_res = 0
        self.water_res = 0
        self.holy_res = 0
        self.darkness_res = 0
        
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
        self.front_standing = cache.get_char_sprite("sidekick.png", 0, 0, 32, 48)
        self.back_standing = cache.get_char_sprite("sidekick.png", 0, 144, 32, 48)
        self.left_standing = cache.get_char_sprite("sidekick.png", 0, 48, 32, 48)
        self.right_standing = cache.get_char_sprite("sidekick.png", 0, 96, 32, 48)
        
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
            (cache.get_char_sprite("sidekick.png", 0, 144, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 32, 144, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 64, 144, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 96, 144, width, height), anim_speed)
        ]
        goingDownImages = [
            (cache.get_char_sprite("sidekick.png", 0, 0, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 32, 0, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 64, 0, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 96, 0, width, height), anim_speed)
        ]
        goingLeftImages = [
            (cache.get_char_sprite("sidekick.png", 0, 48, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 32, 48, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 64, 48, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 96, 48, width, height), anim_speed)
        ]
        goingRightImages = [
            (cache.get_char_sprite("sidekick.png", 0, 96, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 32, 96, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 64, 96, width, height), anim_speed),
            (cache.get_char_sprite("sidekick.png", 96, 96, width, height), anim_speed)
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
