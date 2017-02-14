#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import formatting
import colors
import utils

# Class that handles dialog and dialog choices.

class Dialog:

    def __init__(self, cache, canvas, gamedata, menu=0):
        self.cache = cache
        self.canvas = canvas
        self.gamedata = gamedata
        self.menu = menu
        
    def render(self, dialog, choices=["None"], character_name=None, real_w=1280, real_h=720):
        
        # Draw the boxes that hold the dialog.
        pygame.draw.rect(self.canvas.canvas, colors.white, pygame.Rect(10, 508 , 1006, 203), 3)
        pygame.draw.rect(self.canvas.canvas, colors.menu_blue, pygame.Rect(12, 510 , 1002 ,199), 0)
        
        # Need to add multi line support to this later.
        self.dialog = [
            formatting.MenuOption(dialog, (22, 520), self.cache)
            ]
        
        for x in range(len(self.dialog)):
            self.canvas.canvas.blit(self.dialog[x].rend, self.dialog[x].pos)
        
        # Turn the choices into menu entry objects.
        if choices[0] != "None":
            options = []
            y = 520
            for x in range(len(choices)):
                options.append(formatting.MenuOption(choices[x], (800, y), self.cache))
                y = y + 30
            
            # Highlight the selected option.
            options[self.menu].select()
            
            # Draw the options to the screen.    
            for x in range(len(options)):
                self.canvas.canvas.blit(options[x].rend, options[x].pos)
            
            self.menu_rects = []
        
            # Run through the options list.
            for x in range(len(options)):
                # Add a collidable rectangle to a list for mouse input processing.
                self.menu_rects.append(options[x].rend.get_rect(topleft=options[x].pos))
                
            # Scale the rect objects so they corospond to the scaled disaply output.
            for x in range(len(self.menu_rects)):
                self.menu_rects[x] = utils.scale_rect(self.menu_rects[x], real_w, real_h)
