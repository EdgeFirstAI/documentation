# Validation

EdgeFirst Studio supports validation of *Vision* models trained using ModelPack and *Fusion* models trained by fusing Camera and Radar sensors as model inputs.  The purpose of validation is to assess the performance of the model after training.  During validation, the model outputs can be compared against the ground truth.  After validation, the overall performance of the model is best summarized based on the validation metrics. 

There are two types of validation: **managed** and **user-managed**.  Managed validations are set to default in EdgeFirst Studio which triggers an EC2 instance that downloads the dataset and the inference model for validation.  This type of validation is best used if you do not have an embedded platform to deploy the model.  User-managed validations are hosted in embedded platforms where the dataset and the inference model will be downloaded.  This type of validation is best used if you have an embedded platform available to verify how the model would perform in the platform and determine the model's inference time when deployed.  The instructions for these types of validation will be listed below. 

## ModelPack

For validating *Vision* models tasked with detecting objects in an image, follow tutorials for [managed](../modelpack/validation/managed.md) and [user-managed](../modelpack/validation/user_managed.md) validation in EdgeFirst Studio.  The validation metrics are distinguished between [Detection Metrics](../metrics/detection.md) and [Segmentation Metrics](../metrics/segmentation.md).

## Fusion

For validating *Fusion* models tasked with predicting the object's position in the field, follow tutorials for [managed](../fusion/validation.md) and user-managed (*coming soon*) validation in EdgeFirst Studio.  The validation metrics for Fusion models are given as Precision, Recall, F1, and IoU.  EdgeFirst Studio also reports *Bird's Eye View Heatmaps* shown as the top down view of the model's field of view as a grid which describes the performance of the model's predictions at the individual cells.  The metrics for Fusion models are described in more detail under the [Fusion Metrics](../metrics/fusion.md).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?si=PPmbJ1-8dZPLhGh2" title="EdgeFirst Validation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>