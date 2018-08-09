#!/bin/bash

GROUP=${3:-dev}
USER=$1
PASSWORD=$2

if grep -q $GROUP /etc/group
 then
      echo "$GROUP exits"
 else
      echo " $GROUP not exits"
      groupadd $GROUP
 fi

useradd $USER
usermod -aG wheel $USER
usermod -aG $GROUP $USER

passwd  $USER <<EOF
$PASSWORD
$PASSWORD
EOF

mkdir /home/$USER/.ssh
cp /home/centos/.ssh/auth* /home/$USER/.ssh/
chown -R $USER:$USER /home/$USER/.ssh

echo "$USER ALL=NOPASSWD: ALL" >> /etc/sudoers

