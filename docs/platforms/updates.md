# Software Updates

The Maivin platform runs a Linux operating system which is based on the [Torizon][torizon] distribution.  The Maivin version of the distribution is refered to as "Torizon for Maivin" (TfM).  This TfM distribution uses [OSTree][ostree] to manage software udpates, this updates both the Linux operating system including the kernel, drivers, and core system packages as well as the EdgeFirst Middleware which provides the perception stack.

The version naming for the TfM distribution follows the YEAR.MONTH.PATCH format.  The YEAR and MONTH refer to the data of the initial release of the software and the PATCH is the incremental patch release within this release cycle.  The upstream Torizon OS version number is documented in the release notes.

## OSTree
OSTree is a tool that provides a way to manage the filesystem of a Linux system as a series of snapshots.  Each snapshot is a complete filesystem image that can be booted into.  The system can be updated by switching to a new snapshot.  This allows for atomic updates where the system is either in the old state or the new state.  If the update fails the system can be rolled back to the previous snapshot.

The TfM OSTree repository uses branches to manage the different versions of the software.  Three core branches are used:

- torizon/maivin/release
  - The release branch is the stable branch that is used for production systems.  This branch tracks the latest YEAR.MONTH.PATCH release.

- torizon/maivin/testing
  - The testing branch is used for testing new software releases.  This branch tracks the latest YEAR.MONTH.PATCHrcX release candidates.

- torizon/maivin/develop
  - The dev branch is used for development of new features.  This branch is updated frequently and is likely to contain breaking or undocumented changes.  This branch should only be used by developers working on the platform.

```{warning}
It is recommended that users should only pull ostree updates from the Release branch.
```

Other branches may be used for specific purposes such as tracking major changes to the system such as a new major Torizon update or similar updates that have a high impact to the overall system.

The currently booted TfM operating system release information can be read from the `/etc/os-release` file.

```bash
cat /etc/os-release
```

### Updating the System
The TfM system can be updated using the OSTree client.  The client is a command-line utility that can be used to manage the system snapshots.

To update the release:
1. Access your Maivin through SSH
2. Pull the latest Maivn release update with the `ostree pull` command:
    ```bash
    torizon@verdin-imx8mp-15141091:~$ sudo ostree pull maivin:torizon/maivin/release
    1 delta parts, 2 loose fetched; 481 KiB transferred in 2 seconds; 0 bytes content written
    ```
3. Deploy the pulled release with the `ostree admin deploy` command:
    ```bash
    torizon@verdin-imx8mp-15141091:~$ sudo ostree admin deploy torizon/maivin/release
    note: Deploying commit 71815d485d8237adedfd4cc041511d43406e9861b5e9107dba7e5b3e217442c4 which contains content in /var/local that will be ignored.
    Copying /etc changes: 14 modified, 12 removed, 21 added
    Transaction complete; bootconfig swap: yes; bootversion: boot.1.1, deployment count change: 0
    Freed objects: 6.7?MB
    ```
4. Reboot the Maivin with the `sudo reboot` command.

### Status
The current ostree status can be viewed using the following command:

```bash
ostree admin status
```

This will show the currently loaded snapshot and the rollback snapshot if one is available.  Whenever OStree is updated, the previous version will be available as a snapshot allowing rollbacks if the update fails or causes issues.

### Changelogs


### Update Rollback


### OSTree Repository
The Torizon for Maivin OSTree repository is hosted by Au-Zone Technologies and is available [here][auz-ostree].  This repository is accessed through the OSTree client 
using the configuration file under `/etc/ostree/remotes.d/maivin.conf`.

## Further Reading
For further information about how the Torizon platform uses ostree, refer to the official Toradex documentation [Torizon In-Depth OSTree][tor-ostree].

[torizon]: https://developer.toradex.com/torizon/
[ostree]: https://ostreedev.github.io/ostree/
[tor-ostree]: https://developer.toradex.com/torizon/in-depth/ostree/
[auz-ostree]: https://maivin.deepviewml.com/ostree