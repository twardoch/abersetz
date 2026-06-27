# FontLab 7: Full 20-Chapter Overview

This document contains the merged 20-chapter detailed overview of FontLab 7 capabilities, tools, and workflows.

---

# Chapter 1: Welcome to FontLab 7

## Introduction and System Requirements

FontLab 7 is a comprehensive, professional-grade desktop font editor designed to satisfy the rigorous demands of type designers, typographers, and font engineers. Built on a completely rewritten engine compared to legacy platforms like FontLab Studio 5, FontLab 7 offers a modern, non-destructive editing workflow. It operates natively on macOS 10.10 (Yosemite) and higher, as well as Windows 7 and newer. The application supports high-DPI displays and integrates seamlessly into production pipelines. Unlike its predecessor, which relied on separate files for different formats, FontLab 7 introduces a unified `.vfc` (FontLab Document) working format, which stores all glyph layers, references, and variable axes in a single database file.

> [!NOTE] For new users evaluating the software, FontLab 7 offers a fully functional 30-day trial. During the trial period, all professional tools—including font generation, OpenType feature compiling, and Python scripting—remain fully active without watermarks or design limitations.

## Industry Position and Capabilities

As a standard in the digital type industry, FontLab 7 is used by major type foundries and independent designers to develop everything from single-weight display faces to massive, multi-axis variable font families. The editor provides unparalleled drawing tools optimized for precision vector design. Designers can manipulate Bézier curves with advanced control over node continuity (including G2 curvature matching), slide points along contours without altering curve geometry, and balance handles to ensure optimal outline quality. The drawing environment supports both PostScript (cubic Bézier) and TrueType (quadratic Bézier) curves, allowing developers to convert between curve types losslessly.

FontLab 7 features native, multi-script support. It contains comprehensive tools for design systems spanning Latin, Cyrillic, Greek, Arabic, Hebrew, Indic, and Chinese, Japanese, and Korean (CJK) character sets. Beyond traditional formats, FontLab 7 is a leader in modern font technologies, offering robust capabilities for:

- **Variable Fonts (OpenType Font Variations):** Direct editing of design space axes, masters, and interpolation compatibility, featuring visual indicators for matching contours.
- **Color Fonts:** Support for OpenType-SVG, COLR/CPAL, and CBDT/CBLC bitmap formats.
- **Smart Interpolation:** Precision management of master designs, metrics, and kerning classes across multi-dimensional spaces.

## Metrics and Design Mechanics

Designing high-quality typefaces requires careful attention to spacing. FontLab 7 handles sidebearings, advance widths, and kerning with advanced mathematical precision. Users can link metrics dynamically using formulas, ensuring that changes to a glyph's contour immediately update its spacing relationships. The integrated Metrics and Kerning tools operate in a text-editor environment, facilitating real-time proofing of complex script combinations. This allows type designers to adjust sidebearings and kerning pairs directly in context, using class-based kerning to manage thousands of pairs efficiently.

## Evolution and Continuous Updates

In contrast to the static development cycles of legacy tools, FontLab 7 is a continuously evolving tool. Significant enhancements, new commands, performance optimizations, and workflow refinements are introduced in minor version releases (e.g., 7.1, 7.2, and subsequent dot-releases).

> [!IMPORTANT] To maintain compatibility with evolving operating systems and font specifications, users must regularly consult the minor version release notes. These notes serve as the primary documentation for new features and changed keyboard shortcuts.

---

# Chapter 2: The UI Design and Customization

## Workspace Layout Paradigms

FontLab 7 features a highly adaptable user interface designed to accommodate various design styles and multi-monitor setups. Under **Preferences > General**, you can configure the interface to run in one of three window modes:

- **Single Window / Tabs Mode:** Documents, Font windows, and Glyph windows are organized as tabs within a single master application frame. This keeps the workspace clean and prevents windows from overlapping.
- **Floating Windows Mode:** Every opened font and glyph workspace exists in an independent, floating window. This is ideal for multi-monitor setups, allowing you to drag drawings, metrics editors, and preview windows across screens.
- **Windows and Window Tabs:** A hybrid approach allowing windows to be docked together or float. To dock a floating window, use **Window > Docking > Window is Dockable**, or merge them using commands like **Merge All Windows** or **Merge To Font Windows**.

## Panel Docking and Grouping

Panels in FontLab 7 are context-rich and can float freely or dock to the edges of the screen, the application window, or other panels. To dock a panel, drag its title bar toward the edge of another panel or window. A pale blue line indicates a valid docking zone, and the panel becomes semi-transparent during dragging. To create a tabbed panel group, drag a panel directly over another panel. The receiving panel is highlighted in blue; dropping the panel combines them, displaying their titles at the bottom of the group.

> [!NOTE] When a panel is floating, a square toggle in the top-right corner defines its docking behavior:
>
> - **󰀞 (Plus):** Can dock at screen edges or between panels, and can be grouped, but cannot dock inside a window.
> - **󰀟 (Inverted L):** Default behavior. The panel can dock to any window or panel border, screen edges, or group with others.
> - **󰀝 (Empty):** The panel is locked to a floating state and cannot dock or group.

## The Context-Sensitive Property Bar

The Property Bar sits at the top of Font and Glyph windows, providing instant access to settings.

- **Font Window (Static):** The property bar remains constant. It contains toggles for the Sidebar (`◧`), Table (`▦`), and List (`◨`), along with cell caption options, prospective filters (Encoding, Category, Script), sorting selectors, flag/mark highlights, and the Search box.
- **Glyph Window (Dynamic):** The middle section of the bar adapts to the active tool (such as Contour, Zoom, Guides, Metrics, or Kerning) or the current selection. The left and right sections remain static, showing toggles for the Content Sidebar, Spacing Controls, Kerning, Mark Attachment, active layer/master selectors, and search/flag utilities.

## Discovering Features: Quick Help and Workspaces

FontLab 7 includes a built-in **Quick Help** system. Hovering over any UI control and holding `++F1++` (or `++Fn+F1++`) displays a compact explanation balloon. Tapping `++F1++` toggles this mode on permanently. For in-depth context, `++Shift+F1++` opens the dedicated **Help Panel**.

To optimize your environment, configure your layout and choose **Window > Workspaces > Save Workspace**. You can save custom configurations for specific workflows:

- **Drawing Workspace:** Prioritizes the Canvas, Layers, and Element panels.
- **Metrics Workspace:** Emphasizes Spacing controls and the Preview panel.
- **Feature Coding Workspace:** Focuses on the Features and Lookups panels.

> [!TIP] Restore these workspaces via **Window > Workspaces** or use keyboard shortcuts `++Opt+Cmd+1++` through `++Opt+Cmd+6++` (macOS) to switch layouts instantly.

---

# Chapter 3: Font Files and Formats

## Native Working Formats

FontLab 7 utilizes two native file formats for development: **VFC (FontLab Compact)** and **VFJ (FontLab JSON)**. These formats function as your master production documents (analogous to a PSD file in Adobe Photoshop), preserving all proprietary design elements—including glyph notes, pins, element references, smart corners, and workspace arrangements—that compiled formats discard.

- **VFC (.vfc):** A proprietary, cross-platform binary format optimized for maximum speed, fast reading, and compact disk storage. It is the recommended format for daily design work.
- **VFJ (.vfj):** A text-based representation of the native format using JSON structures. While larger than VFC files, VFJs are human-readable, making them excellent for script-based analysis, automated workflows, and version control.

> [!TIP] Under `Preferences > Save Fonts`, disable the **Session** checkbox when saving VFJ files. This strips transient last-modification timestamps from the file, resulting in clean diffs when tracking source files using git or other version control systems. Turn on **Prettify VFJ** to output formatted indentation for human readability.

## Opening, Saving, and Exporting

FontLab differentiates between the working environment and final delivery.

