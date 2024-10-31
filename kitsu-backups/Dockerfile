# Dockerfile for backup container
FROM alpine:latest

# Install rsync and cron
RUN apk add --no-cache rsync tzdata

# Set environment variables for cron schedule, source, and destination
# ARG USER_ID
# ARG GROUP_ID
# ARG NAS_USER

# Add user and group
# RUN addgroup -g $GROUP_ID $NAS_USER && \
#     adduser -u $USER_ID -G $NAS_USER -m $NAS_USER

# USER $NAS_USER

RUN touch /var/log/backup.log

# Create the backup script with error handling and ensure subfolder creation at runtime
RUN echo '#!/bin/sh' > /backup.sh && \
    echo 'echo "Starting rsync backup..."' >> /backup.sh && \
    echo 'if [ ! -d "$RSYNC_SRC" ]; then' >> /backup.sh && \
    echo '  echo "Source directory $RSYNC_SRC does not exist. Exiting."' >> /backup.sh && \
    echo '  exit 1' >> /backup.sh && \
    echo 'fi' >> /backup.sh && \
    echo 'DEST="$RSYNC_DEST/$BACKUP_SUBFOLDER"' >> /backup.sh && \
    echo 'if [ ! -d "$DEST" ]; then' >> /backup.sh && \
    echo '  echo "Creating backup destination $DEST."' >> /backup.sh && \
    echo '  mkdir -p "$DEST"' >> /backup.sh && \
    echo 'fi' >> /backup.sh && \
    echo 'rsync -av --delete "$RSYNC_SRC/" "$DEST/"' >> /backup.sh && \
    echo 'echo "Backup completed."' >> /backup.sh && \
    chmod +x /backup.sh

# Configure cron job to run the backup every 2 minutes
RUN echo "0 1,13 * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root

# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/backup.log"]

