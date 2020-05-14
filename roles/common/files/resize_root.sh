#!/bin/bash

ls /dev/mapper/ceph-* | xargs -I% -- sudo dmsetup remove %
rm -rf /dev/ceph-*
rm -rf /dev/mapper/ceph-*
rm -rf /var/lib/rook
wipefs -a /dev/sdb

(
echo d # Delete sda1
echo 1 # Delete sda1
echo d # Delete sda2
echo 2 # Delete sda2
echo d # Delete sda3
echo 3 # Delete sda3
echo d # Delete sda4
echo 4 # Delete sda4

echo n    # Add a new partition
echo p    # Primary partition
echo 1    # Partition number
echo      # First sector (Accept default: 1)
echo +50G # Create 50G disk
echo a    # Make bootable

echo n    # Add a new partition
echo p    # Primary partition
echo 2    # Partition number
echo      # First sector (Accept default: 1)
echo +1G  # Create 50G disk

echo n    # Add a new partition
echo p    # Primary partition
echo 3    # Partition number
echo      # First sector (Accept default: 1)
echo +1G  # Create 50G disk

echo n    # Add a new partition
echo p    # Primary partition
echo 4    # Partition number
echo      # First sector (Accept default: 1)
echo      # Create disk to end

echo w
) | fdisk /dev/sda

