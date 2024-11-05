#!/bin/sh
echo "RUNNING KITSU DB BACKUP PROCESSES..."

# Get the current date and time in YYYYMMDD_HHMMSS format
CURRENT_DATETIME=$(date +"%Y%m%d_%H%M%S")

# Step 1: Database dump in the dynamically named container
echo "Starting database dump..."

# Ensure the backup directory exists in the container
mkdir -p /backup-dest/$DB_BACKUP_FOLDER

# Run the database dump command, setting the working directory
cd $DB_BACKUP_FOLDER && DB_PASSWORD=$DB_PASSWORD zou dump-database
