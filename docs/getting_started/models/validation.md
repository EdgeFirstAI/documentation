# Model Validation

EdgeFirst Studio supports validation of *Vision* models trained using ModelPack and *Fusion* models trained by fusing Camera and Radar sensors as model inputs.  The purpose of validation is to assess the performance of the model after training.  In this stage, analysis is usually practiced for finding the best model parameters to use for deploying the model or finding further refinements needed to the model prior to deployment which could require retraining with different parameters. 

## ModelPack

For validating *Vision* models tasked with detecting objects in an image, follow tutorials for [Validating ModelPack](../../models/modelpack/validation.md) in EdgeFirst Studio.  The validation metrics are distinguished between [Object Detection Metrics via Bounding Boxes](../../models/metrics.md#object-detection-metrics) and [Segmentation Metrics](../../models/metrics.md#segmentation-metrics).

## Fusion

For validating *Fusion* models tasked with detecting the position of the object in the field, follow tutorials for [Validating Fusion](../../models/fusion/validation.md) in EdgeFirst Studio.  The validation metrics for Fusion models are given as Precision, Recall, F1, and IoU.  EdgeFirst Studio also reports *Bird's Eye View Heatmaps* shown as the top down view of the model's field of view as a grid which describes the performance of the model's predictions at the individual cells.  The metrics for Fusion models are described in more detail under the [Fusion Metrics](../../models/metrics.md#fusion).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?si=PPmbJ1-8dZPLhGh2" title="EdgeFirst Validation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>