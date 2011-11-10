Code Folding for Gedit
========================

A simple plugin that adds keyboard-based code folding to Gedit.

Installation
--------------

####Unix/Linux
* Move `folding.plugin` and `folding.py` into `~/.local/share/gedit/plugins`
* In Gedit, go to Edit &rarr; Preferences &rarr; Plugins to enable the plugin.

####Windows

**Note**: As stated in IRC conversation at #gedit public channel, gedit3 is not ready for Windows (yet). Eventually this installation section will be updated when gedit3 supports Windows.

Usage
--------

* `Alt-Z` on selected lines will collapse them
* `Alt-Z` on an indented block's top line will collapse that block
* `Alt-Z` on a folded block will expand it
* `Alt-X` will collapse all blocks on the deepest indention column (you can keep pressing Alt-X until all indention levels are folded)
* `Shift-Alt-X` will expand all the collapsed blocks