- **Opening:** Use `File > Open Font(s)...` to load files. Opening non-native files (like compiled OTF/TTF files) triggers an internal conversion process. You can configure conversion preferences under `Preferences > Open Fonts` to control how CID mappings, contour rounding, alignment zones, and OpenType Layout features are handled.
- **Saving:** Commands such as `File > Save Font` (`Cmd+S`) write exclusively to VFC or VFJ formats, preserving edit history and workspace setups.
- **Exporting:** To output usable fonts, use `File > Export Font(s)...`. This compiles the source into distribution-ready formats, converting specialized constructs (like Smart Corners) into standardized Bezier curves.

## Backups and Autosave Configurations

To prevent data loss, FontLab 7 offers robust multi-level backup and autosave mechanisms configured via `Preferences > Save Fonts`.

When saving over an existing file, you can choose how the application handles the previous version:

1. **Overwrite:** Replaces the existing file directly.
2. **Move to Trash:** Sends the older version to the system trash.
3. **Rename:** Appends a timestamp (date and time) to the previous file.

Turning on **Save backup files to subfolder** automatically stores renamed backups in a `.backup` directory adjacent to the master file. Additionally, enabling **Autosave** keeps a background replica of your active workspace. In the event of a crash, FontLab prompts you to restore these autosaved projects upon restarting; they are safely discarded after a clean, manual save and exit.

## Interoperability and Distribution Formats

FontLab 7 provides high-fidelity interoperability across the font industry:

- **Desktop Formats:** Exports standard **OTF** (PostScript/CFF) and **TTF** (TrueType) formats.
- **Web Fonts:** Exports **WOFF** and **WOFF2**, with WOFF2 utilizing Google's Brotli compression to achieve file size reductions of over 30%.
- **Source Interchange:** Seamlessly exchanges files with other editors via XML-based **UFO** (Unified Font Object) or the native **.glyphs** format (supporting Glyphs 2 and 3 pipelines).
- **Color OpenType:** Supports all major color formats, including **OpenType SVG** (vector/bitmap gradients), Microsoft's **COLR** (layered vector colors), and Apple's **sbix** or Google's **CBDT** (bitmap-based color fonts).

---

# Chapter 4: The Font Window Dashboard

The Font Window is the central command center for managing, organizing, and auditing your font files. When you create a new font or open an existing file, FontLab displays your glyphs in a structured cell grid interface, presenting a comprehensive overview of the design space.

## The Cell Grid Interface

The primary area of the Font Window consists of a glyph chart where each cell represents a single glyph. Existing glyphs show their respective outlines on a white background, while empty glyph slots are shown with a grey background containing a light grey placeholder template. These templates serve as visual guides for the expected character but do not contain actual outline data.

To adapt the grid to different design workflows, you can customize cell dimensions in the Footer using the cell width buttons—ranging from narrow to extra wide (16:9 ratio), which is ideal for ligatures and calligraphic scripts. Additionally, the Column (Cols) menu provides preset cell sizes (8, 16, 24, 32, or 64 columns per row) or a "Flex" mode for freeform resizing via zoom keyboard shortcuts (`Cmd+=` and `Cmd+-`).

> [!TIP] The List Sidebar (◨) provides a spreadsheet-like alternative to the grid, displaying customizable columns for sidebearings (LSB/RSB), advance width, and other cell metadata. Double-clicking any value in List view allows for immediate inline editing.

## Navigation, Metadata, and Flagging

Navigating the Font Window grid is intuitive: click to select a glyph, drag to select contiguous ranges, or hold `Cmd` (macOS) / `Ctrl` (Windows) to select non-adjacent cells. One cell remains active as the "current" glyph, highlighted in dark blue. Double-clicking opens the glyph in the Glyph Window for drawing.

Each cell displays crucial metadata in its caption, which can show the glyph name, Unicode codepoint, glyph index, or other encoding data. If the glyph name does not match its assigned Unicode codepoint, FontLab displays a yellow indicator as a warning.

To manage complex projects, you can assign color flags (previously called "Marks") via the Property bar, context menu, or Sidebar. These flags color-code the cell background or caption. In the Sidebar's Flag section, you can see all unique color flags grouped by their numerical hue value, alongside the count of glyphs assigned to each flag.

> [!NOTE] Pressing the Space key on any glyph cell opens a temporary glyph info pop-up showing detailed metrics, Unicode properties, and tags.

## Filtering and Searching the Grid

FontLab offers robust filtering methods using the Property bar and Sidebar to isolate specific glyph sets:

- **Encodings**: Filter by standard and custom encoding files (`.enc`), displaying slots in the encoding order.
- **Unicode Blocks**: Filter by standard Unicode blocks (Ranges) to systematically add characters.
- **Categories**: Filter by typographic groups like uppercase (`_uc_`), lowercase (`_lc_`), punctuation, or figures (`_fig_`).
- **Codepages**: Filter by target platforms or legacy encodings (e.g., Win-1252, MacOS Roman).
- **Index**: Sort and filter glyphs by their Glyph Index (GID) values. When active, manual sorting is disabled.

The quick search bar in the upper-right corner acts as an ad-hoc filter. You can search by glyph name, Unicode character name, range, or script. It supports multi-substring queries (e.g., typing `la ca` finds "Latin Capital", and `cu sy` finds "Currency Symbols"). You can save search results as filters by dragging them to the Sidebar Bookmarks or clicking the `+` button in the Search History section.

---

# Chapter 5: Navigating the Glyph Window

The Glyph Window (GW) is the primary workspace in FontLab 7 where you draw, edit, space, kern, and hint individual glyphs or multi-glyph strings. Double-clicking any glyph cell in the Font Window opens the Glyph Window, placing the selected glyph at the center of the editing canvas.

## The Editing Canvas and View Control

The editing canvas displays glyph shapes along with metrics, guidelines, and outline structures. Managing your view is essential for detailed vector design:

- **Zooming:** Use `Cmd + Plus` and `Cmd + Minus` (macOS) or `Ctrl + Plus` and `Ctrl + Minus` (Windows) to zoom in and out. Press `Cmd+1` to view at 100% scale, `Cmd+2` to zoom to the selection, and `Cmd+0` to fit the active glyph or text string to the window. You can also hold `Cmd+Space` and drag to zoom dynamically.
- **Preferences:** In _Preferences > Glyph Window_, you can customize the default zoom factor, zoom step size, scrolling speed, and whether zooming centers on the mouse pointer.

## Rulers, Guides, and Coordinates

To maintain typographic consistency, the Glyph Window provides precise visual aids and ruler metrics:

- **Rulers:** Toggle rulers using `Cmd+R` (`View > Rulers`). They show the coordinates of the canvas relative to the baseline, x-height, and sidebearings (defining the left sidebearing and advance width boundary).
- **Guides:** Drag from the horizontal or vertical rulers to create guidelines. Local guidelines belong to the active glyph, while global guidelines apply across the entire font. Double-click a guideline to edit its name, precise position, color, or mathematical expressions in the Guideline properties.
- **Coordinates:** FontLab 7 supports both integer coordinate rounding and fractional (double-precision floating-point) coordinates. Choose fractional coordinates to maintain Bezier curve smoothness and G2 node continuity across master variations, and round them using `Contour > Round Coordinates` for final font exports.

## Control Bars and the Property Bar

The interface around the canvas adapts to your workflow:

- **Property Bar:** Positioned at the top of the window, it displays context-sensitive controls for the active tool (e.g., node coordinates, handle angles, or alignment options).
- **Content Sidebar:** Houses the master list, active text layers, and quick access to metrics editing.

## Scope of Editing: Exclusive vs. Shared Control

By default, editing operations are exclusive to the active element on the current master layer. To edit other areas simultaneously, you can adjust the scope of editing:

- **Edit Across Elements:** When enabled (`Edit > Edit Across Elements`), you can select and edit nodes belonging to different vector elements in the same glyph.
- **Edit Across Glyphs:** Toggle this (`Alt+Cmd+E`) to edit contours of any glyph visible in the text string, not just the active one.
- **Edit Across Layers:** When active, changes can be applied across multiple master layers or the Mask layer concurrently.

> [!TIP] Use `Shift+Alt+Space` to toggle _Details Across Glyphs_. When off, non-active glyphs render as clean, filled silhouettes, hiding distracting node structures.

