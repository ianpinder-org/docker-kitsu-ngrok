#!/bin/sh
echo "RUNING KITSU BACKUP PROCESSES..."


# Step 2: Rsync backup process
echo "Starting rsync backup..."


# Define the destination directory for the backup
DEST="/backup-dest/${PREVIEWS_BACKUP_SUBFOLDER}"
if [ ! -d "$DEST" ]; then
  echo "Creating backup destination $DEST."
  mkdir -p "$DEST"
fi

# Run the rsync command
# rsync -av --delete "/backup-source/" "$DEST/"
rsync -av "/backup-source/" "$DEST/"



if [ $? -eq 0 ]; then
    echo "Previews backup completed successfully."
else
    echo "Previews backup encountered an error."
fi


