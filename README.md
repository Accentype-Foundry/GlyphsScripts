# Glyphs Scripts by Accentype   
---
A collection of Python productivity scripts for **Glyphs 3**. These tools focus on automating repetitive tasks, ensuring geometric precision, and streamlining both the design and production workflows.


## Included Scripts

### 1. Move My Anchor
Moves selected anchors to a specific Y-coordinate across all highlighted glyphs and layers.
* **Best for:** Standardizing accent placement or aligning anchors to custom metrics.
  
* **How to get it:** ***Clone the repository*** or **[**Download**](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/my-anchorposition.py)** the file.
 
* **Usage:** 
  * Select glyphs in Font View.
  * Run the script from the **Scripts** menu.
  * In the popup, enter the **Anchor Name** (e.g., `top`) and the **Target Y position** (e.g., `794`).
  * Click **Move Anchors**.


### 2. Pithagoras Stem Size
Displays the stem width(s) of the selected vertical glyph(s) in Glyphs.

>[!NOTE]
>This tool works only with straight vertical stems.
>It does not yet support rounded glyphs (like o, s) or diagonal stems (like x, z). Future updates may add these features.

> [!TIP]
> Why Pithagoras? The script is called Pithagoras-StemSize because it uses the Pythagorean theorem to measure stem widths.
> Distance between two nodes is calculated as: `distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)`    
> In simple words: the script treats each stem as the “hypotenuse” of a right triangle and calculates its horizontal width reliably.


* **Best for:** Ideal for spotting stem width inconsistencies within your glyphs
  
* **How to get it:** ***Clone the repository*** or **[**Download**](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/pithagoras-stime-size.py)** the file.
 
* **Usage:** 
  * Select one or more glyphs in the Font View.
  * Run the script from the Scripts menu.
  * In the popup window, you will see: 
     - The selected glyphs and their layer names.
     - The number of detected stems and their respective widths.

### 3. Font Coverage Auditor
This script audits a set of required glyphs for a project. It identifies which glyphs are present and which are missing.

For example, if you want to create a minimal alphabet, you can provide a list of required glyphs, and the script will show which ones you already have and which are missing.

* **Best for:** Quickly checking if your font includes all necessary glyphs for a project.
  
* **How to get it:** ***Clone the repository*** or **[**Download**](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/FontCoverageAuditor.py)** the file.

* **Usage:** 
  * Select glyphs in Font View.
  * Run the script from the **Scripts** menu.
  * In the popup, enter or paste all the glyph names you need.     
    *(e.g., Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis ...)*
  * Click the play button ▶️. The script will display the total number of glyphs, which ones are missing, and which ones you already have.

### 4. Alternate Glyphs Creator   
Create or rename multiple alternate glyphs at once.

* **Best for:** Designers who work with a large number of alternate glyphs and need to rename them quickly and reliably. It’s also ideal if you want to generate multiple alternates for each glyph while keeping naming consistent.

* **How to get it:** ***Clone the repository*** or **[**Download**](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/AlternateGlyphsCreator.py)** the file.
  
* **Usage:** 
  * Run the script from the **Scripts** menu.
  * To create alternates:
      * In the popup window, enter the Base Glyph Name (the glyph you want to create alternates for).
      * Enter the Alternate Suffix (e.g. ss → will generate ss01, ss02, etc.).
      * Click Create Alternates.
  * To rename existing alternates:
      * Select the alternate glyphs in Font View.
      * In the popup window, enter the new suffix at the bottom.
      * Click Rename Suffixes.

 ### 5. Terminal Analyzer   
 The script compares the angles of glyph terminals.

* **Best for:** Comparing terminals of the selected glyph(s) based on a given reference glyph. The goal is to help keep terminal angles consistent across the typeface. It is especially useful when terminals have a cut angle and the shapes are not built with components, which can lead to small angle variations. The tool displays the current terminal angles for the selected glyph(s) in a table view.

* **How to get it:** ***Clone the repository*** or **[**Download**](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/Terminal_Analyzer.py)** the file.

* **Usage:**
  * Run the script from the **Scripts** menu.
  * Enter the reference glyph in the popup window (the reference glyph is used to compare the terminal angles of the other glyphs).
  * In Font View, select the glyphs you want to analyze. In Edit View, the script will analyze the currently open glyph.
  * Click Scan.
  * If the script shows a mismatch, you can double-click it. This will jump to the problematic glyph and highlight where the mismatch occurs, so you can check it.
  *  *Note: sometimes you may see a 0–01° difference, because the tolerance is set low to give accurate results.*


### 6. All Masters in Text Mode   
Displays all masters of the current text on separate lines.

* **Best for:** Reviewing and adjusting kerning across all masters simultaneously in **Text Mode**, without the need to switch active masters manually.

* **How to get it:** Clone the repository or **[Download](https://github.com/Accentype-Foundry/GlyphsScripts/blob/main/all_masters_in_text_m.py)** the file.

* **Usage:**
  1. Switch to **[Text Mode](https://handbook.glyphsapp.com/edit-view/#:~:text=Use%20text%20mode%20to%20insert,by%20double%2Dclicking%20a%20glyph.).**
  2. Type your test words or glyphs.
  3. Run the script from the **Script** menu.
  4. The script will instantly display the text across all available masters, each on its own line.
* **Tip:** For a faster workflow, you can assign a custom keyboard shortcut to this script via **Glyphs > Settings > Shortcuts** (search for "All Masters in Text Mode" in the Scripts section). See the **[Glyphs Handbook](https://handbook.glyphsapp.com/settings/shortcuts/)** for more details on managing shortcuts.




## Installation

1. 📂 **Open Scripts Folder:** In Glyphs, go to **`Scripts` → `Open Scripts Folder`**.     
    (**Shift** + **Command** + **Y**)
3. 📥 **Add Files:** Copy the **`.py`** files from this repository into that folder.
4. 🔄 **Reload Scripts:** Press **Cmd** + **Opt** + **Shift** + **Y**
 

## Requirements

* **Glyphs 3.2** or later.
* **Python** must be installed and active in Glyphs Preferences.
* **Vanilla Module:** Required for scripts with a user interface.
  * Install via: **`Window` → `Plugin Manager` → `Modules` → `vanilla`**


## General Usage for Scripts

1. Select the glyphs you want to process in the **Font View**.
2. Go to the **Scripts menu** at the top of your screen.
3. Choose the desired script from the list.
4. (Optional) Check **Window → Macro Panel** if you want to see the process logs or errors.


## Contributing & Support

Suggestions and bug reports are welcome! If a script crashes:
1. Open **Window → Macro Panel**.
2. Copy the error log.
3. [Open an issue](https://github.com/YOUR_USERNAME/Scripts-for-Glyphs/issues) and paste the log.
   
Don’t hesitate to contribute if you’ve made improvements or fixes. Your input is greatly appreciated!

---

**MIT License** – Feel free to use and modify these scripts for your projects.


<sub>Created by **Miklós Ferencz [accentype.xyz](https://accentype.xyz)** </sub>
