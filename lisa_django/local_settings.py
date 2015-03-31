# -*- coding: utf-8 -*-
import os
__author__ = 'nikitos'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'lisa',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'oracle',
        'PORT': '1521',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'systemlog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'system.log'),
            'formatter': 'standard',
        },


        'account': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'account.log'),
            'formatter': 'standard',
        },

          'reports': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'reports.log'),
            'formatter': 'standard',
        },


                'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'other.log'),
            'formatter': 'standard',
        },

        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['systemlog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'account.views': {
            'handlers': ['console', 'account'],
            'level': 'DEBUG',
        },        'reports.views': {
            'handlers': ['console', 'reports'],
            'level': 'DEBUG',
        },
    }
}
