# Uploading Models

This walkthrough describes how to upload new 2D vision models and radar-vision fusion models to the Raivin.  

!!! note "Maivin Instructions"

    The examples below are based on a Raivin platform, however, the same instructions can be applied to a Maivin platform for uploading 2D vision models only.

## Getting New Models

You can [train models using EdgeFirst Studio](../../models/index.md), both [Vision models](../../models/training/vision.md) and [Fusion Radar models](../../models/training/fusion.md).  Once the models are trained, they can be downloaded from their respective, completed training sessions.  The Model service accepts quantized TFLite models with the EdgeFirst configuration embedded, which is how EdgeFirst Studio exports [ModelPack](../../models/modelpack/index.md) and [Ultralytics](../../models/ultralytics/index.md) models for the i.MX 8M Plus.

The models shipped with the device are installed under `/usr/share/edgefirst/modelzoo/` for the vision model and `/usr/share/edgefirst/fusion/` for the RadarExp fusion models.  These directories are part of the read-only operating system image, uploaded models are stored under the `torizon` user home directory instead.

{% include-markdown "discrete/platforms/upload_models.md" %}
{% include-markdown "discrete/platforms/deploy_model_service.md" %}
{% include-markdown "discrete/platforms/deploy_fusion_service.md" %}

## Summary

At this point, the new models should be uploaded to the Raivin and you should be able to see the outputs on the [Camera page](../quickstart/raivin/webui.md#the-camera-page) with the segmentation overlay enabled and, for fusion models, on the [Radar page](../quickstart/raivin/webui.md#the-radar-page).
