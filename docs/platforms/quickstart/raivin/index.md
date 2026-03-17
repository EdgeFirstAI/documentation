# Raivin Quick Start

<figure markdown="span" style="text-align: center;">
![Raivin](../../assets/raivin.png){ width="50%" }
<figcaption>Raivin</figcaption>
</figure>

The Raivin configuration further extends the perception capabilities of the [Maivin platform](../maivin/index.md) through the addition of the [integrated radar module](../../hardware/radar.md) or [LiDAR module](../../hardware/lidar.md).  The EdgeFirst Perception Middleware is augmented for Raivin configurations with the [RadarExp Fusion Model](../../../models/fusion/index.md) which provides low-level radar data fusion with the vision data.  The low-level radar data is represented as the range and doppler data cube, the RadarExp module fuses this data with the vision data to provide a more robust perception stack.  The traditional point-cloud data from the radar is also available for use by the Raivin perception stack, and is especially useful for augmenting the object detection and tracking capabilities through the additional parameters offered by the point cloud data.  

## System Architecture

The Raivin runs a Linux operating system based on Toradex's Torizon, we refer to the operating system as Torizon for Maivin.  The operating system packages include common libraries and tools you would expect to find on a typical embedded Linux operating system focused on computer vision and AI (Python, OpenCV, etc...).  

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, what we call our collection of applications and libraries used in the implementation of the perception stack.  The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../perception/index.md), for this document we focus on describing the application services and how they fit together to deliver the perception middleware.

In this Quick Start, you will find instructions for:

1. [Setting up your Raivin](setup.md)
2. [Visting the Raivin's Web UI](webui.md)
3. [Copying a Sample Dataset in EdgeFirst Studio for Training](copy_dataset.md)
4. [Training a Fusion Model](train.md)
5. [Validating the Fusion Model](validate.md)
6. [Deploying the Fusion Model](deploy.md)
