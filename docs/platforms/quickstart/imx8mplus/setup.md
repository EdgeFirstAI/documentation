# NXP i.MX 8M Plus Setup Guide

In this page you will find instructions to setup the i.MX 8M Plus from start to finish.

## Requirements
1. iMX 8M Plus EVK running [NXP Yocto BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX)
2. USB-C power cable
3. Ethernet cable connected to live network connection
4. [MIPI CSI-2 Camera](https://community.nxp.com/t5/i-MX-Solutions-Knowledge-Base/MIPI-CSI-2-cameras-for-NXP-i-MX-8M-series-Application-Processors/ta-p/1129962)
5. SSH and SCP clients ([OpenSSH](https://www.openssh.com/), [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), etc.) to SSH into the EVK.
6. If connecting to EVK via USB serial

    * USB Micro B Cable
    * Standard HDMI Cable
    * Monitor
    * Mouse and Keyboard
    * Recommendation: USB Port Hub

## Step 1: Flash a microSD card with NXP Yocto BSP

!!! note "BSP Size"
    The size of the BSP installed ~12GB.

1. Download the BSP found in this [page](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX)

    {{ figure("../../assets/setup/imx8mplus_bsp_link.jpg", "i.MX 8M Plus") }}

2. You will need an NXP account to install their BSP.  Enter your credentials.  Otherwise create an account.

    {{ figure("../../assets/setup/nxp_account_login.jpg", "NXP Account Login") }}

3. Once authenticated, accept the license agreement as shown

    {{ figure("../../assets/setup/nxp_bsp_license_agreement.jpg", "NXP License Agreement") }}    

4. The BSP should start downloaded to your machine as a ZIP file named "LF_v6.18.2-1.0.0_images_IMX8MPEVK.zip" or similar

    {{ figure("../../assets/setup/imx8mplus_bsp_download_progress.jpg", "BSP Download Progress") }}   

5. Use [BalenaEtcher](https://etcher.balena.io/) to flash the SD card using an SD card reader connected to your PC.  Select the ZIP file that was downloaded and select the SD card for the storage.  Once selected, click "Flash!" to start

    {{ figure("../../assets/setup/imx8mplus-balena-etcher.jpg", "Balena Etcher") }}

6. Wait for the application to complete flashing ~5 mins. depending on your machine

    {{ figure("../../assets/setup/imx8mplus-flashing.jpg", "Balena Etcher") }}

7. Once completed, a complete status should appear.  Proceed to the next steps to boot the board with the image flashed

    {{ figure("../../assets/setup/imx8mplus-completed-flash.jpg", "Completed Flashing") }}

## Step 2: Boot the i.MX 8M Plus with the NXP BSP

!!! note "Safety Precautions"
    As a safety precaution, ensure the Power Switch is turned off when connecting and disconnecting wires from the EVK.

1. Insert the microSD card into the module

    {{ figure("../../assets/setup/imx8mplus-insert-sdcard.jpg", "Insert Micro SD Card") }}

2. Power on the i.MX 8M Plus by inserting the 5V power supply to the Type C port 0 (1).  Next connect the board to your network by attaching an ethernet cable to the Gigabit Ethernet port (3).  Attach the MPI CSI-2 Camera to the MIPI CSI Camera port (5)

    {{ figure("../../assets/setup/imx8mplus-connections.jpg", "i.MX 8M Plus Physical Connections") }}

    You can connect to your i.MX 8M Plus either connecting a mouse and keyboard, and monitor to the device; or via PuTTY - USB Micro B cable.

    === "Mouse and Keyboard, and Monitor"

        Since there is only one USB Type A port (2) available, we recommend using a USB Port Hub to attach both the keyboard and mouse at the same time.  Connect the monitor using a standard HDMI cable to the standard HDMI Port (4).

        Power on the EVK by switching the power switch (6).

        You should now see the system boot on the monitor.  Access the terminal of the EVK and enter the command

        ```shell
        # ip address
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
            inet 127.0.0.1/8 scope host lo
            valid_lft forever preferred_lft forever
            inet6 ::1/128 scope host noprefixroute
            valid_lft forever preferred_lft forever
        2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
            link/ether 00:04:9f:07:2f:61 brd ff:ff:ff:ff:ff:ff
            inet 10.10.40.210/21 metric 10 brd 10.10.47.255 scope global dynamic eth0
            valid_lft 27175sec preferred_lft 27175sec
            inet6 fe80::204:9fff:fe07:2f61/64 scope link proto kernel_ll
            valid_lft forever preferred_lft forever
        3: eth1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
            link/ether 00:04:9f:07:2f:62 brd ff:ff:ff:ff:ff:ff
        4: can0: <NOARP,ECHO> mtu 16 qdisc noop state DOWN group default qlen 10
            link/can
        ```

        {{ figure("../../assets/setup/imx8mplus-weston-terminal.jpg", "Weston Terminal") }}

        The IP address of the EVK will be shown next to "inet".  In this case, it is `10.10.40.210`.

    === "PuTTY - Micro B Cable"
