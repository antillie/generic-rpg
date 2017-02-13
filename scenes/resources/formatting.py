#!/usr/bin/python
# -*- coding: utf-8 -*-

import colors

# Used for entries in menus.
class MenuOption:
    
    active = False
    
    def __init__(self, text, pos, cache, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.font = font
        self.cache = cache
        self.set_rend()
        
    def set_rend(self):
        self.rend = self.cache.get_font(self.font, 20).render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.active:
            return colors.off_yellow
        else:
            return colors.white
            
    def select(self):
        self.active = True
        self.set_rend()
