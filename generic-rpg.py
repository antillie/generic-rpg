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

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

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
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rend()
        
    def set_rend(self):
        self.rend = get_font(["Arial"], 20).render(self.text, True, self.get_color())
        
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
    def __init__(self, text, pos, size=40):
        self.text = text
        self.pos = pos
        self.size = size
        self.set_rend()
        
    def set_rend(self):
        self.rend = get_font(["Palatino"], self.size).render(self.text, True, white)

class JukeBox:
    # Sound class that handles all audio output.
    def __init__(self):
        self.music_playing = False
    
    def play_music(self, song):
        if self.music_playing == False:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(-1)
            self.music_playing = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def play_sound(self, sound):
        effect = pygame.mixer.Sound(sound)
        effect.play()

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
    pygame.display.set_caption("Genric RPG")
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
                        # Move to the next scene when the user pressed Enter
                        self.SwitchToScene(GameScene())
                    # Load game.
                    if self.menu == 1:
                        # Not yet implimented.
                        pass
                    # Roll credits.
                    if self.menu == 2:
                        # Not yet fully implimented.
                        sound.stop_music()
                        self.SwitchToScene(CreditsScene())
                    # Exit.
                    if self.menu == 3:
                        self.Terminate()
                # Down arrow.
                if event.key == pygame.K_DOWN:
                    # Play the menu sound effect.
                    path = os.path.dirname(os.path.realpath(__file__)) + "/sound/menu_change.wav"
                    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                    sound.play_sound(path)
                    # Incriment the menu.
                    self.menu = self.menu + 1
                    if self.menu == 4:
                        # Loop the menu if we went past the end.
                        self.menu = 0
                # Up arrow.
                if event.key == pygame.K_UP:
                    # Play the menu sound effect.
                    path = os.path.dirname(os.path.realpath(__file__)) + "/sound/menu_change.wav"
                    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                    sound.play_sound(path)
                    # Incriment the menu.
                    self.menu = self.menu - 1
                    if self.menu == -1:
                        # Loop the menu if we went past the end.
                        self.menu = 3
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click.
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    if self.url_rect.collidepoint(mpos):
                        # Launch the default web browser for the URL.
                        webbrowser.open("http://www.matthewpablo.com", new=2)
    
    # Internal game logic. Doesn't really apply to the main menu.
    def Update(self):
        pass
        
    # Draws things.
    def Render(self, screen):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        # Play the title music.
        path = os.path.dirname(os.path.realpath(__file__)) + "/sound/music/" + self.song
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound.play_music(canonicalized_path)
        
        # Title text.
        title = get_font(["Arial"], 70).render("Generic RPG Name",True,white)
        screen.blit(title, [200, 60])
        
        # Menu entries.
        self.options = [
            Option("New Game", (450, 300)),
            Option("Load Game", (450, 330)),
            Option("Credits", (450, 360)),
            Option("Exit", (450, 390))
            ]
            
        self.options[self.menu].select()
        for x in range(len(self.options)):
            screen.blit(self.options[x].rend, self.options[x].pos)
        
        
        # Title music credit at the bottom of the screen.
        #music_credit = get_font(["Arial"], 13).render(str("Featuring Music by Matthew Pablo"),True,white)
        #screen.blit(music_credit, [412, 730])
        #music_url = get_font(["Arial"], 13).render(str("www.matthewpablo.com"),True,white)
        #screen.blit(music_url, [428, 747])
        #self.url_rect = music_url.get_rect(topleft=(428, 747))

class GameScene(SceneBase):
    # The actual game. Different versions of this class will need to load maps, characters, dialog, and detect interactions between objects on the screen. Each area will be its own class.
    def __init__(self, song="plesantcreekloop.mp3"):
        SceneBase.__init__(self)
        self.song = song
        
        # Play music.
        path = os.path.dirname(os.path.realpath(__file__)) + "/sound/music/" + song
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound.play_music(canonicalized_path)
        
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
        path = os.path.dirname(os.path.realpath(__file__)) + "/sound/music/" + song
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound.play_music(canonicalized_path)
        self.x = 768
        self.y = 100
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                    # Enter or Escape key returns to title screen.
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                        sound.stop_music()
                        self.SwitchToScene(TitleScene())
                    
    def Update(self):
        self.x = self.x - 1
    
    def Render(self, screen):
        # Start with a black screen.
        screen.fill((0, 0, 0))
        
        credits_roll = [
            Credit("Main Programming: George Markeloff", (self.y, self.x)),
            Credit("Art/Additional Programming: ???", (self.y, self.x + 100)),
            Credit("Title Music - Enchanted Festival, By: Matthew Pablo", (self.y, self.x + 200)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 230), 28),
            Credit("Credits Music - Her Violet Eyes, By: tgfcoder", (self.y, self.x + 300)),
            Credit("https://twitter.com/tgfcoder", (self.y, self.x + 330), 28),
            Credit("Battle Music - A Wild Creature Appears, By: Aaron Parsons", (self.y, self.x + 400)),
            Credit("Boss Fight Music - Battle of the Void, By: Marcelo Fernandez", (self.y, self.x + 500)),
            Credit("Forest Area Music - Forest, By: syncopika", (self.y, self.x + 600)),
            Credit("https://greenbearmusic.bandcamp.com/track/forest", (self.y, self.x + 630), 28),
            Credit("Town Music - Plesant Creek, By: Matthew Pablo", (self.y, self.x + 700)),
            Credit("http://www.matthewpablo.com", (self.y, self.x + 730), 28),
            Credit("Combat System Design: George Markeloff", (self.y, self.x + 800)),
            Credit("Combat Balancing: George Markeloff", (self.y, self.x + 900)),
            Credit("Character Class Design: George Markeloff", (self.y, self.x + 1000)),
            Credit("Story: George Markeloff", (self.y, self.x + 1100)),
            Credit("Dialog: George Markeloff", (self.y, self.x + 1200)),
            Credit("All audio and art assets licensed under CC-BY 3.0/4.0", (self.y, self.x + 1300)),
            Credit("https://creativecommons.org/licenses/by/3.0/", (self.y, self.x + 1330), 28),
            Credit("Written in Python using the Pygame engine.", (self.y, self.x + 1400))
        ]
        for x in range(len(credits_roll)):
            screen.blit(credits_roll[x].rend, credits_roll[x].pos)
        
# Create a global sound object so that whatever scene is active can use it.
sound = JukeBox()

# Start the game with; window width, window height, FPS limit, and starting scene.
run_game(1024, 768, 60, TitleScene())
