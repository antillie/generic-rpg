#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
import virtualscreen
import cache
import sound
import base
import colors
import credits_s
import gameinit

sound = sound.JukeBox()

class Option:
    # Used for entries in menus.
    active = False
    
    def __init__(self, text, pos, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.font = font
        self.set_rend()
        
    def set_rend(self):
        self.rend = cache.get_font(self.font, 20).render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.active:
            return colors.off_yellow
        else:
            return colors.grey
            
    def select(self):
        self.active = True
        self.set_rend()

class TitleScene(base.SceneBase):
    # Main title screen. You can start/load a game, view the credits, or close the program from here.
    def __init__(self, song="enchantedfestivalloop.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        self.menu = 1
        # initialize the mixer. This only needs to be done in the title screen.
        pygame.mixer.init()
        # Stop whatever music is playing, if any.
        sound.stop_music()
        # Play the title theme.
        sound.play_music(self.song)
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Enter key.
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # New game.
                    if self.menu == 0:
                        sound.stop_music()
                        # Switch to the main game scene.
                        self.SwitchToScene(gameinit.GameScene())
                    # Load game.
                    if self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Roll credits.
                    if self.menu == 2:
                        sound.stop_music()
                        # Switch to the credits scene.
                        self.SwitchToScene(credits_s.CreditsScene())
                    # Exit the game.
                    if self.menu == 3:
                        self.Terminate()
                # Down arrow.
                if event.key == pygame.K_DOWN:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 4:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow.
                if event.key == pygame.K_UP:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 3
    
    # Internal game logic. Doesn't really apply to the main menu.
    def Update(self):
        pass
        
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Title text.
        title = cache.get_font(["Immortal"], 70).render("Generic RPG Name",True,colors.white)
        canvas.canvas.blit(title, [175, 60])
        
        menu_x = 430
        
        # Menu entries.
        self.options = [
            Option("New Game", (menu_x, 300)),
            Option("Load Game", (menu_x, 330)),
            Option("Credits", (menu_x, 360)),
            Option("Exit", (menu_x, 390))
            ]
        
        # Highlight the currently selected menu item.    
        self.options[self.menu].select()
        
        # Draw the menu entries.
        for x in range(len(self.options)):
            canvas.canvas.blit(self.options[x].rend, self.options[x].pos)
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
        
