# Dataset Annotations

This page will provide tutorials for annotating datasets in EdgeFirst Studio.  As described in the [EdgeFirst Dataset Format](../format.md), a dataset can have 2D and 3D annotations.  Shown below is an example of 2D annotations (left) and 3D annotations (right).  A 2D annotation is a combination of 2D bounding boxes and segmentation masks for any given object that are semantic pixel-based image coordinates.  A 3D annotation is a 3D bounding box surrounding the object in real world coordinates (meters).

<figure markdown="span">
![Sample Annotations](../assets/sample-studio-annotations.jpg){ align=center }
<figcaption>Sample Annotations</figcaption>
</figure>

To reduce the effort required during the annotation process, EdgeFirst Studio provides the tools to auto annotate either a single image or a sequential set of frames in a dataset by leveraging SAM-2 auto-segment and tracking capabilities.  The following sections will describe this auto-annotation feature.  Please note that it is not always guaranteed that the auto-annotations will yeild 100% accuracy, so EdgeFirst Studio provides the tools to audit the existing annotations to correct any mistaked which will be described in the audit sections below.

## Dataset Labels

Each annotation has a label associated to it.  The label identifies the object that is being annotated.  For example, a dataset containing coffee cups contains multiple, but varying objects of coffee cups, but tagged with a single label given as "Coffee Cup".

<figure markdown="span">
![Sample Coffee Cups](../assets/coffee-cups-annotations.jpg){ align=center }
<figcaption>Sample Coffee Cups</figcaption>
</figure>

### Edit Label

EdgeFirst Studio provides features for updating the labels in the dataset.  To update the label "Coffee Cup" to "coffeecup", click on the button with a pencil icon under "Labels" on the dataset card.

<figure markdown="span">
![Edit Labels](../assets/edit-labels.jpg){ align=center }
<figcaption>Edit Labels</figcaption>
</figure>

This will bring the option to edit the label, the color associated to the label, and the index.  The index controls the label order which is relevant in multi-class datasets (more than one label).  The first label is given the index 0.  Since this dataset only has one label, its index is 0.  Here the label color was modified to blue and the label was modified to "coffeecup".

<figure markdown="span">
![Edited Label](../assets/edited-label.jpg){ align=center }
<figcaption>Edited Label</figcaption>
</figure>

The changes should now be reflected in the gallery as shown below.

<figure markdown="span">
![Edited Sample Coffee Cups](../assets/coffee-cups-annotations-edited.jpg){ align=center }
<figcaption>Edited Sample Coffee Cups</figcaption>
</figure>

### Add Label

To add a new label, click on the button with a pencil icon under "Labels" on the dataset card.

<figure markdown="span">
![Edit Labels](../assets/edit-labels.jpg){ align=center }
<figcaption>Edit Labels</figcaption>
</figure>

This will bring the option to edit the labels.  Click on the "+" button on the top right and this will add a new label as shown below.  By default it will show as "NewLabel" with no color associated to it.  

<figure markdown="span">
![Add Label](../assets/add-new-label-via-pencil.jpg){ align=center }
<figcaption>Add Label</figcaption>
</figure>

