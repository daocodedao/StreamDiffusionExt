import sys
import logging
from logging.config import dictConfig
import os

logging_config = dict(
    version=1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(module)s:%(lineno)s] %(message)s"),
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'api-logger': {'class': 'logging.handlers.RotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': 'logs/api.log',
                           'maxBytes': 52428800,
                           'backupCount': 7},
        'batch-process-logger': {'class': 'logging.handlers.RotatingFileHandler',
                             'formatter': 'verbose',
                             'level': logging.DEBUG,
                             'filename': 'logs/batch.log',
                             'maxBytes': 52428800,
                             'backupCount': 7},
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
    loggers={
        'api_logger': {
            'handlers': ['api-logger', 'console'],
            'level': logging.DEBUG
        },
        'batch_process_logger': {
            'handlers': ['batch-process-logger', 'console'],
            'level': logging.DEBUG
        }
    }
)


logPath = os.path.dirname("logs/api.log")
if not os.path.exists(logPath): 
    os.makedirs(logPath, exist_ok=True)

dictConfig(logging_config)

api_logger = logging.getLogger('api_logger')
batch_process_logger = logging.getLogger('batch_process_logger')