## Text Mode

Switch to the Text tool (`T`) to enter Text Mode. This transforms the drawing canvas into an interactive text editor:

- **Direct Input:** Type Unicode characters directly onto the canvas to view how they space and kern.
- **Glyphtext Notation:** Enter glyphs by name using the `/name` syntax (e.g., `/A/B/C/d.sc`) or hex codepoints (`\u0041`).
- **Exit:** Press `Esc` to return to your previous drawing or editing tool.

---

# Chapter 6: Basic Vector Drawing Tools

FontLab 7 provides a powerful set of vector drawing tools designed specifically for type design and font engineering. Drawing glyph outlines requires precise control over Bézier curves, node continuity, and shape geometry. This chapter covers the primary tools for creating and editing outlines: the Pencil, Pen, and Rapid tools, along with geometric primitives and node insertion techniques.

## The Pencil Tool (N)

The **Pencil** tool is optimized for freehand sketching and rapid prototyping. It allows designers to draw paths naturally without manually placing individual Bézier control points. FontLab automatically converts the freehand stroke into smooth Bézier curves and straight line segments.

- **Freehand Drawing:** Drag to sketch curves. Hold `Alt` to draw straight lines, or `Alt+Shift` to constrain the path horizontally or vertically.
- **Closing Paths:** Bring the cursor back to the start node; a blue circle indicates that releasing the mouse will close the contour.
- **Editing Existing Contours:** With _Pen and pencil tools can continue on a contour_ enabled in Preferences, drawing over an existing contour from node to node will seamlessly replace or extend that section.

> [!TIP] Use the Pencil tool with a drawing tablet to quickly trace imported background scans or analog sketches before refining nodes manually.

## The Pen Tool (P)

The traditional Bézier **Pen** tool offers absolute manual control over node placement and vector handle direction, which is critical for achieving clean outlines and perfect node continuity (such as G1 and G2 smoothness).

- **Creating Nodes:** Click to place a corner node. Click and drag to create a smooth node with symmetrical Bézier control points.
- **Adjusting Handles:** Hold `Alt` while dragging to break the handle alignment, creating a corner point with asymmetric handles. Hold `Shift` to constrain handle angles to 45-degree increments.
- **Closing and Ending:** Click the start node to close the loop, or press `Esc` to leave the contour open.

## The Rapid Tool (5)

The **Rapid** tool is an intelligent click-by-click drawing tool that automatically determines node placement and handles based on where you click. It draws quadratic Bézier curves with a special interface that automatically converts to cubic Bézier curves when switching tools.

- **Node Placement:** Click to add a straight node; double-click (or `Ctrl+Click`) to place a smooth node. `Cmd+Alt+Click` places a tangent node.
- **Tension Control:** Curved segments are created using the default tension defined in Font Info. Higher tension values produce super-elliptical curves.
- **Interactive Adjustments:** Drag any node or control point during drawing to modify the path immediately. Double-click any node to toggle between smooth and corner connection types.

> [!IMPORTANT] Enabling _Rapid tool remembers last state_ in Preferences allows you to continually place nodes of the same type without double-clicking for each curve.

## Primitive Shapes (I and O)

For geometric glyph construction, FontLab includes the **Rectangle** (`I`) and **Ellipse** (`O`) tools.

- **Drawing Gestures:** Drag to define the shape boundaries. Hold `Shift` to constrain to a square or circle, and hold `Alt` to draw from the center.
- **Numeric Input:** Click once on the canvas to open the Add Rectangle or Add Oval dialog box and enter precise dimensions.
- **Geometric vs. Curved:** In the property bar, toggle between traditional geometric ellipses or curved ellipses that honor the font's Tension parameter.

## Inserting Nodes on Paths

Adding nodes to existing paths is crucial for path refinement and adding detail:

- **With Pen/Rapid Tools:** Hover over an active segment and click to insert a corner node (or double-click with the Rapid tool for a smooth node).
- **With Contour Tool (`A`):** Double-click any segment to insert a new node without modifying the existing curve geometry.

---

# Chapter 7: Advanced Point & Node Editing

## Node Types: Corner vs. Smooth

In FontLab 7, contours are defined by Bézier curves and two primary node types that determine how path segments connect.

- **Corner Nodes**: Indicated by red, square symbols, corner (or sharp) nodes create an abrupt angle between any two segments (straight or curved).
- **Smooth Nodes**: Indicated by green, round symbols, smooth nodes ensure tangent continuity. Between two curves, they are _curve nodes_, aligning handles collinearly. Between a curve and a straight line, they are _tangent nodes_, forcing the handle to align with the straight segment.

Double-clicking a node toggles it between corner and smooth.

> [!NOTE] There is no smooth node type for connecting two straight segments. If they are collinear, the node should be deleted to form a single segment.

## Smart Nodes: Servant and Genius

Smart nodes are special properties assigned to nodes to automate curve drawing and tracking.

### Servant Nodes

A servant node has its X, Y, or both coordinates linked to neighboring non-servant nodes. When you move a neighboring node, the servant node’s position is interpolated, and its handles scale proportionally. This is ideal for maintaining proportion in rounded shapes. To assign this, right-click a node and choose **X-Servant** or **Y-Servant** from the context menu.

### Genius Nodes

Genius nodes always maintain G2 curvature continuity (ultra-smoothness). Unlike G1 continuity, which only aligns handles collinearly, G2 continuity matches the rate of curvature change on both sides of the node. When you adjust the handles of a Genius node, FontLab automatically shifts the node's position along the path to maintain this perfect G2 curve.

> [!TIP] Use **View > Show > Curvature** to inspect G2 continuity. Curvature combs will match in height on both sides of a Genius node.

## Path Direction and Fills

Every contour has a designated **Start Point** (the first node) and a path direction, which can be clockwise or counter-clockwise.

- **Start Point**: Indicated by a gray direction arrow when **View > Show > Contour Direction** is enabled.
- **Winding Rules**: PostScript (Type 1) contours require counter-clockwise paths to be filled (black) and clockwise paths to be unfilled (knockouts/holes). TrueType outlines use the opposite rule.

While FontLab 7 automatically corrects path directions and resolves overlaps during export, you can manually reverse contour directions or change the start point by right-clicking a node and choosing **Make Start Point**.

## Selection Mechanics

Precise node editing is essential because shifting outlines directly alters the glyph's advance width and sidebearings. This requires understanding how FontLab differentiates between nodes and handles during selection.

- **Individual Selection**: Click a node or handle directly. Shift-click to add or remove points from the selection.
- **Marquee Selection**: Drag a rectangle over the canvas. Its behavior is governed by `Preferences > Editing > Marquee selection ignores handles when selecting nodes`. If enabled, dragging over both nodes and handles selects only the nodes. If the marquee encloses only handles, they are selected.
- **Lasso Selection**: Hold **Alt** while dragging to draw a freeform lasso, selecting all enclosed nodes and handles.

> [!IMPORTANT] When `Marquee selection ignores handles` is active, using **Shift-marquee** to deselect will still always deselect all captured items, whether they are nodes or handles.

---

# Chapter 8: Segment Manipulation and Tunni Lines

Modifying outlines in FontLab 7 requires understanding path geometry, node continuity, and handle behaviors. Vector paths consist of nodes and Bezier curves. Adjusting handle lengths and angles determines curve tension and curvature, affecting the smoothness of transitions between segments.

## Symmetrical Editing with Tunni Lines

When editing curves defined by two control handles, maintaining balanced tension is challenging. FontLab 7 solves this with **Tunni lines**—imaginary blue dotted lines linking matching Bezier handles of a curve segment. They allow adjusting tension and proportion of handles simultaneously.

To toggle Tunni lines, tap `L` or choose **View > Tunni Lines**. Hovering between handles displays the Tunni line and its central control point (a large blue dot).

