# Accept the ZOU_VERSION argument with a default fallback
ARG ZOU_VERSION

# Base image with specified ZOU_VERSION or defaults to 'latest'
FROM registry.gitlab.com/mathbou/docker-cgwire/zou:${ZOU_VERSION:-latest}

# Accept the EVENT_HANDLERS_FOLDER argument
ARG EVENT_HANDLERS_FOLDER

# Ensure that the EVENT_HANDLERS_FOLDER variable is used correctly in both build and runtime
ENV EVENT_HANDLERS_FOLDER=${EVENT_HANDLERS_FOLDER}

# Create the event handlers folder
RUN mkdir -p "$EVENT_HANDLERS_FOLDER" \
    && echo "Event handlers folder: $EVENT_HANDLERS_FOLDER"

# Copy event handler scripts into the specified folder
COPY ./kitsu-event-handlers/. "$EVENT_HANDLERS_FOLDER"


# CMD ["gunicorn", "--error-logfile", "-", "--access-logfile", "-", "-w 3 -k gevent", "-b", ":5000 zou.app:app"]

# CMD ["sh", "-c", "crond -f -l 8 & tail -f /var/log/backup.log"]

# CMD "gunicorn --error-logfile - --access-logfile - -w 3 -k gevent -b :5000 zou.app:app"