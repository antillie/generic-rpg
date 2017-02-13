#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import formatting
import colors

# Class that handles dialog and dialog choices.

class Dialog:

    def __init__(self, cache, canvas, gamedata):
        self.menu = None
        self.cache = cache
        self.canvas = canvas
        self.gamedata = gamedata
        
    def render(self, character_name, dialog, choices=["None"]):
        
        #pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(menu_x - 3,7,220,206), 3)
        #pygame.draw.rect(canvas.canvas, colors.menu_blue, pygame.Rect(menu_x,10,214,200), 0)
        
        pygame.draw.rect(self.canvas.canvas, colors.white, pygame.Rect(10, 508 , 1006, 203), 3)
        
        pygame.draw.rect(self.canvas.canvas, colors.menu_blue, pygame.Rect(12, 510 , 1002 ,199), 0)
        
        
        # Draw stuff to surface. Make it look like the battle menu.
