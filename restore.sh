#!/bin/bash
#Purpose = restore a backup
#Version 1.0

STARTTIME=$(date +%s)

if [ -z "$1" ]; then
 echo "Usage: restore.sh <archive name>"
 exit 0;
fi

ARCHIVE=${1}
DESDIR=${2:-`pwd`}


if [ ! -d "$DESDIR" ]; then
 sudo mkdir -p $DESDIR
fi

echo tar -xpzf $ARCHIVE -C $DESDIR
sudo tar -xpzf $ARCHIVE -C $DESDIR



ENDTIME=$(date +%s)

echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete this task..."