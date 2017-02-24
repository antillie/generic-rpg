from cx_Freeze import setup, Executable
import sys
import os

icon_file = os.path.dirname(os.path.realpath(__file__)) + "/images/window_shield.ico"

exe = Executable(
      script="generic-rpg.py",
      base="Win32GUI",
      targetName="generic-rpg.exe",
      icon=icon_file
     )

buildOptions = dict(
    include_files = ["gamedata/", "scenes/", "sound/", "images/", "fonts/", "colors.py", "utils.py", "virtualscreen.py", "pyganim.py"],
    excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "email", "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", "tcl", "Tkconstants", "Tkinter"]
    )

setup(
         name = "Generic RPG",
         version = "0.2",
         description = "Generic RPG",
         author = "George Markeloff",
         options = dict(build_exe = buildOptions),
         executables = [exe]
    )
