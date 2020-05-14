#!/bin/bash

# NOTES:
# on a new setup /etc/hostname is not present on system -> this script adds this manually

#if ! grep -q "$NODE_NAME" /etc/hosts; then
#    echo "Adding hostname to /etc/hosts ..."
#    echo "127.0.0.1 $NODE_HOSTNAME $NODE_NAME localhost" >> /etc/hosts
#    echo "127.0.1.1 $NODE_HOSTNAME $NODE_NAME localhost" >> /etc/hosts
#fi

NODE_HOSTNAME="$1"

hostname "$NODE_HOSTNAME"
echo "$NODE_HOSTNAME" > /etc/hostname
