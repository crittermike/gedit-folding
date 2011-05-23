Code Folding for Gedit
========================

A simple plugin that adds keyboard-based code folding to Gedit.

Installation
--------------

For Unix/Linux:
- Move `folding.gedit-plugin` and `folding.py` into `~/.gnome2/gedit/plugins`
- In Gedit, go to Edit &rarr; Preferences &rarr; Plugins to enable the plugin.

For Windows:
- Move `folding.gedit-plugin` and `folding.py` into `C:\Program Files\gedit\lib\gedit-2\plugins`
- In Gedit, go to Edit &rarr; Preferences &rarr; Plugins to enable the plugin.

Usage
--------

- `Alt-Z` on selected lines will collapse them
- `Alt-Z` on an indented block's top line will collapse that block
- `Alt-Z` on a folded block will expand it
- `Alt-X` will collapse all blocks on the deepest indention column (you can keep pressing Alt-X until all indention levels are folded)
- `Shift-Alt-X` will expand all the collapsed blocks

