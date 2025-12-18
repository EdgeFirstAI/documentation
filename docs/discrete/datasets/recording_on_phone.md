!!! warning "Data Usage"
    It is recommended to use a phone connected to a Wifi network. A device connected to mobile data might be subject to intense usage when uploading files; video files or image files can be large in size. In the examples below, the video file used was ~15MB and the image files were ~2MB each.

# Record Video

Using a smartphone, try to record a 30 second or more video with the camera application showing various orientations of coffee cups.  Typically, the video recording can be started by pressing the red circular button. The video can be stopped by pressing the same button again.

<figure markdown="span">
![Mobile Video Capture](../../datasets/assets/capture/mobile-video-capture.jpg){ align=center }
<figcaption>Android Mobile Video Capture</figcaption>
</figure>

# Capture Images

Furthermore, you can also capture individual images as shown below.  You can take image snapshots from the camera by pressing the white circular button.

<figure markdown="span">
![Mobile Image Capture](../../datasets/assets/capture/mobile-image-capture.jpg){ align=center }
<figcaption>Android Mobile Image Capture</figcaption>
</figure>

!!! tip "Leveraging Videos"
    It is recommended to use videos rather than individual images.  This is because the [Automatic Ground Truth Generation (AGTG)](../../datasets/tutorials/annotations/automatic.md) feature leverages SAM-2 with tracking information which only needs a single annotation to annotate all frames.  However, individual images requires more effort by annotating each image separately.

!!! warning "Limited Datasets"
    Throughout the demos, the dataset is kept small.  However, training on limited datasets will result in poor model performances when the model is deployed under conditions that differs from the dataset samples.  It is suggested to increase the amount of training data under various conditions and backgrounds to train a more robust model.
