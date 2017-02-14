#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import formatting
import colors

# Class that handles dialog and dialog choices.

class Dialog:

    def __init__(self, cache, canvas, gamedata):
        self.cache = cache
        self.canvas = canvas
        self.gamedata = gamedata
        
    def render(self, dialog, character_name=None, choices=["None"]):
        
        pygame.draw.rect(self.canvas.canvas, colors.white, pygame.Rect(10, 508 , 1006, 203), 3)
        
        pygame.draw.rect(self.canvas.canvas, colors.menu_blue, pygame.Rect(12, 510 , 1002 ,199), 0)
