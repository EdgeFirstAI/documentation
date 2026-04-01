# Annotation Sets

This page will describe the context of the annotation sets.  For tutorials on annotating datasets please refer to the [Dataset Annotations](../../datasets/tutorials/annotations/index.md) sections.  Each dataset can have multiple annotations sets. An annotation set is a container for storing the annotations in the dataset. Each annotation set contains annotations from a different source (i.e. different annotation teams, or inferences from models).

## Annotation Set Operation

For these operations please refer to the following figure.

{{ figure("../assets/datasets/annotationset-attributes.jpg", "Auditing Tasks") }}

- Click on the add annotation set button (+) to add an annotation set.
- Each annotation set has an (x) button to delete the annotation set - all associated annotations will also be deleted.  Please note that deleted annotation sets goes the the Recycle Bin and can either be restored or permanently deleted.  The storage is only freed when the Recycling Bin is cleared.  
- Each annotation set has an (i) button to get/set the details of the annotation set.

## Editing 2D Annotations

There are two modes of operations:

1. Edit Annotations from the Auditing Tasks Board.
2. Edit Annotations from the Gallery

## Auditing Tasks Board

EdgeFirst Studio allows multiple users to remotely access a single dataset and annotation set and make changes without interfering with each other. Users can navigate to this page using the Apps Menu.

{{ figure("../assets/datasets/auditing-tasks.png", "Auditing Tasks") }}

Labelling is the process of creating new annotations whereas auditing is the process of reviewing annotations to potentially make any changes to correct any errors in the annotations.

User reviews annotations in the reference annotation set:

- Accepted annotations move to the target annotation set.  
- Rejected annotation are not copied to the target annotation set.
- Edited annotations are copied with edits to the target annotation set.

Create a new task in the Auditing Task Board.

{{ figure("../assets/datasets/create-task.png", "The Task") }}

- Enter the task name and description.
- Select a dataset from the current project you want to work on.
- Select target annotation set.  If "New annotation set" is selected then the result will be stored here.
- If "Audit" type is selected.  A reference annotation set is required.  You will be performing audits on annotations from this set.

Task entry is created in the Task board. There are three columns:

1. Open - Created but no work has started.
2. In Progress - Some images have been worked on - the remaining images are shown.
3. Completed - All images have been worked on.

{{ figure("../assets/datasets/task-board.png", "Task Board") }}

Click on any task entry and start editing. The editing process is described below.

## Edit images from gallery

The tutorials for annotating images from the gallery is provided in the [Dataset Annotations](../../datasets/tutorials/annotations/index.md) sections.

1. Open the dataset [gallery](gallery.md)
2. Click on an image.

{{ figure("../assets/datasets/edit-options.png", "Edit Options") }}

### Add a Bounding Box

1. Click on a label from Labels section – all boxes drawn will be of this class.
2. Click on the Detection Bounding Box Mode (or press b).
3. Click and drag on image to draw as many rectangular bounding boxes.
4. Select any other class and add boxes for that class.
5. Click on "SAVE ANNOTATIONS" to finalize the annotations.

### Add a Polygon Annotation with Vertices

1. Click on a label from Labels section – all polygons drawn will be of this class.
2. Click on the Segmentation Vertex Mode (or press p).
3. Continuously click on image to draw as many vertices of the polygon as required.
4. Select any other class and polygons for that class.
5. Select Pointer mode (q) to edit any vertices.
6. Click on "SAVE ANNOTATIONS" to finalize the annotations.

### Add a Polygon Annotation with Brush

1. Click on a label from Labels section – all polygons drawn will be of this class.
2. Click on the Segmentation Brush Mode (or press w).
3. Hold mouse down on image to draw the polygon as required.
4. Select any other class and add polygons for that class.
5. Select Pointer mode (q) to edit any vertex.
6. Select Segmentation Eraser mode (e) to erase parts of the polygon.
7. NOTE: Only the polygon selected (using pointer tool) will be erased.
8. Use [+] and [-] buttons to make the brush/eraser larger or smaller.
9. Click on "SAVE ANNOTATIONS" to finalize the annotations.

### Change Class Label of an Annotation

1. Click on a label from Labels section – all annotations clicked will be of this class.
3. Click on the Change Label Mode (or press l).
4. Click on any annotation to change its class to the selected class.

### Edit Images from the Auditing Task Board

Go to the Auditing Tasks board.

{{ figure("../assets/datasets/auditing-tasks.png", "Audit Annotations") }}

Create a new task or continue an existing task.

#### Label

Add, delete, or edit annotations in one annotation set in the target annotation set and save changes in the same annotation set.

#### Audit

Review annotations in the reference annotation set then approve, reject, or edit annotation and place changes in a reference annotation set.

There are two auditing modes:

1. Image-Based Audit
2. Annotation-Based Audit

{{ figure("../assets/datasets/task.png", "Start Auditing") }}

### Image-Based Audit

Clicking on the task takes you directly to the image mode auditing.  All the editing is the same as described in the [Gallery-Based Editing](#edit-images-from-gallery) above.

Users can switch between Image-based and Annotation-Based Audit from the top header.

{{ figure("../assets/datasets/audit-tool-type.png", "Audit Tool Type") }}

### Annotation-Based Audit

In this mode only one annotation is shown at a time.  The user can edit with single click and the next annotation is automatically presented.  Hot keys are provided to speed up the process:

1. (ENTER) – accept annotation.
2. (SPACE) – reject annotation.
3. (<--) Go to previous annotation – no change to the current annotation.
4. (-->) Go to next annotation – no change to the current annotation.
5. (Z) – Toggle zoom to annotation view and full image.
6. (1-9) - change the annotation class from 1 to 9.
7. (SHIFT 0-9) - change the annotation class from 10 to 19.

Users can edit the size of the annotation by mouse click and drag.

## Next Steps

This page has described the features and contexts of annotations sets and making any changes to the annotations.  For more tutorials on annotating datasets, visit the [Dataset Annotations](../../datasets/tutorials/annotations/index.md) section.  Otherwise, proceed to the [Model Experiments Dashboard](../models.md) to learn more about the context of model training and validation.
