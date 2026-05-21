# Setup Wi-Fi Access Point

This article will show how to setup the Jetson Orin Nano with a Wi-Fi Access Point such that other wireless devices (such as your mobile phone) can connect to the device’s wired network.

!!! info
    Each command is specific to your setup - pay attention to the key words from the commands

    * "wlP1p1s0" (Wi-Fi interface which could change depending on your system)
    * "enP8p1s0" (Ethernet interface which could change depending on your system)
    * "192.168.1.204" (static IP address you can set)

1. Find your device’s Wi-Fi interface (wlP1p1s0 in this case)

    ```shell
    $ iw dev
    phy#0
    Interface wlP1p1s0
            ifindex 2
            wdev 0x1
            addr 9c:c7:d3:97:62:ad
            type managed
            txpower -100.00 dBm
    ```

2. Verify Wi-Fi AP support - you must see AP in supported modes

    ```shell
    $ sudo iw list | sed -n '/Supported interface modes:/,/Band/p'
            Supported interface modes:
                    * IBSS
                    * managed
                    * AP
                    * P2P-client
                    * P2P-GO
            Band 1:
    ```

3. Install required packages

    ```shell
    $ sudo apt update
    $ sudo apt install -y hostapd dnsmasq iptables-persistent
    ```

4. Prevent NetworkManager from controlling Wi-Fi AP interface.  Create a NetworkManager override so wlP1p1s0 (specific to your system) is unmanaged

    ```shell
    sudo tee /etc/NetworkManager/conf.d/99-unmanaged-wifi.conf >/dev/null <<'EOF'
    [keyfile]
    unmanaged-devices=interface-name:wlP1p1s0
    EOF
    ```

5. Restart NetworkManager

    ```shell
    $ sudo systemctl restart NetworkManager
    ```

6. Assign static IP to Wi-Fi interface at boot.  Create a small systemd unit

    ```shell
    sudo tee /etc/systemd/system/ap-interface.service >/dev/null <<'EOF'
    [Unit]
    Description=Configure AP interface wlP1p1s0
    After=network.target
    Before=hostapd.service dnsmasq.service
    [Service]
    Type=oneshot
    ExecStart=/sbin/ip link set wlP1p1s0 up
    ExecStart=/sbin/ip addr flush dev wlP1p1s0
    ExecStart=/sbin/ip addr add 192.168.1.204/24 dev wlP1p1s0
    RemainAfterExit=yes
    [Install]
    WantedBy=multi-user.target
    EOF
    ```

7. Configure hostapd by creating hostapd config.  Note you can set the access point ssid and wpa_passphrase. The wpa_passphrase must be at least 8 characters

    ```shell
    sudo tee /etc/hostapd/hostapd.conf >/dev/null <<'EOF'
    interface=wlP1p1s0
    driver=nl80211
    ssid=my_ssid
    hw_mode=g
    channel=6
    wmm_enabled=1
    country_code=CA
    ieee80211n=1
    ieee80211d=1
    auth_algs=1
    wpa=2
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    wpa_passphrase=mypassphrase
    EOF
    ```

8. Point hostapd service to this config

    ```shell
    sudo sed -i 's|^#\?DAEMON_CONF=.*|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd
    ```

9. Configure dnsmasq for DHCP by creating AP DHCP config

    ```shell
    sudo tee /etc/dnsmasq.d/jetson-ap.conf >/dev/null <<'EOF'
    interface=wlP1p1s0
    bind-interfaces
    dhcp-range=192.168.1.50,192.168.1.150,255.255.255.0,24h
    dhcp-option=3,192.168.1.204
    dhcp-option=6,1.1.1.1,8.8.8.8
    EOF
    ```

10. Enable IPv4 forwarding

    ```shell
    sudo tee /etc/sysctl.d/99-jetson-ap.conf >/dev/null <<'EOF'
    net.ipv4.ip_forward=1
    EOF
    sudo sysctl --system
    ```

11. Add NAT and forwarding rules (Wi-Fi → Ethernet); your ethernet can be found via ip addr → enP8p1s0 in this case

    ```shell
    sudo iptables -t nat -A POSTROUTING -o enP8p1s0 -j MASQUERADE
    sudo iptables -A FORWARD -i enP8p1s0 -o wlP1p1s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlP1p1s0 -o enP8p1s0 -j ACCEPT
    sudo netfilter-persistent save
    ```

12. Unmask `hostapd`

    ```shell
    sudo systemctl unmask hostapd
    sudo systemctl enable hostapd
    ```

13. Enable and start services

    ```shell
    sudo systemctl daemon-reload
    sudo systemctl enable ap-interface hostapd dnsmasq
    sudo systemctl restart ap-interface
    sudo systemctl restart hostapd
    sudo systemctl restart dnsmasq
    ```

14. Verify the static IP address 

    ```shell
    $ ip addr show wlP1p1s0
    2: wlP1p1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
        link/ether f8:3d:c6:56:fe:93 brd ff:ff:ff:ff:ff:ff
        inet 192.168.1.204/24 scope global wlP1p1s0
        valid_lft forever preferred_lft forever
    ```

15. Test on your mobile

    * Connect to SSID `my_ssid`
    * Enter WPA password `mypassphrase`

16. Check System Status

    ```shell
    systemctl status hostapd --no-pager
    systemctl status dnsmasq --no-pager
    ip -4 addr show wlP1p1s0
    sudo journalctl -u hostapd -n 50 --no-pager
    ```

## System Debugging

1. If you get the error trying to restart hostapd

    ```shell
    $ sudo systemctl restart hostapd
    Job for hostapd.service failed because the control process exited with error code.
    See "systemctl status hostapd.service" and "journalctl -xeu hostapd.service" for details.
    ```

    Check the service status 

    ```shell
    $ sudo journalctl -u hostapd -n 80 --no-pager
    Apr 30 12:48:00 systemd[1]: Stopped Access point and authentication server for Wi-Fi and Ethernet.
    Apr 30 12:48:00 systemd[1]: Starting Access point and authentication server for Wi-Fi and Ethernet...
    Apr 30 12:48:00 hostapd[9829]: Line 14: invalid WPA passphrase length 5 (expected 8..63)
    Apr 30 12:48:00 hostapd[9829]: WPA-PSK enabled, but PSK or passphrase is not configured.
    Apr 30 12:48:00 hostapd[9829]: 2 errors found in configuration file '/etc/hostapd/hostapd.conf'
    Apr 30 12:48:00 hostapd[9829]: Failed to set up interface with /etc/hostapd/hostapd.conf
    Apr 30 12:48:00 hostapd[9829]: Failed to initialize interface
    Apr 30 12:48:00 systemd[1]: hostapd.service: Control process exited, code=exited, status=1/FAILURE
    Apr 30 12:48:00 systemd[1]: hostapd.service: Failed with result 'exit-code'.
    Apr 30 12:48:00 systemd[1]: Failed to start Access point and authentication server for Wi-Fi and Ethernet.
    ```

    Check the wpa_passphrase and this must be at least 8 characters, up to 63.

2. If the AP does not start, run these commands

    ```shell
    rfkill list
    sudo rfkill unblock all
    sudo ip link set wlP1p1s0 up
    sudo iw reg set US
    sudo systemctl restart hostapd
    sudo journalctl -u hostapd -n 80 --no-pager
    ```