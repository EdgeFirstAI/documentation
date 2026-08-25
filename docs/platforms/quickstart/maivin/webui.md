# Maivin Web UI Walkthrough

This article will walk you through the Maivin's Web User Interface (Web UI).

## The Main Page

The Main Page of the Maivin web interface should look as follows:

{{ figure("../../assets/setup/ui-maivinMain.png", "Maivin Main Page") }}

There are three cards on the Main Page that link to the Visualization pages:

- **GPS**: This page displays a map with the current location of the device, along with GPS coordinates.
- **IMU**: This page displays the 3D orientation of the device with current roll, pitch, and yaw values.
- **Segmentation View**: This page shows the camera with running segmentation and/or detection pipeline.

{% include-markdown "discrete/platforms/edgefirst_main_page_overview.md" heading-offset=2 %}

## The Visualization Pages

These pages contain the user-facing functionality of the vision module.

### The Segmentation Page

The Segmentation page shows camera overlain with the current visual model output.

{{ figure("../../assets/setup/ui-maivinSegmentation.jpg", "Maivin Segmentation Page") }}

{% include-markdown "discrete/platforms/edgefirst_common_services.md" heading-offset=2 %}

## Next Steps

Now that you have set up your Maivin and are familiar with the Maivin's Web UI, you can proceed to [copying a public dataset](copy_dataset.md) in {{ studio_link("EdgeFirst Studio") }} to train your own vision model that will be deployed in this device.
