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
        
    def render(self, dialog, choices=["None"], character_name=None):
        
        pygame.draw.rect(self.canvas.canvas, colors.white, pygame.Rect(10, 508 , 1006, 203), 3)
        
        pygame.draw.rect(self.canvas.canvas, colors.menu_blue, pygame.Rect(12, 510 , 1002 ,199), 0)
        
        self.dialog = [
            formatting.MenuOption(dialog, (22, 520), self.cache)
            ]
        
        for x in range(len(self.dialog)):
            self.canvas.canvas.blit(self.dialog[x].rend, self.dialog[x].pos)
        
        if choices[0] != "None":
            options = []
            y = 520
            for x in range(len(choices)):
                options.append(formatting.MenuOption(choices[x], (800, y), self.cache))
                y = y + 30
                
        
            for x in range(len(options)):
                self.canvas.canvas.blit(options[x].rend, options[x].pos)
