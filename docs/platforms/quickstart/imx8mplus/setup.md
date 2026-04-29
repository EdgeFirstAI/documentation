# NXP i.MX 8M Plus Setup Guide

In this page you will find instructions to setup the i.MX 8M Plus from start to finish.  For the official instructions to setup the i.MX 8M Plus, refer to the [Getting Started Guide from NXP](https://www.nxp.com/document/guide/getting-started-with-the-i-mx-8m-plus-evk:GS-iMX-8M-Plus-EVK).

## Requirements
1. i.MX 8M Plus EVK running [NXP Yocto BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX)
2. USB-C power cable
3. Ethernet cable connected to live network connection
4. [MIPI CSI-2 Camera](https://community.nxp.com/t5/i-MX-Solutions-Knowledge-Base/MIPI-CSI-2-cameras-for-NXP-i-MX-8M-series-Application-Processors/ta-p/1129962)
5. SSH and SCP clients ([OpenSSH](https://www.openssh.com/), [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), etc.) to SSH into the EVK
6. If connecting to EVK via USB serial

    * USB Micro B Cable
    * Standard HDMI Cable
    * Monitor
    * Mouse and Keyboard
    * Recommendation: USB Port Hub

## Flash a microSD card with NXP Yocto BSP

!!! note "BSP Size"
    The size of the BSP installed ~12GB.

1. Download the "i.MX 8M Plus EVK,FRDM" BSP found under "Supported Platforms/Demo Images" in this [page](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX) as shown below

    {{ figure("../../assets/setup/imx8mplus_bsp_link.jpg", "i.MX 8M Plus") }}

2. You will need an NXP account to install this BSP.  Enter your credentials.  Otherwise create an account

    {{ figure("../../assets/setup/nxp_account_login.jpg", "NXP Account Login") }}

3. Once authenticated, accept the license agreement as shown

    {{ figure("../../assets/setup/nxp_bsp_license_agreement.jpg", "NXP License Agreement") }}    

4. The BSP should start downloading to your PC as a ZIP file named "LF_v6.18.2-1.0.0_images_IMX8MPEVK.zip" or similar

    {{ figure("../../assets/setup/imx8mplus_bsp_download_progress.jpg", "BSP Download Progress") }}   

5. Use [balenaEtcher](https://etcher.balena.io/) to flash the SD card using an SD card reader connected to your PC.  Select the ZIP file that was downloaded and select the SD card for the storage.  Once selected, click "Flash!" to start

    {{ figure("../../assets/setup/imx8mplus-balena-etcher.jpg", "balenaEtcher") }}

6. Wait for the application to complete flashing ~5 mins depending on your machine

    {{ figure("../../assets/setup/imx8mplus-flashing.jpg", "balenaEtcher") }}

7. Once completed, a complete status should appear.  Proceed to the next steps to boot the board with the image flashed

    {{ figure("../../assets/setup/imx8mplus-completed-flash.jpg", "Completed Flashing") }}

## Boot the i.MX 8M Plus with the NXP BSP

!!! note "Safety Precautions"
    As a safety precaution, ensure the Power Switch is turned OFF when connecting and disconnecting wires from the EVK.

1. In order to boot from the SD card, the BOOT jumpers need to be set properly.  Set the **BOOT MODE** DIP switches (SW4) on the EVK to 0011 as shown.  More information is provided in the [Getting Started Guide from NXP](https://www.nxp.com/document/guide/getting-started-with-the-i-mx-8m-plus-evk:GS-iMX-8M-Plus-EVK)

    {{ figure("../../assets/setup/imx8mplus_DIP_BOOT_PXL_20220627_151503071.png", "DIP Switches Set to 0011") }}

2. Insert the microSD card into the module

    {{ figure("../../assets/setup/imx8mplus-insert-sdcard.jpg", "Insert Micro SD Card") }}

3. Insert the 5V power supply to the Type C port 0 (2).  Next connect the board to your network by attaching an ethernet cable to the Gigabit Ethernet port (4).  Attach the MIPI CSI-2 Camera to the MIPI CSI Camera port (6)

    {{ figure("../../assets/setup/imx8mplus-connections.png", "i.MX 8M Plus Physical Connections") }}

    You can connect to your i.MX 8M Plus either connecting a mouse and keyboard, and monitor to the device; or via PuTTY - Debug Port.

    === "Mouse and Keyboard, and Monitor"

        Since there is only one USB Type A port (3) available, we recommend using a USB Port Hub to attach both the keyboard and mouse at the same time.  Connect the monitor using a standard HDMI cable to the standard HDMI Port (5).
        
        Power ON the EVK by switching the power switch (7).

        You should now see the system boot on the monitor.  Access the terminal of the EVK and enter the command.

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

        Now that you have the IP address of the EVK, you can [SSH](../../networking/ssh.md) to the EVK from any host connected to the same network as the EVK.

        ```shell
        $ ssh root@10.10.40.210
        ```

    === "PuTTY - Debug Port"

        You can connect to the EVK from your PC using [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).  
        
        Download PuTTY in your PC, by following the instructions in the link provided.

        Connect a USB cable from your PC to the USB Micro B Debug Port (1) on the EVK.

        Power ON the EVK by switching the power switch (7).

        Open "Device Manager" in your PC and under "Ports (COM & LPT)" take a note of the list of available serial ports on your PC.

        {{ figure("../../assets/setup/imx8mplus-device-manager-ports.jpg", "Device Manager") }}

        The serial ports on this setup are (COM6, COM7, COM8, COM9).

        Open PuTTY on your PC and under "Session", select the connection type to "Serial", specify the serial line to one of the COM ports listed, and change the BAUD rate "Speed" to 115200.  Once the settings are set, click "Open" on the bottom right to open the connection.

        {{ figure("../../assets/setup/imx8mplus-PuTTY-Configuration.jpg", "PuTTY Configuration") }}

        This should open a terminal window.  If the connection is successful, output will appear in the terminal.  If nothing is displayed, try the other listed COM ports until the connection works.  In some cases, you may need to press **Enter** on your keyboard to initiate the display.

        A successful connection will show "imx8mpevk login: " on the terminal.  Enter "root" to login to the device.

        {{ figure("../../assets/setup/imx8mplus-COM8-PuTTY-terminal.jpg", "PuTTY Terminal") }}

        Once logged in.  Enter the command `ip address`.

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

        {{ figure("../../assets/setup/imx8mplus-successful-PuTTY-connection.jpg", "IP Address") }}

        The IP address of the EVK will be shown next to "inet".  In this case, it is `10.10.40.210`.

        Now that you have the IP address of the EVK, you can [SSH](../../networking/ssh.md) to the EVK from any host connected to the same network as the EVK.

        ```shell
        $ ssh root@10.10.40.210
        ```

{% include-markdown "discrete/platforms/resize_sdcard_partition.md" %}

{% include-markdown "discrete/platforms/edgefirst_performance_scaling.md" %}

## Next Steps

Now that you have setup your i.MX 8M Plus, you can begin training your Vision Model that will be deployed in this platform, but first, [copy one of our ready-to-use dataset](copy_dataset.md) that will be used to train the model.
