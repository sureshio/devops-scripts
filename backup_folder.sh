#!/bin/bash
#Purpose = Backup of Important Data
#Version 1.0

STARTTIME=$(date +%s)
DATA_FOLER=/opt/dockerbox/data
BACKUP_FOLDER=/opt/s3box/backups
EXCLUDES=${1:-NONE}

echo -e " Starting Backup `date` \n  " 

while getopts d:b: option
do
        case $option in
                b)
		    BACKUP_FOLDER=${OPTARG};
					;;
	        d)
               	    DATA_FOLER=${OPTARG};
                	;;
                \?) echo "Unknown option: -$OPTARG" >&2; phelp; exit 1;;
        		:) echo "Missing option argument for -$OPTARG" >&2; phelp; exit 1;;
        		*) echo "Unimplimented option: -$OPTARG" >&2; phelp; exit 1;;
        esac
done


TIME=`date +%y%m%d-%H%M`            # This Command will add date in Backup File Name.

if [ ! -d "$DATA_FOLER" ]; then
  echo "Data Folder $DATA_FOLER folder does not exist"
  exit 0
fi

if [ ! -d "$BACKUP_FOLDER" ]; then
  echo "Backup $BACKUP_FOLDER folder does not exist"
  exit 0
fi
 

for i in $(ls -d ${DATA_FOLER}/*); 
    do 
        SRCDIR=${i};
        APP_DIR=`echo $SRCDIR | rev | cut -d"/" -f1 | rev`


        if [ ! -d "$BACKUP_FOLDER/$APP_DIR" ]; then
            echo "Creating dir  $BACKUP_FOLDER/$APP_DIR "
            mkdir -p $BACKUP_FOLDER/$APP_DIR
        fi
        	
        TAR_FILENAME=${APP_DIR}-${TIME}.tar.gz
        FILENAME=$BACKUP_FOLDER/$APP_DIR/${TAR_FILENAME}    # Here i define Backup file name format.
        LATEST_BACKUP_LINK=$BACKUP_FOLDER/$APP_DIR/latest
         

      echo /usr/bin/tar -cpzf $FILENAME -C $DATA_FOLER  $APP_DIR --exclude $EXCLUDES
      /usr/bin/tar -cpzf $FILENAME -C $DATA_FOLER  $APP_DIR --exclude $EXCLUDES
    
      if [ -f $FILENAME ] ; then
	chmod 400 $FILENAME
        rm $LATEST_BACKUP_LINK
        ln -s ./${TAR_FILENAME} $LATEST_BACKUP_LINK
      fi
      
      echo " Backup file Size  `du -sh $FILENAME`"
    done
    
   echo "Top 10 Data folder by size"
   du -m $DATA_FOLER/*  | sort -nr | head -n 10 
ENDTIME=$(date +%s)
echo -e "It took $(($ENDTIME - $STARTTIME)) seconds to complete this task..." 

