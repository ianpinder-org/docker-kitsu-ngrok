# Dockerfile for backup container
FROM alpine:latest

# Install rsync and cron
RUN apk update && apk add --no-cache rsync tzdata

RUN touch /var/log/slack-set-notifications.log

# Copy backup script to container
COPY ./slack-set-notifications.sh /

# Configure cron job to run the backup
RUN echo "0 9,12,15,18,21,0 * * * /slack-set-notifications.sh >> /var/log/slack-set-notifications.log 2>&1" > /etc/crontabs/root


# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/slack-set-notifications.log"]