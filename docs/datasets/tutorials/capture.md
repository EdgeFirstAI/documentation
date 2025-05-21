# Dataset Capture

This page will provide tutorials for capturing datasets.  Datasets can be captured using any device with a camera such as a phone.  However, these datasets will only train [Vision models](../../models/modelpack/index.md).  Datasets that were captured using a [Raivin Platform](../../platforms/index.md) with Radar or LiDAR modules can train [Fusion models](../../models/fusion/index.md).

## Record MCAPs 

This tutorial provides high-level instructions for recording MCAPs using an [EdgeFirst Platform](../../platforms/index.md).  For an in depth tutorial, please refer to the [MCAP Recording Service](../../platforms/recording.md).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/GVlkq9p0G5c" title="Dataset Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

On your browser, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted to the [Web UI Service](../../platforms/walkthrough.md) page.

<figure markdown="span">
![Web UI Service Page](../assets/webui-service-page.jpg){ align=center }
<figcaption>Web UI Service Page</figcaption>
</figure>

To record data, click on the "MCAP Recorder" service indicated in red above.  Once clicked, you will be greeted with the [MCAP Recording Service](../../platforms/walkthrough.md#the-mcap-recording-page) page.

<figure markdown="span">
![MCAP Recording Page](../assets/mcap-recording-page.jpg){ align=center }
<figcaption>MCAP Recording Page</figcaption>
</figure>

To start recording toggle/enable the *Recording* button indicated above and to stop the recording re-toggle/disable the same button. 

For more information on managing recordings, please see the [Managing Recordings Tutorial](../../platforms/recording.md#managing-recordings).

### Download Recorded MCAPs

This tutorial shows how to download recorded MCAPs.  For more information on downloading MCAPs, please see [Downloading and Analysis](../../platforms/recording.md#downloading-and-analysis).

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=0&end=558" title="Download Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

The MCAP files are listed under the list of MCAP files which can then be downloaded to your PC.

<figure markdown="span">
![Recorded MCAP](../assets/recorded-mcap.jpg){ align=center }
<figcaption>Recorded MCAP</figcaption>
</figure>

To upload the downloaded MCAPs into EdgeFirst Studio, follow the instructions for [uploading MCAPs](management.md#upload-mcaps).