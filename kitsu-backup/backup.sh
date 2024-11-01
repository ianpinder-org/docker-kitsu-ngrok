#!/bin/sh
echo "RUNING KITSU BACKUP PROCESSES..."

# Define the container name dynamically using COMPOSE_PROJECT_NAME
ZOU_APP_CONTAINER="${COMPOSE_PROJECT_NAME}_zou-app"

# Step 1: Database dump in the dynamically named container
echo "Starting database dump in the $ZOU_APP_CONTAINER container..."

# Ensure the backup directory exists in the container
docker exec "$ZOU_APP_CONTAINER" sh -c "mkdir -p /opt/zou/previews/db-backups"

# Run the database dump command, setting the working directory
docker exec "$ZOU_APP_CONTAINER" sh -c "cd /opt/zou/previews/db-backups && DB_PASSWORD=$DB_PASSWORD zou dump-database"

echo "Database dump completed."

# Step 2: Rsync backup process
echo "Starting rsync backup..."
if [ ! -d "$RSYNC_SRC" ]; then
  echo "Source directory $RSYNC_SRC does not exist. Exiting."
  exit 1
fi

# Define the destination directory for the backup
DEST="${RSYNC_DEST}/${BACKUP_SUBFOLDER}"
if [ ! -d "$DEST" ]; then
  echo "Creating backup destination $DEST."
  mkdir -p "$DEST"
fi

# Run the rsync command
rsync -av --delete "$RSYNC_SRC/" "$DEST/"
echo "Backup completed."