- **Symmetrical Editing:** Drag the Tunni line or hold `Shift` and drag the control point to move both handles in sync.
- **Asymmetrical Editing:** Drag the control point without `Shift` to adjust only one handle.
- **Keyboard Adjustments:** Select a Tunni line and press `Alt` with arrows:
  - `Alt + Left/Right` shifts the Tunni point parallel, lengthening one handle while shortening the other.
  - `Alt + Up/Down` moves it orthogonally, increasing or decreasing curve tension.
- **Batch Editing:** **Contour > Edit Tunni Lines** (`Cmd + Alt + L`) activates Tunni lines for selected segments; press `Esc` to deactivate.

> [!NOTE] Adjusting tension with Tunni lines helps preserve G2 curvature continuity, essential for smooth curve transitions.

## Node and Segment Deletion Models

FontLab 7 offers two distinct models for deleting nodes and segments: curve preservation and path avulsion.

- **Curve-Preserving Deletion (Backspace):** Removes the selected node or handle while keeping the contour closed. FontLab recalculates remaining handles to approximate the original path shape.
- **Path Avulsion (Delete):** Deletes the node and breaks the contour, leaving open endpoints.
- **Segment Deletion:** Pressing `Backspace` removes a segment and its nodes but keeps the contour closed. Pressing `Delete` deletes only the segment, leaving end nodes intact but breaking the contour.

## The Scissors Tool and Looped Corners

The **Scissors tool** (`Q`) unlinks nodes, splits paths, and manages overlaps.

- **Unlinking:** Clicking a node cuts the contour and elongates adjacent segments.
- **Ink Traps:** Shift-clicking a node duplicates and separates them by the distance in **Font Info > Font Dimensions > Ink trap width**.
- **Looped Corners:** Alt-clicking a sharp node creates a closed, self-intersecting "looped corner." Loops extending into filled areas are _inner looped corners_; those extending into blank areas are _outer looped corners_. These loops maintain matching node counts for variable fonts.

## Contour Simplification Filters

For automated optimization, FontLab provides two filters:

- **Simplify** (`Alt + Cmd + B`): Streamlines outlines, removes redundant nodes, and adds extremum nodes. It converts TrueType curves to PostScript and may alter the shape.
- **Clean Up:** Removes unnecessary nodes without adding new ones, keeping the contour shape closer to the original.

> [!TIP] Use the **Eraser tool** (`2`) for localized simplification by `Ctrl`-clicking a node, then clicking another on the same contour.

---

# Chapter 9: Element References & Compositing

FontLab 7 utilizes a flexible, object-oriented approach to glyph construction through **Elements**. Rather than relying on simple, flat contours, FontLab allows you to build complex glyphs using individual, reusable design components. This chapter explains the mechanics of compositing, the concept of Element References, and how to manage them within your font project.

## Component-Based Design & Elements

In professional type design, glyphs are often composed of discrete parts—such as stems, serifs, or diacritics. In FontLab 7, any vector drawing, image, or text box is treated as an **Element**. A glyph layer can contain one element or a composite of multiple elements.

Unlike standard layers, which separate entire master designs (like Regular and Bold) or coordinate spaces, elements are structural blocks within a single layer. Compositing involves assembling these blocks to form complete glyphs, such as combining an `e` element and an `acute` element to create `eacute`.

## Element References vs. Components

While other font editors use "components" to link one glyph's outline into another, FontLab 7 utilizes **Element References**. An Element Reference is a link to a source element. The key distinction is that elements do not need to exist as standalone glyphs in your font; they can reside solely in the font’s **Gallery** or as unmapped elements.

When you copy an element and paste it as a reference (using `Edit > Paste Special > Links` or `Element > Reference`), you create a live clone.

- **Live Linking:** Editing the Bezier curves, node continuity (G1 or G2 status), or coordinates of one element reference immediately updates all other instances across the entire font.
- **Non-Destructive Transformations:** Each reference instance can be uniquely scaled, rotated, mirrored, or shifted without breaking the connection to the source contours.
- **Independent Metrics:** The advance width and sidebearings of the composited glyph remain adjustable, while the reference's internal positioning updates dynamically.

> [!TIP] Use Element References for shared features like serifs, stems, or diacritic accents. This ensures stylistic consistency and speeds up global design adjustments.

## Managing Elements

FontLab 7 provides several tools and panels to organize and manipulate your elements:

### The Elements Panel and Layers List

The **Elements panel** displays the hierarchical structure of the active layer. Here, you can name elements, view their references, and reorder them. Reordering elements changes their rendering stack, which is critical for color fonts or overlapping shapes.

### The Gallery Panel

The **Gallery panel** acts as a repository for all elements in the font. You can drag elements from the canvas into the Gallery to save them for future use, or drag them from the Gallery into a glyph to place a reference.

### Decomposing References

If you need to make unique edits to an instance of an element without affecting other glyphs, you must **decompose** it.

1. Select the element reference in the Glyph window.
2. Choose `Element > Decompose` (or click the decompose icon in the Elements panel).
3. The reference is converted into independent, local Bezier contours.

> [!IMPORTANT] Decomposing is destructive and cannot be undone once the file is saved. The link to the parent element is severed permanently.

---

# Chapter 10: Working with Colors and Swatches

FontLab 7 provides a comprehensive set of color tools designed for managing design workflow and engineering multi-colored, layered OpenType fonts. Color can be applied as metadata to flag glyph cells in the interface, or directly to glyph contours as vector stroke and fill properties.

## Visual Color Organization

Color is an essential organizing tool in type design. FontLab 7 distinguishes between UI-level organization (such as marking glyphs to track design progress) and outline-level color assignments (such as creating color fonts with SVG or COLR/CPAL tables).

## Cell Flagging

Cell flagging (referred to as "glyph marks" in FontLab Studio 5) allows you to apply a background and caption color highlight to glyph cells in the Font Window. Flagging is an excellent way to visually categorize glyphs by status, type (uppercase, lowercase, digits), or script.

- **Applying Flags:** Select glyph cells and choose one of the five predefined flag colors (Red, Blue, Green, Magenta, Cyan) from the Font Window header or the context menu's **Flag** submenu.
- **Custom Flags:** Select **Custom...** to specify a custom hue value (0–360) using a slider or direct numeric entry.
- **Removing Flags:** Select the flagged glyphs and click **No flag** in the header or context menu.
- **Sidebar and Filtering:** In the Font Window sidebar, the **Flag** section displays all active flags along with the number of glyphs assigned to each. Click a flag in the sidebar to filter the Font Window. Enable **Hide Unfiltered Glyphs** to see only the flagged subset, or keep it off to group the flagged glyphs at the top.
- **Selection:** Use **Select > Same Flag** from the context menu to select all glyphs sharing the active glyph's flag.

> [!TIP] Cell flagging does not affect the exported font's visual outlines, but FontLab uses this metadata during development for filtering, sorting, and batch-processing.

## Contour Outlines and Fills

To design color fonts, you can apply stroke and fill colors to glyph outlines. In FontLab 7, color is applied to the **Element** level rather than to individual contours or nodes. Contours belonging to the same element must share the same stroke and fill, but separate elements or element references within a single glyph can be colored independently.

The **Color Panel** (**Window > Panels > Color**) features three interface modes: wheel, sliders, and box.

- To color a contour outline, click the unfilled circle in the top-left of the panel, pick a color, and click **Apply**.
- To color a contour fill, click the filled circle, choose a color, and click **Apply**.
- To batch-apply colors, select multiple cells in the Font Window. Hold `Alt` while clicking **Apply** to assign the color to the current layer of all selected glyphs.

## The Swatches Panel

While the Color Panel acts as a picker, the **Swatches Panel** (**Window > Panels > Swatches**) acts as a repository for predefined colors, allowing you to assign consistent style properties across your font family.

- **Display Modes:** Toggle between **List Mode** (shows swatches with names) and **Table Mode** (displays a compact grid of color icons).
- **Creating Swatches:** Mix a color in the Color Panel, then click the **Add Color (+)** button in the Swatches Panel's status bar to save it.

## Palette Libraries Management

