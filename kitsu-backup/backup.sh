#!/bin/sh
echo "RUNING KITSU BACKUP PROCESSES..."


# Step 2: Rsync backup process
echo "Starting rsync backup..."
# if [ ! -d "$RSYNC_SRC" ]; then
#   echo "Source directory $RSYNC_SRC does not exist. Exiting."
#   exit 1
# fi

# Define the destination directory for the backup
DEST="/backup-dest/${PREVIEWS_BACKUP_SUBFOLDER}"
if [ ! -d "$DEST" ]; then
  echo "Creating backup destination $DEST."
  mkdir -p "$DEST"
fi

# Run the rsync command
rsync -av --delete "/backup-source/" "$DEST/"
echo "Backup completed."
