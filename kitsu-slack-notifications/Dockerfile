# Dockerfile for backup container
FROM python:3.10-buster

# Install rsync, cron, and tzdata
RUN apt update && apt install -y rsync tzdata cron && rm -rf /var/lib/apt/lists/*

# Set up Python virtual environment
RUN python3 -m venv /opt/venv
RUN mkdir -p /etc/cron.d

# Copy necessary files
COPY ./requirements.txt requirements.txt
COPY ./slack-set-notifications.py /

# Install Python dependencies
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Configure cron job
RUN echo "*/15 * * * * root . /opt/venv/bin/activate && python /slack-set-notifications.py >> /proc/1/fd/1 2>&1" > /etc/cron.d/slack-job

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/slack-job

# Apply the cron job
RUN crontab /etc/cron.d/slack-job

# Run cron in the foreground
CMD ["cron", "-f"]
