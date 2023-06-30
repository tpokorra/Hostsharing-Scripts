#!/bin/bash

df -h | grep -v /run/user

# define in crontab: DISKSPACE_GB HOST MAILADDR


# required space in GB
if [[ -z $DISKSPACE_GB ]]; then
    DISKSPACE_GB=5
fi
freespace=`df -h | grep -E '/dev/sda2 ' | awk '{ print $4; }'`
if [[ ! "${freespace: -1}" == "G" ]]
then
  error="Unexpected free space: "$freespace
else
  value=`echo $freespace | tr -d G`
  if (( $(echo "$value < $DISKSPACE_GB" |bc -l) ))
  then
    error="Zu wenig Speicherplatz: "$freespace
  fi
fi

if [ ! -z "$error" ]
then
   echo $error

   if [[ ! -z $MAILADDR ]]; then
     echo "$error" | mail -s "Zuwenig Speicherplatz auf $HOST" -a "From: errors@$HOST" $MAILADDR
   fi
fi
