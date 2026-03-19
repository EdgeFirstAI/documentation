# Maivin Quick Start

<figure markdown="span" style="text-align: center;">
![Maivin](../../assets/maivin-2.png){ width="50%" }
<figcaption>Maivin</figcaption>
</figure>

The Maivin configuration is a vision-only platform that provides a vision-based perception stack for use in harsh environments, providing an IP66/67 waterproof enclosure and connectors.  The Maivin platform is built on the [NXP i.MX 8M Plus](https://www.nxp.com/products/i.MX8MPLUS) processor which includes a 2 TOPS AI accelerator.  The [EdgeFirst Perception Middleware](../../../perception/index.md) leverages the AI-accelerator enabling this vision sensor to be deployed in the field to deliver real-time edge perception applications.

## System Architecture

The Maivin runs a Linux operating system based on Toradex's Torizon, we refer to the operating system as Torizon for Maivin.  The operating system packages include common libraries and tools you would expect to find on a typical embedded Linux operating system focused on computer vision and AI (Python, OpenCV, etc...).  

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, what we call our collection of applications and libraries used in the implementation of the perception stack.  The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../perception/index.md), for this document we focus on describing the application services and how they fit together to deliver the perception middleware.

In this Quick Start, you will find instructions for:

1. [Setting up your Maivin](setup.md)
2. [Visiting the Maivin's Web UI](webui.md)
3. [Copying a Sample Dataset in EdgeFirst Studio for Training](copy_dataset.md)
4. [Training a Vision Model](train.md)
5. [Validating the Vision Model](validate.md)
6. [Deploying the Vision Model](deploy.md)