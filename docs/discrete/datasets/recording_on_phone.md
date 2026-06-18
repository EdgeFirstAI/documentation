!!! warning "Data Usage"
    It is recommended to use a phone connected to a Wi-Fi network. A device connected to mobile data might be subject to intense usage when uploading files; video files or image files can be large in size. In the examples below, the video file used was ~15MB and the image files were ~2MB each.

!!! warning "Limited Datasets"
    The example below uses a small video recording and only a handful of images. While this is sufficient for demonstrating the workflow, training a model on a limited dataset will typically result in poor performance when deployed in real-world conditions that differ from the training samples.

    To improve model robustness and generalization, it is recommended to collect training data across a variety of conditions, backgrounds, lighting environments, and object variations. As a general guideline, a minimum dataset size of approximately 1,000 images or video frames is recommended, although the optimal size depends on the complexity of the task.

!!! note "Device UI May Vary"
    The video and image capture screenshots shown in this guide were taken on a Samsung smartphone.
    Camera app layouts, button locations, labels, and available options may differ on other devices and operating system versions.
    For device-specific steps, refer to your phone manufacturer documentation or device manual.

# Record Video

Using a smartphone, try to record a 30 second or more video with the camera application showing various orientations of coffee cups.  Typically, the video recording can be started by pressing the red circular button. The video can be stopped by pressing the same button again.

{{ figure("/datasets/assets/capture/mobile-video-capture.jpg", "Mobile Video Capture") }}

# Capture Images

Furthermore, you can also capture individual images as shown below.  You can take image snapshots from the camera by pressing the white circular button.

{{ figure("/datasets/assets/capture/mobile-image-capture.jpg", "Mobile Image Capture") }}

!!! tip "Leveraging Videos"
    It is recommended to use videos rather than individual images.  This is because the [Automatic Ground Truth Generation (AGTG)](../../datasets/tutorials/annotations/automatic.md) feature leverages SAM-2 with tracking information which only needs a single annotation to annotate all frames.  However, individual images requires more effort by annotating each image separately.
