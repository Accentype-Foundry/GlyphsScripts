#MenuTitle: all_masters_in_text_mode
# -*- coding: utf-8 -*-
__doc__ = """
Displays all masters of the current Edit Tab text on separate lines. Perfect for reviewing and adjusting kerning across all masters simultaneously without switching tabs.
"""

# ---------------------------------------------------------------
# All Masters in Tab
# Opens a multi-line preview with one line per master,
# useful for kerning review.
# ---------------------------------------------------------------

font = Glyphs.font

# Get the currently active Edit View tab
tab = font.currentTab

if tab:
	# Extract the content of the first line only
	original_layers = []
	for l in tab.layers:
		# Stop collecting when we hit the first newline (GSControlLayer)
		if l.className() == "GSControlLayer":
			break
		original_layers.append(l)

	# This list will store all layers for the final multi-line preview
	new_layers = []

	# Iterate through all available masters in the font
	for master in font.masters:
		# Iterate through each character collected from the first line
		for l in original_layers:
			# 'parent' refers to the GSGlyph object (the "soul" of the character)
			glyph = l.parent

			# Get the specific layer associated with the current master ID
			master_layer = glyph.layers[master.id]

			# Add this master-specific layer to our new list
			new_layers.append(master_layer)

		# Append a newline after each master's line to separate them
		new_layers.append(GSControlLayer.newline())

	# Update the tab's content with our newly constructed list of layers
	tab.layers = new_layers

else:
	print("Error: Please open an Edit Tab first.")
