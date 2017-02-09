#!/usr/bin/python
# -*- coding: utf-8 -*-

# For backwards compatibility with Python 2.
from __future__ import print_function

# Import modules.
import pygame
import os
import sys
import cache
sys.path.append("scenes")
import title
import credits_s
import gameinit

# Main engine. Sets up the window, handles rendering, manages scene changes, and forwards player input to the active scene.
def run_game(width=1024, height=576, fps=60, fullscreen=False):
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
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF)
    
    clock = pygame.time.Clock()
    pygame.display.set_caption("Generic RPG")
    
    # Initialize scenes.
    TitleScene = title.TitleScene()
    CreditsScene = credits_s.CreditsScene()
    GameScene = gameinit.GameScene()
    
    # Set the starting scene.
    active_scene = TitleScene
    
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
        if fullscreen:
            # Fullscreen mode.
            active_scene.Render(screen, screen_info.current_w, screen_info.current_h)
        else:
            # Windowed mode.
            active_scene.Render(screen, width, height)
        # Change the active scene to whichever scene should be next.
        
        next_scene = active_scene.next
        
        if next_scene == "TitleScene":
            TitleScene.next = "TitleScene"
            active_scene = TitleScene
        elif next_scene == "CreditsScene":
            CreditsScene.next = "CreditsScene"
            active_scene = CreditsScene
        elif next_scene == "GameScene":
            active_scene = GameScene
            
        if next_scene == None:
            active_scene = None
        
        # Draw the updated display buffer on the screen.
        pygame.display.flip()
        
        # Increment the internal game state at the desired FPS limit.
        clock.tick(fps)
        
    print("Thanks for playing!")

# Start the game with; window width, window height, FPS limit, and starting scene. Window width and height are ignored in fullscreen mode.
run_game()
