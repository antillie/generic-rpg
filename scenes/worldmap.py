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

# World map.
class WorldMap(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata, song="worldmap.mp3"):
        self.song = song
        self.sound = sound
        self.cache = cache
        self.battlebound = 0
        self.transition = transition
        self.gamedata = gamedata
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        self.canvas = virtualscreen.VirtualScreen(gamedata.current_w, gamedata.current_h)
        
        # Load the map.
        path = os.path.dirname(os.path.realpath(__file__)) + "/maps/world_map.tmx"
        path = path.replace('/', os.sep).replace("\\", os.sep)
        self.tmx_data = pytmx.util_pygame.load_pygame(path)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        
        # Initialize the map view.
        screen_size = (1280, 720)
        map_layer = pyscroll.BufferedRenderer(self.map_data, screen_size)
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        
        # Create the player object.
        self.player = self.gamedata.party_slots[0]
        # Initialize the sprites group.
        self.all_sprites_list = pygame.sprite.Group()
        # Then add the player object to it.
        self.all_sprites_list.add(self.player)
    
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the forest theme for now.
        self.sound.play_music(self.song)
        
        self.moved = False
        self.future_x = 0
        self.future_y = 0
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Escape key pulls up the party screen.
                if event.key == pygame.K_ESCAPE and self.gamedata.npc.dialog_toggle == None:
                    self.gamedata.next_scene = "PartyScreen"
                    self.gamedata.previous_scene = "WorldMap"
        
        # Look for keys being held down. Arrow keys or WASD for movment.
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.moved = True
            self.player.update_image("up")
            self.future_y = -3
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.moved = True
            self.player.update_image("down")
            self.future_y = 3
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.moved = True
            self.player.update_image("left")
            self.future_x = -3
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.moved = True
            self.player.update_image("right")
            self.future_x = 3
            
        # Rect that represents the bottom half of the player sprite.
        player_feet = pygame.Rect(self.player.rect.left, self.player.rect.top + 16, 32, 24)
        
        # Rect that represents where the player is trying to go.
        future_location = player_feet.move(self.future_x, self.future_y)
        
        # Collision avoidance.
        for layer in self.tmx_data.visible_layers:
            # The name of the object layer in the TMX file we are interested in. There could be more than one.
            if layer.name == "Meta":
                for obj in layer:
                    # Look for a collision. Nullify player movment if found.
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(future_location) == True:
                        self.future_y = 0
                        self.future_x = 0
                        self.moved = False
            # Look for collisions with zone exit points.
            elif layer.name == "Exit":
                for obj in layer:
                    # Look for a collision.
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(player_feet) == True:
                        if obj.name == "GrassArea":
                            self.sound.stop_music()
                            self.gamedata.next_scene = "GameScene"
                            self.gamedata.previous_scene = "WorldMap"
                            self.gamedata.worldpos_x = 500
                            self.gamedata.worldpos_y = 350
        
        if self.moved:
            self.battlebound = self.battlebound + 3
            self.player.moveConductor.play()
        else:
            self.player.moveConductor.stop()
            self.player.update_image(None)
            
        self.gamedata.worldpos_x = self.gamedata.worldpos_x + self.future_x
        self.gamedata.worldpos_y = self.gamedata.worldpos_y + self.future_y
        
    # Internal game logic.
    def Update(self):
        
        self.player.rect.top = self.gamedata.worldpos_y
        self.player.rect.left = self.gamedata.worldpos_x
        self.all_sprites_list.update()
        
        # There is a 0.5% chance of a random battle every time the player moves past a certain distance.
        if self.battlebound > 250 and self.moved:
            if utils.rand_chance(5):
                self.battlebound = 0
                self.sound.stop_music()
                self.sound.play_music("awildcreatureappears.ogg")
                self.transition.run("fadeOutUp")
                self.gamedata.next_scene = "BattleScreen"
                self.gamedata.previous_scene = "WorldMap"
                if self.gamedata.worldpos_y > 490:
                    self.gamedata.battlebackground = "articlandscape.png"
                else:
                    self.gamedata.battlebackground = "forestbackground.png"
                    
        if self.battlebound > 1800 and self.moved:
            self.battlebound = 0
            self.sound.stop_music()
            self.sound.play_music("awildcreatureappears.ogg")
            self.transition.run("fadeOutUp")
            self.gamedata.next_scene = "BattleScreen"
            self.gamedata.previous_scene = "GameScene"
            if self.gamedata.worldpos_y > 490:
                self.gamedata.battlebackground = "articlandscape.png"
            else:
                self.gamedata.battlebackground = "forestbackground.png"
        
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        self.canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Move the map view along with the player.
        self.group.center(self.player.rect.center)
        
        # Add the sprites in the area to the group so that they move properly with the scrolling map.
        self.group.add(self.player)
        
        # Draw the scolled view.
        self.group.draw(self.canvas.canvas)
            
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(self.canvas.render(), (0, 0))
        
        
