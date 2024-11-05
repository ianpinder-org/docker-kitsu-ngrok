FROM python:3.10-buster

RUN python3 -m venv /opt/venv

# ADD src /usr/project
RUN mkdir -p /usr/project

WORKDIR /usr/project
COPY ./requirements.txt requirements.txt
COPY ./kitsu-events.py kitsu-events.py 
COPY ./messages.py messages.py 

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Run the application:
CMD . /opt/venv/bin/activate && exec python kitsu-events.py