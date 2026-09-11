# Software Updates

The Maivin platform runs a Linux operating system which is based on the [Torizon][torizon] distribution.  The Maivin version of the distribution is referred to as Torizon for Maivin.  This Torizon for Maivin distribution uses [OSTree][ostree] to manage software updates, this updates both the Linux operating system including the kernel, drivers, and core system packages as well as the EdgeFirst Perception Middleware which provides the perception stack.

The version naming for the Torizon for Maivin distribution follows the YEAR.MONTH.PATCH format.  The YEAR and MONTH refer to the date of the initial release of the software and the PATCH is the incremental patch release within this release cycle.  Release candidates carry an `-rcN` suffix, for example `2026.08.0-rc1`.  Versions only move forward, a patch release always includes every change since the previous release rather than an isolated backport.  The upstream Torizon OS version number is documented in the [release notes](release_notes.md).

## OSTree

OSTree is a tool that provides a way to manage the filesystem of a Linux system as a series of snapshots.  Each snapshot is a complete filesystem image that can be booted into.  The system can be updated by switching to a new snapshot.  This allows for atomic updates where the system is either in the old state or the new state.  If the update fails the system can be rolled back to the previous snapshot.

The Torizon for Maivin OSTree repository publishes three channels, each channel is an OSTree branch.

- **torizon/maivin/release**
    - The release channel is the stable channel used for production systems.  This channel tracks the latest YEAR.MONTH.PATCH release.
- **torizon/maivin/testing**
    - The testing channel is used for qualifying new software releases.  This channel tracks the latest YEAR.MONTH.PATCH-rcN release candidates.
- **torizon/maivin/develop**
    - The develop channel is updated on every change to the platform and is likely to contain breaking or undocumented changes.  This channel should only be used by developers working on the platform.

!!! note

    It is recommended that users should only pull OSTree updates from the release channel.

The channel names are a permanent contract with the fleet.  When a future Torizon generation is introduced it will be published under a generation specific prefix, such as `torizon-8/maivin/<channel>`, while `torizon/maivin/<channel>` continues to follow the supported generation.

### Release Information

The currently booted Torizon for Maivin operating system release information can be read from the `/etc/os-release` file.  The `VERSION_ID` field carries the Torizon for Maivin version and the `BUILD_ID` the build number.  Please include both when contacting support.

```bash
cat /etc/os-release
```

The version string also identifies the channel the image was built for.  A release build carries a bare version such as `2026.08.0+build.1`, a testing build carries the release candidate suffix such as `2026.08.0-rc1+build.4`, and a develop build is versioned `main+build.N`.  The kernel version reported by `uname -r` carries the same suffix.

### Deployment Origin

Each image ships with its channel recorded in the OSTree deployment origin, so a freshly installed unit already tracks the channel it was built from.  A release image tracks `torizon/maivin/release`, a release candidate tracks `torizon/maivin/testing`, and a develop image tracks `torizon/maivin/develop`.  The OSTree remote named `maivin` is configured in `/etc/ostree/remotes.d/maivin.conf` and points to the [Torizon for Maivin OSTree repository][auz-ostree].

The current status, including the tracked channel, can be viewed using the following command.

```bash
ostree admin status
```

This will show the currently booted snapshot, its `refspec` which should start with `maivin:`, and the rollback snapshot if one is available.  Whenever the system is updated the previous version remains available as a snapshot, allowing rollbacks if the update fails or causes issues.

### Updating the System

The Torizon for Maivin system can be updated using the OSTree client.  Because the channel is recorded in the deployment origin, the upgrade command needs no arguments.

1. Access your Maivin through [SSH](../networking/ssh.md).
2. Pull and deploy the latest update from the tracked channel with the `ostree admin upgrade` command:

    ```bash
    torizon@verdin-imx8mp-15141091:~$ sudo ostree admin upgrade
    ```

    The command prints `No update available.` when the device already runs the latest commit on its channel.

3. Reboot the Maivin with the `sudo reboot` command to boot into the new deployment.

The update can also be performed in two explicit steps, which is useful when you want to inspect the pulled commit before deploying it.

```bash
sudo ostree pull maivin:torizon/maivin/release
sudo ostree admin deploy maivin:torizon/maivin/release
sudo reboot
```

!!! warning

    Always qualify the branch with the `maivin:` remote prefix when using `ostree admin deploy`.  Deploying a bare branch name clears the channel from the deployment origin, after which `ostree admin upgrade` reports `No update available` and the device stops receiving updates.  Refer to [Repairing the Deployment Origin](#repairing-the-deployment-origin) if this happens.

Static delta files are generated for the release channel from every release published in the previous six months, which keeps release to release upgrades small.  When no delta matches, for example when upgrading from an older release, the client fetches the objects normally.

### Switching Channels

A device can be moved to another channel, for example to qualify a release candidate from the testing channel.  The `switch` command pulls the new channel, deploys it, and records the new channel in the deployment origin so later upgrades follow the new channel with no arguments.  The switch takes effect on the next boot.

```bash
sudo ostree admin switch maivin:torizon/maivin/testing
sudo reboot
```

The `switch` command only moves between channels and refuses with `Old and new refs are equal` when the booted deployment already tracks the requested channel.

### Update Rollback

OSTree keeps the previous deployment as a rollback snapshot.  If the new deployment fails to boot, the bootloader falls back to the previous deployment automatically.  To roll back manually, undeploy the pending or booted deployment by index as shown by `ostree admin status`, where index `0` is the first deployment listed.

```bash
sudo ostree admin undeploy 0
sudo reboot
```

Configuration changes made under `/etc` are carried forward into the new deployment by OSTree's three-way merge.  A file you have modified, such as `/etc/default/camera`, keeps your version and does not pick up new keys added by the release.  Compare your configuration against the shipped defaults under `/usr/etc/default/` after an upgrade, refer to [Configuration](../configuration/index.md).

### Repairing the Deployment Origin

Two operations clear the channel from the deployment origin: a Torizon OTA (aktualizr) update, which replaces the refspec with a bare commit hash, and `ostree admin deploy` invoked with a branch name missing the `maivin:` prefix.  A device in this state does not report an error, `ostree admin upgrade` prints `No update available` and the device silently stops updating.

Check the deployment origin with `ostree admin status` and confirm the `refspec` starts with `maivin:`.  If it does not, restore the origin without deploying anything using `set-origin` and reboot.

```bash
sudo ostree admin set-origin maivin https://maivin.deepviewml.com/ostree torizon/maivin/release
sudo reboot
```

### Changelogs

The changes included in each release are documented in the [Release Notes](release_notes.md).  The EdgeFirst Perception Middleware services are open source and each service publishes its own changelog on GitHub, the per-package versions shipped in a release are listed in the release notes.

### OSTree Repository

The Torizon for Maivin OSTree repository is hosted by Au-Zone Technologies at the [Torizon for Maivin OSTree repository][auz-ostree].  This repository is accessed through the OSTree client using the configuration file under `/etc/ostree/remotes.d/maivin.conf`.

## Further Reading

For further information about how the Torizon platform uses OSTree, refer to the official Toradex documentation [Torizon In-Depth OSTree][tor-ostree].

[torizon]: https://developer.toradex.com/torizon/
[ostree]: https://ostreedev.github.io/ostree/
[tor-ostree]: https://developer.toradex.com/torizon/in-depth/ostree/
[auz-ostree]: https://maivin.deepviewml.com/ostree
