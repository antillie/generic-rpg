# generic-rpg
An SNES style JRPG. Mostly to teach myself OOP and proper python habbits.

This is more of a framework/game engine at this point than an actual game.
Although it runs fine and you can move around there isn't anything to actually play yet.

Resizing the window or running in fullscreen mode takes a somewhat beefy CPU.
This is because pygame's smoothscale() function is CPU intensive.

System requirments:

    Python 2.7 with libraries:
        (These can be installed with pip.)
        pygame
        pyscroll
        pytmx
    
    1280x720 (or larger) display
    Keyboard
    Sound output

Controls:
    
    Menus:
        Arrow keys or W/S and Enter/Space or the mouse
    
    Game world:
        Move with the arrow keys or WASD
        Interact with Enter or Space
    
    Fullscreen mode toggle:
        F11 or ALT+ENTER
    
    Escape pulls up the party screen from the game world.
    Escape and Enter exit the credits screen.
    
Tested on Windows and Linux. But any platform that has Python 2.7 and the needed libraries should work.

It runs on Python 3.4 on Linux but Python 3.6 on Windows seems to dislike my imports.
I am not terribly interested in fixing this right now.

Uses creative commons art and sound assets. Mostly CC-BY. Some CC-BY-SA. Some public domain.
(https://creativecommons.org/licenses/)
Artists and specific asset details are listed in the credits screen.

The python code is Copyright (c) 2017 by George Markeloff and licensed under the GNU GPL version 3 unless noted otherwise.
See LICENSE.txt for the full license terms.

The transitions module is Copyright (c) 2014 by Death_Miner and is licensed under the MIT license.
(https://github.com/DeathMiner/Pygame-Transitions)
Full license terms are in the module itself.

The pyganim module is Copyright (c) 2011 by Al Sweigart and is licensed under the "Simplified BSD" license.
(http://inventwithpython.com/pyganim/)
Full license terms are in the module itself.
