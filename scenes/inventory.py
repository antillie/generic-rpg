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
        self.target_selection = 0
        
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
                        if self.gamedata.party_slots[self.target_selection] != None:
                            self.use_item(self.items[self.menu].text, self.target_selection)
                        
                    # Select target for item usage.
                    else:
                        if self.non_combat_item(self.items[self.menu].text, int(self.amounts[self.menu].text)):
                            self.target_select = True
                        
                # Down arrow or S.
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.target_select:
                        pass
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu + 1
                        if self.menu == 30:
                            # Loop the menu if we went past the end.
                            self.menu = 0
                # Up arrow or W.
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.target_select:
                        pass
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu - 1
                        if self.menu == -1:
                            # Loop the menu if we went past the end.
                            self.menu = 29
                # Left arrow or A.
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.target_select:
                        # Incriment the status selection rectangle.
                        self.target_selection = self.target_selection - 1
                        self.sound.play_sound("menu_change.wav")
                        if self.target_selection == -1:
                            # Loop the selection if we went past the end.
                            self.target_selection = 3
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu - 10
                        if self.menu < 0:
                            # Loop the menu if we went past the end.
                            self.menu = 29
                # Right arrow or D.
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.target_select:
                        # Incriment the status selection rectangle.
                        self.target_selection = self.target_selection + 1
                        self.sound.play_sound("menu_change.wav")
                        if self.target_selection == 4:
                            # Loop the selection if we went past the end.
                            self.target_selection = 0
                    elif not self.target_select:
                        # Play the menu sound effect.
                        self.sound.play_sound("menu_change.wav")
                        # Incriment the menu.
                        self.menu = self.menu + 10
                        if self.menu > 29:
                            # Loop the menu if we went past the end.
                            self.menu = 0
                
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
                        # Use the selected item on the target.
                        
                        print(self.items[self.menu].text)
                        
                    # Normal menu entry selection.
                    else:
                        for x in range(len(self.menu_rects)):
                            if self.menu_rects[x].collidepoint(event.pos):
                                self.target_select = True
                                
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
        
        x = 20
        y = 590
        self.font = ["Immortal"]
        
        # Draw the party members on the screen.
        for character in self.gamedata.party_slots:
            if character != None:
                canvas.canvas.blit(character.right_standing, (x, y))
                
                # Current / Max HP.
                current_hp = self.cache.get_font(self.font, 20).render(str(character.current_hp), True, colors.white)
                canvas.canvas.blit(current_hp, (x + 50, y + 5))
                
                slash = self.cache.get_font(self.font, 20).render("/", True, colors.white)
                canvas.canvas.blit(slash, (x + 120, y + 5))
                
                max_hp = self.cache.get_font(self.font, 20).render(str(character.max_hp), True, colors.white)
                canvas.canvas.blit(max_hp, (x + 135, y + 5))
                
                # Color coded HP % bar.
                pygame.draw.line(canvas.canvas, colors.dark_grey, (x + 50, y + 33), (x + 160, y + 33), 2)
                
                hp_p = character.current_hp * 1.0 / character.max_hp
                hp_len = int(hp_p * 140) + 50
                
                if hp_p > 0.75:
                    pygame.draw.line(canvas.canvas, colors.green, (x + 50, y + 33), (x + hp_len, y + 33), 2)
                
                elif hp_p > .40:
                    pygame.draw.line(canvas.canvas, colors.dark_yellow, (x + 50, y + 33), (x + hp_len, y + 33), 2)
                
                else:
                    pygame.draw.line(canvas.canvas, colors.red, (x + 50, y + 33), (x + hp_len, y + 33), 2)
                    
                # Current / Max MP.
                if character.max_mp > 0:
                    current_mp = self.cache.get_font(self.font, 20).render(str(character.current_mp), True, colors.white)
                    canvas.canvas.blit(current_mp, (x + 50, y + 40))
                    
                    canvas.canvas.blit(slash, (x + 120, y + 40))
                    
                    max_mp = self.cache.get_font(self.font, 20).render(str(character.max_mp), True, colors.white)
                    canvas.canvas.blit(max_mp, (x + 135, y + 40))
                    
                    # Color coded MP % bar.
                    pygame.draw.line(canvas.canvas, colors.dark_grey, (x + 50, y + 68), (x + 160, y + 68), 2)
                    
                    mp_p = character.current_mp * 1.0 / character.max_mp
                    mp_len = int(mp_p * 140) + 50
                    
                    if mp_p > 0.75:
                        pygame.draw.line(canvas.canvas, colors.green, (x + 50, y + 68), (x + mp_len, y + 68), 2)
                    
                    elif mp_p > .40:
                        pygame.draw.line(canvas.canvas, colors.dark_yellow, (x + 50, y + 68), (x + mp_len, y + 68), 2)
                    
                    else:
                        pygame.draw.line(canvas.canvas, colors.red, (x + 50, y + 68), (x + mp_len, y + 68), 2)
                
                stat_x = 0
                stat_y = 70
                
                # Status effects.
                for status, applied in character.status_effects.items():
                    # List any active status effects.
                    if applied:
                        status_render = self.cache.get_font(self.font, 14).render(status, True, colors.white)
                        canvas.canvas.blit(status_render, (x + stat_x, y + stat_y))
                        stat_x = stat_x + 60
                    # Organize the active effects into up to three rows and three columns.
                    if stat_x == 180:
                        stat_x = 0
                        stat_y = stat_y + 20
                
                # Shift the next character to the right.
                x = x + 220
        
        self.items = []
        self.amounts = []
        
        items_x = 100
        items_y = 60
        
        # Create the inventory items and their quantities as menu objects.
        for item, amount in self.gamedata.inventory.items():
            self.items.append(formatting.MenuOption(item, (items_x, items_y), self.cache))
            self.amounts.append(formatting.MenuOption(str(amount), (items_x + 200, items_y), self.cache))
            
            items_y = items_y + 30
            
            # Organise the items into 10 rows and 3 columns.
            if items_y == 360:
                items_y = 60
                items_x = items_x + 300
        
        # Highlight the currently selected item.    
        self.items[self.menu].select()
        
        # Draw the items and quantities.
        for x in range(len(self.items)):
            canvas.canvas.blit(self.items[x].rend, self.items[x].pos)
        
        for x in range(len(self.amounts)):
            canvas.canvas.blit(self.amounts[x].rend, self.amounts[x].pos)
        
        self.menu_rects = []
        
        # Run through the items list.
        for x in range(len(self.items)):
            # Add a collidable rectangle to a list for input processing.
            self.menu_rects.append(self.items[x].rend.get_rect(topleft=self.items[x].pos))
            
        # Scale the rect objects so they corospond to the scaled disaply output.
        for x in range(len(self.menu_rects)):
            self.menu_rects[x] = utils.scale_rect(self.menu_rects[x], real_w, real_h)
        
        # Draw the item usage dialog.
        if self.target_select:
            pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(5,485,155,55), 2)
            text = self.cache.get_font(["Immortal"], 20).render("Use item on?", True, colors.white)
            canvas.canvas.blit(text, (20 ,500))
            
            # Draw the item target selection retical.
            if self.target_selection == 0:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(10,550,220,160), 2)
            elif self.target_selection == 1:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(230,550,220,160), 2)
            elif self.target_selection == 2:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(430,550,220,160), 2)
            elif self.target_selection == 3:
                pygame.draw.rect(canvas.canvas, colors.off_yellow, pygame.Rect(630,550,220,160), 2)
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
    
    def non_combat_item(self, item, amount):
        
        non_combat_items = [
        "Potion",
        "Hi-Potion",
        "Mega-Potion",
        "X-Potion",
        "Ether",
        "Hi-Ether",
        "Mega-Ether",
        "X-Ether",
        "Minor Elixer",
        "Elixer",
        "Antidote",
        "Echo Screen",
        "Eye Drops",
        "Gold Needle",
        "Green Cherry",
        "Holy Water",
        "Phoenix Feather",
        "Tent",
        "Megalixer",
        "Warp Stone"
        ]
        
        if item in non_combat_items and amount > 0:
            return True
        else:
            self.sound.play_sound("negative_2.wav")
            return False
    
    def use_item(self, item, target):
        if self.gamedata.inventory[item] > 0:
            print("Used " + item + " on " + self.gamedata.party_slots[target].name)
            self.gamedata.inventory[item] = self.gamedata.inventory[item] - 1
            self.sound.play_sound("misc_menu.wav")
        else:
            self.sound.play_sound("negative_2.wav")
