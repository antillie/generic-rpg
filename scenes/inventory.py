#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import utils
import formatting

# The inventory screen. Lets you use items outside of battle.
class InventoryScreen(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata):
        self.menu = 0
        self.sound = sound
        self.cache = cache
        self.transition = transition
        self.gamedata = gamedata
        self.menu_rects = []
        
        self.target_select = False
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Escape key closes the inventory screen.
                if event.key == pygame.K_ESCAPE and self.target_select == False:
                    self.gamedata.next_scene = "PartyScreen"
                # Or cancels item usage.
                elif event.key == pygame.K_ESCAPE and self.target_select == True:
                    self.target_select = False
                # Enter key or space.
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    # Item usage target selection.
                    if self.target_select == True:
                        # Use the selected item on the target.
                        pass # Not yet implimented.
                    # Select target for item usage.
                    else:
                        # Item slot 1.
                        if self.menu == 0:
                            self.target_select = True
                        # Item slot 2.
                        elif self.menu == 1:
                            # Not yet implimented.
                            pass
                        # Item slot 3.
                        elif self.menu == 2:
                            # Not yet implimented.
                            pass
                        # Item slot 4.
                        elif self.menu == 3:
                            # Not yet implimented.
                            pass
                        
                        # Lots more here...    
                        
                # Down arrow or S.
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.target_select:
                        # Incriment the status selection rectangle.
                        self.gamedata.target_selection = self.gamedata.target_selection + 1
                        self.sound.play_sound("menu_change.wav")
                        if self.gamedata.target_selection == 4:
                            # Loop the selection if we went past the end.
                            self.gamedata.target_selection = 0
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu + 1
                        if self.menu == 4:
                            # Loop the menu if we went past the end.
                            self.menu = 0
                # Up arrow or W.
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.target_select:
                        # Incriment the status selection rectangle.
                        self.gamedata.target_selection = self.gamedata.target_selection - 1
                        self.sound.play_sound("menu_change.wav")
                        if self.gamedata.target_selection == -1:
                            # Loop the selection if we went past the end.
                            self.gamedata.target_selection = 3
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu - 1
                        if self.menu == -1:
                            # Loop the menu if we went past the end.
                            self.menu = 3
            # Mouse moved.
            elif event.type == pygame.MOUSEMOTION:
                if not self.target_select:
                    for x in range(len(self.menu_rects)):
                        if self.menu_rects[x].collidepoint(event.pos):
                            self.menu = x
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    # Status screen selection.
                    if self.target_select == True:
                        pass
                    # Normal menu entry selection.
                    else:
                        for x in range(len(self.menu_rects)):
                            if self.menu_rects[x].collidepoint(event.pos):
                                # Item slot 1.
                                if self.menu == 0:
                                    self.target_select = True
                                # Item slot 2.
                                elif self.menu == 1:
                                    # Not yet implimented.
                                    pass
                                # Item slot 3.
                                elif self.menu == 2:
                                    # Not yet implimented.
                                    pass
                                # Item slot 4.
                                elif self.menu == 3:
                                    # Not yet implimented.
                                    pass
                                
                                # Lots more here...
                                
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Start with a blue screen.
        canvas.canvas.fill(colors.menu_blue)
        
        # Draw the rectangle at the bottom of the screen.
        pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(5,545,1000,170), 2)
        
        x = 40
        y = 590
        
        # Draw the party members on the screen.
        for character in self.gamedata.party_slots:
            if character != None:
                canvas.canvas.blit(character.right_standing, (x, y))
                x = x + 200
        
        menu_x = 1069
        
        # Menu entries.
        self.options = [
            formatting.MenuOption("Status", (menu_x, 23), self.cache),
            formatting.MenuOption("Inventory", (menu_x, 53), self.cache),
            formatting.MenuOption("Spells", (menu_x, 83), self.cache),
            formatting.MenuOption("Equipment", (menu_x, 113), self.cache)
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
        
        
        self.font = ["Immortal"]
        
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
