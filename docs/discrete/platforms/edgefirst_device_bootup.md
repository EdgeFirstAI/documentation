# On Boot Up

On the back of the device, you will find an eight-digit number.  This is the ID number.  The hostname of the device will be "verdin-imx8mp-**ID**.local", which is advertised over Multicast Domain Name System (mDNS).  For the steps below, the eight-digit number is "15141029".  The device will have a hostname of `verdin-imx8mp-15141029.local`.  This hostname can be used to connect to the device over [SSH](../../platforms/networking/ssh.md) and HTTP.

!!! Tip
    On Windows machines, you will not need to add the '.local' suffix.

The device has a web interface that can be connected to via both HTTP and HTTPS by entering `http://verdin-imx8mp-<id>.local`.  On first connection to the web interface, you will get a "Your connection is not private" warning.

{{ figure("/platforms/assets/setup/quickStart-sslCert.png", "Main Page Warning") }}

This is expected and nothing to worry about -- the HTTPS connection needs a SSL certificate which the vision module does not have.  Click the "Advanced" button, and then "Proceed to" link.

{{ figure("/platforms/assets/setup/quickStart-sslAdvanced.png", "Advanced Information") }}
