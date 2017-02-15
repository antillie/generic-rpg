#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import colors
import utils
import pyganim

# This class represents a random NPC.
class npc(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, direction, width=32, height=48):
        # Call the parent class constructor.
        super(npc, self).__init__()
        self.direction = direction
        
        # Start with a transparant surface the size of our sprite and make a rect for it.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        self.rect = self.image.get_rect()
        # Quack quack!
        
        # Set the standing still images.
        self.front_standing = cache.get_char_sprite("npc.png", 0, 0, 32, 48)
        self.back_standing = cache.get_char_sprite("npc.png", 0, 144, 32, 48)
        self.left_standing = cache.get_char_sprite("npc.png", 0, 48, 32, 48)
        self.right_standing = cache.get_char_sprite("npc.png", 0, 96, 32, 48)
        
        # Dialog information.
        self.dialog_toggle = None
        self.conversation_counter = 0
        
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
        # Format: Image file, top left corner of the part of the file that we want (in x, y format), character width, character height, animation speed.
        goingUpImages = [
            (cache.get_char_sprite("npc.png", 0, 144, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 32, 144, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 64, 144, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 96, 144, width, height), anim_speed)
        ]
        goingDownImages = [
            (cache.get_char_sprite("npc.png", 0, 0, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 32, 0, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 64, 0, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 96, 0, width, height), anim_speed)
        ]
        goingLeftImages = [
            (cache.get_char_sprite("npc.png", 0, 48, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 32, 48, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 64, 48, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 96, 48, width, height), anim_speed)
        ]
        goingRightImages = [
            (cache.get_char_sprite("npc.png", 0, 96, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 32, 96, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 64, 96, width, height), anim_speed),
            (cache.get_char_sprite("npc.png", 96, 96, width, height), anim_speed)
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
    
    # Holds all of the NPC's dialog and any corosponding dialog choices.
    def get_dialog(self, conversation_name):
        if conversation_name == "conversation1":
            conversation = [
            "This is a pretty cool engine.",
            "Who knew that pygame was so capable?",
            "Do you think anyone will make a game with this?"
            ]
            
            options = [
                "Yes",
                "No",
                "Maybe"
            ]
            
            responses = [
                "Well I hope so too.",
                "I suppose not, but maybe someone else will find the engine useful.",
                "Yeah, its pretty hard to predict the future."
            ]
            
            return conversation, True, options, responses
            
        elif conversation_name == "conversation2":
            conversation = [
            "This is comming along pretty well if you ask me."
            ]
            
            options = [""]
            
            responses = [""]
            
            return conversation, False, options, responses
