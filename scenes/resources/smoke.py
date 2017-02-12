#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class Particle():
    def __init__(self, startx, starty, color, height, drift):
        self.y = random.randint(starty - height, starty)
        self.x = int((starty - self.y) * (drift / 2.0)) + startx
        self.color = color
        self.sx = startx
        self.sy = starty
        self.height = height
        self.drift = drift
        
    def move(self):
        if self.y < random.randint((self.sy - self.height -20 ), (self.sy - self.height + 20)):
            self.x=self.sx
            self.y=self.sy
        else:
            self.y = self.y - random.randint(0, 2)
        
        if self.drift >= 0:
            self.x = self.x + random.randint(-2, 2 + self.drift)
        else:
            self.x = self.x + random.randint(-2 + self.drift , 2)
