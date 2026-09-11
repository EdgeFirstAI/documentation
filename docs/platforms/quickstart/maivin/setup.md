# Maivin Setup Guide

This article will walk you through the Maivin hardware setup and then lead you to resources for using additional features.

## Unboxing

The Maivin box contains the following items:

- The Maivin vision module
- A five-meter power cable, M12 circular connector (male) to 2.1mm x5.5mm barrel adapter (female)
- Box with power adapters
    - Power-adapter with interchangeable plugs.  2.1mm x 5.5mm barrel adapter (male) connector.
    - Interchangeable plugs for the following regions:
        - NEMA 1-15P (Type A) (North America)
        - CEE-7/16 Alternative II "Europlug" (Type C) (Europe)
        - AS/NZS 3112, ungrounded (Type I) (Australia / Oceania)
        - BS 1363 (Type B) (British) wall adapter
- Desktop tripod

{% include-markdown "discrete/platforms/edgefirst_device_connections.md" %}

{% include-markdown "discrete/platforms/edgefirst_device_bootup.md" %}

After all that, you should see the [Maivin Main Page](webui.md).

{{ figure("../../assets/setup/ui-maivinMain.png", "Maivin Main Page") }}

From here, we recommend that you check out the Camera page by clicking the "Camera" card, then enable the segmentation overlay from the page controls to see the detections of the default model drawn over the live video.

{{ figure("../../assets/setup/quickStart-segmentation.png", "Maivin Camera Page") }}

{% include-markdown "discrete/platforms/edgefirst_performance_scaling.md" %}

## Next Steps

Now that you have completed these initial steps, we recommend that you read the following walkthroughs:  

- [Maivin Web UI Walkthrough](webui.md), to see what each UI card on the splash screen does  
- [SSH Walkthrough](../../networking/ssh.md), to learn how to SSH into your Maivin and basic command-line operations  
- [Maivin Recording Walkthrough](../../../perception/data_collection/recording.md), to learn how to record datasets and download them to your PC  
- [Model Upload Walkthrough](../../software/model_uploads.md), to learn how to upload vision models to your Maivin  
- [Software Updates](../../software/updates.md), to keep your Maivin on the latest release  
