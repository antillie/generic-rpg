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
import smoke

# The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
class GameScene(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata, song="forest.mp3"):
        self.song = song
        self.sound = sound
        self.cache = cache
        self.battlebound = 0
        self.transition = transition
        self.gamedata = gamedata
        
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
        self.player = self.gamedata.hero
        # Initialize the sprites group.
        self.all_sprites_list = pygame.sprite.Group()
        # Then add the player object to it.
        self.all_sprites_list.add(self.player)
        
        self.smoke_particles = []
        for number in range(300):
            self.smoke_particles.append(smoke.Particle(225, 575, (60, 60, 60), 100, 1))
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the forest theme for now.
        self.sound.play_music(self.song)
        
        self.moved = False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Escape key pulls up the party screen.
                if event.key == pygame.K_ESCAPE:
                    self.gamedata.next_scene = "PartyScreen"
                    self.gamedata.previous_scene = "GameScene"
                if event.key == pygame.K_RETURN:
                    print(self.rect_y)
        
        # Look for keys being held down. Arrow keys or WASD for movment.
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.rect_y = self.rect_y - 3
            self.moved = True
            self.player.update_image("up")
            
            if self.rect_y > 330 and self.rect_y < 770:
                for particle in self.smoke_particles:
                    particle.y = particle.y + 3
                    particle.sy = particle.sy + 3
                
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect_y = self.rect_y + 3
            self.moved = True
            self.player.update_image("down")
            
            if self.rect_y > 330 and self.rect_y < 770:
                for particle in self.smoke_particles:
                    particle.y = particle.y - 3
                    particle.sy = particle.sy - 3
            
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.rect_x = self.rect_x - 3
            self.moved = True
            self.player.update_image("left")
            
            if self.rect_x > 625 and self.rect_x < 1400:
                for particle in self.smoke_particles:
                    particle.x = particle.x + 3
                    particle.sx = particle.sx + 3
            
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect_x = self.rect_x + 3
            self.moved = True
            self.player.update_image("right")
            
            if self.rect_x > 625 and self.rect_x < 1400:
                for particle in self.smoke_particles:
                    particle.x = particle.x - 3
                    particle.sx = particle.sx - 3
            
        if self.moved:
            self.battlebound = self.battlebound + 3
            self.player.moveConductor.play()
        else:
            self.player.moveConductor.stop()
            self.player.update_image(None)
            
        # Don't let the player walk off the top or bottom of the map.
        if self.rect_x < 0:
            self.rect_x = 0
        elif self.rect_x > 2016:
            self.rect_x = 2016
        
        # Don't let the player walk off the left or right sides of the map.
        if self.rect_y < 0:
            self.rect_y = 0
        elif self.rect_y > 1104:
            self.rect_y = 1104
        
    # Internal game logic.
    def Update(self):
        
        self.player.rect.top = self.rect_y
        self.player.rect.left = self.rect_x
        self.all_sprites_list.update()
        
        # There is a 0.5% chance of a random battle every time the player moves past a certain distance.
        if self.battlebound > 240:
            if utils.rand_chance(5):
                self.battlebound = 0
                self.sound.stop_music()
                self.sound.play_music("awildcreatureappears.ogg")
                self.transition.run("fadeOutUp")
                self.gamedata.next_scene = "BattleScreen"
                self.gamedata.previous_scene = "GameScene"
                    
        if self.battlebound > 1600:
            self.battlebound = 0
            self.sound.stop_music()
            self.transition.run("fadeOutUp")
            self.sound.play_music("awildcreatureappears.ogg")
            self.gamedata.next_scene = "BattleScreen"
            self.gamedata.previous_scene = "GameScene"
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Move the map view along with the player.
        self.group.center(self.player.rect.center)
        self.group.add(self.player)
        
        
        
        
            
        # Draw the scolled view.
        self.group.draw(canvas.canvas)
        
        for particle in self.smoke_particles:
            particle.move()
            pygame.draw.rect(canvas.canvas, particle.color, pygame.Rect(particle.x, particle.y, 1, 1))
            
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
        
        
