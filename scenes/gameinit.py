#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import pyscroll
import pytmx.util_pygame
import os
import utils

class Car(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color=colors.brown, width=32, height=48):
        # Call the parent class (Sprite) constructor
        super(Car, self).__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.brown)
        self.image.set_colorkey(colors.brown)
 
        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, colors.brown, [0, 0, width, height])
        
        # Instead we could load a proper pciture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

# The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
class GameScene(base.SceneBase):
    
    def __init__(self, sound, cache, song="forest.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        self.name = "GameScene"
        self.sound = sound
        self.cache = cache
        self.rect_x = 512
        self.rect_y = 288
        
        path = os.path.dirname(os.path.realpath(__file__)) + "/maps/initial.tmx"
        path = path.replace('/', os.sep).replace("\\", os.sep)
        self.tmx_data = pytmx.util_pygame.load_pygame(path)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        
        screen_size = (1280, 720)
        map_layer = pyscroll.BufferedRenderer(self.map_data, screen_size)
        
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer)
        
        self.player = Car()
        
        self.all_sprites_list = pygame.sprite.Group()
        
        self.all_sprites_list.add(self.player)
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the town theme for now.
        self.sound.play_music(self.song)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Escape key pulls up the party screen.
                if event.key == pygame.K_ESCAPE:
                    self.SwitchToScene("PartyScreen")
                if event.key == pygame.K_RETURN:
                    print("x: " + str(self.rect_x))
                    print("y: " + str(self.rect_y))
                
        if pressed_keys[pygame.K_UP]:
            
            if self.rect_y < 200 or self.rect_y > 475:
            
                self.rect_y = self.rect_y - 5
            else:
                self.rect_y = self.rect_y - 2
            
            
        if pressed_keys[pygame.K_DOWN]:
            
            if self.rect_y < 200 or self.rect_y > 475:
            
                self.rect_y = self.rect_y + 5
            else:
                self.rect_y = self.rect_y + 2
            
        if pressed_keys[pygame.K_LEFT]:
            
            if self.rect_x < 380 or self.rect_x > 870:
            
                self.rect_x = self.rect_x - 5
            else:
                self.rect_x = self.rect_x - 2
            
        if pressed_keys[pygame.K_RIGHT]:
            
            if self.rect_x < 380 or self.rect_x > 870:
            
                self.rect_x = self.rect_x + 5
            else:
                self.rect_x = self.rect_x + 2
            
                
        if self.rect_x < 0:
            self.rect_x = 0
        if self.rect_y < 0:
            self.rect_y = 0
        
        if self.rect_x > 1248:
            self.rect_x = 1248
        if self.rect_y > 672:
            self.rect_y = 672
        
    # Internal game logic.
    def Update(self):
        
        self.player.rect.top = self.rect_y
        self.player.rect.left = self.rect_x
        
        self.all_sprites_list.update()
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        scaled_w = self.player.rect.center[0] * 1.6
        scaled_h = self.player.rect.center[1] * 1.6
        new_center = (scaled_w, scaled_h)
        
        self.group.center(new_center)
        
        self.group.add(self.player)
        
        self.group.draw(canvas.canvas)
        
        self.all_sprites_list.draw(canvas.canvas)
        
        pygame.draw.rect(canvas.canvas, colors.brown, self.player.rect)
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
