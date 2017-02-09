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
import utils

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
        # Initialise the menu rects list.
        self.menu_rects = []
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Enter key.
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # New game.
                    if self.menu == 0:
                        sound.stop_music()
                        # Switch to the main game scene.
                        self.SwitchToScene(gameinit.GameScene())
                    # Load game.
                    elif self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Game options.
                    elif self.menu == 2:
                        # Not yet implimented.
                        pass
                    # Roll credits.
                    elif self.menu == 3:
                        sound.stop_music()
                        # Switch to the credits scene.
                        self.SwitchToScene(credits_s.CreditsScene())
                    # Exit the game.
                    elif self.menu == 4:
                        self.Terminate()
                # Down arrow.
                elif event.key == pygame.K_DOWN:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 5:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow.
                elif event.key == pygame.K_UP:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 4
            # Mouse moved.
            elif event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                for x in range(len(self.menu_rects)):
                    if self.menu_rects[x].collidepoint(mpos):
                        self.menu = x
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    for x in range(len(self.menu_rects)):
                        if self.menu_rects[x].collidepoint(mpos):
                            # New game.
                            if x == 0:
                                sound.stop_music()
                                # Switch to the main game scene.
                                self.SwitchToScene(gameinit.GameScene())
                            # Load game.
                            elif x == 1:
                                # Not yet implimented.
                                pass
                            # Game options.
                            elif x == 2:
                                # Not yet implimented.
                                pass
                            # Roll credits.
                            elif x == 3:
                                sound.stop_music()
                                # Switch to the credits scene.
                                self.SwitchToScene(credits_s.CreditsScene())
                            # Exit the game.
                            elif x == 4:
                                self.Terminate()
                
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
            Option("Game Options", (menu_x, 360)),
            Option("Credits", (menu_x, 390)),
            Option("Exit", (menu_x, 420))
            ]
        
        # Highlight the currently selected menu item.    
        self.options[self.menu].select()
        
        # Draw the menu entries.
        for x in range(len(self.options)):
            canvas.canvas.blit(self.options[x].rend, self.options[x].pos)
        
        self.menu_rects = []
        
        # Run through the options list.
        for x in range(len(self.options)):
            # Add a collidable rectangle to a list for input processing.
            self.menu_rects.append(self.options[x].rend.get_rect(topleft=self.options[x].pos))
            
        # Scale the rect objects so they corospond to the scaled disaply output.
        for x in range(len(self.menu_rects)):
            self.menu_rects[x] = utils.scale_rect(self.menu_rects[x], real_w, real_h)
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
        
