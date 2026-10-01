# phyFLEX-i.MX 95 Libra Setup Guide

This guide walk you through how to flash the BSP for the phyFLEX-i.MX95 Libra development kit. You can also find the official [setup guide](https://phytec.github.io/doc-bsp-yocto/bsp/imx9/imx95-fpsc/alpha2.html) provided by Phytec.

## Flash a microSD card with the phytec-vision-image

1. Using a Linux machine, fetch the BSP from Phytec's download page.

    ```shell
    wget https://download.phytec.de/Software/Linux/BSP-Yocto-i.MX95/BSP-Yocto-NXP-i.MX95-ALPHA2/images/ampliphy-vendor/imx95-phyflex-libra-rdk-2/phytec-vision-image-imx95-phyflex-libra-rdk-2.rootfs.wic.xz
    ```

2. Flash the SD card using the following command.

    !!! warning "Data Loss"
        Be very careful when specifying the SD card mounting point.
        Specifying the wrong device will lead to data loss. Find your SD card mounting point using `lsblk`.

        Replace "/dev/sdX" with the correct device in your system.

    ```shell
    xzcat phytec-vision-image-imx95-phyflex-libra-rdk-2.rootfs.wic.xz | sudo dd of=/dev/sdX bs=4M status=progress && sync
    ```

## Boot from SD card

1. To boot from the SD card set the bootmode switches (S1) to the following position.

    {{ figure("../../assets/setup/phytec/sdcard_switches.png", "SD Boot Mode") }}

## Connect to the device

{{ figure("../../assets/setup/phytec/Libra-front-components2.jpg", "Libra FPSC Components (front)") }}

1. Use X14 (Debug) USB-C port to connect your host PC to the board via Serial using a baudrate 115200.

    !!! note "PuTTY"
        You can use [PuTTY](https://putty.org/index.html) to access the board's serial monitor.

2. Power the board by attaching the power supply to the X8 port of the board.

## Next Steps

Now that you have set up your phyFLEX-i.MX 95 Libra, you can use the board to start [capturing videos and images](capture.md) for your dataset.
