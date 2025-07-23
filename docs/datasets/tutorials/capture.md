# Dataset Capture
This page will provide tutorials for capturing datasets.  Datasets can be captured using any device with a camera such as a phone.  However, these datasets will only train [Vision models](../../models/modelpack/index.md).  Datasets that were captured using a [Raivin Platform](../../platforms/index.md) with Radar or LiDAR modules can train [Fusion models](../../models/fusion/index.md).

## Remote Device Web Interface
Use your browser to connect to the Web UI of the remote device, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted with the Maivin [WebUI Main Page](../../platforms/walkthrough.md) page.

<figure markdown="span">
![WebUI Main Page](../../platforms/assets/ui-maivinMain.png){ align=center }
<figcaption>WebUI Main Page</figcaption>
</figure>

{% include-markdown "discrete/recording_mcap_on_device.md" %}
{% include-markdown "discrete/downloading_mcap_from_device.md" %}

## Video Tutorials
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