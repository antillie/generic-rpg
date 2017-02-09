#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import utils

# Used for entries in the menu.
class Option:
    
    active = False
    
    def __init__(self, text, pos, cache, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.font = font
        self.cache = cache
        self.set_rend()
        
    def set_rend(self):
        self.rend = self.cache.get_font(self.font, 20).render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.active:
            return colors.off_yellow
        else:
            return colors.white
            
    def select(self):
        self.active = True
        self.set_rend()

# The party screen. Lets you save/quit, use items, change classes, ect...
class PartyScreen(base.SceneBase):
    
    def __init__(self, sound, cache):
        base.SceneBase.__init__(self)
        self.name = "PartyScreen"
        self.previous_scene = None
        self.menu = 0
        self.sound = sound
        self.cache = cache
        self.menu_rects = []
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Escape key closes the menu.
                if event.key == pygame.K_ESCAPE:
                    self.SwitchToScene(self.previous_scene)
                # Enter key.
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
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
                    # Close menu.
                    elif self.menu == 5:
                        self.SwitchToScene(self.previous_scene)
                    # Quit to title screen.
                    elif self.menu == 6:
                        self.sound.stop_music()
                        self.SwitchToScene("TitleScene")
                    # Quit to desktop.
                    elif self.menu == 7:
                        self.Terminate()
                # Down arrow.
                elif event.key == pygame.K_DOWN:
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 8:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow.
                elif event.key == pygame.K_UP:
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 7
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
                            # Close menu.
                            elif self.menu == 5:
                                self.SwitchToScene(self.previous_scene)
                            # Quit to title screen.
                            elif self.menu == 6:
                                self.sound.stop_music()
                                self.SwitchToScene("TitleScene")
                            # Quit to desktop.
                            elif self.menu == 7:
                                self.Terminate()
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Start with a blue screen.
        canvas.canvas.fill((0, 90, 170))
        
        pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(800,10,214,264), 3)
        
        menu_x = 813
        
        # Menu entries.
        self.options = [
            Option("Status", (menu_x, 23), self.cache),
            Option("Inventory", (menu_x, 53), self.cache),
            Option("Spells", (menu_x, 83), self.cache),
            Option("Equipment", (menu_x, 113), self.cache),
            Option("Change Job", (menu_x, 143), self.cache),
            Option("Close Menu", (menu_x, 173), self.cache),
            Option("Quit to Title", (menu_x, 203), self.cache),
            Option("Quit to Desktop", (menu_x, 233), self.cache)
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
