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
import campfire
import dialog

# An area in the game. Different variations of this class will need to load different maps, characters, battles, dialog, ect. Each area will be its own class (and .py file).
class GameScene(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata, song="forest.mp3"):
        self.song = song
        self.sound = sound
        self.cache = cache
        self.battlebound = 0
        self.transition = transition
        self.gamedata = gamedata
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        self.canvas = virtualscreen.VirtualScreen(gamedata.current_w, gamedata.current_h)
        
        # Create a dialog object.
        self.dialog = dialog.Dialog(cache, self.canvas, gamedata)
        self.dialog_toggle = False
        
        # Make an animated campfire instance.
        self.campfire = campfire.Campfire(cache)
        
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
        
        self.npc = self.gamedata.npc
        self.all_sprites_list.add(self.npc)
        
        self.all_sprites_list.add(self.campfire)
        
        self.npc.rect.top = 400
        self.npc.rect.left = 300
        
        self.campfire.rect.top = 900
        self.campfire.rect.left = 500
        
        self.npc_move_counter = 0
        self.npc_flag = "down"
        
        self.pre_x = []
        self.pre_y = []
    
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
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    if not self.dialog_toggle:
                        self.dialog_toggle = True
                    else:
                        self.dialog_toggle = False
                    
        
        # Look for keys being held down. Arrow keys or WASD for movment.
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.rect_y = self.rect_y - 3
            self.moved = True
            self.player.update_image("up")
            self.pre_y.append(self.rect_y)
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect_y = self.rect_y + 3
            self.moved = True
            self.player.update_image("down")
            self.pre_y.append(self.rect_y)
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.rect_x = self.rect_x - 3
            self.moved = True
            self.player.update_image("left")
            self.pre_x.append(self.rect_x)
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect_x = self.rect_x + 3
            self.moved = True
            self.player.update_image("right")
            self.pre_x.append(self.rect_x)
            
        if self.moved:
            self.battlebound = self.battlebound + 3
            self.player.moveConductor.play()
        else:
            self.player.moveConductor.stop()
            self.player.update_image(None)
        
        # Collision detection.
        for layer in self.tmx_data.visible_layers:
            # The name of the object layer in the TMX file we are interested in. There could be more than one.
            if layer.name == "Meta":
                for obj in layer:
                    # Rect that represents the bottom half of the player sprite.
                    player_feet = pygame.Rect(self.player.rect.left, self.player.rect.top + 16, 32, 24)
                    
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(player_feet) == True:
                        # Move the player back to where they were before the collision.
                        self.rect_x = self.pre_x[-3]
                        self.rect_y = self.pre_y[-3]
                        # Delete the colliding point in the trail.
                        del self.pre_x[-1]
                        del self.pre_y[-1]
                        # Then add a new non colliding point.
                        self.pre_x.append(self.rect_x)
                        self.pre_y.append(self.rect_y)
        
        # Don't let the movement trail grow forever.
        if len(self.pre_x) > 500:
            del self.pre_x[:-250]
        if len(self.pre_y) > 500:
            del self.pre_y[:-250]
        
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
        
        if self.npc_move_counter < 200 and self.npc_flag == "down":
            
            self.npc_move_counter = self.npc_move_counter + 1
            
            self.npc.rect.top =  self.npc.rect.top + 2
            self.npc.update_image("down")
            self.npc.moveConductor.play()
            
            if self.npc_move_counter == 200:
                self.npc_flag = "up"
            
        if self.npc_flag == "up":
            self.npc_move_counter = self.npc_move_counter - 1
            
            self.npc.rect.top =  self.npc.rect.top - 2
            self.npc.update_image("up")
            self.npc.moveConductor.play()
            
            if self.npc_move_counter == 0:
                self.npc_flag = "down"
        
        self.campfire.update_image()
        self.campfire.moveConductor.play()
                
        self.player.rect.top = self.rect_y
        self.player.rect.left = self.rect_x
        self.all_sprites_list.update()
        
        # There is a 0.5% chance of a random battle every time the player moves past a certain distance.
        if self.battlebound > 250 and self.moved:
            if utils.rand_chance(5):
                self.battlebound = 0
                self.sound.stop_music()
                self.sound.play_music("awildcreatureappears.ogg")
                self.transition.run("fadeOutUp")
                self.gamedata.next_scene = "BattleScreen"
                self.gamedata.previous_scene = "GameScene"
                    
        if self.battlebound > 1800 and self.moved:
            self.battlebound = 0
            self.sound.stop_music()
            self.sound.play_music("awildcreatureappears.ogg")
            self.transition.run("fadeOutUp")
            self.gamedata.next_scene = "BattleScreen"
            self.gamedata.previous_scene = "GameScene"
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Move the map view along with the player.
        self.group.center(self.player.rect.center)
        
        # Add the sprites in the area to the group so that they move properly with the scrolling map.
        self.group.add(self.player)
        self.group.add(self.npc)
        self.group.add(self.campfire)
        
        # Draw the scolled view.
        self.group.draw(self.canvas.canvas)
        
        if self.dialog_toggle:
            self.dialog.render("The Hero", "bla bla bla",)
            
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(self.canvas.render(), (0, 0))
        
        