Manage groups of swatches by clicking the palette icon in the Swatches status bar to open the **Palettes** dialog. Here, you can add, duplicate, rename, or delete palettes. Custom palettes can be saved as `.palettes` files, which is ideal for organizing style categories and sharing color configurations between different projects.

> [!IMPORTANT] When exporting color fonts, FontLab automatically generates CPAL (color palette) and COLR tables, or SVG tables, depending on your export profile.

---

# Chapter 11: Importing Artwork & Autotracing

FontLab 7 offers robust tools to convert physical sketches, raster images, and external vector templates into precise, edit-ready glyph contours. Type designers can choose to directly import vector graphics or paste bitmap images, utilizing advanced filters and autotracing parameters to generate clean Bezier paths.

## Importing Vector vs. Bitmap Artwork

FontLab support varies depending on whether you are working with vector artwork or bitmap files:

- **Vector Graphics (SVG, EPS, PDF, AI):** You can import vector files via `File > Import > Artwork` or by copy-pasting directly from vector editors. When pasting, FontLab supports both legacy **AICB** (ideal for monochrome paths) and **PDF** formats (ideal for complex multi-color designs, clipping masks, or artwork from Affinity Designer and Sketch). The _Paste or Import Artwork_ dialog allows you to choose between importing **Elements and Colors** (retains stroke, fill, and color) or **Contours Only** (ignores styling and automatically rounds coordinates to integer units).
- **Bitmap Files (PNG, JPG, BMP, TIFF):** Raster images are imported as background image elements. By default, 1 pixel in a raster image corresponds to 1 font unit. For optimal resolution, design sketches should be scaled so that key dimensions (like Cap Height) match your target UPM size (e.g., drawing an uppercase 'H' at 700 pixels high for a 700-unit cap height).

> [!TIP] If your vector artwork has fractional coordinates, enable coordinate rounding preferences to automatically align paths to the font grid upon import.

## Preparing Bitmaps via the Image Panel

Before autotracing, clean up your raster sketches using the **Image Panel** (`Window > Panels > Image`). Select the image element and apply these non-destructive filters:

- **Remove Background:** Isolates the glyph drawing from paper backgrounds.
- **Despeckle / Reduce Noise:** Cleans scanning artifacts, dust, and stray pixels.
- **Gaussian Blur & Threshold:** Blurring an image slightly and applying a Threshold (based on Luminosity, Opacity, or Color) sharpens rough edges, turning pixelated gradients into high-contrast black-and-white shapes.

## Autotracing Parameters

To convert a prepared image, select it and choose `Element > Image > Autotrace...`. The dialog offers real-time preview and features three key sliders to control initial contour generation:

1.  **Trace Tolerance:** Controls how closely the path follows the pixel boundaries. A value of 1 follows edges precisely, while higher values follow loosely, yielding straighter segments.
2.  **Curve Fit Distance:** The allowed curve approximation error. Lower values generate more nodes; higher values yield fewer nodes and flatter curve segments.
3.  **Straighten Angle:** Determines the threshold for converting curves to straight lines. Higher values favor corner points and straight lines.

Under **Trace result is**, choose between **PS contours** (cubic Bezier), **TT contours** (quadratic Bezier), or **Lines only**.

> [!IMPORTANT] Postprocess your trace by checking **Nodes at extremes** to automatically place nodes at horizontal and vertical curve maxima, which is critical for rendering and hinting.

## Tracing Workflows & Manual Tips

After autotracing, choose to **Keep**, **Remove**, or **Move to Mask** the source image. Moving the image to the Mask layer with reduced opacity (e.g., 20–30%) allows you to keep the original sketch as a visual template for manual tracing and fine contour adjustments.

For sheets containing entire alphabets, place the scanned artwork on the Sketchboard and choose `Element > Image > Separate and Trace`. FontLab will segment the sheet into individual glyph elements using optical separation settings and autotrace them in a single batch.

---

# Chapter 12: Managing Layers and Masks

## The Layers and Masters Panel

The Layers and Masters panel (**Window > Panels > Layers & Masters**) is the central hub for managing multi-layer glyph construction, master designs, and auxiliary outlines in FontLab 7. The panel features a structured hierarchy: a local toolbar at the top, a scrollable list of layers in the middle, a collapsible properties section, and a status bar at the bottom.

In the layers list, each entry displays its name, a thumbnail preview, the number of constituent elements, and status columns for visibility, locking, service layer attributes, and wireframe visualization. Visual feedback is color-coded to indicate interpolation compatibility:

- **Bold Names:** Indicate font or glyph master layers that contribute to variations.
- **Pale Green:** The master is fully compatible for interpolation.
- **Yellow:** The master is compatible, but contour or node order differs.
- **Pale Red:** The master is incompatible, indicating mismatched point or contour counts.
- **Grey Name (`#instance`):** Represents the dynamically interpolated virtual instance.

## Master Layers vs. Service and Auxiliary Layers

FontLab 7 distinguishes between exportable masters and non-exportable utility layers:

- **Master Layers:** These define the design space boundaries for variable fonts. They contain the primary Bézier contours, anchors, and advance widths that are exported into final formats.
- **Service Layers:** Activating the service attribute (`_service`) hides the layer from the Font Window and the Preview panel. Service layers do not export or participate in interpolation.
- **Background and Locked Layers:** Layers can be moved to the background (bottom of the stack) or locked to prevent accidental vector edits.
- **Wireframe Mode:** Renders filled vector shapes as outlines, useful for inspecting overlapping paths.

> [!NOTE] Cmd-clicking (`++Cmd++` on macOS or `++Ctrl++` on Windows) the color dot column header automatically assigns unique colors to all layers, excluding mask layers.

## Layer Operations and Properties

In the status bar, you can add layers (`++Cmd+Shift+N++`), duplicate them, or delete them. The properties section, toggled via the toolbar, exposes opacity controls (0–100%) and the Auto Layer toggle. Activating **Auto Layer** locks manual editing, instead generating the glyph's contours automatically using FontLab's predefined or custom glyph recipes.

> [!TIP] Use the **Merge Visible Layers** button in the status bar to combine visible, non-service layers prior to flattening and exporting.

## Glyph Mask Layers

A Mask layer is a dedicated service layer tied to a parent design layer, used to preserve temporary vector states.

- **Creating a Mask:** Select a contour and choose **Tools > Copy to Mask** (`++Cmd+M++`).
- **Editing a Mask:** Choose **Tools > Edit Mask** (`++Ctrl+H++`) or double-click the mask contours. The canvas background shifts color to indicate mask-editing mode.
- **Interactions:** Toggle **View > Snap > Mask** to snap active outline nodes directly to mask vectors. Use **Tools > Swap with Mask** (`++Ctrl+Alt+M++`) to exchange contours between the main outline and the mask.

## The Global Mask System

Unlike local masks, the **Global Mask** is a font-wide reference template that displays across all glyphs and layers. It does not appear in the Layers and Masters panel.

- **Creating:** Select contours in any glyph and run **Tools > Copy to Global Mask** (`++Shift+Cmd+M++`).
- **Usage:** Enable **View > Show > Global Mask** and **View > Snap > Global Mask** to project the template and snap contours to it across the design space.
- **Clearing:** Run **Tools > Clear Global Mask** (`++Shift+Cmd+K++`).

---

# Chapter 13: Using the Sketchboard

The Sketchboard is FontLab 7’s open-canvas environment—an infinite virtual desktop designed to support the early stages of type design. Unlike the structured Font Window or individual Glyph Windows, which force elements into rigid metric boxes and strict glyph hierarchies, the Sketchboard functions as an unconstrained drafting area. It allows designers to sketch, import raw assets, trace scanned artwork, and format proofing specimens within a single cohesive workspace.

## Drawing Outside the Font Grid

On the Sketchboard, you can create and manipulate vector geometry without assigning it to a specific Unicode codepoint or being bound by standard font coordinates. This freedom is ideal for experimental lettering, drawing logotypes, or exploring Bezier curve concepts before committing them to a formal glyph slot.

