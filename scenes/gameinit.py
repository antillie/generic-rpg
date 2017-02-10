#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors

# The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
class GameScene(base.SceneBase):
    
    def __init__(self, sound, cache, song="plesantcreekloop.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        self.name = "GameScene"
        self.sound = sound
        self.cache = cache
        self.rect_x = 512
        self.rect_y = 288
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the town theme for now.
        self.sound.play_music(self.song)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Escape key pulls up the party screen.
                if event.key == pygame.K_ESCAPE:
                    self.SwitchToScene("PartyScreen")
                
        if pressed_keys[pygame.K_UP]:
            self.rect_y = self.rect_y - 5
        if pressed_keys[pygame.K_DOWN]:
            self.rect_y = self.rect_y + 5
        if pressed_keys[pygame.K_LEFT]:
            self.rect_x = self.rect_x - 5
        if pressed_keys[pygame.K_RIGHT]:
            self.rect_x = self.rect_x + 5
                
        if self.rect_x < 0:
            self.rect_x = 0
        if self.rect_y < 0:
            self.rect_y = 0
        
        if self.rect_x > 992:
            self.rect_x = 992
        if self.rect_y > 528:
            self.rect_y = 528
        
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Filling a 1024x576 screen requires 16x9 64x64 pixel tiles.
        x_count = 16
        y_count = 9
        
        for y in range(y_count):
            for x in range(x_count):
                canvas.canvas.blit(self.cache.get_image("landscaping/mountain_landscape.png"), (x * 64, y * 64), (448, 128, 64, 64))
        
        pygame.draw.rect(canvas.canvas, colors.brown, pygame.Rect(self.rect_x, self.rect_y, 32, 48))
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
