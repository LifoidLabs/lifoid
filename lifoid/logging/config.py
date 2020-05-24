import os


ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S.%s%z"


CONFIGURATION = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '%(name)s\t%(user)s\t%(levelname)s\t[%(asctime)s]\t%(message)s',
            'datefmt': ISO8601_DATETIME,
        },
        'onelineexception': {
            'class': 'lifoid.logging.formatter.OneLineFormatter',
            'format': '%(name)s\t%(user)s\t%(levelname)s\t[%(asctime)s]\t%(message)s',
            'datefmt': ISO8601_DATETIME,
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },

        'console': {
            'level': os.environ.get('LOGGING_CONSOLE_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },

        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('LOGGING_DEBUG_FILE', 'DEBUG'),
            'maxBytes': 536870912,  # 512 MB
            'formatter': 'simple',
        },

        'logfile': {
            'level': os.environ.get('LOGGING_FILE_LEVEL', 'INFO'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('LOGGING_FILE', 'LOG'),
            'maxBytes': 536870912,  # 512 MB
            'formatter': 'onelineexception',
        },

        'rotatedlogfile': {
            'level': os.environ.get('LOGGING_ROTATED_FILE_LEVEL', 'INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': os.environ.get('LOGGING_ROTATED_FILE_INTERVAL', 'H'),
            'filename': os.environ.get('LOGGING_ROTATED_FILE', 'ROTATED_LOG'),
            'formatter': 'onelineexception',
        }
    },

    'loggers': {
        '{}'.format(os.environ.get('LOGGING_SERVICE', 'process')): {
            'level': os.environ.get('LOGGING_LEVEL', 'INFO'),
            'handlers': os.environ.get('LOGGING_HANDLERS',
                                       'null').split(','),
            'propagate': 0,
        }
    },
}