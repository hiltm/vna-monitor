#!/bin/bash

#get current date for folder name to check
date=$(date '+%Y%m%d')

#monitor this directory
WATCH_DIR="/home/chiptamper/chiptamper/data/${date}"
#upload to this directory
DEST_DIR="/home/chiptamper/ecresearch/data/${date}"

if [ ! -d "$DEST_DIR" ]; then
   sudo mkdir -p "$DEST_DIR"
   echo "made directory ${DEST_DIR}"
else
   echo "directory ${DEST_DIR} already exists"
fi

#time to wait after the last file writing before uploading in seconds
INACTIVITY_TIME=300

#tmp file to track the last modifition time of files
LAST_MOD_TIME="/tmp/last_mod_time.txt"

if [ ! -d "$LAST_MOD_TIME" ]; then
   sudo touch "$LAST_MOD_TIME"
   echo "made file ${LAST_MOD_TIME}"
else
   echo "file ${LAST_MOD_TIME} already exists"
fi

upload_data() {
   echo "Uploading data"
   scp -p $WATCH_DIR/* $DEST_DIR
}

monitor_dir() {
   inotifywait -m -r -e modify,create,move,delete "$WATCH_DIR" | while read -r path action file; do
      CURRENT_TIME=$(date +%s)

      #get the time of the last modification from the tmp file
      if [ -f "$LAST_MOD_TIME" ]; then
         LAST_TIME=$(cat "$LAST_MOD_TIME")
      else
         LAST_TIME=0
      fi

      #backup data if enough time has passed since the last upload
      if (( CURRENT_TIME - LAST_TIME >= INACTIVITY_TIME )); then
         upload_data
      fi

      #update last modification time
      echo $CURRENT_TIME > "$LAST_MOD_TIME"
   done
}

#start the monitoring process
echo "Starting process"
monitor_dir
