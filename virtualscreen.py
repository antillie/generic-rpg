#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

# Certral location for our virtual screen object.
class VirtualScreen:    
    def __init__(self, real_w, real_h, width=1280.0, height=720.0):
        self.width = width
        self.height = height
        self.real_w = real_w
        self.real_h = real_h
        # Create a virtual screen with a static size. This makes positioning things on the screen much easier.
        self.canvas = pygame.Surface((self.width, self.height))
        
        self.w_ratio = self.real_w / self.width
        self.h_ratio = self.real_h / self.height
        
    def render(self):
        # Upscale the virtual screen to the size of the actual screen and return the resulting surface object so it can be drawn.
        return pygame.transform.smoothscale(self.canvas, (self.real_w, self.real_h))
