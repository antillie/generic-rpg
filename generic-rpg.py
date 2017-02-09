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

# Global sound object that handles all audio output.
sound = sound.JukeBox()

# Global cache object that handles all image and font object caching.
cache = cache.CacheEngine()

# Main engine. Sets up the window, handles rendering, manages scene changes, and forwards player input to the active scene.
def run_game(width=1024, height=576, fps=60, fullscreen=False):
    # Initialize the engine and get information about the user's display.
    pygame.init()
    screen_info = pygame.display.Info()
    
    # Load and set the window icon.
    temp_path = os.path.dirname(os.path.realpath(__file__)) + "/images/window_shield.png"
    canonicalized_path = temp_path.replace('/', os.sep).replace('\\', os.sep)
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
    
    # Initialize scenes and pass them all the sound object so that all audio output is centralized.
    TitleScene = title.TitleScene(sound, cache)
    CreditsScene = credits_s.CreditsScene(sound, cache)
    GameScene = gameinit.GameScene(sound, cache)
    PartyScreen = party_screen.PartyScreen(sound, cache)
    
    # Set the starting scene.
    active_scene = TitleScene
    
    # Main game loop.
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
            elif not fullscreen:
                if event.type == pygame.VIDEORESIZE:
                    # Update the rendering surface when the user resizes the game window.
                    width = event.size[0]
                    height = event.size[1]
                    screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            if quit_attempt:
                # Close the program.
                active_scene.Terminate()
            else:
                # Queue the input to be sent to the active scene.
                filtered_events.append(event)
        
        if active_scene.name != "PartyScreen":
            PartyScreen.previous_scene = active_scene.name
        
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
        
        # Change the active scene to whichever scene should be next.
        if next_scene == "TitleScene":
            TitleScene.next = "TitleScene"
            active_scene = TitleScene
        elif next_scene == "CreditsScene":
            CreditsScene.next = "CreditsScene"
            active_scene = CreditsScene
        elif next_scene == "GameScene":
            GameScene.next = "GameScene"
            active_scene = GameScene
        elif next_scene == "PartyScreen":
            PartyScreen.next = "PartyScreen"
            active_scene = PartyScreen
        elif next_scene == None:
            active_scene = None
        
        # Draw the updated display buffer on the screen.
        pygame.display.flip()
        
        # Increment the internal game state at the desired FPS limit.
        clock.tick(fps)
        
    print("Thanks for playing!")

# Start the game with; window width, window height, FPS limit, and starting scene. Window width and height are ignored in fullscreen mode.
run_game()
