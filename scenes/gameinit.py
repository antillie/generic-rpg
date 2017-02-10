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
    
    def __init__(self, cache, color=colors.brown, width=32, height=48):
        # Call the parent class constructor.
        super(Car, self).__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.white)
        self.image.set_colorkey(colors.white)
        
        # Load the image.
        person = cache.get_alpha_image("character.png")
        
        # Blit the part of the image that we want to our surface.
        self.image.blit(person, (0, 0), (0, 0, 32, 48))
        
        # Draw the character.
        pygame.draw.rect(self.image, colors.brown, [512, 288, width, height])
        
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
        # Player starting position.
        self.rect_x = 512
        self.rect_y = 288
        # Load the map.
        path = os.path.dirname(os.path.realpath(__file__)) + "/maps/initial.tmx"
        path = path.replace('/', os.sep).replace("\\", os.sep)
        self.tmx_data = pytmx.util_pygame.load_pygame(path)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        
        # Initialize the map view.
        screen_size = (1280, 720)
        map_layer = pyscroll.BufferedRenderer(self.map_data, screen_size)
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer)
        
        # Create the player object.
        self.player = Car(self.cache)
        # Initialize the sprites group.
        self.all_sprites_list = pygame.sprite.Group()
        # Then add the player object to it.
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
        
        # Look for keys being held down. Arrow keys or WASD for movment.
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            if self.rect_y < 200 or self.rect_y > 475:
                self.rect_y = self.rect_y - 5
            else:
                self.rect_y = self.rect_y - 5
            
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            if self.rect_y < 200 or self.rect_y > 475:
                self.rect_y = self.rect_y + 5
            else:
                self.rect_y = self.rect_y + 5
            
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            if self.rect_x < 380 or self.rect_x > 870:
                self.rect_x = self.rect_x - 5
            else:
                self.rect_x = self.rect_x - 5
            
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            if self.rect_x < 380 or self.rect_x > 870:
                self.rect_x = self.rect_x + 5
            else:
                self.rect_x = self.rect_x + 5
            
        # Don't let the player walk off the top or bottom of the map.
        if self.rect_x < 0:
            self.rect_x = 0
        elif self.rect_x > 2016:
            self.rect_x = 2016
        
        # Don't let the player walk off the left or right sides of the map.
        if self.rect_y < 0:
            self.rect_y = 0
        elif self.rect_y > 1108:
            self.rect_y = 1108
        
    # Internal game logic.
    def Update(self):
        
        self.player.rect.top = self.rect_y
        self.player.rect.left = self.rect_x
        
        self.all_sprites_list.update()
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Move the map view along with the player.
        self.group.center(self.player.rect.center)
        self.group.add(self.player)
        
        # Draw the scolled view.
        self.group.draw(canvas.canvas)
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
