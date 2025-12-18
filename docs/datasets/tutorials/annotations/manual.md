# Manual Annotations

This page will describe the steps for manually adding annotations in the dataset.  Ideally, the dataset is mostly already [annotated via AGTG](automatic.md).  However, for any errors in the annotations that requires adjustments and corrections, the features described below will allow you to audit the annotations.

As mentioned, a dataset can have 2D and 3D annotations.  This page is split into tutorials for manually annotating 2D and 3D annotations.

{% include-markdown "discrete/datasets/manual_2d.md" %}

{% include-markdown "discrete/datasets/manual_3d.md" %}

## Video Tutorials

This is a high-level video tutorial showing adjustments to the 3D annotations.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=1536&end=2144" title="Visualize Annotations" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Next Steps

Once you have verified that your dataset has been properly annotated, you can now proceed to training your [Vision](../../../models/training/vision.md) or [Fusion](../../../models/training/fusion.md) model.

Otherwise, additional dataset tutorials are provided under [Dataset Management](../management.md).
