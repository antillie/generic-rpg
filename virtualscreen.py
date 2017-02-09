#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

class VirtualScreen:
    # Certral location for our virtual screen object. 1024x576 is a 16x9 ratio that is also divisible by 64, this allows us to use 64x64 pixel background tiles easily with the proper aspect ratio.
    def __init__(self, real_w, real_h, width=1024.0, height=576.0):
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
