import logging
import logging.config

OUTPUT_RESOLUTION = "1280:1080"

LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
            },
            # 'file': {
            #     'class': 'logging.FileHandler',
            #     'filename': 'mplog.log',
            #     'mode': 'w',
            #     'formatter': 'detailed',
            # },
            # 'foofile': {
            #     'class': 'logging.FileHandler',
            #     'filename': 'mplog-foo.log',
            #     'mode': 'w',
            #     'formatter': 'detailed',
            # },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-errors.log',
                'mode': 'w',
                'level': 'ERROR',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            # 'foo': {
            #     'handlers': ['foofile']
            # }
            # 'aiotg': {
            #     'level': 'DEBUG',
            #     'handlers': ['console', 'errors'],
            # },
            # 'bot':{
            #     'level': 'DEBUG',
            #     'handlers': ['console', 'errors'],
            # }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'errors']
        },
    }

logging.config.dictConfig(LOGGING_CONFIG)
