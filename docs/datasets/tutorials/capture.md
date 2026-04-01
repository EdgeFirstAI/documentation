# Dataset Capture

This page has tutorials for capturing or collecting samples for datasets and then uploading the samples into EdgeFirst Studio for [annotation](annotations/index.md).  At the bare minimum, datasets can be captured with any device with a camera such as a phone.  However, [EdgeFirst Platforms](../../platforms/index.md) such as a Maivin or a Raivin can also capture dataset samples for model training which can then be deployed back into the platform for model inference.  Image samples will [train Vision models](../../models/training/vision.md).  However, devices that are custom fitted with Radar or LiDAR modules such as a Raivin platform can capture dataset samples suited to [train Fusion models](../../models/training/fusion.md).

## Capture with a Phone

If you have a phone or any device with a camera with Wifi access, follow this tutorial to see how to capture and upload datasets into EdgeFirst Studio.

{% include-markdown "discrete/datasets/recording_on_phone.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/create_dataset_container.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/uploading_video_to_studio.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/uploading_images_to_studio.md" heading-offset=2 %}

In this tutorial you have seen how to capture videos and images from your mobile phone and upload the videos and images into EdgeFirst Studio. Proceed to the [Next Steps](#next-steps) to see what's next in your dataset creation.

## Capture with an EdgeFirst Platform

If you have an EdgeFirst Platform, follow this tutorial to see how to capture and upload datasets into EdgeFirst Studio.  Use your browser to connect to the Web UI of the remote device, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted with the Maivin [Web UI Main Page](../../platforms/quickstart/maivin/webui.md) page.

{{ figure("../../platforms/assets/setup/ui-maivinMain.png", "Web UI Main Page") }}

{% include-markdown "discrete/datasets/recording_mcap_on_device.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/downloading_mcap_from_device.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/uploading_mcap_to_studio.md" heading-offset=2 %}

In this tutorial you have seen how to record MCAPs using an EdgeFirst Platform and downloaded and uploaded the MCAP recording into EdgeFirst Studio. Proceed to the [Next Steps](#next-steps) to see what's next in your dataset creation.

### Video Tutorials

This video tutorial provides high-level instructions for recording MCAPs using an [EdgeFirst Platform](../../platforms/index.md).  For in-depth documentation, please refer to the [MCAP Recording Service](../../perception/data_collection/recording.md).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/GVlkq9p0G5c" title="Dataset Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

This video tutorial shows how to download recorded MCAPs.  
<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=0&end=558" title="Download Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

This video tutorial shows how to upload recorded MCAPs into EdgeFirst Studio.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=558&end=720" title="Upload MCAP" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

For more information on managing recordings, please see the [Managing Recordings Section](../../perception/data_collection/recording.md#managing-recordings).

## Next Steps

See the imported files by viewing the [dataset gallery](management.md#view-dataset).

EdgeFirst Studio also supports [import of existing datasets](import.md) and its annotations with various formats.

For auto-annotating datasets, see the [Automatic Ground Truth Generation (AGTG)](annotations/automatic.md). Otherwise, you can perform [manual annotations](annotations/manual.md) which is typically used to correct errors or make some adjustments in the annotations.
