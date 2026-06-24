# Setup Static IP Address

This article will show how to set up a static IP address for the Jetson Orin. By default, the Jetson Orin uses DHCP for Ethernet connections, and a hostname to find the unit on the network.  This setup will use [NetworkManager](https://networkmanager.dev/) already installed as part of the Jetpack v6.2.1 BSP.

!!! warning
    If the static IP address is set to something that is not accessible on the network, then the unit will no longer be accessible using the hostname, or IP address.  This will require the unit to be opened to access the internal serial port to reconfigure the network or connected to a network that can be accessed.

To set a static IP address:

1. [SSH](../../platforms/networking/ssh.md) into the device using the host name and username
2. Find the connection name of the interface you want to set the static IP address to

    ```shell
    $ nmcli connection show
    NAME                UUID                                  TYPE      DEVICE
    Wired connection 1  d5ea0964-cdc5-438b-b9f1-cca7031926d8  ethernet  enP8p1s0
    docker0             76e2a476-bfb0-4039-93fb-43fe0aa435d6  bridge    docker0
    ```

    For example, to set the ethernet port to a static IP address, the connection name is 'Wired connection 1'.

3. Set the static IP address using:

    ```shell
    sudo nmcli con mod '<Connection_name>' ipv4.addresses "<desired IP/mask>"
    ```

    For example:

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.addresses "10.10.41.108/21"
    ```

4. Set the gateway

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.gateway "10.10.40.1"
    ```

    You can find the gateway using

    ```shell
    $ ip route
    default via 10.10.40.1 dev enP8p1s0 proto dhcp metric 100
    10.10.40.0/21 dev enP8p1s0 proto kernel scope link src 10.10.41.109 metric 100
    169.254.0.0/16 dev docker0 scope link metric 1000 linkdown
    172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
    192.168.1.0/24 dev wlP1p1s0 proto kernel scope link src 192.168.1.201
    ```

    The gateway is `10.10.40.1` in this case.

5. Configure DNS

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.dns "10.10.40.3"
    ```

    You can find the DNS IP using

    ```shell
    $ nmcli dev show | grep DNS
    IP4.DNS[1]:                             127.0.0.1
    IP4.DNS[2]:                             10.10.40.3
    ```

    The DNS is 10.10.40.3 in this case.

6. Finally, set the connection type to manual. This will save the static configuration

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.method "manual"
    ```

7. After running the commands above, you can visualize your entire network configuration by opening the `<connection-name>` file:

    ```shell
    cd /etc/NetworkManager/system-connections/
    sudo cat Wired\ connection\ 1
    ```

    Expected file output:

    ```shell
    [connection]
    id=Wired connection 1
    uuid=d5ea0964-cdc5-438b-b9f1-cca7031926d8
    type=ethernet
    timestamp=1777917663
    [ethernet]
    [ipv4]
    address1=10.10.41.108/21,10.10.40.1
    dns=10.10.40.3;
    method=manual
    [ipv6]
    addr-gen-mode=eui64
    ip6-privacy=2
    method=auto
    [proxy]
    ```

8. Reload the configuration file

    ```shell
    sudo nmcli connection reload
    ```

9. Reboot the unit for the IP address to update

    ```shell
    sudo reboot
    ```

10. You should now be able to ping the IP address you’ve set

    ```shell
    > ping 10.10.41.108
    Pinging 10.10.41.108 with 32 bytes of data:
    Reply from 10.10.41.108: bytes=32 time<1ms TTL=63
    Reply from 10.10.41.108: bytes=32 time<1ms TTL=63
    Reply from 10.10.41.108: bytes=32 time<1ms TTL=63
    Reply from 10.10.41.108: bytes=32 time<1ms TTL=63
    Ping statistics for 10.10.41.108:
        Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
    Approximate round trip times in milli-seconds:
        Minimum = 0ms, Maximum = 0ms, Average = 0ms
    ```

    You can also verify the IP address set to the Ethernet connection using

    ```shell
    $ ip address show
    4: enP8p1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
        link/ether 3c:6d:66:b4:83:7b brd ff:ff:ff:ff:ff:ff
        inet 10.10.41.108/21 scope global noprefixroute enP8p1s0
        valid_lft forever preferred_lft forever
        inet6 fe80::3e6d:66ff:feb4:837b/64 scope link noprefixroute
        valid_lft forever preferred_lft forever
    ```

To return to Dynamic Network Configuration (DHCP):
Enter the following commands to remove the static IP address and return to DHCP mode.  Note the order of commands is important.  The examples assume 'Wired connection 1'.  If not using 'Wired connection 1', replace with the connection name.

1. Set the connection type to auto

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.method "auto"
    ```

2. Remove the gateway from the list

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.gateway ""
    ```

3. Remove the static IP address from the list

    ```shell
    sudo nmcli con mod 'Wired connection 1' ipv4.addresses ""
    ```
