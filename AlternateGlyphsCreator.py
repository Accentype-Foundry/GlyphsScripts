# MenuTitle: Alternate Glyphs Creator
# Author: Miklós Ferencz
#
# This script can create X number of alternates for your glyphs.
# It also allows renaming selected alternates directly from Glyphs.

from GlyphsApp import Glyphs, GSGlyph, GSComponent
from vanilla import Window, EditText, Button, TextBox, SplitView, Group

class AltGlyphCreator:

    def __init__(self):
        # 1. Main Window
        self.w = Window((450, 300), "Alternate Glyphs Creator")

        # 2. Define Panels as Groups
        # --- Top panel: Create alternates ---
        self.create_group = Group((0, 0, 0, 0))
        self.create_group.glyphLabel = TextBox((10, 10, 150, 20), "Base Glyph Name:")
        self.create_group.glyphInput = EditText((170, 10, 100, 20), "")
        self.create_group.suffixLabel = TextBox((280, 10, 80, 20), "Alt Suffix:")
        self.create_group.suffixInput = EditText((360, 10, 70, 20), ".alt")
        self.create_group.numberLabel = TextBox((10, 40, 150, 20), "Number of alternates:")
        self.create_group.numberInput = EditText((170, 40, 100, 20), "6")
        self.create_group.createButton = Button((10, 80, -10, 25), "Create Alternates", callback=self.createAlternates)
        self.create_group.createStatus = TextBox((10, 115, -10, 20), "")

        # --- Bottom panel: Rename selected glyphs ---
        self.rename_group = Group((0, 0, 0, 0))
        self.rename_group.line = TextBox((0, 0, -0, 1), "—" * 200)
        self.rename_group.infoLabel = TextBox((10, 15, 400, 20), "Select glyphs, type ONLY the new suffix:")
        self.rename_group.renameInput = EditText((10, 40, 200, 20), "")
        self.rename_group.renameButton = Button((220, 40, 210, 25), "Rename Suffixes", callback=self.renameSelectedGlyphs)
        self.rename_group.renameStatus = TextBox((10, 75, -10, 25), "")

        # 3. Setup SplitView
        panels = [
            dict(view=self.create_group, identifier="create", minSize=140),
            dict(view=self.rename_group, identifier="rename", minSize=110)
        ]
        
        self.w.splitView = SplitView((0, 0, -0, -0), panels, isVertical=False)
        self.w.open()

    def createAlternates(self, sender):
        font = Glyphs.font
        if not font:
            self.create_group.createStatus.set("⚠️ No font open.")
            return

        base_name = self.create_group.glyphInput.get().strip()
        suffix = self.create_group.suffixInput.get().strip()

        try:
            num_alts = int(self.create_group.numberInput.get())
        except ValueError:
            self.create_group.createStatus.set("⚠️ Use an integer.")
            return

        font.disableUpdateInterface()
        try:
            for i in range(1, num_alts + 1):
                new_glyph_name = f"{base_name}{suffix}{i:02d}"
                if new_glyph_name in font.glyphs:
                    continue

                new_glyph = GSGlyph(new_glyph_name)
                font.addGlyph_(new_glyph)

                for layer in new_glyph.layers:
                    if base_name in font.glyphs:
                        component = GSComponent(base_name)
                        layer.components.append(component)
        finally:
            font.enableUpdateInterface()
        self.create_group.createStatus.set(f"Done for '{base_name}'.")

    def renameSelectedGlyphs(self, sender):
        font = Glyphs.font
        if not font or not font.selectedLayers:
            self.rename_group.renameStatus.set("⚠️ Select glyphs first.")
            return

        raw_suffix = self.rename_group.renameInput.get().strip()
        if not raw_suffix:
            self.rename_group.renameStatus.set("⚠️ Enter a new suffix.")
            return
            
        # Ensure the suffix starts with a dot
        new_suffix = raw_suffix if raw_suffix.startswith(".") else f".{raw_suffix}"

        font.disableUpdateInterface()
        try:
            for idx, layer in enumerate(font.selectedLayers, start=1):
                glyph = layer.parent
                old_name = glyph.name

                # Split and take only the base part (before the first dot)
                base_name = old_name.split('.')[0]
                
                # Construct: base + .new_suffix + 01, 02...
                new_name = f"{base_name}{new_suffix}{idx:02d}"

                if new_name in font.glyphs:
                    print(f"⚠️ '{new_name}' exists. Skipping.")
                    continue

                glyph.name = new_name
                print(f"✅ Renamed: {old_name} → {new_name}")
        finally:
            font.enableUpdateInterface()

        self.rename_group.renameStatus.set("Finished renaming suffixes.")

# Launch GUI
AltGlyphCreator()