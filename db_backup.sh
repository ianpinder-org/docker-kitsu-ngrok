#!/bin/sh
echo "RUNNING KITSU DB BACKUP PROCESS..."

# Get the current date and time in YYYYMMDD_HHMMSS format
CURRENT_DATETIME=$(date +"%Y%m%d_%H%M%S")

# Step 1: Database dump in the dynamically named container
echo "Starting database dump..."

# Ensure the backup directory exists in the container
mkdir -p /backup-dest/$DB_BACKUP_FOLDER


# Define the destination directory for the backup
DEST="/backup-dest/${DB_BACKUP_SUBFOLDER}"
if [ ! -d "$DEST" ]; then
  echo "Creating backup destination $DEST."
  mkdir -p "$DEST"
fi

cd /backup-dest/$DB_BACKUP_SUBFOLDER

# Run the pg_dump command with the dynamically generated filename
PGPASSWORD=$DB_PASSWORD pg_dump -h $BACKUP_DB_HOST -U $BACKUP_DB_USERNAME -d $BACKUP_DB_DATABASE > "$DEST/gwkitsu_db_backup_$CURRENT_DATETIME.sql"


if [ $? -eq 0 ]; then
    echo "Database backup completed successfully."
else
    echo "Database backup encountered an error."
fi

