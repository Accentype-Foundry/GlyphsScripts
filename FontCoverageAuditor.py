# MenuTitle: Font Coverage Auditor
# Author: Miklós Ferencz
# 
# This script audits a set of required glyphs for a project.
# It identifies which glyphs are present and which are missing.

from GlyphsApp import Glyphs
from vanilla import Window, EditText, List, SplitView, Button, TextBox, TextEditor, ScrollView
import objc

NSFont = objc.lookUpClass("NSFont")

thisFont = Glyphs.font

if not thisFont:
    Glyphs.showNotification("Error", "Please open a font file first.")
else:
    class GlyphAudit:
        def __init__(self):
            # --- Main window ---
            self.w = Window((1000, 600), "Font Coverage Auditor")
            
            # Font settings
            self.fontSize = 14
            self.uiFont = NSFont.systemFontOfSize_(self.fontSize)
            
            # Internal storage
            self.raw_glyph_list = []
            self.missing = []
            self.existing = []

            # Use a Scrollable TextEditor for the input to allow scrolling
            self.w.editText = TextEditor((10, 10, -10, 100), 
                                         callback=self.updateRawList)
            
            # Initial text setup
            default_text = "Paste or type here the glyphs you want to audit, separated by spaces or commas."
            self.w.editText.set(default_text)
            self.updateRawList(None)

            # Start button
            self.w.startButton = Button((10, 120, -10, 25), "▶️ Start Audit", callback=self.runAudit)

            # Summary
            self.w.summary = TextBox((10, 155, -10, 20), "Total: 0 | Missing: 0 | Existing: 0")

            # Search UI
            self.w.searchField = EditText((400, 150, 200, 22), callback=self.filterList)
            self.w.searchLabel = TextBox((345, 153, 50, 20), "Search:")

            # Panels
            self.imported_text_view = TextEditor((0, 0, -0, -0), readOnly=True)
            self.missing_list_view = List((0, 0, -0, -0), [])
            self.existing_list_view = List((0, 0, -0, -0), [])

            panels = [
                dict(view=self.imported_text_view, identifier="imported", minSize=100),
                dict(view=self.missing_list_view, identifier="missing", minSize=100),
                dict(view=self.existing_list_view, identifier="existing", minSize=100)
            ]
            self.w.splitView = SplitView((0, 185, -0, -0), panels, isVertical=False)

            self.w.open()

        def updateRawList(self, sender):
            content = self.w.editText.get()
            clean_content = content.replace("[", "").replace("]", "")
            self.raw_glyph_list = [g.strip() for g in clean_content.split() if g.strip()]

        def runAudit(self, sender):
            self.updateRawList(None)
            all_glyphs = self.raw_glyph_list

            self.existing = [f"{g} ✅" for g in all_glyphs if thisFont.glyphs[g]]
            self.missing = [f"{g} 🟥" for g in all_glyphs if not thisFont.glyphs[g]]

            self.imported_text_view.set(", ".join(all_glyphs))
            self.missing_list_view.set(self.missing)
            self.existing_list_view.set(self.existing)

            self.w.summary.set(f"Total: {len(all_glyphs)} | Missing: {len(self.missing)} | Existing: {len(self.existing)}")

        def filterList(self, sender):
            query = self.w.searchField.get().lower()
            
            # 1. Highlight and Jump to text
            full_text = " ".join(self.raw_glyph_list)
            highlighted_text = ""
            scroll_to_index = -1

            if query:
                for word in self.raw_glyph_list:
                    if query in word.lower():
                        marked = f"[{word}]"
                        if scroll_to_index == -1:
                            scroll_to_index = len(highlighted_text)
                        highlighted_text += marked + " "
                    else:
                        highlighted_text += word + " "
                
                self.w.editText.set(highlighted_text.strip())
                
                # Try to scroll by setting the selection/cursor near the match
                if scroll_to_index != -1:
                    textView = self.w.editText.getNSTextView()
                    textView.setSelectedRange_((scroll_to_index, len(query) + 2))
                    textView.scrollRangeToVisible_((scroll_to_index, len(query) + 2))
            else:
                self.w.editText.set(full_text)

            # 2. Filter Result Lists
            if self.missing or self.existing:
                self.missing_list_view.set([g for g in self.missing if query in g.lower()])
                self.existing_list_view.set([g for g in self.existing if query in g.lower()])

    GlyphAudit()
