# Raivin Web UI Walkthrough

This article will walk you through the Raivin's Web User Interface (Web UI).  The Web UI is served by the `websrv` service on the device over HTTP and HTTPS and is reached at `https://verdin-imx8mp-XXXXXXXX.local` where the eight digits are the device serial number.

## The Main Page

The Main Page of the Raivin web interface should look as follows:

{{ figure("../../assets/setup/quickStart-mainPage.png", "Raivin Main Page") }}

The Main Page shows one card for each running visualization.  Cards only appear while their service is running, so a Raivin with the radar publisher enabled shows the following cards:

- **Camera**: This page shows the live camera video with optional detection and segmentation overlays from the model service and, for LiDAR equipped devices, the projected LiDAR points.
- **Radar**: This page shows the radar point cloud over a polar occupancy grid.
- **LiDAR**: This page shows the 3D LiDAR point cloud, it appears when the LiDAR publisher is running.
- **IMU**: This page displays the 3D orientation of the device with current roll, pitch, and yaw values.
- **GPS**: This page displays a map with the current location of the device, along with GPS coordinates.

{% include-markdown "discrete/platforms/edgefirst_main_page_overview.md" heading-offset=2 %}

## The Visualization Pages

These pages contain the user-facing functionality of the vision module.

### The Camera Page

The Camera page shows the live camera video decoded from the `camera/h264` topic.  The controls at the top of the page toggle the segmentation overlay, which draws the detection boxes and segmentation masks published by the model service on `model/output` over the video, and the LiDAR overlay which projects the LiDAR points onto the image colored by distance, cluster, or the classes assigned by the fusion service.

{{ figure("../../assets/setup/quickStart-segmentation.png", "Raivin Camera Page") }}

### The Radar Page

The Radar page shows the radar point cloud on a polar grid spanning 140 degrees in front of the device with range rings every two meters.  The Source dropdown selects between the raw radar targets, the radar clusters, and the fusion radar output.  The Color dropdown colors the points by speed, power, radar cross-section (RCS), cluster, vision class, track ID, or instance ID depending on the fields carried by the selected stream, and the Elevation toggle lifts the points off the grid plane by their height.  A "Radar Unavailable" overlay is shown when the selected stream is not publishing.

{{ figure("../../assets/setup/quickStart-occupancy.png", "Radar Page") }}

{% include-markdown "discrete/platforms/edgefirst_common_services.md" heading-offset=2 %}

### The LiDAR Page

This page shows the 3D LiDAR point cloud from the `lidar/points` topic with the same Source, Color, and Elevation controls as the Radar page, including coloring by the vision classes from the fusion service.  The page is available when the LiDAR publisher is running.

{{ figure("../../assets/setup/quickStart-lidar.png", "LiDAR Page") }}

## Next Steps

Now that you have set up your Raivin and are familiar with the Raivin's Web UI, you can proceed to [copying a public dataset](copy_dataset.md) in {{ studio_link("EdgeFirst Studio") }} to train your own vision model that will be deployed in this device.
