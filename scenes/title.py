#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import utils
import formatting

# Main title screen. You can start/load a game, view the credits, or close the program from here.
class TitleScene(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata, song="enchantedfestivalloop.mp3"):
        self.song = song
        self.menu = 1
        self.sound = sound
        self.cache = cache
        self.gamedata = gamedata
        self.menu_rects = []
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the title theme.
        self.sound.play_music(self.song)
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Enter key.
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == K_SPACE:
                    # New game.
                    if self.menu == 0:
                        self.sound.stop_music()
                        self.menu = 1
                        # Switch to the main game scene.
                        self.gamedata.next_scene = "GameScene"
                        self.gamedata.previous_scene = "TitleScene"
                    # Load game.
                    elif self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Reset display.
                    elif self.menu == 2:
                        # Just resets the display mode.
                        self.sound.play_sound("menu_thwump.wav")
                        self.gamedata.reset_display = True
                    # Roll credits.
                    elif self.menu == 3:
                        self.sound.stop_music()
                        self.menu = 1
                        # Switch to the credits scene.
                        self.gamedata.next_scene = "CreditsScene"
                        self.gamedata.previous_scene = "TitleScene"
                    # Exit the game.
                    elif self.menu == 4:
                        self.gamedata.next_scene = None
                # Down arrow or S.
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 5:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow or W.
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 4
            # Mouse moved.
            elif event.type == pygame.MOUSEMOTION:
                for x in range(len(self.menu_rects)):
                    if self.menu_rects[x].collidepoint(event.pos):
                        self.menu = x
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    for x in range(len(self.menu_rects)):
                        if self.menu_rects[x].collidepoint(event.pos):
                            # New game.
                            if self.menu == 0:
                                self.sound.stop_music()
                                self.menu = 1
                                # Switch to the main game scene.
                                self.gamedata.next_scene = "GameScene"
                                self.gamedata.previous_scene = "TitleScene"
                            # Load game.
                            elif self.menu == 1:
                                # Not yet implimented.
                                pass
                            # Game options.
                            elif self.menu == 2:
                                # Just resets the display mode.
                                self.sound.play_sound("menu_thwump.wav")
                                self.gamedata.reset_display = True
                            # Roll credits.
                            elif self.menu == 3:
                                self.sound.stop_music()
                                self.menu = 1
                                # Switch to the credits scene.
                                self.gamedata.next_scene = "CreditsScene"
                                self.gamedata.previous_scene = "TitleScene"
                            # Exit the game.
                            elif self.menu == 4:
                                self.gamedata.next_scene = None
                
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
        title = self.cache.get_font(["Immortal"], 70).render("Generic RPG Name",True,colors.white)
        canvas.canvas.blit(title, [310, 60])
        
        menu_x = 555
        
        # Menu entries.
        self.options = [
            formatting.MenuOption("New Game", (menu_x, 300), self.cache),
            formatting.MenuOption("Load Game", (menu_x, 330), self.cache),
            formatting.MenuOption("Reset Display", (menu_x, 360), self.cache),
            formatting.MenuOption("Credits", (menu_x, 390), self.cache),
            formatting.MenuOption("Exit", (menu_x, 420), self.cache)
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
        