You can use the full suite of FontLab drawing tools—including the Rapid, Pen, Pencil, and Brush tools—directly on the canvas. As you draw, you can refine vector nodes, manage handles, and enforce node continuity (such as G1 or G2 curvature continuity) without worrying about advance widths, sidebearings, or vertical metrics. Once you are satisfied with a vector shape, you can convert it into an element and drag it directly into a cell in the Font Map panel, instantly promoting the artwork to a standard glyph.

> [!TIP] To quickly turn a series of disconnected drawings on the Sketchboard into glyphs, select them with the Element tool (V) and choose **Element > Place As Glyphs > Selected Elements**.

## Text Boxes and Sample Strings

The Sketchboard is also a robust tool for typographic proofing and testing. By selecting the Text tool and clicking anywhere on the canvas, you can create a Text Box. These text boxes are not static displays; they act as live, fully editable multi-glyph sample strings using any active font currently open in FontLab.

Any edits you make to the contours, sidebearings, or kerning within a text box instantly update all instances of those glyph elements across the canvas and the open font itself. Text boxes support three distinct wrapping modes:

1. **Continuous String**: Keeps the sample text on a single line, ideal for testing word rhythm and headline settings.
2. **Auto-Wrap Block**: Wraps text inside a resizable rectangular frame to test paragraph textures.
3. **Table View**: Places each character in a separate cell, allowing for clean side-by-side metric inspections.

> [!NOTE] FontLab automatically saves the text boxes associated with an open font in the corresponding VFC or VFJ file. If you close the font, its text boxes disappear, but they will reappear in the exact same positions when the font is reopened.

## Importing Graphics and Directories

When starting a project from physical drawings, the Sketchboard simplifies the ingestion of raw artwork. You can import large graphics files or directories of scanned images using **File > Import > Artwork**. FontLab supports vector formats (EPS, SVG, PDF-compatible AI) and standard bitmap images.

Once imported, you can use **Element > Image > Separate and Trace** to optically split a scanned sheet of letters into individual glyph components and autotrace them into clean Bezier contours.

## Exporting the Sketchboard

To share specimens or export layouts, you can output the Sketchboard contents directly using **File > Export > Window Contents**. This command exports the canvas to vector-based PDF or SVG formats, preserving not only outline shapes and color bitmaps but also guides, hints, alignment zones, and metrics.

---

# Chapter 14: Spacing & Sidebearings

To design a functional typeface, spacing is just as critical as drawing outlines. In FontLab 7, spacing is managed via horizontal glyph metrics, which determine how individual characters position themselves relative to each other. Controlling this spatial rhythm requires a clear understanding of horizontal dimensions, the Metrics tool, and dynamic linking systems.

## Horizontal Metrics Definitions

A glyph’s horizontal spacing is governed by four core spatial properties:

- **Bounding Box (BBox) Width:** The physical width of the glyph’s outlines, measured from the leftmost point of the contour (the left outline edge) to the rightmost point (the right outline edge).
- **Left Sidebearing (LSB):** The distance between the glyph origin (the zero coordinate point on the horizontal axis) and the leftmost edge of the bounding box. It represents the negative or positive white space on the glyph’s left side.
- **Right Sidebearing (RSB):** The distance between the rightmost edge of the bounding box and the advance width boundary.
- **Advance Width:** The total horizontal space assigned to the glyph. This value determines the horizontal distance the text cursor moves after typing the character. It is the sum of the LSB, the BBox width, and the RSB.

> [!NOTE] Sidebearings can be positive (for typical spacing) or negative (when parts of a contour, such as the serifs of a "T" or "f", overhang the advance width boundary).

## The Metrics Tool and Property Bar

To edit these values, activate the **Metrics tool** by clicking its icon in the Toolbar or pressing `M`. If no Glyph window is open, activating the tool automatically opens one for the selected glyph.

In Metrics mode, the active glyph is highlighted with contrasting sidebearing lines. If these lines are hidden, click the **Show Spacing Controls** button in the property bar. The Metrics Property bar displays editable fields for **L** (LSB), **R** (RSB), and **W** (Width).

Developers can edit spacing in three ways:

1. Dragging the sidebearing lines or triangle handles directly in the Glyph window.
2. Clicking and dragging the glyph itself to redistribute the LSB and RSB without changing the total advance width (or Alt-dragging to adjust the advance width).
3. Entering values directly in the Property bar fields, the Metrics Table, or the Glyph panel.

> [!TIP] Tapping the semicolon key (`;`) in Metrics mode triggers FontLab’s autospacing algorithm to instantly assign optical sidebearings to the current glyph.

## Binding Sidebearings and Italic Slanting

FontLab 7 allows designers to bind metrics together using **linked metrics expressions**. Instead of manual numbers, you can enter a glyph name (e.g., `o` or `H`) in the LSB, RSB, or Width fields. FontLab supports basic math operations (e.g., `o * 1.05 + 10`).

To link metrics across different masters, use the colon prefix (e.g., `:Regular` or `:Regular * 1.1`). For automatic updates, enable **Font > Live Update > Live Metrics**.

For italic fonts, sidebearings must be measured along the slant. Turn on **View > Apply Italic Angle to Metrics** (or enable **Preferences > Grid > Follow the font’s Italic Angle**) to skew the metrics grid. This ensures LSB and RSB coordinates are calculated parallel to the italic axis, maintaining visual consistency in slanted designs.

---

# Chapter 15: Kerning Classes and Exceptions

Kerning adjusts the horizontal space between specific glyph pairs to achieve visually consistent spacing, supplementing the default sidebearings. While flat (glyph-to-glyph) kerning is straightforward, it can dramatically bloat font files. To optimize GPOS tables, FontLab 7 utilizes OpenType class-based kerning.

## Left vs. Right Kerning Classes

To manage kerning efficiently, glyphs with similar optical shapes are grouped into kerning classes. Since a glyph behaves differently depending on whether it appears on the left or the right side of a pair, FontLab 7 distinguishes between:

- **1st Kerning Class (Left-Side):** Applied when the glyph is on the left side of a pair. For example, glyphs like `O`, `Q`, and `C` share a class indicator for their right sidebearings.
- **2nd Kerning Class (Right-Side):** Applied when the glyph is on the right side of a pair. For example, glyphs like `O`, `U`, and `D` share a class indicator for their left sidebearings.

A glyph can belong to one 1st class and one 2nd class. Within each class, a designated **key glyph** (or class leader) defines the spacing relationship for the entire group.

> [!IMPORTANT] A glyph cannot belong to multiple classes on the same side. Doing so creates conflicts that prevent GPOS table compilation.

## Class Kerning Workflow and Exceptions

To build a class kerning workflow, designers group glyphs under left and right classes and define kerning for the class leaders. In a class-to-class workflow, adjusting space between two key glyphs automatically applies that adjustment to all combinations of glyphs in those classes. This significantly reduces the overhead of defining pairwise adjustments for every combination.

However, certain pairs require unique spacing that departs from the class rule. These are handled as **kerning exceptions**:

1.  Select the pair in the Glyph Window with the **Kerning tool** (`K`) active.
2.  Locate the **lock icons** in the Property bar or Kerning panel next to the active glyphs.
3.  Click the lock icon to unlock it, detaching the glyph from its class for this pair.
4.  Adjust the kerning value to write a glyph-specific exception, overriding the class rule.

> [!TIP] Keep exceptions to a minimum. Excessive exceptions inflate GPOS table sizes and can cause rendering issues in legacy environments.

## The Pairs & Phrases Panel

Systematic testing is crucial for quality kerning. Use the **Pairs & Phrases** panel (`Window > Panels > Pairs & Phrases`) to proof combinations:

- **List Selection:** Load predefined lists of common pairs, words, or custom texts.
- **Filtering:** Filter the list to display only active pairs, class pairs, or specific characters.
- **Navigation:** Double-click any pair in the panel to display it instantly in the Glyph Window for rapid editing.

## Quick Kerning Controls and Editing

With the Kerning tool active, you can edit kerning values visually or numerically:

