# Hardware Workflows

Hardware-specific workflows are tailored for users who have an EdgeFirst-supported target device and want to go through the full MLOps loop: device setup, dataset acquisition, model training, model conversion, on-target validation, and deployment.

Select your platform from the table below to get started.

!!! note "About these workflows"
    The hardware workflows use the **Coffee Cup** sample dataset and train a **ModelPack** vision model. Cost estimations shown in the table reflect this specific configuration — actual costs will vary depending on your dataset size, the model type, and training configurations.

| Persona | Hardware | Features | Cost | Time |
|---------|----------|----------|------|------|
| [Maivin](../../platforms/quickstart/maivin/index.md) | PC + Maivin | Record MCAP, Annotate 2D, Train, Validate, Deploy on Maivin | TBA | TBA |
| [Raivin](../../platforms/quickstart/raivin/index.md) | PC + Raivin w/ Radar | Record MCAP, Annotate 2D + 3D, Train, Validate, Deploy on Raivin | TBA | TBA |
| LiDAR (*coming soon*) | PC + Raivin w/ LiDAR | Record MCAP, Annotate 2D + 3D (enhanced), Train, Validate, Deploy on Raivin | TBA |
| [i.MX 8M Plus](../../platforms/quickstart/imx8mplus/index.md) | PC + i.MX 8M Plus | Copy Dataset, Train, Validate, Deploy on i.MX 8M Plus | ~\$8 USD | ~1 hour |
| [i.MX 95](../../platforms/quickstart/imx95/index.md) | PC + i.MX 95 | Copy Dataset, Train, Validate, Deploy on i.MX 95 | ~\$8 USD | ~1 hour |
| [Jetson Orin](../../platforms/quickstart/jetson_orin/index.md) | PC + Jetson Orin | Copy Dataset, Train, Validate, Deploy on Jetson Orin | ~\$8 USD | ~1 hour |
| [Raspberry Pi 5](../../platforms/quickstart/raspberrypi/index.md) | PC + Raspberry Pi 5 | Copy Dataset, Train, Validate, Deploy on Raspberry Pi 5 | ~\$8 USD | ~1 hour |

1. [Maivin Workflow](../../platforms/quickstart/maivin/index.md)

    This workflow explores recording MCAPs from the Maivin to create and annotate datasets with 2D bounding boxes and segmentation masks.  Once annotated, you will train and validate a Vision model, then deploy it back to the Maivin for inference.

2. [Raivin Workflow](../../platforms/quickstart/raivin/index.md)

    This workflow explores recording MCAPs from the Raivin to create and annotate datasets with 2D and 3D annotations.  Once annotated, you will train and validate a Fusion model, then deploy it back to the Raivin for inference.

3. LiDAR Workflow *(coming soon)*

    An extension of the Raivin workflow for users with a LiDAR sensor integrated on the Raivin.  Adds enhanced 3D annotation and Fusion model capabilities.

4. [i.MX 8M Plus Workflow](../../platforms/quickstart/imx8mplus/index.md)

    This workflow explores copying the Coffee Cup dataset from "Sample Project" and training a Vision model that detects coffee cups.  Once trained, you will convert the model for the i.MX 8M Plus NPU, validate on target, and deploy it.

5. [i.MX 95 Workflow](../../platforms/quickstart/imx95/index.md)

    This workflow will cover copying a dataset, training a Vision model, converting it for the i.MX 95 eIQ Neutron NPU, and deploying it on device.

6. [Jetson Orin Workflow](../../platforms/quickstart/jetson_orin/index.md)

    This workflow explores copying the Coffee Cup dataset from "Sample Project" and training a Vision model that detects coffee cups.  Once trained, you will convert the model to TensorRT, validate it, and deploy it on the Jetson Orin.

7. [Raspberry Pi 5 Workflow](../../platforms/quickstart/raspberrypi/index.md)

    This workflow will cover copying a dataset, training a Vision model, converting it for the Raspberry Pi 5 with Hailo-8L NPU, and deploying it on device.

!!! note "Future Work"

    The workflows with missing links are a work in progress and currently unavailable.