# MenuTitle: 📐 TERMINAL ANALYZER
# -*- coding: utf-8 -*-

import vanilla
import math
from GlyphsApp import Glyphs

class TerminalAnalyzer(object):
    def __init__(self):
        self.results = []
        
        # The window
        self.win = vanilla.FloatingWindow((890, 520), "Terminal Analyzer")
        note_text = "⚠️ Run it on actual paths only! Won't work on components."
        self.win.note = vanilla.TextBox((20, 45, -20, 17), note_text, sizeStyle='small', alignment='center')

        # UI elements
        self.win.textRef = vanilla.TextBox((20, 12, 140, 17), "Reference Glyph:", sizeStyle='regular')
        self.win.refGlyphs = vanilla.EditText((140, 10, -100, 24), "C", sizeStyle='regular')
        self.win.scanButton = vanilla.Button((-90, 10, 80, 24), "Scan", callback=self.scan)
        
        self.win.list = vanilla.List(
            (0, 75, -0, -20), [], 
            columnDescriptions=[
                {"title": "Status", "width": 120},
                {"title": "Glyph Name", "width": 100},
                {"title": "Master", "width": 100},
                {"title": "Angle (±180°)", "width": 140, "key": "Angle"},
                {"title": "Coordinates (P1 / P2)", "width": 180},
                {"title": "Length", "width": 60}
            ], 
            selectionCallback=self.focus
        )
        
        self.win.open()

    def scan(self, sender):
        font = Glyphs.font
        if not font:
            return
        
        mid = font.selectedFontMaster.id
        master_name = font.selectedFontMaster.name
        self.results = []
        list_items = []

        # Collecting reference angles
        refs = []
        ref_input = self.win.refGlyphs.get()
        for name in ref_input.split(","):
            g = font.glyphs[name.strip()]
            if g:
                l = g.layers[mid]
                for p in l.paths:
                    for i in range(len(p.nodes)):
                        n1, n2 = p.nodes[i-1], p.nodes[i]
                        if n1.type != "offcurve" and n2.type != "offcurve":
                            dist = math.sqrt((n2.x-n1.x)**2 + (n2.y-n1.y)**2)
                            if 5.0 < dist < 200.0:
                                ang = math.degrees(math.atan2(n2.y-n1.y, n2.x-n1.x)) % 360
                                if 1.0 < (ang % 90) < 89.0:
                                    refs.append(ang)

        # Scanning
        for layer in list(font.selectedLayers):
            curr_glyph = layer.parent
            curr_layer = layer
            start_count = len(list_items)
            show_name = curr_glyph.name

            for p in curr_layer.paths:
                node_count = len(p.nodes)
                for i in range(node_count):
                    n1, n2 = p.nodes[i-1], p.nodes[i]
                    
                    if n1.type != "offcurve" and n2.type != "offcurve":
                        dx, dy = n2.x - n1.x, n2.y - n1.y
                        dist = math.sqrt(dx**2 + dy**2)

                        # 1. Get neighboring segments to see if this is a "cap"
                        prev_node = p.nodes[i-2]
                        next_node = p.nodes[(i+1) % node_count]
                        
                        dist_prev = math.sqrt((n1.x - prev_node.x)**2 + (n1.y - prev_node.y)**2)
                        dist_next = math.sqrt((next_node.x - n2.x)**2 + (next_node.y - n2.y)**2)

                        # 2. TERMINAL LOGIC: 
                        # It's a terminal if it's relatively short AND 
                        # the segments before and after it are longer (the stems).
                        is_terminal = dist < 150.0 and dist < dist_prev and dist < dist_next

                        if is_terminal and dist > 2.0:
                            ang = math.degrees(math.atan2(dy, dx)) % 360
                            alt_ang = (ang + 180) % 360
                            
                            # Check if it's Straight
                            is_straight = abs(dx) < 0.2 or abs(dy) < 0.2
                            
                            is_ok = False
                            for r in refs:
                                if abs(ang - r) < 2.0 or abs(ang - r) > 358.0 or abs(alt_ang - r) < 2.0:
                                    is_ok = True
                                    break
                            
                            state = "Straight" if is_straight else ("✅ MATCH" if is_ok else "❌ MISMATCH")
                            
                            self.results.append({"layer": curr_layer, "n1": n1, "n2": n2})
                            list_items.append({
                                "Status": state, 
                                "Glyph Name": show_name, 
                                "Master": master_name,
                                "Angle": f"{ang:.1f}° ({alt_ang:.1f}°)", 
                                "Coordinates (P1 / P2)": f"{int(n1.x)},{int(n1.y)} / {int(n2.x)},{int(n2.y)}",
                                "Length": f"{dist:.1f}"
                            })
                            show_name = ""

            # Separator only if findings were added for this glyph
            if len(list_items) > start_count:
                list_items.append({
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
        sel = sender.getSelection()
        if not sel:
            return
        
        index = sel[0]
        if index >= len(self.results):
            return
            
        item = self.results[index]
        if item is None:
            return
            
        font = Glyphs.font
        layer = item["layer"]
        n1, n2 = item["n1"], item["n2"]
        
        # Following the Glyphs API: tab = font.newTab([layer1, layer2])
        # We put our single layer into a list: [layer]
        if not font.currentTab:
            font.newTab([layer])
        else:
            # If a tab is already open, just switch the layer
            font.currentTab.layers = [layer]
        
        # Selecting nodes
        layer.selection = None
        n1.selected = True
        n2.selected = True
        
        Glyphs.redraw()

TerminalAnalyzer()