# MenuTitle: 📐 TERMINAL ANALYZER
# -*- coding: utf-8 -*-

import vanilla
import math
from GlyphsApp import Glyphs

class TerminalAnalyzer(object):
    def __init__(self):
        self.results = []
        
        # The window
        self.win = vanilla.FloatingWindow((940, 520), "Terminal Analyzer")
        note_text = "⚠️ Run it on actual paths only! Won't work on components."
        self.win.note = vanilla.TextBox((20, 45, -20, 17), note_text, sizeStyle='small', alignment='center')

        # UI elements
        self.win.textRef = vanilla.TextBox((20, 12, 140, 17), "Reference Glyph:", sizeStyle='regular')
        self.win.refGlyphs = vanilla.EditText((140, 10, -100, 24), "C", sizeStyle='regular')
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
            editCallback=self.save_verification # Save when checkbox is toggled
        )
        
        self.win.open()

    def save_verification(self, sender):
        # Save the checkbox state into glyph's userData
        list_items = sender.get()
        for i, item in enumerate(list_items):
            if i < len(self.results):
                res_item = self.results[i]
                if res_item and "layer" in res_item:
                    glyph = res_item["layer"].parent
                    # Key based on Master and Coordinates to be specific
                    storage_key = f"terminalChecked_{res_item['layer'].associatedMasterId}_{item['Coordinates (P1 / P2)']}"
                    glyph.userData[storage_key] = item["Verified"]

    def scan(self, sender):
        font = Glyphs.font
        if not font:
            return
        
        masterID = font.selectedFontMaster.id
        master_name = font.selectedFontMaster.name
        
        # Deselect any item to prevent selectionCallback (focus) from firing during scan
        self.win.list.setSelection([])
        self.results = []
        list_items = []

        # Collecting reference angles
        refs = []
        ref_input = self.win.refGlyphs.get()
        for name in ref_input.split(","):
            glyph = font.glyphs[name.strip()]
            if glyph:
                layer = glyph.layers[masterID]
                for path in layer.paths:
                    for i in range(len(path.nodes)):
                        node1, node2 = path.nodes[i-1], path.nodes[i]
                        if node1.type != "offcurve" and node2.type != "offcurve":
                            dist = math.sqrt((node2.x-node1.x)**2 + (node2.y-node1.y)**2)
                            if 5.0 < dist < 200.0:
                                angle = math.degrees(math.atan2(node2.y-node1.y, node2.x-node1.x)) % 360
                                if 1.0 < (angle % 90) < 89.0:
                                    refs.append(angle)

        # Scanning
        for layer_obj in list(font.selectedLayers):
            curr_glyph = layer_obj.parent
            curr_layer = layer_obj
            
            # Clear any previous selection to avoid ghost highlights from previous scans
            curr_layer.selection = None
            
            start_count = len(list_items)
            show_name = curr_glyph.name

            for path in curr_layer.paths:
                node_count = len(path.nodes)
                for i in range(node_count):
                    # Define the segment by current and previous node
                    node1, node2 = path.nodes[i-1], path.nodes[i]
                    
                    # Check only straight line segments (ignore curves/off-curves)
                    if node1.type != "offcurve" and node2.type != "offcurve":
                        # Calculate vector components and segment length
                        deltaX, deltaY = node2.x - node1.x, node2.y - node1.y
                        dist = math.sqrt(deltaX**2 + deltaY**2)

                        # Get neighboring segments to see if this is a "cap"
                        prev_node = path.nodes[i-2]
                        next_node = path.nodes[(i+1) % node_count]
                        
                        dist_prev = math.sqrt((node1.x - prev_node.x)**2 + (node1.y - prev_node.y)**2)
                        dist_next = math.sqrt((next_node.x - node2.x)**2 + (next_node.y - node2.y)**2)

                        # TERMINAL LOGIC: 
                        # It's a terminal if it's relatively short AND 
                        # the segments before and after it are longer (the stems).
                        is_terminal = dist < 150.0 and dist < dist_prev and dist < dist_next

                        if is_terminal and dist > 2.0:
                            angle = math.degrees(math.atan2(deltaY, deltaX)) % 360
                            alt_ang = (angle + 180) % 360
                            
                            # Check if it's Straight
                            is_straight = abs(deltaX) < 0.2 or abs(deltaY) < 0.2
                            
                            is_ok = False
                            for r in refs:
                                if abs(angle - r) < 2.0 or abs(angle - r) > 358.0 or abs(alt_ang - r) < 2.0:
                                    is_ok = True
                                    break
                            
                            state = "Straight" if is_straight else ("✅ MATCH" if is_ok else "❌ MISMATCH")
                            
                            coords_str = f"{int(node1.x)},{int(node1.y)} / {int(node2.x)},{int(node2.y)}"
                            
                            # Load verified state from userData
                            storage_key = f"terminalChecked_{curr_layer.associatedMasterId}_{coords_str}"
                            is_verified = False
                            if curr_glyph.userData[storage_key]:
                                is_verified = curr_glyph.userData[storage_key]

                            self.results.append({"layer": curr_layer, "node1": node1, "node2": node2})
                            list_items.append({
                                "Verified": is_verified,
                                "Status": state, 
                                "Glyph Name": show_name, 
                                "Master": master_name,
                                "Angle": f"{angle:.1f}° ({alt_ang:.1f}°)", 
                                "Coordinates (P1 / P2)": coords_str,
                                "Length": f"{int(dist)}" # Rounded for cleaner look
                            })
                            show_name = ""

            # Separator only if findings were added for this glyph
            if len(list_items) > start_count:
                list_items.append({
                    "Verified": False,
                    "Status": "───", 
                    "Glyph Name": "───", 
                    "Master": "───", 
                    "Angle": "", 
                    "Coordinates (P1 / P2)": "", 
                    "Length": ""
                })
                self.results.append(None) 
        
        self.win.list.set(list_items)

    def focus(self, sender):
        # Syncs the UI selection with the Edit View and highlights the nodes
        selection = sender.getSelection()
        if not selection:
            return
        
        index = selection[0]
        # If the index is out of bounds or you clicked a separator (None), stop here
        if index >= len(self.results) or self.results[index] is None:
            return
            
        item = self.results[index]
        font = Glyphs.font
        layer = item["layer"]
        node1, node2 = item["node1"], item["node2"]
        
        # Tab handling
        if not font.currentTab:
            font.newTab([layer])
        else:
            font.currentTab.layers = [layer]
        
        # Selection: only if all objects are available
        if layer and node1 and node2:
            # Clear previous selection within the glyph
            layer.selection = None
            node1.selected = True
            node2.selected = True
            Glyphs.redraw()

TerminalAnalyzer()
