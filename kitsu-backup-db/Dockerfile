# Use Alpine as a base image
FROM alpine:latest

# Install PostgreSQL client and cron
RUN apk update && apk add --no-cache postgresql-client rsync tzdata


# Copy the backup script and cron job
COPY ./backup-db.sh /

# Make the backup script executable
# RUN chmod +x /backup-db.sh && \
#     touch /backup.log
RUN chmod +x /backup-db.sh


# Configure cron job to run the backup every 2 minutes
# RUN echo "*/2 * * * * /backup-db.sh >> /backup.log 2>&1" > /etc/crontabs/root
# RUN echo "0 9,12,15,18,21,0 * * * /backup-db.sh >> /backup.log 2>&1" > /etc/crontabs/root
RUN echo "0 9,12,15,18,21,0 * * * /backup-db.sh" > /etc/crontabs/root


# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
CMD ["sh", "-c", "crond -f -l 8"]


