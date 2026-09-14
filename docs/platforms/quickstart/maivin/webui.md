# Maivin Web UI Walkthrough

This article will walk you through the Maivin's Web User Interface (Web UI).  The Web UI is served by the `websrv` service on the device over HTTP and HTTPS and is reached at `https://verdin-imx8mp-XXXXXXXX.local` where the eight digits are the device serial number.

## The Main Page

The Main Page of the Maivin web interface should look as follows:

{{ figure("../../assets/setup/ui-maivinMain.png", "Maivin Main Page") }}

The Main Page shows one card for each running visualization.  Cards only appear while their service is running, so a stock Maivin shows the following three cards:

- **Camera**: This page shows the live camera video with optional detection and segmentation overlays from the model service.
- **IMU**: This page displays the 3D orientation of the device with current roll, pitch, and yaw values.
- **GPS**: This page displays a map with the current location of the device, along with GPS coordinates.

The **LiDAR** and **Radar** cards described in the [Raivin Web UI Walkthrough](../raivin/webui.md) appear when the LiDAR or radar publisher services are running.

{% include-markdown "discrete/platforms/edgefirst_main_page_overview.md" heading-offset=2 %}

## The Visualization Pages

These pages contain the user-facing functionality of the vision module.

### The Camera Page

The Camera page shows the live camera video decoded from the `camera/h264` topic.  The controls at the top of the page toggle the segmentation overlay, which draws the detection boxes and segmentation masks published by the model service on `model/output` over the video, and the LiDAR overlay for devices with a LiDAR sensor.  A statistics panel reports the model latency and throughput.

{{ figure("../../assets/setup/quickStart-segmentation.png", "Maivin Camera Page") }}

!!! note

    The overlay state is not persisted across page refreshes and enabling the overlays can stutter the live video with segmentation models, refer to the [Known Issues](../../software/issues.md).

{% include-markdown "discrete/platforms/edgefirst_common_services.md" heading-offset=2 %}

## Next Steps

Now that you have set up your Maivin and are familiar with the Maivin's Web UI, you can proceed to [copying a public dataset](copy_dataset.md) in {{ studio_link("EdgeFirst Studio") }} to train your own vision model that will be deployed in this device.
