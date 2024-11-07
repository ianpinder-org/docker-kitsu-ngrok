# Dockerfile for backup container
FROM alpine:latest

# Install rsync and cron
RUN apk update && apk add --no-cache rsync tzdata

RUN touch /var/log/slack-set-notifications.log

RUN python -m venv /opt/venv

COPY ./requirements.txt requirements.txt
COPY ./slack-set-notifications.sh /

RUN . /opt/venv/bin/activate && pip install -r requirements.txt


# Configure cron job to run the backup
# RUN echo "0 9,12,15,18,21,0 * * * /slack-set-notifications.sh >> /var/log/slack-set-notifications.log 2>&1" > /etc/crontabs/root
RUN echo "0 9,12,15,18,21,0 * * * /slack-set-notifications.sh" > /etc/crontabs/root


# Start cron daemon and tail log in foreground to capture logs in stdout and stderr
# CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/slack-set-notifications.log"]
CMD ["sh", "-c", "crond -f -l 8"]
