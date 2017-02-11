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

# All characters are instances of this class.
class Character(pygame.sprite.Sprite):
    
    def __init__(self, cache, direction, width=32, height=48):
        # Call the parent class constructor.
        super(Character, self).__init__()
        self.direction = direction
        
        # Start with a black surface the size of our sprite.
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        
        # Load the starting image.
        if self.direction == "up":
            self.person = cache.get_char_sprite("character.png", 0, 144, 32, 48)
        elif self.direction == "down":
            self.person = cache.get_char_sprite("character.png", 0, 0, 32, 48)
        elif self.direction == "left":
            self.person = cache.get_char_sprite("character.png", 0, 48, 32, 48)
        elif self.direction == "right":
            self.person = cache.get_char_sprite("character.png", 0, 96, 32, 48)
        else:
            raise Exception("You must pass in a direction for the character to be facing.")
        
        # Blit the part of the image that we want to our surface.
        self.image.blit(self.person, (0, 0), (0, 0, 32, 48))
        
        # Draw the character.
        pygame.draw.rect(self.image, colors.brown, [512, 288, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
        self.front_standing = cache.get_char_sprite("character.png", 0, 0, 32, 48)
        self.back_standing = cache.get_char_sprite("character.png", 0, 144, 32, 48)
        self.left_standing = cache.get_char_sprite("character.png", 0, 48, 32, 48)
        self.right_standing = cache.get_char_sprite("character.png", 0, 96, 32, 48)
        
        self.animObjs = {}

        anim_speed = 0.15
        
        goingUpimagesAndDurations = [
            (cache.get_char_sprite("character.png", 0, 144, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 32, 144, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 64, 144, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 96, 144, 32, 48), anim_speed)
        ]
        
        goingDownimagesAndDurations = [
            (cache.get_char_sprite("character.png", 0, 0, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 32, 0, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 64, 0, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 96, 0, 32, 48), anim_speed)
        ]
        
        goingLeftimagesAndDurations = [
            (cache.get_char_sprite("character.png", 0, 48, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 32, 48, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 64, 48, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 96, 48, 32, 48), anim_speed)
        ]
        
        goingRightimagesAndDurations = [
            (cache.get_char_sprite("character.png", 0, 96, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 32, 96, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 64, 96, 32, 48), anim_speed),
            (cache.get_char_sprite("character.png", 96, 96, 32, 48), anim_speed)
        ]
        
        self.animObjs["front_walk"] = pyganim.PygAnimation(goingDownimagesAndDurations)
        self.animObjs["back_walk"] = pyganim.PygAnimation(goingUpimagesAndDurations)
        self.animObjs["left_walk"] = pyganim.PygAnimation(goingLeftimagesAndDurations)
        self.animObjs["right_walk"] = pyganim.PygAnimation(goingRightimagesAndDurations)
        
        self.moveConductor = pyganim.PygConductor(self.animObjs)
        
    def update_image(self, direction):
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
    
    def __init__(self, sound, cache, transition, song="forest.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        self.name = "GameScene"
        self.sound = sound
        self.cache = cache
        self.battlebound = 0
        self.transition = transition
        
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
        self.player = Character(self.cache, "down")
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
                    self.SwitchToScene("PartyScreen")
                if event.key == pygame.K_RETURN:
                    print("x: " + str(self.rect_x))
                    print("y: " + str(self.rect_y))
        
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
                self.SwitchToScene("BattleScreen")
        
        if self.battlebound > 1600:
            self.battlebound = 0
            self.sound.stop_music()
            self.transition.run("fadeOutUp")
            self.sound.play_music("awildcreatureappears.ogg")
            self.SwitchToScene("BattleScreen")
    
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
