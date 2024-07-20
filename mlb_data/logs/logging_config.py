import os
import logging
import logging.config

log_path = os.path.join(os.path.dirname(__file__), 'project.log')

def setup_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': log_path,
            },
        },
        'loggers': {
            'root': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

    logging.config.dictConfig(logging_config)
