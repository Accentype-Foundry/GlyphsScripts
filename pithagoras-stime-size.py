# MenuTitle: Pithagoras-StemSize
# Author: Miklós Ferencz
# Help: Displays the stem width(s) of the selected vertical glyphs.
#       Note: This tool works only for straight vertical stems. 
#       It does NOT yet support rounded glyphs (like 'o', 's') 
#       or diagonal stems (like 'x', 'z'). Future updates may add these features.
#       Ideal for spotting stem width inconsistencies within your glyphs.


from GlyphsApp import Glyphs
from math import sqrt
from vanilla import Window, List, SplitView

# Function to calculate distance between two nodes
def distance(p1, p2):
	return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

# Get the current font and selected layers
font = Glyphs.font
selected_layers = font.selectedLayers

# Two lists for the SplitView: left = glyph names, right = stem info
glyph_list = []
stem_list = []

# Process each selected layer
for layer in selected_layers:
	glyph = layer.parent

	# Automatic minimum and maximum stem dimensions
	bbox_height = layer.bounds.size.height
	MIN_HEIGHT = bbox_height * 0.3

	bbox_width = layer.bounds.size.width
	MAX_STEM_WIDTH = bbox_width * 0.4

	# 1️⃣ Collect vertical segments from paths
	verticals = []

	for path in layer.paths:
		nodes = path.nodes
		for i, node in enumerate(nodes):
			next_node = nodes[(i + 1) % len(nodes)]
			if node.x == next_node.x:  # Only vertical segments
				y1, y2 = sorted([node.y, next_node.y])
				height = y2 - y1
				if height >= MIN_HEIGHT:
					verticals.append((node.x, y1, y2))

	# 2️⃣ Process components
	for comp in layer.components:
		base_glyph = comp.component
		base_layer = base_glyph.layers[layer.layerId]
		xx, xy, yx, yy, tx, ty = comp.transform  # unpack transform

		for path in base_layer.paths:
			nodes = path.nodes
			for i, node in enumerate(nodes):
				next_node = nodes[(i + 1) % len(nodes)]
				# Apply transform to node coordinates
				n1x = node.x * xx + node.y * xy + tx
				n1y = node.x * yx + node.y * yy + ty
				n2x = next_node.x * xx + next_node.y * xy + tx
				n2y = next_node.x * yx + next_node.y * yy + ty

				if n1x == n2x:
					y1, y2 = sorted([n1y, n2y])
					height = y2 - y1
					if height >= MIN_HEIGHT:
						verticals.append((n1x, y1, y2))

	# 3️⃣ Find stem pairs
	stems = []
	used = set()
	for i in range(len(verticals)):
		if i in used:
			continue
		x1, y1a, y1b = verticals[i]
		for j in range(i + 1, len(verticals)):
			if j in used:
				continue
			x2, y2a, y2b = verticals[j]

			# Y-range overlap
			overlap = min(y1b, y2b) - max(y1a, y2a)
			if overlap > 0:
				width = abs(x1 - x2)
				if 5 < width < MAX_STEM_WIDTH:
					stems.append(width)
					used.add(i)
					used.add(j)
					break

	# 4️⃣ Store info in the lists
	info1 = f"{glyph.name} | {layer.name}"           # Left panel: glyph + layer
	info2 = f"stems: {len(stems)} | widths: {stems}" # Right panel: stem info
	glyph_list.append(info1)
	stem_list.append(info2)

# 5️⃣ Create Vanilla window with SplitView
class SplitViewDemo:

	def __init__(self, glyph_list, stem_list):
		# Window size: width x height
		self.w = Window((600, 400), "Pithagoras-StemSize", minSize=(300, 200))

		# SplitView panels
		panels = [
			dict(view=List((0, 0, -0, -0), glyph_list), identifier="glyphs"),
			dict(view=List((0, 0, -0, -0), stem_list), identifier="stems")
		]

		# Add SplitView to window
		self.w.splitView = SplitView((0, 0, -0, -0), panels)
		self.w.open()

# Instantiate and open
SplitViewDemo(glyph_list, stem_list)
