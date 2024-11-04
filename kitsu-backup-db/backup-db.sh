#!/bin/sh
echo "RUNING KITSU DB BACKUP PROCESSES..."

# Step 1: Database dump in the dynamically named container
echo "Starting database dump..."

# Ensure the backup directory exists in the container
mkdir -p /backup-dest/$DB_BACKUP_FOLDER

# Run the database dump command, setting the working directory
cd $DB_BACKUP_FOLDER && DB_PASSWORD=$DB_PASSWORD zou dump-database
