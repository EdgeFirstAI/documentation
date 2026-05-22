# NVIDIA Jetson Orin Nano Quick Start

{{ figure("../../assets/jetsonorin.png", "Jetson Orin", "50%") }}

The NVIDIA Jetson Orin Nano is a compact, low-power computing module designed for running AI workloads directly on embedded devices.  Built on NVIDIA’s Ampere GPU architecture, it delivers significantly higher performance than earlier Jetson Nano platforms while maintaining efficiency suitable for edge deployments.  The Jetson Orin Nano supports the EdgeFirst pipeline from model training to running real-time vision inference at the edge.

## System Architecture

The Jetson Orin Nano runs a Linux-based environment built around NVIDIA JetPack, which packages the core Jetson software stack for development and deployment.  JetPack provides CUDA, cuDNN, TensorRT, multimedia APIs, and platform libraries used to accelerate AI inference and vision pipelines on-device.  Alongside common tooling such as Python and OpenCV, this ecosystem enables streamlined model optimization, hardware-accelerated runtime execution, and reproducible edge AI deployment workflows on Jetson hardware.

In this Quick Start, you will find instructions for:

1. [Setting up your Jetson Orin](setup.md)
2. [Copying a Sample Dataset in EdgeFirst Studio for Training](copy_dataset.md)
3. [Training Vision Model](train.md)
4. [Converting ONNX to TensorRT](convert_tensorrt.md)
5. [Validating the Vision Model](validate.md)
6. [Deploying the Vision Model](deploy.md)
