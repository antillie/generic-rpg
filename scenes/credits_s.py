#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
import webbrowser
import virtualscreen
import base
import colors
import utils

class Credit:
    # Used for scrolling text on the credits screen.
    def __init__(self, text, pos, cache, size=30, color=colors.white, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font
        self.cache = cache
        self.set_rend()
        
    def set_rend(self):
        self.rend = self.cache.get_font(self.font, self.size).render(self.text, True, self.color)

# The credits screen.
class CreditsScene(base.SceneBase):
    
    def __init__(self, sound, cache, transition, gamedata, song="hervioleteyes.mp3"):
        self.song = song
        self.sound = sound
        self.cache = cache
        self.transition = transition
        self.gamedata = gamedata
        
        # Starting point for the credits scroll, just off screen.
        self.x = 730
        self.y = 80
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        # Play the credits theme.
        self.sound.play_music(self.song)
        
        for event in events:
            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                    # Enter or Escape key returns to title screen.
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                        self.x = 730
                        self.transition.run("fadeOutDown")
                        self.sound.stop_music()
                        self.gamedata.next_scene = "TitleScene"
                        self.gamedata.previous_scene = "CreditsScene"
            # Mouse click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    for x in range(len(self.credit_url_rects)):
                        if self.credit_url_rects[x].collidepoint(mpos):
                            # Launch the default web browser for the URL.
                            webbrowser.open(self.credit_urls[x], new=2)
                    
                    if self.x == -2500:
                        self.x = 730
                        self.transition.run("fadeOutDown")
                        self.sound.stop_music()
                        self.gamedata.next_scene = "TitleScene"
                        self.gamedata.previous_scene = "CreditsScene"
                    
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        url_size = 19
        
        font_eula = os.path.dirname(os.path.realpath(__file__)) + "/../fonts/fonts_license.html"
        font_eula = font_eula.replace('/', os.sep).replace('\\', os.sep)
        
        # List of credit entries and their starting positions.
        credits_roll = [
            Credit("Main Programming: George Markeloff", (self.y, self.x), self.cache),
            Credit("Additional Programming: ???", (self.y, self.x + 100), self.cache),
            Credit("Art: ???", (self.y, self.x + 200), self.cache),
            Credit("Title Music - Enchanted Festival, By: Matthew Pablo", (self.y, self.x + 300), self.cache),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 330), self.cache, url_size, colors.link_blue),
            Credit("Credits Music - Her Violet Eyes, By: tgfcoder", (self.y, self.x + 400), self.cache),
            Credit("https://twitter.com/tgfcoder", (self.y, self.x + 430), self.cache, url_size, colors.link_blue),
            Credit("Battle Theme - A Wild Creature Appears, By: Aaron Parsons", (self.y, self.x + 500), self.cache),
            Credit("http://opengameart.org/content/a-wild-creature-appears", (self.y, self.x + 530), self.cache, url_size, colors.link_blue),
            Credit("Boss Theme - Battle of the Void, By: Marcelo Fernandez", (self.y, self.x + 600), self.cache),
            Credit("http://opengameart.org/content/battle-of-the-void", (self.y, self.x + 630), self.cache, url_size, colors.link_blue),
            Credit("Forest Theme - Forest, By: syncopika", (self.y, self.x + 700), self.cache),
            Credit("https://greenbearmusic.bandcamp.com/track/forest", (self.y, self.x + 730), self.cache, url_size, colors.link_blue),
            Credit("Town Theme - Plesant Creek, By: Matthew Pablo", (self.y, self.x + 800), self.cache),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 830), self.cache, url_size, colors.link_blue),
            Credit("Combat System Design: George Markeloff", (self.y, self.x + 900), self.cache),
            Credit("Combat Balancing: George Markeloff", (self.y, self.x + 1000), self.cache),
            Credit("Character Class Design: George Markeloff", (self.y, self.x + 1100), self.cache),
            Credit("Story: George Markeloff", (self.y, self.x + 1200), self.cache),
            Credit("Dialog: George Markeloff", (self.y, self.x + 1300), self.cache),
            Credit("Wood Tileset: Jetrel, Daniel Cook, Bertram and Zabin", (self.y, self.x + 1400), self.cache),
            Credit("http://opengameart.org/content/2d-lost-garden-tileset-transition-to-jetrels-wood-tileset", (self.y, self.x + 1430), self.cache, url_size, colors.link_blue),
            Credit("Snow Tilset: Daniel Cook, Jetrel, yd, and Zabin.", (self.y, self.x + 1500), self.cache),
            Credit("ttp://opengameart.org/content/2d-lost-garden-zelda-style-tiles-winter-theme-with-additions", (self.y, self.x + 1530), self.cache, url_size, colors.link_blue),
            Credit("Mountain Landscape Tileset: Daniel Cook, Jetrel, Bertram, Zabin, Saphy", (self.y, self.x + 1600), self.cache),
            Credit("http://opengameart.org/content/2d-lost-garden-zelda-style-tiles-resized-to-32x32-with-additions", (self.y, self.x + 1630), self.cache, url_size, colors.link_blue),
            Credit("Most audio and art assets licensed under CC-BY or CC-BY-SA", (self.y, self.x + 1700), self.cache),
            Credit("https://creativecommons.org/licenses/by/4.0/", (self.y, self.x + 1730), self.cache, url_size, colors.link_blue),
            Credit("https://creativecommons.org/licenses/by-sa/4.0/", (self.y, self.x + 1760), self.cache, url_size, colors.link_blue),
            Credit("Window Icon: MrReynevan2", (self.y, self.x + 1800), self.cache),
            Credit("http://opengameart.org/content/simple-shield", (self.y, self.x + 1830), self.cache, url_size, colors.link_blue),
            Credit("General GUI Sound Effects: Lokif", (self.y, self.x + 1900), self.cache),
            Credit("http://opengameart.org/content/gui-sound-effects", (self.y, self.x + 1930), self.cache, url_size, colors.link_blue),
            Credit("Forest Battle Background (resized): Tamara Ramsay", (self.y, self.x + 2000), self.cache),
            Credit("http://vectorgurl.com/", (self.y, self.x + 2030), self.cache, url_size, colors.link_blue),
            Credit("http://opengameart.org/content/forest-background-art", (self.y, self.x + 2060), self.cache, url_size, colors.link_blue),
            Credit('Screen Reset "Thwump" sound: Arthur', (self.y, self.x + 2100), self.cache),
            Credit("http://opengameart.org/content/sci-fi-shwop-1", (self.y, self.x + 2130), self.cache, url_size, colors.link_blue),
            Credit("Fonts used under Larabie Fonts Freeware Fonts EULA.", (self.y, self.x + 2200), self.cache),
            Credit(font_eula, (self.y, self.x + 2230), self.cache, url_size, colors.link_blue),
            Credit("Built with the Generic RPG engine written by George Markeloff.", (self.y, self.x + 2300), self.cache),
            Credit("Thanks for playing!", (self.y + 410, self.x + 2800), self.cache)
        ]
        
        url_pattern = []
        
        # Run through the credits roll entries.
        for x in range(len(credits_roll)):
            # Draw the entries on the screen.
            canvas.canvas.blit(credits_roll[x].rend, credits_roll[x].pos)
            # Populate the url pattern list with the index numbers of URL entries.
            if credits_roll[x].color == colors.link_blue:
                url_pattern.append(x)
        
        self.credit_urls = []
        self.credit_url_rects = []
        
        # Run through the URL pattern list.
        for x in range(len(url_pattern)):
            # Add the actual URL to a list for input processing.
            self.credit_urls.append(credits_roll[url_pattern[x]].text)
            # Add a collidable rectangle to a list for input processing.
            self.credit_url_rects.append(credits_roll[url_pattern[x]].rend.get_rect(topleft=credits_roll[url_pattern[x]].pos))
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))
        
        # Scale the rect objects so they corospond to the scaled disaply output.
        for x in range(len(self.credit_url_rects)):
            self.credit_url_rects[x] = utils.scale_rect(self.credit_url_rects[x], real_w, real_h)
        
        # Move the credits up one pixel for the next frame.
        if self.x > -2500:
            self.x = self.x - 1
