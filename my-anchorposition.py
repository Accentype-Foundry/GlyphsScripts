# MenuTitle: Move My Anchor
# Author: Miklós Ferencz
# Help: Moves anchors by name to a user-defined height.

# Moves selected anchors to a specific Y-coordinate across all highlighted glyphs.
# Ideal for standardizing accent placement or aligning anchors to custom metrics.

from vanilla import *


class FixAnchorPosition(object):
	def __init__(self):
		self.w = Window((250, 120), "Move My Anchor")
		self.w.text_name = TextBox((10, 15, 100, 17), "Anchor Name:", sizeStyle='small')
		self.w.anchorName = EditText((110, 12, 120, 19), "top", sizeStyle='small')
		
		self.w.text_y = TextBox((10, 45, 100, 17), "Target Y pos:", sizeStyle='small')
		self.w.targetY = EditText((110, 42, 120, 19), "794", sizeStyle='small')
		
		self.w.runButton = Button((10, 80, 230, 20), "Move Anchors", callback=self.move_anchors)
		self.w.open()

	def move_anchors(self, sender):
		anchor_name = self.w.anchorName.get()
		try:
			target_y = float(self.w.targetY.get())
		except ValueError:
			print("Error: Y position must be a number.")
			return

		thisFont = Glyphs.font
		# Csak a kijelölt gliféken fusson végig
		selectedLayers = thisFont.selectedLayers
		
		for thisLayer in selectedLayers:
			for thisAnchor in thisLayer.anchors:
				if thisAnchor.name == anchor_name:
					thisAnchor.y = target_y
			
		print(f"Done: All '{anchor_name}' anchors moved to {target_y}")

FixAnchorPosition()
