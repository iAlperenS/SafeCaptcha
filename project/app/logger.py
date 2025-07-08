import logging
import os
from logging.handlers import RotatingFileHandler
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'time': self.formatTime(record, self.datefmt),
            'message': record.getMessage(),
            'name': record.name
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

def setup_logger(app=None):
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'app.log')

    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5, encoding='utf-8')
    handler.setLevel(logging.INFO)
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Debug moddaysa consola da yaz
    # If in debug write to console
    if app and app.config.get("DEBUG", False):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(JSONFormatter())
        logger.addHandler(console)