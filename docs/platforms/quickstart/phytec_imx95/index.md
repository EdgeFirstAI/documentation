# phyFLEX-i.MX 95 Libra Quick Start

{{ figure("../../assets/phytec_imx95-libra.png", "phyFLEX-i.MX 95 Libra", "50%") }}

The phyFLEX-i.MX 95 Libra is a development-focused platform for building and evaluating vision-based edge AI applications on NXP hardware using PHYTEC's i.MX 95 development kit. This platform is built on the [NXP i.MX 95](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-9-applications-processors/i-mx-95-applications-processors:IMX95) application processor, which includes the Neutron NPU for accelerated inference. The [EdgeFirst Perception Middleware](../../../perception/index.md) and EdgeFirst Studio workflow support training, conversion, validation, and deployment of vision models for this target.

## System Architecture

The phyFLEX-i.MX 95 Libra runs a Linux environment based on [PHYTEC's Yocto BSP](https://phytec.github.io/doc-bsp-yocto/bsp/imx9/imx95-fpsc/alpha2.html), including the common packages needed for embedded vision and AI development such as Python, GStreamer, camera tooling, and related multimedia libraries. In the current workflow, the platform is used both as a target for on-device model validation and as a development kit for capturing videos and images from attached cameras.

Central to the EdgeFirst platform workflow is [EdgeFirst Studio](../../../studio/index.md) for dataset management, annotation, training, and validation, together with the [EdgeFirst Perception Middleware](../../../perception/index.md) for deployment-oriented edge workflows. On the phyFLEX-i.MX 95 Libra, this enables a practical pipeline from camera capture, to dataset import and annotation, to model training, Neutron conversion, and deployment on target hardware.

In this Quick Start, you will find instructions for:

1. [Setting up your phyFLEX-i.MX 95 Libra](setup.md)
2. [Capturing videos and images with GStreamer](capture.md)
3. [Importing videos and images into EdgeFirst Studio](import.md)
4. [Annotating your dataset](annotate.md)
5. [Training a vision model](train.md)
6. [Converting the model with the Neutron Converter](convert_neutron.md)
7. [Validating the model on target](validate.md)
8. [Deploying the vision model](deploy.md)
