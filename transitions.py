#!/usr/bin/python
# -*- coding: utf-8 -*-
#      ____        ______                        ______                      _ __  _                 
#     / __ \__  __/ ____/___ _____ ___  ___     /_  __/________ _____  _____(_) /_(_)___  ____  _____
#    / /_/ / / / / / __/ __ `/ __ `__ \/ _ \     / / / ___/ __ `/ __ \/ ___/ / __/ / __ \/ __ \/ ___/
#   / ____/ /_/ / /_/ / /_/ / / / / / /  __/    / / / /  / /_/ / / / (__  ) / /_/ / /_/ / / / (__  ) 
#  /_/    \__, /\____/\__,_/_/ /_/ /_/\___/    /_/ /_/   \__,_/_/ /_/____/_/\__/_/\____/_/ /_/____/  
#        /____/                                                                                      
#
# Adds the ability to do transitions on pygame games
# v0.0.1
# By Death_Miner
# Copyright (c) 2014 Death_Miner
# MIT License

#The MIT License (MIT)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# George's note:
# This version has been modified to be an importable class object.

import pygame
import time

#
# Object class for bypassing dot notation object
#
class Object():
	pass
		
#
# Current transition
# @var string|bool
transition = False

#
# Current transition data
# @var object|bool
transition_data = False

#
# Color to fill the screen when reseting it
# @var list
background_color = [0, 0, 0]

#
# Main screen object for drawing
# @var object
screen = False

#
# Window width
# @var int
window_width = False

#
# Window width
# @var int
window_height = False

#
# See if transitions module has been initialized
# @var bool
inited = False

class Transition:

    def __init__(self, i_screen, i_window_width, i_window_height, i_background_color=[0, 0, 0]):
        global screen, window_width, window_height, background_color, inited
        screen = i_screen
        window_width = i_window_width
        window_height = i_window_height
        background_color = i_background_color
        inited = True
    
    def run(self, name, duration = 1.5, x = -1, y = -1):
        global transition, transition_data
        if inited == False:
            raise Exception("You must init transitions before using it!")
        transition = name
        transition_data = Object()
        transition_data.duration = duration
        transition_data.start = time.process_time()
        transition_data.screen = screen.copy()
        transition_data.current_screen = False
        transition_data.x = x
        transition_data.y = y
    
    def updateScreen(self):
        global transition, transition_data
        if inited == False:
            raise Exception("You must init transitions before using it!")
        if transition != False:
            current_time = time.process_time()
            time_ratio = (current_time - transition_data.start) / transition_data.duration
            if time_ratio > 1.0:
                transition_data = False
                transition = False
            else:
                screen.fill(background_color)
                if transition == "fadeOutUp":
                    transition_data.screen.set_alpha(255-255*time_ratio)
                    rect1 = transition_data.screen.get_rect()
                    transition_data.current_screen = pygame.transform.smoothscale(transition_data.screen, [int(rect1[2]*(1+time_ratio)), int(rect1[3]*(1+time_ratio))])
                    transition_data.current_screen = pygame.transform.rotate(transition_data.current_screen, 40*time_ratio)
                elif transition == "fadeOutDown":
                    transition_data.screen.set_alpha(255-255*time_ratio)
                    rect1 = transition_data.screen.get_rect()
                    transition_data.current_screen = pygame.transform.smoothscale(transition_data.screen, [int(rect1[2]*(1-time_ratio)), int(rect1[3]*(1-time_ratio))])
    
    
                rect2 = transition_data.current_screen.get_rect()
    
                if transition_data.x != -1:
                    x = (rect2[2]*transition_data.x)/window_width
                else:
                    x = rect2[2]/2
    
                if transition_data.y != -1:
                    y = (rect2[3]*transition_data.y)/window_height
                else:
                    y = rect2[3]/2
    
                screen.blit(transition_data.current_screen, [window_width/2-x, window_height/2-y])
        return transition