- **Visual Dragging:** Drag the active glyph or the interactive kerning handle between glyphs to adjust the space.
- **Keyboard Shortcuts:** Press the `Left`/`Right` arrow keys for 1-unit adjustments, or hold `Shift` for 10-unit steps.
- **Property Bar:** Enter precise numerical values directly into the kerning field at the top of the window.

---

# Chapter 16: OpenType Layout Features

OpenType layout features transform static glyphs into dynamic, intelligent typographic systems. By defining glyph substitutions and precise positioning adjustments, designers can manage complex scripts, ligatures, small caps, contextual alternates, and mark-to-base attachments. FontLab 7 provides a comprehensive environment to write, compile, test, and manage this layout code using the standard Adobe Feature File syntax (FEA).

## The Features Panel

The central hub for managing feature code is the **Features panel** (Window > Panels > Features). Here, you can define glyph classes, prefix blocks, and specific OpenType features (such as `liga`, `smcp`, or `kern`).

- **Glyph Classes**: Group glyphs sharing common typographic roles (e.g., lowercase letters, small caps, or base glyphs) to streamline rules. FontLab supports both named classes (e.g., `@lc_vowels`) and inline classes.
- **Prefix**: Add global declarations, such as languagesystem statements (e.g., `languagesystem latn dflt;`), which register features across operating systems, layout engines, and applications.
- **Features**: Individual blocks containing substitution and positioning rules grouped by their four-letter OpenType tags.

> [!TIP] You can automatically generate standard features by selecting **Create Features from Font Info** in the panel menu. FontLab analyzes glyph names to generate rules for ligatures, small caps, and figures.

## Writing Substitution and Positioning Rules

OpenType feature code separates instructions into two primary categories: GSUB (Glyph Substitution) and GPOS (Glyph Positioning).

### Glyph Substitutions (GSUB)

Substitutions replace one or more glyphs with alternative glyphs. The most common substitution rules include:

- **Ligatures (`liga`, `dlig`)**: Multiple input glyphs are replaced by a single composite glyph. `sub f i by f_i;`
- **Small Caps (`smcp`, `c2sc`)**: Replaces standard lowercase or uppercase characters with small capital variants. `sub a by a.sc;`
- **Contextual Alternates (`calt`)**: Substitutes a glyph based on its surrounding glyph context. `sub f' [i e] by f.short;`

### Glyph Positioning (GPOS)

Positioning rules adjust the placement or advance width of glyphs without replacing them. This is essential for kerning and diacritic placement:

- **Pair Adjustment (Kerning)**: Shifts the distance between specific glyph pairs. `pos T e -50;`
- **Mark Attachment (`mark`, `mkmk`)**: Anchors diacritical marks to base glyphs using coordinate-based anchor points. `pos base [a] <anchor 450 600> mark @TOP_MARKS;`

> [!IMPORTANT] When defining positioning adjustments, FontLab translates visual anchors (such as `top` or `bottom` points defined inside the Glyph window) directly into GPOS anchor code during compilation.

## Compiling and Testing Features

OpenType features must be compiled into binary tables to function. FontLab 7 uses the integrated Adobe AFDKO library to compile feature code in-app.

- To compile, click the **Compile** button (the play icon) in the Features panel. Any syntax errors or compilation warnings will appear in the Output panel.
- To test the compiled features, open the **Preview panel** (Window > Panels > Preview). Type test strings and toggle active features from the panel's feature selector to verify substitutions and positioning in real-time.

## Managing External Feature Files

For complex workflows, FontLab allows loading and saving external `.fea` files. Through the Features panel menu, you can import external feature code to overwrite or append to your existing rules.

> [!NOTE] External FEA imports are parsed and mapped to existing glyphs. Ensure that all glyph names referenced in external files exactly match the glyph names present in your FontLab Font Map.

---

# Chapter 17: Font Info and Axes Configuration

The **Font Info** panel (File > Font Info) serves as the centralized repository for all metadata, styling attributes, global metrics, and variation parameters within a FontLab project. Configuring these settings accurately is critical for generating fully functional OpenType, TrueType, and Variable fonts.

## The Font Info Metadata Structure

Font Info is organized into hierarchical sections. The core metadata includes:

- **Names**: Contains the naming fields required across different operating systems.
- **Family Naming Strategies**: FontLab manages the complex naming schema required by legacy and modern platforms. The family name serves as the overarching identifier, while style names differentiate variants. Best practice dictates configuring both the _Preferred Family_ (allowing unlimited weights/styles) and the _Style Map Family_ (restricting style groups to the standard four-style RIBBI structure: Regular, Italic, Bold, Bold Italic) for maximum compatibility.
- **Styling and Classification**: Under _Classification_, users can define the weight class, width class, and slope of each master. Additionally, **PANOSE** parameters allow you to specify numerical descriptors for characteristics such as serif style, proportion, contrast, and mid-line behavior. These values assist operating systems in substituting missing fonts with visually similar designs.
- **Metrics and Parameters**: Global metrics—including ascender, descender, cap height, x-height, and alignment zones—are defined per master. These values dictate the vertical metrics and influence auto-hinting behavior.

> [!IMPORTANT] Inconsistent family naming or misconfigured RIBBI style mapping can lead to installation conflicts, cross-platform style-linking errors, and incorrect rendering in word-processing software.

## Setting Up Axes of Variation

When designing a variable font or a multi-master family, defining the design space axes is the primary step. An axis represents a direction of variation, such as Weight, Width, or custom design axes.

- **Standard Axes**: Typically use standard four-letter tags defined by the OpenType specification, such as `wght` (Weight) and `wdth` (Width).
- **Custom Axes**: You can create custom axes using uppercase tags (e.g., `GRAD` for Grade, `SERF` for Serif Size).

Each axis requires a Tag, Name, and defined range. Each master is placed at a specific coordinate junction.

> [!NOTE] Every glyph master must share the exact same number of contours, nodes, handles, and starting points to ensure interpolation compatibility. Changing node continuity (e.g., G2 curvature continuity) or altering contour direction between masters will break interpolation.

## The Axis Graph Mapping

One of the most powerful features in FontLab 7's variation engine is the **Axis Graph**, which maps design space coordinates to user coordinates.

1. **Design Space Coordinates**: The raw, internal values used during drawing (e.g., stem thickness measurements like 40 to 180 units, which directly govern Bezier curve node placements and advance widths).
2. **User Coordinates**: The external values exposed to end-users (e.g., CSS weight scale from 100 to 900).

The Axis Graph defines the mapping between these two spaces. By default, this mapping is linear. However, visual weight progression is rarely linear; a leap from Light (300) to Regular (400) requires a different physical increment in stem width and sidebearings than from Bold (700) to Black (900).

> [!TIP] Use the Axis Graph to create a non-linear mapping. This ensures that the user-facing sliders interpolate smoothly and produce visually balanced transitions, even if the underlying Bezier curve coordinate shifts are non-linear.

---

# Chapter 18: Variable Fonts and Outline Compatibility

In FontLab 7, the process of working with multiple masters and design axes to output dynamic instances is referred to as variation. Creating a variable font requires setting up a designspace and ensuring that master outlines are fully compatible for interpolation.

## Designing the Designspace

A designspace is defined by one or more variation axes—such as Weight (`wght`), Width (`wdth`), or Slant (`slnt`)—configured in **Font Info > Axes**. Font masters and font-less masters (defined at the glyph level using axis-location suffix names like `:wt=350,wd=75`) are mapped to specific coordinates within this multidimensional designspace. FontLab 7 uses these coordinates to calculate the interpolation and extrapolation of intermediate instances.

> [!IMPORTANT] Ensure that all master styles have unique locations in the designspace. You will be unable to export your font or preview variations correctly if two masters share identical coordinates.

## Outline Compatibility Rules

For smooth interpolation, the outline geometry of each glyph must match perfectly across all active masters. Outlines are compatible when they satisfy the following structural requirements:

