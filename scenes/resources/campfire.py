#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import colors
import utils
import pyganim

# This class represents an animated campfire.
class Campfire(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, width=64, height=64):
        # Call the parent class constructor.
        super(Campfire, self).__init__()
        
        # Start with a transparant surface the size of our sprite and make a rect for it.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        self.rect = self.image.get_rect()
        
        # Set the still images.
        self.frame1 = cache.get_char_sprite("campfire.png", 0, 0, 64, 64)
        self.frame2 = cache.get_char_sprite("campfire.png", 64, 0, 64, 64)
        self.frame3 = cache.get_char_sprite("campfire.png", 128, 0, 64, 64)
        self.frame4 = cache.get_char_sprite("campfire.png", 192, 0, 64, 64)
        self.frame5 = cache.get_char_sprite("campfire.png", 256, 0, 64, 64)
        
        self.image.blit(self.frame1, (0, 0))
        
        # Set the animation speed. (in seconds)
        anim_speed = 0.18
        
        # Define the still images to use for each frame of the animation.
        # Format: Image file, top left corner of the part of the file that we want (in x, y format), character width, character height.
        animationframes = [
            (self.frame1, anim_speed),
            (self.frame2, anim_speed),
            (self.frame3, anim_speed),
            (self.frame4, anim_speed),
            (self.frame5, anim_speed)
        ]
        
        # Create a dictionary to hold the animation objects.
        self.animObjs = {}
        self.animObjs["burn"] = pyganim.PygAnimation(animationframes)
        
        # Create the conductor object that will do the actual animation.
        self.moveConductor = pyganim.PygConductor(self.animObjs)
    
    # Displays the animation on the screen.
    def update_image(self):
        self.image.fill(colors.black)
        self.animObjs["burn"].blit(self.image, (0, 0))
