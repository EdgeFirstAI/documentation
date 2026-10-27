# phyFLEX-i.MX 95 Libra Setup Guide

This guide walks you through how to flash the BSP for the phyFLEX-i.MX95 Libra development kit. You can also find the official [setup guide](https://phytec.github.io/doc-bsp-yocto/bsp/imx9/imx95-fpsc/alpha2.html) provided by PHYTEC.

Please use the following images when the various ports are referenced throughout this guide.

{{ figure("../../assets/setup/phytec/libra-front-components2.jpg", "Libra FPSC Components (front)") }}

{{ figure("../../assets/setup/phytec/libra-back-components2.jpg", "Libra FPSC Components (back)") }}

## Flash a microSD card with the phytec-vision-image

1. Using a Linux machine, fetch the BSP from [PHYTEC's download page](https://download.phytec.de/Software/Linux/BSP-Yocto-i.MX95/BSP-Yocto-NXP-i.MX95-ALPHA2/images/ampliphy-vendor/imx95-phyflex-libra-rdk-2/)

    ```shell
    wget https://download.phytec.de/Software/Linux/BSP-Yocto-i.MX95/BSP-Yocto-NXP-i.MX95-ALPHA2/images/ampliphy-vendor/imx95-phyflex-libra-rdk-2/phytec-vision-image-imx95-phyflex-libra-rdk-2.rootfs.wic.xz
    ```

2. Flash the SD card using the following command

    !!! warning "Data Loss"
        Be very careful when specifying the SD card device.
        Specifying the wrong device can cause data loss. Find your SD card's block-device path using `lsblk`.

        Replace `/dev/sdX` with the correct block-device path for your system.

    ```shell
    xzcat phytec-vision-image-imx95-phyflex-libra-rdk-2.rootfs.wic.xz | sudo dd of=/dev/sdX bs=4M status=progress && sync
    ```

## Connect to the device

1. To boot from the SD card set the bootmode switches (S1) to the following position

    {{ figure("../../assets/setup/phytec/sdcard_switches.png", "SD Boot Mode") }}

2. Use X14 (Debug) USB-C port to connect your host PC to the board via Serial using the baudrate 115200

    !!! note "PuTTY"
        You can use [PuTTY](https://putty.org/index.html) to access the board's serial monitor.

3. Provide power to the board by attaching the power supply to the X8 port of the board

## Next Steps

Now that you have set up your phyFLEX-i.MX 95 Libra, you can use the board to start [capturing videos and images](capture.md) for your dataset.
