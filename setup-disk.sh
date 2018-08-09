#!/bin/bash

DEVICE_NAME=${1:-/dev/xvdf}
MOUNT_DIR=${2:-/opt/stackdata}

if [ -f /dev/xvdf ] && [ ! grep -q xvdf /etc/fstab ] ; then

mkfs -t ext4 $DEVICE_NAME

mkdir -p  $MOUNT_DIR

mount $DEVICE_NAME $MOUNT_DIR

echo -e "\n${DEVICE_NAME}    ${MOUNT_DIR}   ext4    defaults,nofail        0       2" >> /etc/fstab

fi
