#!/usr/bin/python
# -*- coding: utf-8 -*-

class GameData:

    def __init__(self):
        # Scene transition data. Used to move between scenes and to allow the context dependant scenes know which scene called them.
        self.next_scene = "TitleScene"
        self.previous_scene = ""
        self.reset_display = False
