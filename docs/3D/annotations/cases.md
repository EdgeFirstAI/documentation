# Objects and Annotation Cases

An object in a frame can have more than one annotation.  For example, a car can have a 2D bounding box, a segmentation polygon and a 3D bounding box, all describing the same car.  EdgeFirst Studio groups these annotations under a single **object** so that they share the same label and are edited together. In addition, this format also maintains the structure established in the ["EdgeFirst Dataset"](../../datasets/format/schema.md) format where each object is represented as a single row and that individual columns to store the various annotation types exists.

This page explains how objects are organised in the annotation editor, how to attach annotations to an existing object, and how to resolve the common cases where annotations end up on separate objects.

## Objects and Annotation Types

An object has one label and at most one annotation of each type:

| Annotation Type | Description |
|---|---|
| 2D box | Bounding box in the image. |
| Polygon | Segmentation polygon or mask in the image. |
| 3D box | 3D bounding box in the point cloud. |

All objects in the current frame are listed in the **Annotations** panel on the left side of the annotation editor.

{{ figure("../assets/objects-panel.jpg", "Annotations panel with two objects listed, one object showing its label, type icons (2D box, polygon, 3D box), visibility toggle and delete icon") }}

Each row in the list represents one object and shows:

* A checkbox (edit mode) used to select objects for joining.
* The object label.
* An icon for each annotation type the object has.  Click an icon to expand the details for that annotation.
* A visibility toggle and, in edit mode, a **Delete Object** button.

Expanding an annotation type shows options to toggle its 2D projection, display its label, toggle its visibility and, in edit mode, delete that annotation only.

{{ figure("../assets/objects-panel-expanded.jpg", "One object row expanded to show the per-type options, including the 'Delete 3D Box' button") }}

!!! tip
    Press the `Down` or `Up` arrow keys to select the next or previous object.  The selected object is highlighted in the 2D and 3D canvases at the same time.

### Add or Replace an Annotation on an Object

To add an annotation to an existing object, or to redraw one of its annotations:

1. Select the object, either from the **Annotations** panel or by clicking it in the canvas.  Make sure only one object is selected.
2. Pick the tool for the annotation type: the box, point or brush tool in the 2D canvas, or the 3D box or clustering tool in the 3D canvas.
3. Draw the annotation.

If the object already has an annotation of that type, the new drawing **replaces** it.  Otherwise the annotation is added to the object.  When no object is selected, drawing creates a new object with the currently selected label.

!!! note
    The 2D box tool does not keep the new box selected after it is drawn, so the next box starts a new object.  Select the object again before drawing its next annotation.

### Delete an Annotation or an Object

* To delete a single annotation, expand the object in the **Annotations** panel and click the delete button for that type.  The other annotations on the object are kept.
* To delete the whole object, click **Delete Object**, or select it and press the `Delete` key.
* Deleting the last remaining annotation of an object deletes the object.

### Join Objects

Use **Join** to merge several objects into one:

1. In edit mode, check the objects to merge in the **Annotations** panel.  The first object you check is the one that is kept.
2. Click **Join (N)** in the panel title, or **JOIN** in the toolbar ribbon, where N is the number of checked objects.
3. The annotations of the other objects are moved onto the first object and the other objects are deleted.  If more than one object has a polygon, the polygons are combined.

{{ figure("../assets/join-objects.jpg", "Two objects checked in the Annotations panel with the 'Join (2)' button and the ribbon '2 selected / JOIN' button highlighted") }}

Click **Save Image Annotations** to save the result.

## Cases

### Redefine the 3D Box of an Object

The 3D box of an object is not in the right position and shaping it with the translate and scale tools is not practical.

1. Select the object in the **Annotations** panel.
2. Choose the Clustering Mode (`C`) in the 3D canvas and draw a box region around the cluster of interest.
3. The new box replaces the previous 3D box on the same object.  The label and the other annotations of the object are unchanged.

The 2D box and the polygon can be redrawn the same way with the object selected.

{{ figure("../assets/case-redraw-3d-box.jpg", " Object selected and a new 3D box drawn over the old one, showing the object keeping its 2D box and label") }}

### 3D Box Created as a Separate Object

The 2D box or polygon of a drone is on one object, but the 3D box of the same drone was created as another object, for example by clustering with nothing selected, or by Automatic Ground Truth Generation.  The Annotations panel lists two objects for one drone.

1. Check both objects in the **Annotations** panel.  Check the object you want to keep first, as the other object is merged into it.
2. Click **Join (2)**.
3. The first object now has the 2D box, polygon and 3D box, and the second object is removed.

{{ figure("../assets/join-objects.jpg", "Joining two objects in the list into one object showing the 2D box, polygon and 3D box icons") }}

### Join Fails with Multiple Boxes

Joining objects that both have a 2D box, or both have a 3D box, is not allowed because an object can only have one of each.  Studio shows the error **Cannot join multiple 2D / 3D boxes**.

{{ figure("../assets/case-join-error.jpg", "The 'Cannot join multiple 2D / 3D boxes' error message shown after clicking Join") }}

To resolve this:

1. Expand the object whose box you do not want to keep.
2. Click the delete button for that annotation type (for example, **Delete 3D Box**).
3. Check both objects again and click **Join**.

### Create an Object Manually When SAM Fails

When SAM does not produce a usable segmentation, build the object by hand:

1. Select the label for the object.
2. In the 2D canvas, draw the 2D box with the box tool (`B`).  This creates the object.
3. Select the new object in the **Annotations** panel.
4. Draw the polygon with the point tool (`P`) to click the outline, or with the brush tool (`W`) to paint the mask.  The polygon is added to the same object.
5. Select the object again if needed, switch to the 3D canvas and add the 3D box with the [clustering tool (preferred)](3d_annotations.md#cluster-3d-annotation) (`C`) or the 3D box tool (`B`).  The 3D box is added to the same object.
6. Click **Save Image Annotations** to save.

If the 3D box was drawn with no object selected, it is a separate object.  Use [Join](#join-objects) to merge it.

{{ figure("../assets/case-manual-objects.jpg", "Final result: one object in the Annotations panel with the 2D box, polygon and 3D box icons, shown in both the 2D and 3D canvases") }}

For the full list of shortcuts used in these steps, see [3D Keyboard Hotkeys](hotkeys.md).
