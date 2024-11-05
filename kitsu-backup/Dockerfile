# Dockerfile for backup container
FROM alpine:latest

# Install rsync and cron
RUN apk update && apk add --no-cache rsync tzdata

RUN touch /var/log/backup.log

# Copy backup script to container
COPY ./backup.sh /

# Configure cron job to run the backup
# RUN echo "*/5 * * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root
# RUN echo "0 1,13 * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root
RUN echo "0 9,12,15,18,21,0 * * * /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root


# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/backup.log"]