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
import math

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
        self.choice_flag = False
        self.con_length = 0
        
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
        
        # Create an NPC sprite and add it to the group as well.
        self.npc = self.gamedata.npc
        self.all_sprites_list.add(self.npc)
        
        # Make and add an animated campfire instance.
        self.campfire = campfire.Campfire(cache)
        self.all_sprites_list.add(self.campfire)
        
        self.npc.rect.top = 400
        self.npc.rect.left = 300
        
        self.campfire.rect.top = 900
        self.campfire.rect.left = 500
        
        self.npc_move_counter = 0
        self.npc_flag = "down"
        
        self.pre_x = []
        self.pre_y = []
        
        self.response_flag = None
    
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the forest theme for now.
        self.sound.play_music(self.song)
        
        self.moved = False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Escape key pulls up the party screen.
                if event.key == pygame.K_ESCAPE and self.gamedata.npc.dialog_toggle == None:
                    self.gamedata.next_scene = "PartyScreen"
                    self.gamedata.previous_scene = "GameScene"
                # Space and Enter interact with things.
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    if self.gamedata.npc.dialog_toggle == None:
                        # Collision/gamedata logic to detect the proper NPC and conversation goes here. Maybe a function call.
                        dist = math.hypot((self.player.rect.center[0] - self.npc.rect.center[0]),(self.player.rect.center[1] - self.npc.rect.center[1]))
                        if dist < 50: # Simple proximity detection.
                            self.gamedata.npc.dialog_toggle = "conversation1"
                    else:
                        # Allow the player to continue past the NPC's response to the dialog choice.
                        if self.response_flag != None:
                            self.gamedata.npc.dialog_toggle = None
                            self.choice_flag = False
                            self.gamedata.npc.conversation_counter = 0
                            self.response_flag = None
                            self.dialog.menu = 0
                        # Dialog choice selection.
                        elif self.choice_flag == True and self.gamedata.npc.conversation_counter == (self.con_length - 1):
                            # Do something with the dialog choice here.
                            self.response_flag = self.dialog.menu
                        # Just increment through the conversation.
                        elif self.con_length > self.gamedata.npc.conversation_counter:
                            self.gamedata.npc.conversation_counter = self.gamedata.npc.conversation_counter + 1
                
                # Single button hits, used for dialog.
                if self.gamedata.npc.dialog_toggle != None and self.gamedata.npc.conversation_counter == (self.con_length - 1):
                    # Down arrow or S.
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.dialog.menu = self.dialog.menu + 1
                        if self.dialog.menu == len(self.choices):
                            self.dialog.menu = 0
                    # Up arrow or W.
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.dialog.menu = self.dialog.menu - 1
                        if self.dialog.menu == -1:
                            self.dialog.menu = len(self.choices) - 1
                    
        if self.gamedata.npc.dialog_toggle == None:
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
        
        # The NPC should stop if you are talking to him.
        if self.gamedata.npc.dialog_toggle == None:
        
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
        
        # Get the conversation data from the NPC object.
        if self.gamedata.npc.dialog_toggle != None:
            self.conversationdata, self.choice_flag, self.choices, self.responses = self.gamedata.npc.get_dialog(self.gamedata.npc.dialog_toggle)
            self.con_length = len(self.conversationdata)
        
        # End the conversation if we hit the last element in the dialog list.
        if self.gamedata.npc.conversation_counter == self.con_length and self.gamedata.npc.dialog_toggle != None:
            self.gamedata.npc.conversation_counter = 0
            self.gamedata.npc.dialog_toggle = None
        
    # Draws things.
    def Render(self, screen, real_w, real_h):
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        self.canvas = virtualscreen.VirtualScreen(real_w, real_h)
        # Re initialize the dialog object just in case the screen was resized.
        self.dialog = dialog.Dialog(self.cache, self.canvas, self.gamedata, self.dialog.menu)
        
        # Move the map view along with the player.
        self.group.center(self.player.rect.center)
        
        # Add the sprites in the area to the group so that they move properly with the scrolling map.
        
        self.group.add(self.npc)
        self.group.add(self.campfire)
        self.group.add(self.player)
        
        # Draw the scolled view.
        self.group.draw(self.canvas.canvas)
        
        # Draw the response dialog if needed.
        if self.response_flag != None:
            self.dialog.render(self.responses[self.dialog.menu])
        
        # Draw the dialog with a choice box if needed.
        elif self.choice_flag == True and self.gamedata.npc.conversation_counter == (self.con_length - 1):
            self.dialog.render(self.conversationdata[self.gamedata.npc.conversation_counter], self.choices, real_w, real_h)
        
        # Draw the dialog on the screen.
        elif self.gamedata.npc.dialog_toggle != None:
            self.dialog.render(self.conversationdata[self.gamedata.npc.conversation_counter])
            
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(self.canvas.render(), (0, 0))
        
        
