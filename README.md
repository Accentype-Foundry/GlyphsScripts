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
  1. Select one or more glyphs in the Font View.
  2. Run the script from the Scripts menu.
  3. In the popup window, you will see: 
     - The selected glyphs and their layer names.
     - The number of detected stems and their respective widths.


## Installation

1. 📂 **Open Scripts Folder:** In Glyphs, go to **`Scripts` → `Open Scripts Folder`** (Cmd+Opt+Shift+Y).
2. 📥 **Add Files:** Copy the **`.py`** files from this repository into that folder.
3. 🔄 **Reload:** Hold the **Option (Alt)** key and go to `Scripts` → `Reload Scripts`.


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

---

**MIT License** – Feel free to use and modify these scripts for your projects.


<sub>Created by **Miklós Ferencz [accentype.xyz](https://accentype.xyz)** </sub>
