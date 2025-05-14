# Model Training

EdgeFirst Studio supports training of *Vision* models using ModelPack tasked for image object detection.  EdgeFirst Studio also supports training of "Fusion" models tasked for detecting the object's position in the field.  In this stage, we use annotated datasets with 2D annotations (segmentation masks and 2D bounding boxes) for training ModelPack or 3D annotations (3D bounding boxes) for training Fusion. 

## ModelPack

For training *Vision* models tasked with detecting objects in an image, follow tutorials for [Training ModelPack](../../models/modelpack/training.md).  EdgeFirst Studio supports *Vision* models tasked with performing object detection via bounding boxes, segmentation masks, or multi-task (bounding boxes and segmentation masks).

## Fusion

For training *Spatial Perception Models* tasked with detecting the position of the object in the field, follow tutorials for [Training Fusion](../../models/fusion/training.md).  EdgeFirst Studio trains these models by fusing sensor outputs (Camera or Radar) as model inputs. These models are better known as *Fusion* models.  EdgeFirst Studio provides options for toggling these sensors on/off at the start of training.  However, by default training uses both the Camera and the Radar outputs.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4" title="EdgeFirst Training" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
