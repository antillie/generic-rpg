#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("scenes")
import pygame
import os
import webbrowser
import virtualscreen
import cache
import sound
import base
import colors
import title

sound = sound.JukeBox()

class Credit:
    # Used for scrolling text on the credits screen.
    def __init__(self, text, pos, size=30, color=colors.white, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font
        self.set_rend()
        
    def set_rend(self):
        self.rend = cache.get_font(self.font, self.size).render(self.text, True, self.color)

class CreditsScene(base.SceneBase):
    # The credits screen.
    def __init__(self, song="hervioleteyes.mp3"):
        base.SceneBase.__init__(self)
        self.song = song
        # Stop whatever music is playing, if any.
        sound.stop_music()
        # Play the credits theme.
        sound.play_music(self.song)
        
        # Starting point for the credits scroll, just off screen.
        self.x = 588
        self.y = 80
    
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                    # Enter or Escape key returns to title screen.
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                        sound.stop_music()
                        self.SwitchToScene(title.TitleScene())
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    for x in range(len(self.credit_url_rects)):
                        if self.credit_url_rects[x].collidepoint(mpos):
                            # Launch the default web browser for the URL.
                            webbrowser.open(self.credit_urls[x], new=2)
    
    # Internal game logic.
    def Update(self):
        # Move the credits up one pixel per frame.
        self.x = self.x - 1
    
    # Draws things.
    def Render(self, screen, real_w, real_h):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        # Create our staticly sized virtual screen so we can draw stuff on it.
        canvas = virtualscreen.VirtualScreen(real_w, real_h)
        
        url_size = 19
        
        font_eula = os.path.dirname(os.path.realpath(__file__)) + "/fonts/fonts_license.html"
        font_eula = font_eula.replace('/', os.sep).replace('\\', os.sep)
        
        # List of credit entries and their starting positions.
        credits_roll = [
            Credit("Main Programming: George Markeloff", (self.y, self.x)),
            Credit("Additional Programming: ???", (self.y, self.x + 100)),
            Credit("Art: ???", (self.y, self.x + 200)),
            Credit("Title Music - Enchanted Festival, By: Matthew Pablo", (self.y, self.x + 300)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 330), url_size, colors.link_blue),
            Credit("Credits Music - Her Violet Eyes, By: tgfcoder", (self.y, self.x + 400)),
            Credit("https://twitter.com/tgfcoder", (self.y, self.x + 430), url_size, colors.link_blue),
            Credit("Battle Theme - A Wild Creature Appears, By: Aaron Parsons", (self.y, self.x + 500)),
            Credit("Boss Theme - Battle of the Void, By: Marcelo Fernandez", (self.y, self.x + 600)),
            Credit("Forest Theme - Forest, By: syncopika", (self.y, self.x + 700)),
            Credit("https://greenbearmusic.bandcamp.com/track/forest", (self.y, self.x + 730), url_size, colors.link_blue),
            Credit("Town Theme - Plesant Creek, By: Matthew Pablo", (self.y, self.x + 800)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 830), url_size, colors.link_blue),
            Credit("Combat System Design: George Markeloff", (self.y, self.x + 900)),
            Credit("Combat Balancing: George Markeloff", (self.y, self.x + 1000)),
            Credit("Character Class Design: George Markeloff", (self.y, self.x + 1100)),
            Credit("Story: George Markeloff", (self.y, self.x + 1200)),
            Credit("Dialog: George Markeloff", (self.y, self.x + 1300)),
            Credit("All audio and art assets licensed under CC-BY 3.0/4.0", (self.y, self.x + 1400)),
            Credit("https://creativecommons.org/licenses/by/3.0/", (self.y, self.x + 1430), url_size, colors.link_blue),
            Credit("Fonts used under Larabie Fonts Freeware Fonts EULA.", (self.y, self.x + 1500)),
            Credit(font_eula, (self.y, self.x + 1530), url_size, colors.link_blue),
            Credit("Written in Python using the Pygame engine.", (self.y, self.x + 1600))
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
            # Add collidable rectangle to a list for input processing.
            self.credit_url_rects.append(credits_roll[url_pattern[x]].rend.get_rect(topleft=credits_roll[url_pattern[x]].pos))
        
        # Draw the upscaled virtual screen to actual screen.
        screen.blit(canvas.render(), (0, 0))

