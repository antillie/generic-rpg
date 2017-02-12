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
import pyganim

# This class represents the player character.
class Hero(pygame.sprite.Sprite):
    
    # Init builds everything.
    def __init__(self, cache, direction, width=32, height=48):
        # Call the parent class constructor.
        super(Hero, self).__init__()
        self.direction = direction
        
        # Start with a transparant surface the size of our sprite and make a rect for it.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        self.rect = self.image.get_rect()
        
        # Set the standing still images.
        self.front_standing = cache.get_char_sprite("character.png", 0, 0, 32, 48)
        self.back_standing = cache.get_char_sprite("character.png", 0, 144, 32, 48)
        self.left_standing = cache.get_char_sprite("character.png", 0, 48, 32, 48)
        self.right_standing = cache.get_char_sprite("character.png", 0, 96, 32, 48)
        
        # Draw the starting image.
        if self.direction == "up":
            self.image.blit(self.back_standing, (0, 0))
        elif self.direction == "down":
            self.image.blit(self.front_standing, (0, 0))
        elif self.direction == "left":
            self.image.blit(self.left_standing, (0, 0))
        elif self.direction == "right":
            self.image.blit(self.right_standing, (0, 0))
        else:
            raise Exception("You must pass in a valid direction for the character to be facing.")
        
        # Set the walking animation speed. (in seconds)
        anim_speed = 0.15
        
        # Define the still images to use for each frame of the animation.
        # Format: Image file, top left corner of the part of the file that we want (in x, y format), character width, character height.
        goingUpImages = [
            (cache.get_char_sprite("character.png", 0, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 144, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 144, width, height), anim_speed)
        ]
        goingDownImages = [
            (cache.get_char_sprite("character.png", 0, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 0, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 0, width, height), anim_speed)
        ]
        goingLeftImages = [
            (cache.get_char_sprite("character.png", 0, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 48, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 48, width, height), anim_speed)
        ]
        goingRightImages = [
            (cache.get_char_sprite("character.png", 0, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 32, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 64, 96, width, height), anim_speed),
            (cache.get_char_sprite("character.png", 96, 96, width, height), anim_speed)
        ]
        
        # Create a dictionary to hold the animation objects.
        self.animObjs = {}
        self.animObjs["front_walk"] = pyganim.PygAnimation(goingDownImages)
        self.animObjs["back_walk"] = pyganim.PygAnimation(goingUpImages)
        self.animObjs["left_walk"] = pyganim.PygAnimation(goingLeftImages)
        self.animObjs["right_walk"] = pyganim.PygAnimation(goingRightImages)
        
        # Create the conductor object that will do the actual animation.
        self.moveConductor = pyganim.PygConductor(self.animObjs)
    
    # Displays the walking animation on the screen.
    def update_image(self, direction):
        
        if direction == None:
            if self.direction == "up":
                self.image.fill(colors.black)
                self.image.blit(self.back_standing, (0, 0))
            if self.direction == "down":
                self.image.fill(colors.black)
                self.image.blit(self.front_standing, (0, 0))
            if self.direction == "left":
                self.image.fill(colors.black)
                self.image.blit(self.left_standing, (0, 0))
            if self.direction == "right":
                self.image.fill(colors.black)
                self.image.blit(self.right_standing, (0, 0))
        else:
            self.direction = direction
            if self.direction == "up":
                self.image.fill(colors.black)
                self.animObjs["back_walk"].blit(self.image, (0, 0))
            if self.direction == "down":
                self.image.fill(colors.black)
                self.animObjs["front_walk"].blit(self.image, (0, 0))
            if self.direction == "left":
                self.image.fill(colors.black)
                self.animObjs["left_walk"].blit(self.image, (0, 0))
            if self.direction == "right":
                self.image.fill(colors.black)
                self.animObjs["right_walk"].blit(self.image, (0, 0))

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
        #self.player = Hero(self.cache, "down")
        self.player = self.gamedata.hero
        # Initialize the sprites group.
        self.all_sprites_list = pygame.sprite.Group()
        # Then add the player object to it.
        self.all_sprites_list.add(self.player)
        
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
        
        # Look for keys being held down. Arrow keys or WASD for movment.
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.rect_y = self.rect_y - 3
            self.moved = True
            self.player.update_image("up")
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect_y = self.rect_y + 3
            self.moved = True
            self.player.update_image("down")
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.rect_x = self.rect_x - 3
            self.moved = True
            self.player.update_image("left")
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect_x = self.rect_x + 3
            self.moved = True
            self.player.update_image("right")
            
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
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
