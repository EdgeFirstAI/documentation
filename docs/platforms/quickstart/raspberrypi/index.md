# Raspberry Pi 5 Quick Start

{{ figure("../../assets/raspberrypi5.png", "Raspberry Pi 5", "50%") }}

The Raspberry Pi 5 configuration is a development-focused platform for building and evaluating vision-based edge AI applications on Raspberry Pi hardware. This platform is based on the Raspberry Pi 5 and can optionally pair with a [Hailo accelerator](https://hailo.ai/) for NPU-accelerated inference. The [EdgeFirst Perception Middleware](../../../perception/index.md) enables end-to-end edge perception workflows from data capture through deployment.

## System Architecture

The Raspberry Pi 5 runs a Linux operating system and includes the common packages needed for embedded vision and AI development (Python, OpenCV, and related tooling).

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, our collection of applications and libraries used to implement the perception stack. The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../perception/index.md); in this Quick Start we focus on the application services and workflow used to build and deploy models on the Raspberry Pi 5.

In this Quick Start, you will find instructions for:

1. Setting up your Raspberry Pi 5 (*coming soon*)
2. [Copying a Sample Dataset in EdgeFirst Studio for Training](copy_dataset.md)
3. [Training a Vision Model](train.md)
4. [Converting a Vision Model for Raspberry Pi](conversion/index.md)
5. [Validating a Vision Model](validate.md)
6. [Deploying a Vision Model](deploy.md)
