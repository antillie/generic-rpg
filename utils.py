#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import random

# Scales a rect object to fit properly on the scaled display.
def scale_rect(rect, real_w, real_h):
    canvas = virtualscreen.VirtualScreen(real_w, real_h)
    rect.left = rect.left * canvas.w_ratio
    rect.top = rect.top * canvas.h_ratio
    rect.width = rect.width * canvas.w_ratio
    rect.height = rect.height * canvas.h_ratio
    return rect

# Random chance function.
def rand_chance(chance):
    gen = random.SystemRandom()
    result = gen.randrange(1000)
    if result < chance:
        return True
    else:
        return False
