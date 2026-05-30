# i.MX 95 Quick Start

{{ figure("../../assets/imx95.png", "i.MX 95", "50%") }}

The i.MX 95 configuration is a development-focused platform for building and evaluating vision-based edge AI applications on NXP hardware. This platform is built on the [NXP i.MX 95](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-9-applications-processors/i-mx-95-applications-processors:IMX95) application processor, which includes the Neutron NPU for accelerated inference. The [EdgeFirst Perception Middleware](../../../perception/index.md) leverages the Neutron delegate to enable real-time edge perception workflows from data capture through deployment.

## System Architecture

The i.MX 95 runs a Linux operating system based on [NXP's BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX) and includes the common packages needed for embedded vision and AI development (Python, OpenCV, and related tooling).

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, our collection of applications and libraries used to implement the perception stack. The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../perception/index.md); in this Quick Start we focus on the application services and workflow used to build and deploy models on the i.MX 95.

In this Quick Start, you will find instructions for:

1. Setting up your i.MX 95 (*coming soon*)
2. [Copying a Sample Dataset in EdgeFirst Studio for Training](copy_dataset.md)
3. [Training a Vision Model](train.md)
4. [Converting a Vision Model for the Neutron NPU](conversion/index.md)
5. [Validating a Vision Model](validate.md)
6. [Deploying a Vision Model](deploy.md)
