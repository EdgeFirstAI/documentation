# Raivin Web UI Walkthrough

This article will walk you through the Raivin's Web User Interface (Web UI).

## The Main Page

The Main Page of the Raivin web interface should look as follows:

{{ figure("../../assets/setup/quickStart-mainPage.png", "Raivin Main Page") }}

There are five cards on the Main Page that link to the Visualization pages:

- **GPS**: This page displays a map with the current location of the device, along with GPS coordinates.
- **IMU**: This page displays the 3D orientation of the device with current pitch, yaw, and roll values.
- **Occupancy Grid**: This page will show the radar grid
- **Segmentation View**: This page shows the camera with running segmentation and/or detection pipeline.  For Raivin devices equipped with a radar module, it will also show the radar grid.
- **LiDAR View**: This page will show the LiDAR View, which will include the camera, radar grid, and LiDAR grid.

{% include-markdown "discrete/platforms/edgefirst_main_page_overview.md" heading-offset=2 %}

## The Visualization Pages

These pages contain the user-facing functionality of the vision module.

### The Segmentation Page

The Segmentation page shows camera overlain with the current visual model output.  For Raivin modules, this will also include the occupancy grid at the bottom.  

{{ figure("../../assets/setup/quickStart-segmentation.png", "Raivin Segmentation Page") }}

White points are unmatched, raw data from the radar; green points are raw data matched to segmentation masks.

### The Occupancy Page

The Occupancy Page shows the raw, radar data, colored by radar cross-section (RCS) size.  

{{ figure("../../assets/setup/quickStart-occupancy.png", "Occupancy Page") }}

{% include-markdown "discrete/platforms/edgefirst_common_services.md" heading-offset=2 %}

### The LiDAR View Page

This page shows the segmentation view, the occupancy grid, and the 3D LiDAR view.  The 3D LiDAR view will be blank if the device does not have a LiDAR unit connected.

{{ figure("../../assets/setup/quickStart-lidar.png", "LiDAR View Page") }}

## Next Steps

Now that you have setup your Raivin and are familiar with the Raivin's Web UI, you can proceed to [copying a public dataset](copy_dataset.md) in [EdgeFirst Studio][studio] to train your own vision model that will be deployed in this device.


[studio]: https://test.edgefirst.studio/