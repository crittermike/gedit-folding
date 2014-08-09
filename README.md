Code Folding for Gedit
========================

A simple plugin that adds keyboard-based code folding to Gedit.

Installation
--------------

- Move `folding.gedit-plugin` and `folding.py` into `~/.gnome2/gedit/plugins`
- In Gedit, go to Edit &rarr; Preferences &rarr; Plugins to enable the plugin.

Usage
--------

- `Alt-Z` on highlighted text will collapse it
- `Alt-Z` on an indented block's top line will collapse that block
- `Alt-Z` on a folded block will expand it, but not collapsed sub-blocks
- `Alt-Q` will collapse the whole document
- `Alt-X` will expand all the collapsed blocks

Known limitation
--------
When unfolding (Alt-Z) selected text, unless the second line was indented,
the previously selected text will not appear. Please do a Alt-X to
display such text.