# Dataset Gallery

To open the dataset's gallery, click on the image preview of the dataset card.

{{ figure("../../datasets/assets/management/copied-dataset-result.jpg", "Dataset Card") }}

The gallery is multi-page dashboard split into [sequences](../../datasets/format/structure.md#1-sequence-based-datasets) and [images](../../datasets/format/structure.md#2-image-based-datasets) with a maximum of 40 images shown per page.

{{ figure("../../datasets/assets/management/sample-dataset-sequences.jpg", "Dataset Gallery") }}

## Gallery Controls

The controls above the grid change what is shown and what actions are available.  Some controls only appear in one of the two views, or only when you have write access to the dataset.

{{ figure("../assets/datasets/gallery-toolbar.jpg", "Gallery with numbered callouts on the Sequences/Images tabs, page control, Filter, Display Annotations, Display, Sort By and Actions buttons") }}

| Control | Description |
|---|---|
| **Sequences (N)** / **Images (N)** | Switch between the sequence view and the image view.  The number shows how many items the dataset contains. |
| **Page control** | Shows the current page and the page count, with buttons for the first, previous, next and last page.  Click the page number to jump to a specific page. |
| **Filter** | Opens the [filter panel](#filters).  Available in the image view. |
| **Display Annotations** | Chooses which annotation sets and labels are drawn on the image cards, and whether annotations are coloured by **Label** or by **Annotation Set**. |
| **Display** | Toggles the **Show Image Name** and **Show Labels** overlays on the cards. |
| **Sort By** | Sorts the images by **Frame**, **Image ID**, **Filename** or **Date Taken**, in ascending or descending order. |
| **Tags** | Shows or hides the tag controls.  See [Tag an Image](#tag-an-image). |
| **Actions** | Opens the [Actions menu](#actions-menu) for the selected items.  The badge shows how many items are selected. |

### Cards

Each sequence or image is shown as a card.

- Click the checkbox on a card to select it.  Select several cards to act on them together from the **Actions** menu.
- Click a card to open it in the annotation editor.  See [Annotating from the Gallery](#annotating-from-the-gallery).
- Sequence cards show the number of images in the sequence.  Their menu (the three dots) provides **Info**, **Edit Description**, **Download Sequence** and **Delete Sequence**.

{{ figure("../assets/datasets/gallery-cards.jpg", "A sequence card with its menu open and an image card with the name and labels overlays enabled") }}

## Filters

Filters allow users to select images based on the filter conditions.  The number of images filtered is displayed on the images count.  Filtered images can be copied to another dataset.

{{ figure("../assets/datasets/gallery-filters.png", "Gallery Filters") }}

Filters can be combined.  The available filters are:

| Filter | Selects images by |
|---|---|
| Annotation Set | Annotation set. |
| Annotation Label | Label name. |
| Annotation Type | Annotation type (for example 2D box, segmentation mask or 3D box).  Use **Invert Selection** to select the opposite and **Clear Selection** to reset it. |
| Confidence Range | Confidence of the annotation, useful for model predictions. |
| Bounding Box Size | Size of the bounding boxes. |
| Image Tag | Tags applied to the image. |
| Time Range and Date Range | When the image was captured. |
| Camera Source | The camera that produced the image. |
| Groups | Dataset group, such as training or validation. |
| Image Name | File name. |

The filter panel also provides **Copy Filtered Images** and **Delete Filtered Images** to act on every image that matches the current filters.

## Actions Menu

The **Actions** menu acts on the items that are selected on the cards.  Options that modify the dataset are hidden if you only have read access.

| Option | View | Description |
|---|---|---|
| **Add & update tags** | Images | Applies or removes tags on the selected images.  See [Tag an Image](#tag-an-image). |
| **Copy Selected Images (N)** / **Copy Selected Sequences (N)** | Images / Sequences | Copies the selection to another dataset.  See [Copy Selected Items](#copy-selected-items). |
| **Delete items (N)** / **Delete sequences (N)** | Images / Sequences | Deletes the selection after a confirmation. |
| **Import** | Both | Opens the import dialog to add more data to the dataset. |
| **Merge Annotations** | Images | Opens the merge annotations dialog. |
| **Select all N on this page** | Images | Selects every image on the current page. |
| **Select all images (N)** | Images | Selects every image in the dataset, across all pages. |
| **Unselect All** | Images | Clears the selection.  Shown when something is selected. |

## Tag an Image

You can create tags for images.  These tags can be used to filter out images of certain tags.  Tags can be added from the "Actions" dropdown and can be filtered using the "IMAGE TAGS" filter.

- Display tags: enable "Show Tags" under "Display Image Options".

{{ figure("../assets/datasets/image-options.png", "Image Options") }}

- Create new tags: click on the first line labeled "Click here to add a new tag".  Then press the ENTER key or click the accept button at the right side of the input field to create the tag.  If any image is selected, this tag will be automatically applied to those images.

{{ figure("../assets/datasets/add-tags.png", "Adding Tags") }}

- Edit existing tags: click on the pencil icon when hovering over a tag name.  Enter the new tag name and click the accept button at the right side of the input.

{{ figure("../assets/datasets/enter-tag-name.png", "Enter Tag Name") }}

- Delete existing tags: click on the (+) icon when hovering over a tag name.  A confirmation popup will open.  Confirming this will remove this tag from the dataset and all applied images.

{{ figure("../assets/datasets/remove-tag.png", "Remove Tag") }}

- Apply and revert tags: at least one image must be selected to apply or revert tags.  Click on any tag under the dropdown to select it.  Applied tags are denoted by a check icon.  To remove the applied tags, click on it again.

## Copy Selected Items

You can copy selected items to another dataset.  This operation can be found under the "Actions" dropdown.  The copy dialog will appear.

{{ figure("../assets/datasets/copy-selected-items.png", "Copy Selected Items") }}

1. Select the images to copy by using the checkbox for each image as shown.
2. Select "Copy Selected Images" from the "Actions" dropdown.
3. From the modal, source is auto-filled using the current dataset and first annotation set if applicable.  You can select a different source annotation set.
4. Destination will be defaulted to a new dataset along with any selected annotation set.  You can select another dataset and annotation if needed.
5. Selected file names that will be copied are shown under "Images".
6. Progress can be tracked on the [Tasks page](../tasks.md).

## Annotating from the Gallery

Click a sequence or image card to open the annotation editor.  A label must exist in the dataset before the drawing tools can be used.  Hover over any button to see its tooltip and hotkey.

{{ figure("../assets/datasets/editor-overview.jpg", "Annotation editor with callouts on the left toolbar, top ribbon, canvas, Annotations panel and zoom controls") }}

### Toolbar

The toolbar on the left of the canvas selects the tool.  Each tool has a hotkey shown in its tooltip.

| Tool | Hotkey | Description |
|---|---|---|
| **Pointer Tool** | `Q` | Select and edit annotations.  Hold `Ctrl` (`Cmd`) and click to select several. |
| **Point Tool** | `P` | Click to place the vertices of a polygon. |
| **Brush Tool** | `W` | Paint a segmentation mask. |
| **Eraser Tool** | `E` | Erase part of the selected mask. |
| **Box Tool** | `B` | Drag to create a 2D bounding box. |
| **Edit Label** | `L` | Click an annotation to change its label to the selected label. |
| **Increase / Decrease Cursor Size** | `=` / `-` | Resize the brush or eraser.  Shown while the brush or eraser is active. |
| **Key Frame Editing** | `K` | Sequences only.  See [Key Frames](../../3D/annotations/index.md#key-frames). |
| **AI Segment Tool** | `A` | Starts the [AGTG tool](#annotate-with-the-ai-segment-tool-agtg). |

### Ribbon

The ribbon above the canvas holds the actions for the current image.

| Button | Description |
|---|---|
| **Undo** | Reverts the last change.  Enabled when there are unsaved changes. |
| **Revert All Changes** | Discards all unsaved changes on the current image. |
| **Show Annotation Info** | Shows the details of the selected annotation. |
| **N selected** and **Join** | Shown when two or more annotations are selected.  **Join** merges them into the first selected annotation.  See [Objects and Annotation Cases](../../3D/annotations/cases.md#join-objects). |
| **Save Image Annotations** | Saves the changes on the current image (`Enter`).  Moving to another image or page discards unsaved changes. |

The canvas also provides **Download image**, the zoom percentage, **Zoom To Fit** and **Zoom To Selection** (`Z`).

### Objects and Annotations Panel

The **Annotations** panel on the left lists the objects in the frame.  An object has one label and can hold a 2D box, a segmentation polygon and a 3D box that all describe the same item.  Use the panel to select, hide, join or delete objects and their individual annotations.  See [Objects and Annotation Cases](../../3D/annotations/cases.md) for how annotations are tied to a unique object and how to resolve common cases.

For step-by-step tutorials, see [Dataset Annotations](../../datasets/tutorials/annotations/index.md).  For the properties of annotation sets, see [Annotation Sets](annotations.md).

## Annotate with the AI Segment Tool (AGTG)

The **AI Segment Tool** uses a cloud server running SAM2 to turn a few prompts on one frame into 2D boxes and masks for a whole sequence.  When LiDAR or Radar data is available, 3D boxes are generated as well.  The tool is available from the gallery editor.  For how the generation works, including the models and clustering used, see [Automatic Ground Truth Generation](../agtg.md) and [the AGTG algorithm](../agtg.md#the-agtg-algorithm).  The full walkthroughs are in the [2D](../../datasets/tutorials/annotations/automatic.md#2d-automatic-ground-truth-generation) and [3D](../../datasets/tutorials/annotations/automatic.md#3d-automatic-ground-truth-generation) tutorials.

### Workflow

1. Open a sequence from the gallery and make sure the dataset has the labels you need.
2. Click **AI Segment Tool** (`A`) on the toolbar.  If no server is running, a **Launch AGTG Server** dialog explains that a dedicated GPU server is started, that it incurs usage charges, and that it terminates after 15 minutes of inactivity.  Click **Launch AGTG Server**.  Initialization takes about 3 minutes and the progress is shown in the sidebar.
3. When the sidebar reports that the server is ready, add an object for each item to annotate and prompt it on the current frame.
4. For a sequence, set the end frame and click **Propagate**.
5. Review the result, then click **Save AIGT Annotations**.  The button is named AIGT in the interface.
6. When finished, shut the server down from the sidebar to stop usage charges.

{{ figure("../../datasets/assets/annotations/manual/confirm-agtg-server-launch.jpg", "The Launch AGTG Server confirmation dialog") }}

### Select Objects

The **1. Select Objects** section lists one card per object.  Each object has a label and its own prompts on the current frame.

{{ figure("../assets/datasets/agtg-select-objects.jpg", "Sidebar with an object selected and callouts on each prompt tool and button") }}

| Button | Description |
|---|---|
| **Add Object** (`N`) | Adds a new object card.  Choose its label from the drop-down on the card. |
| **Edit Object** | Selects an object card so that its prompts can be edited. |
| **SAM Hover and Click (Add)** | Left-click on the image to add a positive point inside the object.  Right-click to add a negative point on a region that should be excluded. |
| **SAM Hover and Click (Minus)** | Click to add negative points, which remove regions from the mask. |
| **SAM Box Tool** | Drag a box around the object to use it as the prompt. |
| **Select Existing Box** (`X`) | Click an existing 2D box to use it as the prompt.  The polygon is added to that box's object if it does not have one yet. |
| **Clear Object** | Clears the prompts of the selected object on the current frame. |
| **Remove Object** (x) | Removes the object card. |
| **Start Over** | Resets the prompts for the current frame. |

### Propagate

The **2. Propagate** section is shown for sequences.  It tracks the prompted objects to other frames.  The start frame is always the current frame, and a single propagation is limited to 500 frames.

{{ figure("../assets/datasets/agtg-propagate.jpg", "Propagate section showing Start Frame, End Frame, Reverse Propagate and the Propagate button") }}

| Control | Description |
|---|---|
| **Start Frame** | The current frame.  Read-only. |
| **End Frame** | The last frame to propagate to. |
| **Reverse Propagate** | Propagates backwards from the current frame instead of forwards. |
| **Propagate** | Starts tracking.  Requires at least one prompted object.  The button shows the progress while it runs. |
| **Stop Propagation** | Stops a running propagation. |

!!! tip
    If an object leaves the frame and later re-enters, it might not be tracked correctly.  Repeat the steps on a frame where it re-appears.

### AGTG Ribbon

While the AGTG tool is active the ribbon shows these buttons.

| Button | Description |
|---|---|
| **Clear Annotations** | Clears the unsaved AGTG annotations. |
| **Save AIGT Annotations** | Saves the pending AGTG annotations and edits on the frame, such as joined objects.  Unsaved results are lost if you change frames or leave the page. |

### AGTG Task and Server

The sidebar also shows an **AGTG Task** card with the status of the server.  Use its terminate option or **Shutdown AGTG Server** to stop the server.  The server stops by itself after 15 minutes of inactivity, but shut it down when you are done so that no credits are used unnecessarily.

!!! note
    To place the generated annotations on the right objects, or to fix annotations that ended up on separate objects, see [Objects and Annotation Cases](../../3D/annotations/cases.md).

## Keyboard Hotkeys

{% include-markdown "discrete/datasets/hot_keys.md" heading-offset=1 %}

## Next Steps

This page has described the features and context of the dataset gallery.  Proceed to the next section for learning more about [annotation sets](annotations.md).
