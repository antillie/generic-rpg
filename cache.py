#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os

# Font object generator.
def make_font(fonts, size):
    
    if fonts[0] == "Immortal":
        path = os.path.dirname(os.path.realpath(__file__)) + "/fonts/" + fonts[0] + ".ttf"
        path = path.replace('/', os.sep).replace('\\', os.sep)
        return pygame.font.Font(path, size)
    
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

# Cache generated font objects so we don't have to call the generator all the time.
_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

# Cache image objects so we aren't initializing the same image over and over.
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
            temp_path = os.path.dirname(os.path.realpath(__file__)) + "/images/" + path
            canonicalized_path = temp_path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path).convert()
            _image_library[path] = image
        return image