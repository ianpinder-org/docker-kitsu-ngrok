FROM postgres:15-alpine

# Define build-time arguments
# ARG PGUSER
ARG PGPASSWORD


# Install cron for scheduled backups
RUN apk update && apk add --no-cache cronie

# Create directories for backups and logs
# RUN mkdir -p /opt/backups && mkdir -p /var/log/cron
RUN touch /var/log/backup.log

# Copy the backup script and make it executable
COPY ./backup-db.sh /backup-db.sh
RUN chmod +x /backup-db.sh

# # Copy the cron job
# COPY backup-cron /etc/crontabs/root

# Configure cron job to run the backup at 12:45 and 00:45
# RUN echo "45 0,12 * * * /backup-db.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root
RUN echo "45 0,12 * * * /backup-db.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root


# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/backup.log"]
