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
        self.menu = 0
        self.sound = sound
        self.cache = cache
        self.transition = transition
        self.gamedata = gamedata
        self.menu_rects = []
        
        self.status_select = False
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Escape key closes the menu.
                if event.key == pygame.K_ESCAPE and self.status_select == False:
                    self.gamedata.next_scene = self.gamedata.previous_scene
                    self.gamedata.previous_scene = "PartyScreen"
                elif event.key == pygame.K_ESCAPE and self.status_select == True:
                    self.status_select = False
                # Enter key or space.
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    # Status screen selection.
                    if self.status_select == True:
                        # Go to the status screen.
                        if self.gamedata.party_slots[self.gamedata.status_selection] != None:
                            self.gamedata.next_scene = "StatusScreen"
                    # Normal menu entry selection.
                    else:
                        # Status.
                        if self.menu == 0:
                            self.status_select = True
                        # Inventory.
                        elif self.menu == 1:
                            # Not yet implimented.
                            self.gamedata.next_scene = "InventoryScreen"
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
                            self.menu = 0
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
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.status_select:
                        # Incriment the status selection rectangle.
                        self.gamedata.status_selection = self.gamedata.status_selection + 1
                        self.sound.play_sound("menu_change.wav")
                        if self.gamedata.status_selection == 4:
                            # Loop the selection if we went past the end.
                            self.gamedata.status_selection = 0
                    elif not self.status_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu + 1
                        if self.menu == 9:
                            # Loop the menu if we went past the end.
                            self.menu = 0
                # Up arrow or W.
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.status_select:
                        # Incriment the status selection rectangle.
                        self.gamedata.status_selection = self.gamedata.status_selection - 1
                        self.sound.play_sound("menu_change.wav")
                        if self.gamedata.status_selection == -1:
                            # Loop the selection if we went past the end.
                            self.gamedata.status_selection = 3
                    elif not self.status_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu - 1
                        if self.menu == -1:
                            # Loop the menu if we went past the end.
                            self.menu = 8
            # Mouse moved.
            elif event.type == pygame.MOUSEMOTION:
                if not self.status_select:
                    for x in range(len(self.menu_rects)):
                        if self.menu_rects[x].collidepoint(event.pos):
                            self.menu = x
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    # Status screen selection.
                    if self.status_select == True:
                        pass
                    # Normal menu entry selection.
                    else:
                        for x in range(len(self.menu_rects)):
                            if self.menu_rects[x].collidepoint(event.pos):
                                # Status.
                                if self.menu == 0:
                                    self.status_select = True
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
                                    self.menu = 0
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
            formatting.MenuOption("Change Class", (menu_x, 143), self.cache),
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
        
        # Default font for text objects.
        self.font = ["Immortal"]
        
        # GP display.
        pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(1056,310,214,50), 3)
        gp = self.cache.get_font(self.font, 20).render("GP: " + str(self.gamedata.gp), True, colors.white)
        canvas.canvas.blit(gp, (1066, 322))
        
        # Horozontal lines between characters.
        pygame.draw.line(canvas.canvas, colors.white, (10, 180), (1000, 180), 2)
        pygame.draw.line(canvas.canvas, colors.white, (10, 360), (1000, 360), 2)
        pygame.draw.line(canvas.canvas, colors.white, (10, 540), (1000, 540), 2)
        
        if self.status_select == True:
            if self.gamedata.status_selection == 0:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(5,5,1000,170), 2)
            elif self.gamedata.status_selection == 1:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(5,185,1000,170), 2)
            elif self.gamedata.status_selection == 2:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(5,365,1000,170), 2)
            elif self.gamedata.status_selection == 3:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(5,545,1000,170), 2)
        
        x = 40
        y = 50
        
        # Draw the party on the screen.
        for character in self.gamedata.party_slots:
            if character != None:
                canvas.canvas.blit(character.right_standing, (x, y))
                
                # Name.
                name = self.cache.get_font(self.font, 20).render(character.name, True, colors.white)
                canvas.canvas.blit(name, (x + 110, y - 35))
                
                # Level.
                level = self.cache.get_font(self.font, 20).render("Level: " + str(character.level), True, colors.white)
                canvas.canvas.blit(level, (x + 320, y - 35))
                
                # Class.
                mclass = self.cache.get_font(self.font, 20).render(character.mclass, True, colors.white)
                canvas.canvas.blit(mclass, (x + 110, y - 5))
                
                # Current / Max HP.
                current_hp = self.cache.get_font(self.font, 20).render(str(character.current_hp), True, colors.white)
                canvas.canvas.blit(current_hp, (x + 110, y + 25))
                
                slash = self.cache.get_font(self.font, 20).render("/", True, colors.white)
                canvas.canvas.blit(slash, (x + 180, y + 25))
                
                max_hp = self.cache.get_font(self.font, 20).render(str(character.max_hp) + "    HP", True, colors.white)
                canvas.canvas.blit(max_hp, (x + 195, y + 25))
                
                # Color coded HP % bar.
                pygame.draw.line(canvas.canvas, colors.dark_grey, (x + 110, y + 53), (x + 220, y + 53), 2)
                
                hp_p = character.current_hp * 1.0 / character.max_hp
                hp_len = int(hp_p * 140) + 110
                
                if hp_p > 0.75:
                    pygame.draw.line(canvas.canvas, colors.green, (x + 110, y + 53), (x + hp_len, y + 53), 2)
                
                elif hp_p > .40:
                    pygame.draw.line(canvas.canvas, colors.dark_yellow, (x + 110, y + 53), (x + hp_len, y + 53), 2)
                
                else:
                    pygame.draw.line(canvas.canvas, colors.red, (x + 110, y + 53), (x + hp_len, y + 53), 2)
                    
                # Current / Max MP.
                if character.max_mp > 0:
                
                    current_mp = self.cache.get_font(self.font, 20).render(str(character.current_mp), True, colors.white)
                    canvas.canvas.blit(current_mp, (x + 110, y + 60))
                    
                    canvas.canvas.blit(slash, (x + 180, y + 60))
                    
                    max_mp = self.cache.get_font(self.font, 20).render(str(character.max_mp) + "     MP", True, colors.white)
                    canvas.canvas.blit(max_mp, (x + 195, y + 60))
                    
                    # Color coded MP % bar.
                    pygame.draw.line(canvas.canvas, colors.dark_grey, (x + 110, y + 88), (x + 220, y + 88), 2)
                    
                    mp_p = character.current_mp * 1.0 / character.max_mp
                    mp_len = int(mp_p * 140) + 110
                    
                    if mp_p > 0.75:
                        pygame.draw.line(canvas.canvas, colors.green, (x + 110, y + 88), (x + mp_len, y + 88), 2)
                    
                    elif mp_p > .40:
                        pygame.draw.line(canvas.canvas, colors.dark_yellow, (x + 110, y + 88), (x + mp_len, y + 88), 2)
                    
                    else:
                        pygame.draw.line(canvas.canvas, colors.red, (x + 110, y + 88), (x + mp_len, y + 88), 2)
                
                stat_x = 350
                stat_y = 30
                
                # Status effects.
                for status, applied in character.status_effects.items():
                    # List any active status effects.
                    if applied:
                        status_render = self.cache.get_font(self.font, 14).render(status, True, colors.white)
                        canvas.canvas.blit(status_render, (x + stat_x, y + stat_y))
                        stat_x = stat_x + 60
                    # Organize the active effects into up to three rows and three columns.
                    if stat_x == 530:
                        stat_x = 350
                        stat_y = stat_y + 20
                
                y = y + 180
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
