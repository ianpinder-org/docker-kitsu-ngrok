from flask import current_app

def handle_event(data):
    current_app.logger.info("\n\n\n\nTask update event occured!\n\n\n")