#!/bin/bash
yum install -y wget 

HOST_PREFIX=${1:-$HOST_PREFIX}
NODE_PREFIX=${HOST_PREFIX:-aws-dev}
INSTANCE_ID=$(curl -s "http://169.254.169.254/latest/meta-data/instance-id")
echo node prefix: ${NODE_PREFIX}
NODE_NAME=${NODE_PREFIX}-${INSTANCE_ID:0:10}
echo setting node name to ${NODE_NAME}
hostnamectl set-hostname ${NODE_NAME}



echo -e "\npreserve_hostname: true " >> /etc/cloud/cloud.cfg

