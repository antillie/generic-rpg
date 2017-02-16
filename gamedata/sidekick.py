#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import colors
import utils
import pyganim

# This class represents the player character.
class Sidekick(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, direction, width=32, height=48):
        # Call the parent class constructor.
        super(Sidekick, self).__init__()
        self.direction = direction
        
        self.level = 1
        
        self.current_hp = 26
        self.max_hp = 26
        
        self.current_mp = 8
        self.max_mp = 8
        
        self.status = ["Normal"]
        
        self.strength = 5
        self.vitality = 6
        self.agility = 4
        self.dexterity = 5
        self.mind = 4
        self.inteligence = 2
        self.charisma = 4
        
        self.defence = 18
        self.attack = 22
        self.accuracy = 10
        self.dodge = 4
        self.magic_attack = 2
        self.magic_defense = 3
        
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
            self.image.blit(self.back_standing, (0, 0))
        elif self.direction == "down":
            self.image.blit(self.front_standing, (0, 0))
        elif self.direction == "left":
            self.image.blit(self.left_standing, (0, 0))
        elif self.direction == "right":
            self.image.blit(self.right_standing, (0, 0))
        else:
            raise Exception("You must pass in a valid direction for the character to be facing.")
