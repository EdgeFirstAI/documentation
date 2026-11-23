# 3D Keyboard Hotkeys

The annotation editor supports keyboard shortcuts for the most common tools and actions.  Shortcuts act on the canvas you clicked last, either the 2D image canvas or the 3D point cloud canvas, so click inside the canvas you want to work in before pressing a key.  Shortcuts are ignored while a text field has focus.

!!! tip
    Hover over a tool in the toolbar to see its shortcut in the tooltip, for example *Clustering Mode (c)*.

## 3D Canvas

These shortcuts apply when the 3D canvas is the active pane.

| Key | Action |
|---|---|
| `Q` | 3D pointer tool: select, move and edit existing 3D annotations. |
| `B` | 3D box tool: draw a new 3D box. |
| `C` | [Clustering tool](3d_annotations.md#cluster-3d-annotation): drag a region to box the largest cluster of points. |
| `L` | Edit the label. |
| `G` | Translate (move) the selected 3D box. |
| `S` | Scale the selected 3D box. |
| `Up` / `Down` | Select the previous or next object. |
| `Esc` | Clear the selection, reset the selected label and return to the 3D pointer tool. |

<!-- SCREENSHOT: assets/hotkeys-3d-toolbar.jpg - 3D canvas tool controls with a tooltip showing a hotkey, e.g. "Clustering Mode (c)" -->

## 2D Canvas

These shortcuts apply when the 2D image canvas is the active pane.

| Key | Action |
|---|---|
| `Q` | Pointer tool. |
| `B` | Box tool: draw a 2D bounding box. |
| `W` | Brush tool: paint a segmentation mask. |
| `P` | Line tool: draw a polygon. |
| `L` | Label tool. |
| `E` | Eraser tool.  Available when exactly one annotation is selected. |
| `A` | Launch Automatic Ground Truth Generation (a confirmation dialog is shown). |
| `K` | Key frame editing.  See [Key Frames](index.md#key-frames). |
| `=` / `-` | Increase or decrease the brush cursor size. |
| `Z` | Zoom to the selected annotation, or fit the image to the view when nothing is selected. |
| `Up` / `Down` | Select the previous or next object. |
| `Esc` | Clear the selection and return to the pointer tool. |

!!! note
    To turn key frame editing on, use the **Key Frame Editing** button in the 2D toolbar.  The `K` shortcut is documented for completeness but should not be relied on to enable the mode.

## Editing

These shortcuts apply in either canvas while in edit mode.

| Key | Action |
|---|---|
| `Delete` | Delete the selected annotations. |
| `Ctrl+C` | Copy the selected annotations. |
| `Ctrl+V` | Paste the copied annotations. |
| `Ctrl+X` | Open the bulk delete dialog. |
| `Enter` | Submit: save the current changes from the sequence ribbon, or save the Automatic Ground Truth results. |
| `Ctrl` + click | Add an annotation to the selection (multi-select). |

## Sequences

| Key | Action |
|---|---|
| `Left` | Go to the previous frame. |
| `Right` | Go to the next frame. |

## SAM2 Sidebar

When the SAM2 sidebar is open, these shortcuts are also available.

| Key | Action |
|---|---|
| `N` | Add Object. |
| `X` | Select Existing Box: use an existing 2D box as the SAM prompt. |

## Audit Mode

In audit mode the editing shortcuts above are available, along with the following.

| Key | Action |
|---|---|
| `V` | Verify the selected annotations. |
| `Shift+V` | Set the selected annotations back to unreviewed. |
| `Space` | Toggle the selected annotations between verified and unreviewed. |
| `Enter` | Submit the audit. |
| `Left` / `Right` | Previous or next frame in a sequence audit.  In an image audit, `Right` skips to the next image. |

<!-- SCREENSHOT: assets/hotkeys-audit-mode.jpg - Audit mode ribbon showing the verified / unreviewed state of a selected annotation -->
