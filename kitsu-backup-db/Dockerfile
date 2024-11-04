# Use Alpine as a base image
FROM alpine:3.16

# Install PostgreSQL client and cron
RUN apk update && apk add --no-cache postgresql-client cronie

# Create backup and log directories
RUN mkdir -p /opt/backups && mkdir -p /var/log/cron

# Copy the backup script and cron job
COPY backup-db.sh /opt/backups/backup-db.sh
COPY backup-cron /etc/crontabs/root

# Make the backup script executable
RUN chmod +x /opt/backups/backup-db.sh

# # Start cron in the foreground
# CMD ["crond", "-f", "-l", "8"]


# Configure cron job to run the backup every 2 minutes
RUN echo "*/2 * * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root
# RUN echo "0 1,13 * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root

# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/backup.log"]
