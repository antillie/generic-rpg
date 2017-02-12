#!/usr/bin/python
# -*- coding: utf-8 -*-

# This class holds all data about the current game session. Story progress, characters, inventory, ect...
class GameData:

    def __init__(self):
        # Scene transition data. Used to move between scenes and to allow the context dependent scenes know which scene called them.
        self.next_scene = "TitleScene"
        self.previous_scene = ""
        self.reset_display = False
