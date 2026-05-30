# Resize SD Card Partition

When using an SD Card to boot the platform you might run into the case where the mounted partition does not use the majority of the volume of the SD card.  It is possible to resize this partition to use most of the volume of the SD card as shown in this guide.

Below shows the size of the partition on `/dev/root` is ~10GB, but the SD card used is 128GB.

```shell
root@imx8mpevk:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        10G  5.8G  3.7G  62% /
```

## Procedure

1. List current partitions on `/dev/mmcblk1`
    * Note the starting address of partition #2
2. Delete partition #2
3. Create new partition #2
    * Ensure you use the start address from Step #1
    * Ensure you say no to removing the partition type
4. Write changes and reboot
5. Run resize2fs command
6. Verify changes

## Step 1 - List Current Partitions

```shell
# fdisk -l /dev/mmcblk1
Disk /dev/mmcblk1: 119.08 GiB, 127865454592 bytes, 249737216 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x076c4a2a

Device         Boot  Start      End  Sectors  Size Id Type
/dev/mmcblk1p1 *     16384   540671   524288  256M  c W95 FAT32 (LBA)
/dev/mmcblk1p2      540672 22270745 21730074 10.4G 83 Linux
```

Note the "Start" sector of partition 2 — here it’s `540672`.

!!! tip "`/dev/mmcblk1` does not exist"

    If `/dev/mmcblk1` does not exist in your system, confirm which partition is mounted where based on this command.

    ```shell
    # lsblk -f
    NAME         FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
    mtdblock0
    mmcblk2
    |-mmcblk2p1  vfat         boot  3121-7250                                53M    36% /run/media/boot-mmcblk2p1
    `-mmcblk2p2  ext4         root  85380d8c-285d-418a-94e2-ef1c4d69f0b1  963.7M    66% /run/media/root-mmcblk2p2
    mmcblk2boot0
    mmcblk2boot1
    mmcblk1
    |-mmcblk1p1  vfat         boot  E5F9-7ABE                             216.8M    15% /run/media/boot-mmcblk1p1
    `-mmcblk1p2  ext4         root  2ee72d7b-1c49-41f2-b217-df1d7888b583    3.6G    58% /
    ```

## Step 2,3,4 - Rewrite Partitions using `fdisk`

```shell
# fdisk /dev/mmcblk1

Welcome to fdisk (util-linux 2.41.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

This disk is currently in use - repartitioning is probably a bad idea.
It's recommended to umount all file systems, and swapoff all swap
partitions on this disk.


Command (m for help): d
Partition number (1,2, default 2): 2

Partition 2 has been deleted.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (2048-249737215, default 2048): 540672
Last sector, +/-sectors or +/-size{K,M,G,T,P} (540672-249737215, default 249737215):

Created a new partition 2 of type 'Linux' and of size 118.8 GiB.
Partition #2 contains a ext4 signature.

Do you want to remove the signature? [Y]es/[N]o: n

Command (m for help): w

The partition table has been altered.
Syncing disks.

# reboot
```

## Step 5 - Resize Filesystem

```shell 
# resize2fs /dev/mmcblk1p2
resize2fs 1.47.3 (8-Jul-2025)
Filesystem at /dev/mmcblk1p2 is mounted on /; on-line resizing required
old_desc_blocks = 2, new_desc_blocks = 15
The filesystem on /dev/mmcblk1p2 is now 31149568 (4k) blocks long.
```

## Step 6 - Verify Changes

Verify the changes.  You should see the partition on `/dev/root` filesystem expand to use most of the SD Card volume as shown below.

```shell
# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       115G  5.8G  105G   6% /
```
