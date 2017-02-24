#!/usr/bin/python
# -*- coding: utf-8 -*-

# Use the modern print function and proper division.
from __future__ import print_function, division

# Import modules.
import pygame
import os
import sys
import cache
import sound
import webbrowser
import pyscroll
import pytmx.util_pygame
sys.path.append("gamedata")
sys.path.append("gamedata/characters")
sys.path.append("gamedata/classes")
sys.path.append("gamedata/races")
sys.path.append("gamedata/weapons")
sys.path.append("gamedata/spells")
import gamedata
sys.path.append("scenes")
sys.path.append("scenes/resources")
import title
import credits_s
import gameinit
import party_screen
import battle
import transitions
import worldmap
import status
import inventory

# Global sound object that handles all audio output.
sound = sound.JukeBox()

# Global cache object that handles all image and font object caching.
cache = cache.CacheEngine()

# Main engine. 91 octane minimum. Premium fuel recommended. See owners manual for details.
class Engine:
    
    def reset_game(self, transition, width, height):
        
        if self.fullscreen:
            # Game data object that stores everything about the current game session. Characters, dialog, story progress, scene progression, quests, ect...
            self.gamedata = gamedata.GameData(cache, screen_info.current_w, screen_info.current_h)
        else:
            # Game data object that stores everything about the current game session. Characters, dialog, story progress, scene progression, quests, ect...
            self.gamedata = gamedata.GameData(cache, width, height)
        
        # Once things get going this will instead just call a game data reset function instead of remaking all the objects.
        self.TitleScene = title.TitleScene(sound, cache, transition, self.gamedata)
        self.GameScene = gameinit.GameScene(sound, cache, transition, self.gamedata)
        self.BattleScreen = battle.BattleScreen(sound, cache, transition, self.gamedata)
        self.PartyScreen = party_screen.PartyScreen(sound, cache, transition, self.gamedata)
        self.WorldMap = worldmap.WorldMap(sound, cache, transition, self.gamedata)
        self.CreditsScene = credits_s.CreditsScene(sound, cache, transition, self.gamedata)
        self.InventoryScreen = inventory.InventoryScreen(sound, cache, transition, self.gamedata)
        
    # Sets up the window, handles screen modes/sizes, manages scene changes, and forwards player input to the active scene.
    def run(self, width=1280, height=720, fps=60, fullscreen=False):
        # Initialize the underlying pygame engine and get information about the user's display.
        pygame.init()
        screen_info = pygame.display.Info()
        self.fullscreen = fullscreen
        
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
                self.fullscreen = True
            else:
                self.fullscreen = False
        except:
            # No big deal, just use the defaults.
            pass
        
        # Load and set the window icon.
        
        if getattr(sys, 'frozen', False):
            # frozen
            temp_path = os.path.dirname(sys.executable) + "/images/window_shield.png"
        else:
            # unfrozen
            temp_path = os.path.dirname(os.path.realpath(__file__)) + "/images/window_shield.png"
            
        canonicalized_path = temp_path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canonicalized_path)
        pygame.display.set_icon(image)
        
        if self.fullscreen:
            # Fullscreen mode.
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
            transition = transitions.Transition(screen, screen_info.current_w, screen_info.current_h, [0, 0, 0])
            # Game data object that stores everything about the current game session. Characters, dialog, story progress, scene progression, quests, ect...
            self.gamedata = gamedata.GameData(cache, screen_info.current_w, screen_info.current_h)
        else:
            # Windowed mode.
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF)
            transition = transitions.Transition(screen, width, height, [0, 0, 0])
            # Game data object that stores everything about the current game session. Characters, dialog, story progress, scene progression, quests, ect...
            self.gamedata = gamedata.GameData(cache, width, height)
        
        # Initilize the internal clock and set the window title.
        clock = pygame.time.Clock()
        pygame.display.set_caption("Generic RPG")
        
        # Initialize scenes and pass them all the sound, cache, transition, and gamedata objects.
        self.TitleScene = title.TitleScene(sound, cache, transition, self.gamedata)
        self.CreditsScene = credits_s.CreditsScene(sound, cache, transition, self.gamedata)
        self.GameScene = gameinit.GameScene(sound, cache, transition, self.gamedata)
        self.PartyScreen = party_screen.PartyScreen(sound, cache, transition, self.gamedata)
        self.BattleScreen = battle.BattleScreen(sound, cache, transition, self.gamedata)
        self.WorldMap = worldmap.WorldMap(sound, cache, transition, self.gamedata)
        self.StatusScreen = status.StatusScreen(sound, cache, transition, self.gamedata)
        self.InventoryScreen = inventory.InventoryScreen(sound, cache, transition, self.gamedata)
        
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
                            self.fullscreen = False
                            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                            transition = transitions.Transition(screen, width, height, [0, 0, 0])
                        else:
                            self.fullscreen = True
                            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
                            transition = transitions.Transition(screen, screen_info.current_w, screen_info.current_h, [0, 0, 0])
                    # User pressed F11.
                    elif event.key == pygame.K_F11:
                        # Toggle between fullscreen and windowed mode.
                        if fullscreen:
                            self.fullscreen = False
                            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                            transition = transitions.Transition(screen, width, height, [0, 0, 0])
                        else:
                            self.fullscreen = True
                            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
                            transition = transitions.Transition(screen, screen_info.current_w, screen_info.current_h, [0, 0, 0])
                    else:
                        # Queue the input to be sent to the active scene.
                        filtered_events.append(event)
                
                # Mouse motion.
                elif event.type == pygame.MOUSEMOTION:
                    filtered_events.append(event)
                # Mouse clicks.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    filtered_events.append(event)
                
                # Only listen for resize events in windowed mode.
                elif not self.fullscreen:
                    if event.type == pygame.VIDEORESIZE:
                        # Update the rendering surface when the user resizes the game window.
                        width = event.size[0]
                        height = event.size[1]
                        screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                        transition = transitions.Transition(screen, width, height, [0, 0, 0])
                
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
                        ini_data = ini_data + "xTrue"
                    else:
                        ini_data = ini_data + "xFalse"
                    # Write the data to our ini file.
                    ini_file.write(ini_data)
                    # Then close the file.
                    ini_file.close()
                    
                    # Close the program.
                    print("Thanks for playing!")
                    sys.exit()
                
            # No active scene means that we are done.
            if active_scene != None:
                # If a transition is playing let it finish before we continue.
                if transition.updateScreen() == False:
                    # Pass the input to the active scene for processing.
                    active_scene.ProcessInput(filtered_events, pressed_keys)
                    # Have the active scene run its internal game logic.
                    active_scene.Update()
                    # Tell the active scene to render itself to the display buffer.
                    if self.fullscreen:
                        # Fullscreen mode.
                        active_scene.Render(screen, screen_info.current_w, screen_info.current_h)
                    else:
                        # Windowed mode.
                        active_scene.Render(screen, width, height)
                    
                    # If we are changing from the party screen to the title screen then we need to reset the state of the game.
                    if self.gamedata.next_scene == "TitleScene" and self.gamedata.previous_scene  == "PartyScreen":
                        self.reset_game(transition, width, height)
                        self.gamedata.previous_scene = "something else"
                    
                    # Reset the display to the defaults if requested by the user.
                    if self.gamedata.reset_display:
                        self.gamedata.reset_display = False
                        width=1280
                        height=720
                        self.fullscreen=False
                        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                        transition = transitions.Transition(screen, width, height, [0, 0, 0])
                    
                    # Change the active scene to whichever scene should be next.
                    if self.gamedata.next_scene == "TitleScene":
                        active_scene = self.TitleScene
                    elif self.gamedata.next_scene == "CreditsScene":
                        active_scene = self.CreditsScene
                    elif self.gamedata.next_scene == "GameScene":
                        active_scene = self.GameScene
                    elif self.gamedata.next_scene == "PartyScreen":
                        active_scene = self.PartyScreen
                    elif self.gamedata.next_scene == "BattleScreen":
                        active_scene = self.BattleScreen
                    elif self.gamedata.next_scene == "WorldMap":
                        active_scene = self.WorldMap
                    elif self.gamedata.next_scene == "StatusScreen":
                        active_scene = self.StatusScreen
                    elif self.gamedata.next_scene == "InventoryScreen":
                        active_scene = self.InventoryScreen
                    elif self.gamedata.next_scene == None:
                        active_scene = None
            
            # Draw the updated display buffer on the screen.
            pygame.display.flip()
            
            # Increment the internal game state at the desired FPS limit.
            clock.tick(fps)

# Make an instance of our game engine.
game = Engine()

# Start the game.
game.run()