You can follow the steps shown for [editing the label](#edit-label) to modify the label from "NewLabel" to something else like "plate" with color green as shown below.

<figure markdown="span">
![Added Label](../assets/new-plate-label.jpg){ align=center }
<figcaption>Added Label</figcaption>
</figure>

**Alternatively**, you can also add multiple labels by clicking the button with the "+" icon next to the "Labels" on the dataset card.  This will bring the option for adding comma separated labels. 

<figure markdown="span">
![Add Label Multiple](../assets/add-multiple-labels.jpg){ align=center }
<figcaption>Add Multiple Labels</figcaption>
</figure>

When a new label is added, this allows you to create new annotations with this label as shown in the dropdown in the gallery.

<figure markdown="span">
![Added Plate Label in Gallery](../assets/plate-label-added.jpg){ align=center }
<figcaption>Added Plate Label in Gallery</figcaption>
</figure>

### Remove Label

To remove a label, click on the button with a pencil icon under "Labels" on the dataset card.

<figure markdown="span">
![Edit Labels](../assets/edit-labels.jpg){ align=center }
<figcaption>Edit Labels</figcaption>
</figure>

This will show the list of existing labels.  Click on the "x" button shown on the right of the label when hovering over it.  This will delete the label from the list along with the annotations with this label. 

<figure markdown="span">
![Added Label](../assets/delete-plate-label.jpg){ align=center }
<figcaption>Added Label</figcaption>
</figure>

## Auto Annotations via Gallery

This is a combination of manual and AI assisted workflows.

### AI Assisted Annotation

This feature allows users to annotate 2D,3D or 2D segments with just a 2D box prompt. For details of this workflow please refer to [AI Assisted Annotation](../../studio/agtg.md).

### Manual Annotation

THis feature allows user to annotate 2D,3D boxes and 2D annotations manually. It also allows user to edit the annotations create by AI assisted annotation workflow.

Go the the Dataset Gallery page and click on the image to edit. This will open the image in view / edit made.
Select the annotation ste to edit from the left panel (shown in red box). 

#### ADD 2D Box

1. Click on the box annotation in 2D editing panel (shown in red box)
2. Using mouse, drag on image to create box annotation.
3. Make multiple boxes - one for each annotation.
4. Make sure to change the label type on the left panel if the next label belongs to a different class. 

![alt text](../assets/manual_ann_1.png){: style="height:300px;align=center; "}

#### Deleting 2D Box

1. Click on the Pointer in 2D editing panel (shown in red box)
2. Using mouse, click inside the annotation box to delete. This will highlight the box (as shown in image).
3. Press delete button on the keyboard to delete the box.

![alt text](../assets/manual_ann_2.png){: style="height:300px;align=center; "}


#### Editing 2D Box

1. Click on the Pointer in 2D editing panel (shown in red box).
2. Using mouse, click inside the annotation box to edit. This will highlight the box (as shown in image).
3. Drag the anchor points on the box to resize it.
4. Click and drag the box to move the box

![alt text](../assets/manual_ann_2.png){: style="height:300px;align=center; "}

#### Changing Object label of a 2D Box

1. Click on the label mode in 2D editing panel(shown in red box).
2. Select the label in the left panel (shown in red box).
3. Click on any annotation box to change its label.

![alt text](../assets/manual_ann_3.png){: style="height:300px;align=center; "}


#### ADD 3D Box

1. If there are no 3D annotation in the annotation set, then first add 3D 3D Bounding Box topic. Click on '+' icon (shown in red box) and select 3D Bounding Box.

![alt text](../assets/manual_ann_4.png){: style="height:200px;align=center; "}

2. Open the 3D View Panel by clicking on the "eye" icon for the 3D Bounding box.
3. Click on the box annotation in 3D editing panel (shown in red box).
4. Using mouse, Click on the 3D viewing panel. This will make a 3D bounding box.
5. Make multiple boxes - one for each annotation.
6. Make sure to change the label type on the left panel if the next label belongs to a different class. 

![alt text](../assets/manual_ann_3d.png)


#### Deleting 3D Box

1. Click on the Pointer in 3D editing panel(shown in red box).
2. Using mouse, click inside the annotation box to delete. This will highlight the box (as shown in image).
3. Press delete button on the keyboard to delete the box.

![alt text](../assets/manual_ann_3d_del.png)

#### Editing 3D Box

*Resizing a 3D box*

1. Click on the Scaling in 3D editing panel (shown in red box)
2. Using mouse, click inside the annotation box to edit. This will highlight the box (as shown in image).
3. Drag the anchor points on the box to resize it in x,y,z direct or in xy,yx,zx planes.

![alt text](../assets/manual_ann_3d_size.png){: style="height:200px;align=center; "}


*Moving a 3D box*

1. Click on the Scaling in 3D editing panel (shown in red box)
2. Using mouse, click inside the annotation box to edit. This will highlight the box (as shown in image).
3. Drag the anchor points on the box to move it in z,y, or z direction.

![alt text](../assets/manual_ann_3d_move.png){: style="height:200px;align=center; "}

#### Changing Object label of a 3D Box

1. Click on the label mode in 3D editing panel(shown in red box)
2. Select the label in the left panel (shown in red box)
3. Click on any annotation box to change its label.

![alt text](../assets/manual_ann_3d_label.png){: style="height:200px;align=center; "}









#### Saving Edited annotations

Click on the SAVE ANNOTATIONS button to save the edit, delete or create annotations for this image. Moving to any other image or going to another page will discard the changes.  
