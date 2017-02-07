#!/usr/bin/python
# -*- coding: utf-8 -*-

# For backwards compatibility with Python 2.
from __future__ import print_function

# Import modules.
import pygame
import os
import webbrowser

white = [255,255,255]
off_yellow = [240, 220, 0]
grey = [200, 200, 200]
link_blue = [50, 100, 255]

# Font object generator.
def make_font(fonts, size):
    
    if fonts[0] == "Immortal":
        path = os.path.dirname(os.path.realpath(__file__)) + "/fonts/" + fonts[0] + ".ttf"
        path = path.replace('/', os.sep).replace('\\', os.sep)
        return pygame.font.Font(path, size)
    
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

# Cache generated font objects so we don't have to call the generator all the time.
_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

class Option:
    # Used for entries in menus.
    active = False
    
    def __init__(self, text, pos, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.font = font
        self.set_rend()
        
    def set_rend(self):
        self.rend = get_font(self.font, 20).render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.active:
            return off_yellow
        else:
            return grey
            
    def select(self):
        self.active = True
        self.set_rend()

class Credit:
    # Used for scrolling text on the credits screen.
    def __init__(self, text, pos, size=30, color=white, font=["Immortal"]):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font
        self.set_rend()
        
    def set_rend(self):
        self.rend = get_font(self.font, self.size).render(self.text, True, self.color)

_sound_library = {}
class JukeBox:
    # Sound class that handles all audio output.
    
    # Default volume levels.
    music_volume = 0.2
    fx_volume = 1.0
    
    def __init__(self):
        self.music_playing = False
    
    def play_music(self, song):
        if self.music_playing == False:
            song_path = os.path.dirname(os.path.realpath(__file__)) + "/sound/music/" + song
            song_path = song_path.replace('/', os.sep).replace('\\', os.sep)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_playing = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def play_sound(self, sound):
        # Cache sound effect objects so we don't have to generate them every time a sound is played.
        global _sound_library
        sound_fx = _sound_library.get(sound)
        if sound_fx == None:
            path = os.path.dirname(os.path.realpath(__file__)) + "/sound/" + sound
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound_fx = pygame.mixer.Sound(canonicalized_path)
            _sound_library[path] = sound
        sound_fx.set_volume(self.fx_volume)
        sound_fx.play()

class SceneBase:
    # Template class for scenes. Things like the title screen, loading screen, towns, world map, dungeons, menus, ect...
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

# Main engine. Sets up the window, handles rendering, manages scene changes, and forwards player input to the active scene.
def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Generic RPG")
    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering. Some things should not be passed to the active scene, like the game window being closed or ALT+F4.
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            # User closed the game window.
            if event.type == pygame.QUIT:
                quit_attempt = True
            # All keyboard input.
            elif event.type == pygame.KEYDOWN:
                # User is holding an ALT key.
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                # User pressed F4 while holding an ALT key.
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
                    
            if quit_attempt:
                # Close the program.
                active_scene.Terminate()
            else:
                # Queue the input to be sent to the active scene.
                filtered_events.append(event)
        
        # Pass the input to the active scene for processing.
        active_scene.ProcessInput(filtered_events, pressed_keys)
        # Have the active scene run its internal game logic.
        active_scene.Update()
        # Tell the active scene to render itself to the display buffer.
        active_scene.Render(screen)
        
        # Change the active scene to whichever scene should be next.
        active_scene = active_scene.next
        
        # Draw the updated display buffer on the screen.
        pygame.display.flip()
        
        # Increment the internal game state at the desired FPS limit.
        clock.tick(fps)

class TitleScene(SceneBase):
    # Main title screen. You can start/load a game, view the credits, or close the program from here.
    def __init__(self, song="enchantedfestivalloop.mp3"):
        SceneBase.__init__(self)
        self.song = song
        self.menu = 1
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Enter key.
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # New game.
                    if self.menu == 0:
                        sound.stop_music()
                        # Switch to the main game scene.
                        self.SwitchToScene(GameScene())
                    # Load game.
                    if self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Roll credits.
                    if self.menu == 2:
                        sound.stop_music()
                        # Switch to the credits scene.
                        self.SwitchToScene(CreditsScene())
                    # Exit the game.
                    if self.menu == 3:
                        self.Terminate()
                # Down arrow.
                if event.key == pygame.K_DOWN:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 4:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow.
                if event.key == pygame.K_UP:
                    # Play the menu sound effect.
                    sound.play_sound("menu_change.wav")
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 3
    
    # Internal game logic. Doesn't really apply to the main menu.
    def Update(self):
        pass
        
    # Draws things.
    def Render(self, screen):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        # Play the title music.
        sound.play_music(self.song)
        
        # Title text.
        title = get_font(["Immortal"], 70).render("Generic RPG Name",True,white)
        screen.blit(title, [175, 60])
        
        menu_x = 430
        
        # Menu entries.
        self.options = [
            Option("New Game", (menu_x, 300)),
            Option("Load Game", (menu_x, 330)),
            Option("Credits", (menu_x, 360)),
            Option("Exit", (menu_x, 390))
            ]
        
        # Highlight the currently selected menu item.    
        self.options[self.menu].select()
        
        # Draw the menu entries.
        for x in range(len(self.options)):
            screen.blit(self.options[x].rend, self.options[x].pos)
        
class GameScene(SceneBase):
    # The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
    def __init__(self, song="plesantcreekloop.mp3"):
        SceneBase.__init__(self)
        self.song = song
        
        # Play music.
        sound.play_music(song)
        
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        pass
    
    # Internal game logic.
    def Update(self):
        pass
    
    # Draws things.
    def Render(self, screen):
        # The game scene is just a blank blue screen at the moment.
        screen.fill((0, 0, 255))
        
        # Placeholder text.
        title = get_font(["Arial"], 50).render("Nothing here yet...",True,white)
        screen.blit(title, [200, 60])
        
class CreditsScene(SceneBase):
    # The credits screen.
    def __init__(self, song="hervioleteyes.mp3"):
        SceneBase.__init__(self)
        
        # Play music.
        sound.play_music(song)
        
        # Starting point for the credits scroll, just off screen.
        self.x = 780
        self.y = 100
    
    # Handles user input passed from the main engine.
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                    # Enter or Escape key returns to title screen.
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                        sound.stop_music()
                        self.SwitchToScene(TitleScene())
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
    def Render(self, screen):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        url_size = 19
        
        font_eula = path = os.path.dirname(os.path.realpath(__file__)) + "/fonts/fonts_license.html"
        font_eula = path.replace('/', os.sep).replace('\\', os.sep)
        
        # List of credit entries and their starting positions.
        credits_roll = [
            Credit("Main Programming: George Markeloff", (self.y, self.x)),
            Credit("Additional Programming: ???", (self.y, self.x + 100)),
            Credit("Art: ???", (self.y, self.x + 200)),
            Credit("Title Music - Enchanted Festival, By: Matthew Pablo", (self.y, self.x + 300)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 330), url_size, link_blue),
            Credit("Credits Music - Her Violet Eyes, By: tgfcoder", (self.y, self.x + 400)),
            Credit("https://twitter.com/tgfcoder", (self.y, self.x + 430), url_size, link_blue),
            Credit("Battle Music - A Wild Creature Appears, By: Aaron Parsons", (self.y, self.x + 500)),
            Credit("Boss Fight Music - Battle of the Void, By: Marcelo Fernandez", (self.y, self.x + 600)),
            Credit("Forest Area Music - Forest, By: syncopika", (self.y, self.x + 700)),
            Credit("https://greenbearmusic.bandcamp.com/track/forest", (self.y, self.x + 730), url_size, link_blue),
            Credit("Town Music - Plesant Creek, By: Matthew Pablo", (self.y, self.x + 800)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 830), url_size, link_blue),
            Credit("Combat System Design: George Markeloff", (self.y, self.x + 900)),
            Credit("Combat Balancing: George Markeloff", (self.y, self.x + 1000)),
            Credit("Character Class Design: George Markeloff", (self.y, self.x + 1100)),
            Credit("Story: George Markeloff", (self.y, self.x + 1200)),
            Credit("Dialog: George Markeloff", (self.y, self.x + 1300)),
            Credit("All audio and art assets licensed under CC-BY 3.0/4.0", (self.y, self.x + 1400)),
            Credit("https://creativecommons.org/licenses/by/3.0/", (self.y, self.x + 1430), url_size, link_blue),
            Credit("Fonts used under Larabie Fonts Freeware Fonts EULA.", (self.y, self.x + 1500)),
            Credit(font_eula, (self.y, self.x + 1530), url_size, link_blue),
            Credit("Written in Python using the Pygame engine.", (self.y, self.x + 1600))
            
        ]
        
        url_pattern = []
        
        # Run through the credits roll entries.
        for x in range(len(credits_roll)):
            # Draw the entries on the screen.
            screen.blit(credits_roll[x].rend, credits_roll[x].pos)
            # Populate the url pattern list with the index numbers of URL entries.
            if credits_roll[x].color == link_blue:
                url_pattern.append(x)
        
        self.credit_urls = []
        self.credit_url_rects = []
        
        # Run through the URL pattern list.
        for x in range(len(url_pattern)):
            # Add the actual URL to a list for input processing.
            self.credit_urls.append(credits_roll[url_pattern[x]].text)
            # Add collidable rectangle to a list for input processing.
            self.credit_url_rects.append(credits_roll[url_pattern[x]].rend.get_rect(topleft=credits_roll[url_pattern[x]].pos))
            
# Create a global sound object so that whatever scene is active can use it.
sound = JukeBox()

# Start the game with; window width, window height, FPS limit, and starting scene.
run_game(1024, 768, 60, TitleScene())