1. **Matching Count**: The glyph must have the same number of elements and contours, and each contour must contain the exact same number of nodes (both sharp and smooth) and Bézier curve control points.
2. **Matching Start Points**: The designated start point (node index 0) of every contour must be at the same relative topological position in all masters. If start points do not align, the contour will twist or self-intersect during interpolation.
3. **Consistent Contour Direction**: Contours must flow in the same direction (either clockwise for counters or counter-clockwise for outer paths) in all masters. Inconsistent direction causes rendering and fill artifacts.

> [!TIP] Turn on **Edit > Match when Editing** to synchronize node additions, deletions, and adjustments across all compatible masters simultaneously, preserving outline compatibility during the drawing process.

## Diagnosing and Resolving Incompatibilities

FontLab 7 provides several specialized interfaces to verify outline compatibility before exporting:

- **Non-Matching Sidebar Filter**: In the Font window, expand the **Layers & Masters** section of the sidebar. The **Non-matching** filter displays the exact number of incompatible glyphs. Clicking this filter isolates these glyphs for rapid troubleshooting.
- **Matchmaker Tool**: Activate this tool by tapping the `7` key. The property bar displays a green status indicator if the masters are compatible, and red if they are not. Matchmaker shows node numbers and color-codes matching contours. You can select corresponding node ranges and let Matchmaker automatically harmonize the path segments.
- **Interpolation Preview**: Use the **Variations** panel to navigate your designspace. By drawing an interpolation vector in the Map view, you can check the **Interpolation** preview in the Preview panel to inspect intermediate steps.

## Variable Font Export

Once compatibility is verified, choose **File > Export Font As** and select a variable format, such as **Variable TT (.ttf)** or **Variable PS (.otf)**. FontLab compiles the designspace parameters, default master structures, and interpolation deltas into the final OpenType Variations font.

---

# Chapter 19: Python Scripting and Automation

FontLab 7 includes a built-in, cross-platform Python 3 scripting environment that enables type designers and font engineers to automate repetitive tasks, execute batch modifications, and extend the application's interface. By interacting with FontLab's internal data structures, scripts can programmatically manipulate Bezier curves, adjust horizontal sidebearings and advance widths, manage OpenType layout features, and construct custom workflows.

## The Scripting Panel and Environment

The primary interface for executing script code is the **Scripting panel** (_Window > Panels > Scripting_). The panel contains a simple code editor with syntax highlighting, an output console that displays results or runtime errors, and controls to run scripts. Users can write code directly in the editor, load external `.py` scripts, or run individual statements interactively.

Additionally, scripts saved in the user's `Scripts` folder are automatically registered in the _Tools > Scripts_ menu, allowing them to be assigned custom keyboard shortcuts.

## The `fontlab` High-Level API

The `fontlab` package is the modern, high-level Python API designed for intuitive font and glyph editing. It acts as the wrapper for the active workspace, providing high-level objects to query and modify the current design state:

- **Current Workspace:** The `flWorkspace` class handles window-level management. Access the active workspace using `fontlab.flWorkspace()`.
- **Current Font (Package):** The `CurrentFont()` function returns the active font as a `flPackage` object. Through this object, you can access global font properties, masters, font info metadata, classes, and the font’s glyph collection.
- **Selected Glyphs:** The `CurrentGlyph()` function yields the active `flGlyph` object currently open in the Glyph Window, while `CurrentFont().selectedGlyphs` returns a list of all selected glyphs in the Font Window. You can programmatically iterate through these glyphs to modify contour nodes, shift sidebearings, or insert anchors.

> [!TIP] When modifying glyph outlines programmatically, work with floating-point coordinates to maintain Bezier curve precision and G2 node continuity across masters. Use integer rounding only before final font export.

## Low-Level and Legacy APIs: `fontgate` and `FL`

For deep control over the application's underlying engine and legacy script compatibility, FontLab 7 exposes two additional packages:

- **The `fontgate` Package:** This low-level, C++-wrapped library contains the raw data structures of the FontLab core engine. It deals with the fundamental geometry and serialization classes, such as `fgFont`, `fgGlyph`, `fgContour`, and `fgPoint`. While more complex to write, it offers high-performance processing when executing intensive operations on thousands of nodes or coordinates.
- **The `FL` Package:** To ensure backward compatibility, FontLab 7 includes the legacy `FL` API. This simulates the Python 2 scripting interface of FontLab Studio 5. Using `FL` allows developers to run older scripts with minimal modification, facilitating transition to the modern Python 3 API.

## Custom User Interfaces with PythonQt

Through the integration of **PythonQt**, scripts can access the underlying Qt framework to construct rich, native user interfaces.

Instead of running silently or relying on simple command-line prompts, developers can import modules from `PythonQt.QtGui` and `PythonQt.QtCore` to build custom dialogs, text inputs, buttons, and settings panels. These custom windows inherit FontLab's styling and operate within the application's main loop.

> [!IMPORTANT] When building custom UI windows using PythonQt, always ensure your dialogs are properly parented to the main FontLab window to prevent focus-locking issues or application crashes when the script terminates.

---

# Chapter 20: Testing, Proofing and Exporting

Before releasing a font, a systematic workflow of quality control, outline inspection, and compile verification is essential. FontLab 7 provides built-in tools to preview layout behavior, diagnose contour errors, configure technical export profiles, and package final static or variable fonts.

## Quality Control and Visual Proofing

Visual testing begins in the **Preview panel**, a live sandbox for rendering, spacing, and OpenType features. Unlike the standard Glyph window, the Preview panel allows you to type custom text strings, test interpolation steps across masters, and inspect rendering behaviors at various sizes. You can choose different modes (e.g. Content, Spacing, or Kerning) and preview individual masters or specific design space locations.

To proof layout features—such as ligatures (`liga`), small caps (`smcp`), or mark-to-base positioning (`mark`)—you must first compile the OpenType feature code. Open the **Features panel** and click the **Compile** button. Once compiled, these features can be toggled on or off directly within the Preview panel or the text toolbar to ensure the substitution and positioning rules function as designed.

> [!NOTE] If your font family contains multiple masters and you have manually defined your features, ensure your export profiles are configured to build features for each master separately. This prevents duplicate feature definitions from overriding unique master metrics.

## Automated Audits with FontAudit

FontLab’s **FontAudit** is an automated engine that analyzes glyph outlines for technical errors. You can activate it via `View > Show > FontAudit` or open the FontAudit panel (`Window > Panels > FontAudit`) to inspect the current layer. To audit multiple glyphs, select them in the Font window and choose `Glyph > FontAudit Glyphs`. Red corner flags indicate resolved and unresolved issues, which can be fixed globally using `Glyph > Fix FontAudit Problems` or individually in the panel. Key checks include:

- **Intersections:** Overlapping contours that can cause rasterization artifacts.
- **Missing Extrema:** Curve segments lacking nodes at their outermost vertical or horizontal points. Extrema nodes are crucial for hint placement and interpolation consistency.
- **Curve Flats:** Curved Bezier segments with aligned handles that can be losslessly simplified to straight lines.
- **Irregular and Uncommon Stems:** Inconsistencies in stem thicknesses compared to common values set in `Font Info > Stems`.

## Export Profile Setup

Exporting transforms development source files (`.vfc`/`.vfj`) into production-ready formats via the **Export Profiles** dialog (`File > Export Profiles...`). Profiles define how FontLab processes contours, handles glyph names, and compiles OpenType tables on output.

You can customize profiles to control coordinate precision. TrueType outlines (`.ttf`) require rounding coordinates to integers, while PostScript outlines (`.otf`) support fractional coordinates to preserve Bezier curve fidelity at the cost of slightly larger file sizes. Profiles also manage whether to remove looped corners, convert development glyph names to production names, and generate OpenType kerning or mark-to-mark (`mkmk`) features.

## Compiling and Packaging

To generate your final fonts, choose `File > Export Font As...`.

- **Static OTF/TTF:** Select the standard OpenType PS (`.otf`) or OpenType TT (`.ttf`) profiles.
- **Variable Fonts:** Use the **Variable TT (.ttf)** profile. For variable packaging, all masters must maintain node compatibility—meaning identical contour directions, matching node counts, and identical start points.
