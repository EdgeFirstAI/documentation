# Dataset Capture
This page will provide tutorials for capturing and uploading datasets to EdgeFirst Studio.  At the bare minimum, datasets can be captured with any device with a camera such as a phone.  However, [EdgeFirst Platforms](../../platforms/index.md) such as a Maivin or a Raivin can also capture datasets for model training which can then be deployed back into the platform for model inference.  Datasets captured with a camera will [train Vision models](../../models/modelpack/training.md).  However, devices that are custom fitted with Radar or LiDAR modules such as a Raivin platform can capture datasets suited to [train Fusion models](../../models/fusion/training.md).

## Capture with a Phone
If you have a phone or any device with a camera with Wifi access, follow this tutorial to see how to capture and upload datasets into EdgeFirst Studio. 


## Capture with an EdgeFirst Platform
If you have an EdgeFirst Platform, follow this tutorial to see how to capture and upload datasets into EdgeFirst Studio.  Use your browser to connect to the Web UI of the remote device, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted with the Maivin [WebUI Main Page](../../platforms/walkthrough.md) page.

<figure markdown="span">
![WebUI Main Page](../../platforms/assets/ui-maivinMain.png){ align=center }
<figcaption>WebUI Main Page</figcaption>
</figure>

{% include-markdown "discrete/datasets/recording_mcap_on_device.md" heading-offset=2 %}
{% include-markdown "discrete/datasets/downloading_mcap_from_device.md" heading-offset=2 %}

### Video Tutorials
This tutorial provides high-level instructions for recording MCAPs using an [EdgeFirst Platform](../../platforms/index.md).  For in-depth documentation, please refer to the [MCAP Recording Service](../../platforms/recording.md).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/GVlkq9p0G5c" title="Dataset Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

This tutorial shows how to download recorded MCAPs.  
<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=0&end=558" title="Download Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

For more information on managing recordings, please see the [Managing Recordings Section](../../platforms/recording.md#managing-recordings).

## Next Steps
To upload the downloaded MCAPs into EdgeFirst Studio, follow the instructions for [uploading MCAPs](management.md#upload-mcaps).