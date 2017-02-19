#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import virtualscreen
import base
import colors

# The status screen.
class StatusScreen(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata):
        self.sound = sound
        self.cache = cache
        self.transition = transition
        self.gamedata = gamedata
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Return to party screen.
                if event.key == pygame.K_ESCAPE:
                    self.gamedata.next_scene = "PartyScreen"
                # Return to party screen.
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self.gamedata.next_scene = "PartyScreen"
                    
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    # Return to party screen.
                    self.gamedata.next_scene = "PartyScreen"
                    
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        # Start with a blue screen.
        canvas.canvas.fill(colors.menu_blue)
        
        x = 40
        y = 50
        self.font = ["Immortal"]
        
        # Draw the character information on the screen.
        character = self.gamedata.party_slots[self.gamedata.status_selection]
        
        canvas.canvas.blit(character.right_standing, (x, y))
        
        # Name.
        name = self.cache.get_font(self.font, 20).render(character.name, True, colors.white)
        canvas.canvas.blit(name, (x + 110, y - 35))
        
        # Level.
        level = self.cache.get_font(self.font, 20).render("Level: " + str(character.level), True, colors.white)
        canvas.canvas.blit(level, (x + 320, y - 35))
        
        # Class.
        cclass = self.cache.get_font(self.font, 20).render(character.cclass, True, colors.white)
        canvas.canvas.blit(cclass, (x + 110, y - 5))
        
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
        
        # Character core stats.
        strength = self.cache.get_font(self.font, 20).render("Strength: " + str(character.strength), True, colors.white)
        canvas.canvas.blit(strength, (150, 200))
        
        vitality = self.cache.get_font(self.font, 20).render("Vitality: " + str(character.vitality), True, colors.white)
        canvas.canvas.blit(vitality, (150, 230))
        
        agility = self.cache.get_font(self.font, 20).render("Agility: " + str(character.agility), True, colors.white)
        canvas.canvas.blit(agility, (150, 260))
        
        dexterity = self.cache.get_font(self.font, 20).render("Dexterity: " + str(character.dexterity), True, colors.white)
        canvas.canvas.blit(dexterity, (150, 290))
        
        mind = self.cache.get_font(self.font, 20).render("Mind: " + str(character.mind), True, colors.white)
        canvas.canvas.blit(mind, (150, 320))
        
        inteligence = self.cache.get_font(self.font, 20).render("Inteligence: " + str(character.inteligence), True, colors.white)
        canvas.canvas.blit(inteligence, (150, 350))
        
        charisma = self.cache.get_font(self.font, 20).render("Charisma: " + str(character.charisma), True, colors.white)
        canvas.canvas.blit(charisma, (150, 380))
        
        # XP to next level.
        tnl = self.cache.get_font(self.font, 20).render("XP to next level: " + str(character.tnl), True, colors.white)
        canvas.canvas.blit(tnl, (500, 15))
        
        # Character secondary stats.
        defense = self.cache.get_font(self.font, 20).render("Defense: " + str(character.defense), True, colors.white)
        canvas.canvas.blit(defense, (500, 200))
        
        attack = self.cache.get_font(self.font, 20).render("Attack: " + str(character.attack), True, colors.white)
        canvas.canvas.blit(attack, (500, 230))
        
        accuracy = self.cache.get_font(self.font, 20).render("Accuracy: " + str(character.accuracy), True, colors.white)
        canvas.canvas.blit(accuracy, (500, 260))
        
        dodge = self.cache.get_font(self.font, 20).render("Dodge: " + str(character.dodge), True, colors.white)
        canvas.canvas.blit(dodge, (500, 290))
        
        magic_attack = self.cache.get_font(self.font, 20).render("Magic Attack: " + str(character.magic_attack), True, colors.white)
        canvas.canvas.blit(magic_attack, (500, 320))
        
        magic_defense = self.cache.get_font(self.font, 20).render("Magic Defense: " + str(character.magic_defense), True, colors.white)
        canvas.canvas.blit(magic_defense, (500, 350))
        
        parry = self.cache.get_font(self.font, 20).render("Parry: " + str(character.parry), True, colors.white)
        canvas.canvas.blit(parry, (500, 380))
        
        block = self.cache.get_font(self.font, 20).render("Block: " + str(character.block), True, colors.white)
        canvas.canvas.blit(block, (500, 410))
        
        guard = self.cache.get_font(self.font, 20).render("Guard: " + str(character.guard), True, colors.white)
        canvas.canvas.blit(guard, (500, 440))
        
        counter = self.cache.get_font(self.font, 20).render("Counter: " + str(character.counter), True, colors.white)
        canvas.canvas.blit(counter, (500, 470))
        
        # Elemetal resistances.
        fire_res = self.cache.get_font(self.font, 20).render("Fire Resist: " + str(character.fire_res), True, colors.white)
        canvas.canvas.blit(fire_res, (850, 200))
        
        ice_res = self.cache.get_font(self.font, 20).render("Ice Resist: " + str(character.ice_res), True, colors.white)
        canvas.canvas.blit(ice_res, (850, 230))
        
        wind_res = self.cache.get_font(self.font, 20).render("Wind Resist: " + str(character.wind_res), True, colors.white)
        canvas.canvas.blit(wind_res, (850, 260))
        
        earth_res = self.cache.get_font(self.font, 20).render("Earth Resist: " + str(character.earth_res), True, colors.white)
        canvas.canvas.blit(earth_res, (850, 290))
        
        lightning_res = self.cache.get_font(self.font, 20).render("Lightning Resist: " + str(character.lightning_res), True, colors.white)
        canvas.canvas.blit(lightning_res, (850, 320))
        
        water_res = self.cache.get_font(self.font, 20).render("Water Resist: " + str(character.water_res), True, colors.white)
        canvas.canvas.blit(water_res, (850, 350))
        
        holy_res = self.cache.get_font(self.font, 20).render("Holy Resist: " + str(character.holy_res), True, colors.white)
        canvas.canvas.blit(holy_res, (850, 380))
        
        darkness_res = self.cache.get_font(self.font, 20).render("Darkness Resist: " + str(character.darkness_res), True, colors.white)
        canvas.canvas.blit(darkness_res, (850, 410))
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
