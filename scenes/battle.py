#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors
import utils
import formatting

# The battle screen.
class BattleScreen(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata):
        self.menu = 5
        self.sound = sound
        self.cache = cache
        self.gamedata = gamedata
        self.menu_rects = []
        self.background = cache.get_image(self.gamedata.battlebackground)
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Enter key or space.
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    # Attack.
                    if self.menu == 0:
                        self.active_character.attack_flag = True
                    # Special Move.
                    elif self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Magic.
                    elif self.menu == 2:
                        # Not yet implimented.
                        pass
                    # Use item.
                    elif self.menu == 3:
                        # Not yet implimented.
                        pass
                    # Guard.
                    elif self.menu == 4:
                        # Not yet implimented.
                        pass
                    # End Battle.
                    elif self.menu == 5:
                        self.sound.stop_music()
                        self.gamedata.next_scene = self.gamedata.previous_scene
                        self.gamedata.previous_scene = "BattleScreen"
                # Down arrow or S.
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 6:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow or W.
                elif event.key in (pygame.K_UP, pygame.K_w):
                    # Play the menu sound effect.
                    self.sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 5
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
                            # Attack.
                            if self.menu == 0:
                                self.active_character.attack_flag = True
                            # Special Move.
                            elif self.menu == 1:
                                # Not yet implimented.
                                pass
                            # Magic.
                            elif self.menu == 2:
                                # Not yet implimented.
                                pass
                            # Use item.
                            elif self.menu == 3:
                                # Not yet implimented.
                                pass
                            # Guard.
                            elif self.menu == 4:
                                # Not yet implimented.
                                pass
                            # End Battle.
                            elif self.menu == 5:
                                self.sound.stop_music()
                                self.gamedata.next_scene = self.gamedata.previous_scene
                                self.gamedata.previous_scene = "BattleScreen"
    # Internal game logic.
    def Update(self):
        self.background = self.cache.get_image(self.gamedata.battlebackground)
        
        self.active_character = self.gamedata.party_slots[0]
        
        for character in self.gamedata.party_slots:
            if character != None:
                character.update_standing_image("left")
                
                if character.attack_flag:
                    
                    if character.battle_line_x < 100 and character.attack_starting:
                        character.battle_line_x = character.battle_line_x + 10
                        
                        character.update_image("left")
                        character.moveConductor.play()
                        
                    elif character.battle_line_x > 0 and character.attack_ending:
                        character.battle_line_x = character.battle_line_x - 4
                        
                        character.update_image("left")
                        character.moveConductor.play()
                    
                    elif character.battle_line_x == 100:
                        character.attack_starting = False
                        character.attack_ending = True
                        
                    elif character.battle_line_x == 0:
                        character.attack_flag = False
                        character.attack_starting = True
                        character.attack_ending = False
                
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        canvas.canvas.blit(self.background, (0, 0))
        
        menu_x = 1056
        pygame.draw.rect(canvas.canvas, colors.white, pygame.Rect(menu_x - 3,7,220,206), 3)
        pygame.draw.rect(canvas.canvas, colors.menu_blue, pygame.Rect(menu_x,10,214,200), 0)
        menu_x = menu_x + 13
        
        # Menu entries.
        self.options = [
            formatting.MenuOption("Attack", (menu_x, 23), self.cache),
            formatting.MenuOption("Class Ability", (menu_x, 53), self.cache),
            formatting.MenuOption("Magic", (menu_x, 83), self.cache),
            formatting.MenuOption("Item", (menu_x, 113), self.cache),
            formatting.MenuOption("Guard", (menu_x, 143), self.cache),
            formatting.MenuOption("End Battle", (menu_x, 173), self.cache),
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
        
        
        
        
        
        # Party line starting position.
        self.player_x = 1100
        self.player_y = 420
        # Draw the party on the screen.
        for character in self.gamedata.party_slots:
            if character != None:
                canvas.canvas.blit(character.image, (self.player_x - character.battle_line_x, self.player_y))
                self.player_y = self.player_y + 60
                
                
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
