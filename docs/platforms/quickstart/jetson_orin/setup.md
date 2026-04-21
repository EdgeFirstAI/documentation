# NVIDIA Jetson Orin Nano Setup Guide

In this page, you will find the instructions to setup the Jetson Orin Super Nano from start to finish.  You can also find the official [Getting Started Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#intro) provided by NVIDIA for setting up the Jetson Orin.  This page will build on top of the official documentation and written to be focused more towards adding support for deploying the EdgeFirst pipeline.

!!! info "Device Specification"
    The device used in these examples has these specs.

    * 1024-core NVIDIA Ampere architecture GPU with 32 Tensor Cores
    * 6-core Arm Cortex-A78AE v8.2 64-bit CPU
    * 8GB 128-bit LPDDR5
    * microSD Card slot

    I/O:

    * Display Port
    * 4x USB 3.2 Gen2 Type A
    * USB Type-C UFP
    * M.2 Key M 2280
    * M.2 Key M 2230
    * M.2 Key E (populated)

## Step 1: Flash a microSD card with Jetpack 6.x

It is recommended to use a microSD card that's 64GB and higher to flash Jetpack 6.2.1 which is ~24.1GB.

!!! note "Official Docs"
    The official documentation links towards these [instructions for flashing Jetpack 6.x](https://www.jetson-ai-lab.com/tutorials/initial-setup-jetson-orin-nano/#6%EF%B8%8F%E2%83%A3-boot-with-jetpack-6x-sd-card).

1. Download [Jetpack v6.2.1](https://developer.nvidia.com/downloads/embedded/L4T/r36_Release_v4.4/jp62-r1-orin-nano-sd-card-image.zip) by clicking the link provided.  This should download a ZIP file named "jetson-orin-nano-devkit-super-SD-image_JP6.2.1.zip".

2. Use [BalenaEtcher](https://etcher.balena.io/) to flash the SD card using an SD card reader connected to your PC.  Select the ZIP file that was downloaded and select the SD card for the storage.  Once selected, click "Flash!" to start.

    {{ figure("../../assets/setup/balena_etcher_orin.png", "Balena Etcher") }}

3. Wait for the application to complete flashing ~10 mins. depending on your machine.

    {{ figure("../../assets/setup/orin_flashing.png", "Balena Etcher") }}

4. Once completed, a complete status should appear.  Proceed to the next steps to boot the board with the image flashed.

    {{ figure("../../assets/setup/orin_completed_flash.png", "Completed Flashing") }}

