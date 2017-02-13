#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import utils
import formatting

# The party screen. Lets you save/quit, use items, change classes, ect.
class PartyScreen(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata):
        self.previous_scene = None
        self.menu = 0
        self.sound = sound
        self.cache = cache
        self.transition = transition
        self.gamedata = gamedata
        self.menu_rects = []
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Escape key closes the menu.
                if event.key == pygame.K_ESCAPE:
                    self.gamedata.next_scene = self.gamedata.previous_scene
                    self.gamedata.previous_scene = "PartyScreen"
                # Enter key.
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == K_SPACE:
                    # Status.
                    if self.menu == 0:
                        # Not yet implimented.
                        pass
                    # Inventory.
                    elif self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Spells.
                    elif self.menu == 2:
                        # Not yet implimented.
                        pass
                    # Equipment.
                    elif self.menu == 3:
                        # Not yet implimented.
                        pass
                    # Change Job.
                    elif self.menu == 4:
                        # Not yet implimented.
                        pass
                    # Save game.
                    elif self.menu == 5:
                        # Not yet implimented.
                        pass
                    # Close menu.
                    elif self.menu == 6:
                        self.gamedata.next_scene = self.gamedata.previous_scene
                        self.gamedata.previous_scene = "PartyScreen"
                    # Quit to title screen.
                    elif self.menu == 7:
                        self.transition.run("fadeOutDown")
                        self.sound.stop_music()
                        self.gamedata.next_scene = "TitleScene"
                        self.gamedata.previous_scene = "PartyScreen"
                    # Quit to desktop.
                    elif self.menu == 8:
                        self.gamedata.next_scene = None
                # Down arrow or S.
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 9:
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
                        self.menu = 8
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
                            # Status.
                            if self.menu == 0:
                                # Not yet implimented.
                                pass
                            # Inventory.
                            elif self.menu == 1:
                                # Not yet implimented.
                                pass
                            # Spells.
                            elif self.menu == 2:
                                # Not yet implimented.
                                pass
                            # Equipment.
                            elif self.menu == 3:
                                # Not yet implimented.
                                pass
                            # Change Job.
                            elif self.menu == 4:
                                # Not yet implimented.
                                pass
                            # Save game.
                            elif self.menu == 5:
                                # Not yet implimented.
                                pass
                            # Close menu.
                            elif self.menu == 6:
                                self.gamedata.next_scene = self.gamedata.previous_scene
                                self.gamedata.previous_scene = "PartyScreen"
                            # Quit to title screen.
                            elif self.menu == 7:
                                self.transition.run("fadeOutDown")
                                self.sound.stop_music()
                                self.gamedata.next_scene = "TitleScene"
                                self.gamedata.previous_scene = "PartyScreen"
                            # Quit to desktop.
                            elif self.menu == 8:
                                self.gamedata.next_scene = None
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Start with a blue screen.
        canvas.canvas.fill(colors.menu_blue)
        
        menu_x = 1056
        
        pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(menu_x,10,214,294), 3)
        
        menu_x = menu_x + 13
        
        # Menu entries.
        self.options = [
            formatting.MenuOption("Status", (menu_x, 23), self.cache),
            formatting.MenuOption("Inventory", (menu_x, 53), self.cache),
            formatting.MenuOption("Spells", (menu_x, 83), self.cache),
            formatting.MenuOption("Equipment", (menu_x, 113), self.cache),
            formatting.MenuOption("Change Job", (menu_x, 143), self.cache),
            formatting.MenuOption("Save Game", (menu_x, 173), self.cache),
            formatting.MenuOption("Close Menu", (menu_x, 203), self.cache),
            formatting.MenuOption("Quit to Title", (menu_x, 233), self.cache),
            formatting.MenuOption("Quit to Desktop", (menu_x, 263), self.cache)
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
