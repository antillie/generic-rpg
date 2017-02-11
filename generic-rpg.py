#!/usr/bin/python
# -*- coding: utf-8 -*-

# For backwards compatibility with Python 2.
from __future__ import print_function

# Import modules.
import pygame
import os
import sys
import cache
import sound
sys.path.append("scenes")
import title
import credits_s
import gameinit
import party_screen
import battle
import dummy

# Global sound object that handles all audio output.
sound = sound.JukeBox()

# Global cache object that handles all image and font object caching.
cache = cache.CacheEngine()

# Main engine.
class Engine:
    
    def reset_game(self):
        self.GameScene = gameinit.GameScene(sound, cache)
        self.BattleScreen = battle.BattleScreen(sound, cache)
        self.PartyScreen = party_screen.PartyScreen(sound, cache)
        
        
    # Sets up the window, handles screen modes/sizes, manages scene changes, and forwards player input to the active scene.
    def run(self, width=1280, height=720, fps=60, fullscreen=False):
        # Initialize the engine and get information about the user's display.
        pygame.init()
        screen_info = pygame.display.Info()
        
        # Try to load the previous window size and mode.
        try:
            homedir = os.path.expanduser("~")
            location = homedir + "/.generic-rpg/screen-size.ini"
            location = location.replace("/", os.sep).replace("\\", os.sep)
            ini_file = open(location, "r")
            # Read our ini file.
            geometry_data = ini_file.read()
            # Then close the file.
            ini_file.close()
            # Split the data into a list.
            window_data = geometry_data.split("x")
            # Set our window width and height to what we got from the file.
            width = int(window_data[0])
            height = int(window_data[1])
            # Enable or disable fullscreen mode based on what we got from the file.
            if window_data[2] == "True":
                fullscreen = True
            else:
                fullscreen = False
        except:
            # No big deal, just use the defaults.
            pass
        
        # Load and set the window icon.
        temp_path = os.path.dirname(os.path.realpath(__file__)) + "/images/window_shield.png"
        canonicalized_path = temp_path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canonicalized_path)
        pygame.display.set_icon(image)
        
        if fullscreen:
            # Fullscreen mode.
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        else:
            # Windowed mode.
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF)
        
        # Initilize the internal clock and set the window title.
        clock = pygame.time.Clock()
        pygame.display.set_caption("Generic RPG")
        
        # Initialize scenes and pass them all the sound and cache objects.
        self.TitleScene = title.TitleScene(sound, cache)
        self.CreditsScene = credits_s.CreditsScene(sound, cache)
        self.GameScene = gameinit.GameScene(sound, cache)
        self.PartyScreen = party_screen.PartyScreen(sound, cache)
        self.BattleScreen = battle.BattleScreen(sound, cache)
        self.DummyScreen = dummy.DummyScreen(sound, cache)
        
        # Set the starting scene.
        active_scene = self.TitleScene
        
        # Main game loop.
        while True:
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
                    # User pressed ALT+Enter.
                    elif event.key == pygame.K_RETURN and alt_pressed:
                        # Toggle between fullscreen and windowed mode.
                        if fullscreen:
                            fullscreen = False
                            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                        else:
                            fullscreen = True
                            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
                    # User pressed F11.
                    elif event.key == pygame.K_F11:
                        # Toggle between fullscreen and windowed mode.
                        if fullscreen:
                            fullscreen = False
                            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                        else:
                            fullscreen = True
                            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
                    else:
                        # Queue the input to be sent to the active scene.
                        filtered_events.append(event)
                # Only listen for resize events in windowed mode.
                elif not fullscreen:
                    if event.type == pygame.VIDEORESIZE:
                        # Update the rendering surface when the user resizes the game window.
                        width = event.size[0]
                        height = event.size[1]
                        screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                
                # No active scene means that we are done.
                if active_scene == None:
                    quit_attempt = True
                
                if quit_attempt:
                    # Save the window size and state.
    
                    # Get the user's home directory.
                    homedir = os.path.expanduser("~")
                    
                    # Make a directory called ".generic-rpg" if it doesn't exist.
                    location = homedir + "/.generic-rpg"
                    if not os.path.exists(location):
                        os.makedirs(location)
                    location = location + "/screen-size.ini"
                    location = location.replace("/", os.sep).replace("\\", os.sep)
                    
                    # Get the current window size.
                    ini_file = open(location, "w")
                    ini_data = str(width) + "x" + str(height)
                    if fullscreen:
                        ini_data = ini_data + "x" + "True"
                    else:
                        ini_data = ini_data + "x" + "False"
                    # Write the data to our ini file.
                    ini_file.write(ini_data)
                    # Then close the file.
                    ini_file.close()
                    
                    # Close the program.
                    print("Thanks for playing!")
                    exit()
                
            # No active scene means that we are done.
            if active_scene != None:
                # Let the context dependant scenes know what their previous scene was.
                if active_scene.name != "PartyScreen":
                    self.PartyScreen.previous_scene = active_scene.name
                
                if active_scene.name != "BattleScreen":
                    self.BattleScreen.previous_scene = active_scene.name
            
                # Pass the input to the active scene for processing.
                active_scene.ProcessInput(filtered_events, pressed_keys)
                # Have the active scene run its internal game logic.
                active_scene.Update()
                # Tell the active scene to render itself to the display buffer.
                if fullscreen:
                    # Fullscreen mode.
                    active_scene.Render(screen, screen_info.current_w, screen_info.current_h)
                else:
                    # Windowed mode.
                    active_scene.Render(screen, width, height)
                    
                # Get the next scene that sould be active.
                next_scene = active_scene.next
                
                # If we are changing from the party screen to the title screen then we need to reset the state of the game.
                if next_scene == "TitleScene" and self.previous_scene  == "PartyScreen":
                    self.reset_game()
                
                if next_scene == "TitleScene" and self.previous_scene  == "DummyScreen":
                    width=1280
                    height=720
                    fullscreen=False
                    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                
                # Change the active scene to whichever scene should be next.
                if next_scene == "TitleScene":
                    self.TitleScene.next = "TitleScene"
                    active_scene = self.TitleScene
                elif next_scene == "CreditsScene":
                    self.CreditsScene.next = "CreditsScene"
                    active_scene = self.CreditsScene
                elif next_scene == "GameScene":
                    self.GameScene.next = "GameScene"
                    active_scene = self.GameScene
                elif next_scene == "PartyScreen":
                    self.PartyScreen.next = "PartyScreen"
                    active_scene = self.PartyScreen
                elif next_scene == "BattleScreen":
                    self.BattleScreen.next = "BattleScreen"
                    active_scene = self.BattleScreen
                elif next_scene == "DummyScreen":
                    self.DummyScreen.next = "DummyScreen"
                    active_scene = self.DummyScreen
                elif next_scene == None:
                    active_scene = None
            
            if active_scene != None:
                # Store the current scene to be refrenced as the previous scene during the next loop iteration.
                self.previous_scene  = active_scene.name
            
            # Draw the updated display buffer on the screen.
            pygame.display.flip()
            
            # Increment the internal game state at the desired FPS limit.
            clock.tick(fps)

# Make an instance of our game engine.
game = Engine()

# Start the game.
game.run()
