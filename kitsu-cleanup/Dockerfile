# Dockerfile for backup container
FROM alpine:latest

# Install rsync and cron
RUN apk update && apk add --no-cache rsync tzdata

# RUN touch /var/log/cleanup.log
RUN mkdir -p  /opt/zou/tmp
RUN echo "Temp file removal cron job setup starting..."

# Configure cron job to run the backup
# RUN echo "0 2 * * * /usr/bin/find /opt/zou/tmp/ -mtime +5 -exec rm {} \; >> /var/log/backup.log 2>&1" > /etc/crontabs/root
RUN echo "0 2 * * * /usr/bin/find /opt/zou/tmp/ -mtime +5 -exec rm {} \;" > /etc/crontabs/root


# Start cron daemon in foreground to capture logs in stdout and stderr
# CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/cleanup.log"]
CMD ["sh", "-c", "crond -f -l 8"]
