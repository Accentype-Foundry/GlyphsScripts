# MenuTitle: Font Coverage Auditor
# Author: Miklós Ferencz
# 
# This script audits a set of required glyphs for a project.
# It identifies which glyphs are present and which are missing.

from GlyphsApp import Glyphs
from vanilla import Window, EditText, List, SplitView, Button, TextBox, TextEditor
import objc
NSFont = objc.lookUpClass("NSFont")

thisFont = Glyphs.font

if not thisFont:
	Glyphs.showNotification("Error", "Please open a font file first.")
else:
	class GlyphAudit:
		def __init__(self):
			# --- Main window ---
			self.w = Window((1000, 500), "Font Coverage Auditor")
			
      # Font settings
			self.fontSize = 16
			self.uiFont = NSFont.systemFontOfSize_(self.fontSize)

			# EditText for input
			self.w.editText = EditText((10, 10, -10, 60),
									   text=".notdef a b c d e f")

			# Start button
			self.w.startButton = Button((10, 75, -10, 25),
										"▶️ Start",
										callback=self.runAudit)

			# Summary TextBox
			self.w.summary = TextBox((10, 105, -10, 20),
									 "Total: 0 | Missing: 0 | Existing: 0")

			# SplitView panels
			# Use TextEditor for imported list to support word wrapping
			self.imported_text_view = TextEditor((0, 0, -0, -0), readOnly=True)
			self.missing_list_view = List((0, 0, -0, -0), [])
			self.existing_list_view = List((0, 0, -0, -0), [])

			panels = [
				dict(view=self.imported_text_view, identifier="imported", minSize=50),
				dict(view=self.missing_list_view, identifier="missing", minSize=100),
				dict(view=self.existing_list_view, identifier="existing", minSize=100)
			]

			self.w.splitView = SplitView((0, 130, -0, -0), panels, isVertical=False)
			self.w.open()

		def runAudit(self, sender):
			# Get glyph names from input
			glyph_string = self.w.editText.get()
			all_glyphs = [g.strip() for g in glyph_string.split() if g.strip()]

			# Separate existing and missing glyphs
			existing = [f"{g} ✅" for g in all_glyphs if thisFont.glyphs[g]]
			missing = [f"{g} 🟥" for g in all_glyphs if not thisFont.glyphs[g]]

			# Prepare string for the wrapped text view
			imported_full_text = ", ".join(all_glyphs)

			# Update panels
			self.imported_text_view.set(imported_full_text)
			self.missing_list_view.set(missing)
			self.existing_list_view.set(existing)

			# Update summary stats
			total_count = len(all_glyphs)
			missing_count = len(missing)
			existing_count = len(existing)
			self.w.summary.set(f"Total: {total_count} | Missing: {missing_count} | Existing: {existing_count}")

			# Console output
			print(f"Imported: {total_count}")
			print(f"Existing: {existing_count}")
			print(f"Missing: {missing_count}")

	# Launch script
	GlyphAudit()