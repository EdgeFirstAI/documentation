# On Boot Up

On the back of the device, you will find an eight-digit number.  This is the ID number.  The hostname of the device will be "verdin-imx8mp-**ID**.local", which is advertised over Multicast Domain Name System (mDNS).  For the steps below, the eight-digit number is "15141029".  The device will have a hostname of `verdin-imx8mp-15141029.local`.  This hostname can be used to connect to the device over [SSH](../../platforms/networking/ssh.md) and to open its web interface.

!!! Tip
    On Windows machines, you will not need to add the '.local' suffix.

To open the device's web interface, enter `https://verdin-imx8mp-<id>.local` in your browser.  On first connection, you will get a "Your connection is not private" warning.  This is expected and nothing to worry about: the device uses a self-signed certificate, which browsers don't recognize.  Click the "Advanced" button, and then the "Proceed to" link.

{{ figure("/platforms/assets/setup/quickStart-sslAdvanced.png", "Connection Warning") }}
