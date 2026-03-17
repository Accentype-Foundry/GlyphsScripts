# MenuTitle: 📐 TERMINAL ANALYZER
# -*- coding: utf-8 -*-

import vanilla
import math
from GlyphsApp import Glyphs, NSRect, NSPoint

class TerminalAnalyzer(object):
    def __init__(self):
        self.results = []
        
        # Window
        self.win = vanilla.FloatingWindow((940, 520), "Terminal Analyzer")
        note_text = "⚠️ Run it on actual paths only! Won't work on components."
        self.win.note = vanilla.TextBox((20, 45, -20, 17), note_text, sizeStyle='small', alignment='center')

        # UI elements
        self.win.textRef = vanilla.TextBox((20, 12, 140, 17), "Reference Glyph:", sizeStyle='regular')
        self.win.refGlyphs = vanilla.EditText((140, 10, -200, 24), "C", sizeStyle='regular')
        
        self.win.clearBtn = vanilla.Button((-190, 10, 90, 24), "Clear All", callback=self.clear_all_checks)
        self.win.scanButton = vanilla.Button((-90, 10, 80, 24), "Scan", callback=self.scan)
        
        self.win.list = vanilla.List(
            (0, 75, -0, -20), [], 
            columnDescriptions=[
                {"title": "Verified", "width": 60, "cell": vanilla.CheckBoxListCell()},
                {"title": "Status", "width": 120},
                {"title": "Glyph Name", "width": 100},
                {"title": "Master", "width": 100},
                {"title": "Angle (±180°)", "width": 140, "key": "Angle"},
                {"title": "Coordinates (P1 / P2)", "width": 180},
                {"title": "Length", "width": 60}
            ], 
            selectionCallback=self.focus,
            editCallback=self.save_verification
        )
        
        self.win.open()
    
    # Resets all 'Verified' checkboxes in the UI list and updates the stored data
    def clear_all_checks(self, sender):
        items = self.win.list.get()
        for item in items:
            item["Verified"] = False
        self.win.list.set(items)
        self.save_verification(self.win.list)

    # Stores the verification status of each terminal in the glyph's userData for persistence
    def save_verification(self, sender):
        list_items = sender.get()
        for i, item in enumerate(list_items):
            if i < len(self.results) and self.results[i] is not None:
                res_item = self.results[i]
                glyph = res_item["layer"].parent
                storage_key = f"terminalChecked_{res_item['layer'].associatedMasterId}_{item['Coordinates (P1 / P2)']}"
                glyph.userData[storage_key] = item["Verified"]

    # Scans selected layers to identify terminal segments and compares their angles against reference glyphs
    def scan(self, sender):
        font = Glyphs.font
        if not font: return
        
        masterID = font.selectedFontMaster.id
        master_name = font.selectedFontMaster.name
        
        self.win.list.setSelection([])
        self.results = []
        list_items = []

        refs = []
        ref_input = self.win.refGlyphs.get()
        for name in ref_input.split(","):
            glyph = font.glyphs[name.strip()]
            if glyph:
                layer = glyph.layers[masterID]
                for path in layer.paths:
                    for i in range(len(path.nodes)):
                        n1, n2 = path.nodes[i-1], path.nodes[i]
                        if n1.type != "offcurve" and n2.type != "offcurve":
                            dist = math.sqrt((n2.x-n1.x)**2 + (n2.y-n1.y)**2)
                            if 5.0 < dist < 200.0:
                                angle = math.degrees(math.atan2(n2.y-n1.y, n2.x-n1.x)) % 360
                                if 1.0 < (angle % 90) < 89.0:
                                    refs.append(angle)

        # Iterates through each selected layer to set up tracking and UI display data
        for layer_obj in list(font.selectedLayers):
            curr_glyph = layer_obj.parent
            curr_layer = layer_obj
            start_count = len(list_items)
            show_name = curr_glyph.name

            for path in curr_layer.paths:
                node_count = len(path.nodes)
                for i in range(node_count):
                    n1, n2 = path.nodes[i-1], path.nodes[i]
                    if n1.type != "offcurve" and n2.type != "offcurve":
                        dx, dy = n2.x - n1.x, n2.y - n1.y
                        dist = math.sqrt(dx**2 + dy**2)
                        
                        p_n = path.nodes[i-2]
                        nx_n = path.nodes[(i+1) % node_count]
                        d_prev = math.sqrt((n1.x-p_n.x)**2 + (n1.y-p_n.y)**2)
                        d_next = math.sqrt((nx_n.x-n2.x)**2 + (nx_n.y-n2.y)**2)

                        is_terminal = dist < 150.0 and dist < d_prev and dist < d_next

                        if is_terminal and dist > 2.0:
                            angle = math.degrees(math.atan2(dy, dx)) % 360
                            alt_ang = (angle + 180) % 360
                            is_straight = abs(dx) < 0.2 or abs(dy) < 0.2
                            is_ok = any(abs(angle - r) < 2.0 or abs(angle - r) > 358.0 or abs(alt_ang - r) < 2.0 for r in refs)
                            
                            state = "Straight" if is_straight else ("✅ MATCH" if is_ok else "❌ MISMATCH")
                            coords_str = f"{int(n1.x)},{int(n1.y)} / {int(n2.x)},{int(n2.y)}"
                            
                            storage_key = f"terminalChecked_{curr_layer.associatedMasterId}_{coords_str}"
                            is_verified = curr_glyph.userData.get(storage_key, False)

                            self.results.append({"layer": curr_layer, "node1": n1, "node2": n2})
                            list_items.append({
                                "Verified": is_verified,
                                "Status": state, 
                                "Glyph Name": show_name, 
                                "Master": master_name,
                                "Angle": f"{angle:.1f}° ({alt_ang:.1f}°)", 
                                "Coordinates (P1 / P2)": coords_str,
                                "Length": f"{int(dist)}"
                            })
                            show_name = ""

            if len(list_items) > start_count:
                list_items.append({"Verified": False, "Status": "───", "Glyph Name": "───", "Master": "───", "Angle": "", "Coordinates (P1 / P2)": "", "Length": ""})
                self.results.append(None) 
        
        self.win.list.set(list_items)

    # Navigates to the selected terminal in the Edit View, highlights the nodes, and centers the view
    def focus(self, sender):
        selection = sender.getSelection()
        if not selection: return
        index = selection[0]
        
        if index >= len(self.results) or self.results[index] is None:
            return
            
        item = self.results[index]
        layer = item["layer"]
        n1 = item["node1"]
        n2 = item["node2"]
        
        # Switch tab and layer
        font = Glyphs.font
        if not font.currentTab:
            font.newTab([layer])
        else:
            font.currentTab.layers = [layer]
        
        # SELECTION (Highlight)
        # Clear existing selection at the glyph level for a clean state on all layers
        layer.parent.beginUndo() # Undo support in case of accidental changes
        
        # Clear all selections on the layer
        for path in layer.paths:
            path.selected = False
            for node in path.nodes:
                node.selected = False
        
        # Select only the two target nodes
        n1.selected = True
        n2.selected = True
        
        layer.parent.endUndo()
        
       # SCROLL TO VIEW (Auto-center)
        active_tab = font.currentTab
        view = active_tab.graphicView()
        if view:
            padding = 250
            mid_x = (n1.x + n2.x) / 2
            mid_y = (n1.y + n2.y) / 2
            
            rect_w = abs(n1.x - n2.x) + (padding * 2)
            rect_h = abs(n1.y - n2.y) + (padding * 2)
            rect = NSRect(NSPoint(mid_x - rect_w/2, mid_y - rect_h/2), (rect_w, rect_h))
            
            view.scrollRectToVisible_(rect)
        
        Glyphs.redraw()

TerminalAnalyzer()
