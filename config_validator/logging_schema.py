custom_logging_object = {
    'type': 'dictionary',
    'mandatory': {
        '()': {
            'type': 'not_empty_string'
        }  # TODO: check if it is a valid callable object
    },
    'strict_keys_set': False
}

logging_schema = {
    'type': 'dictionary',
    'mandatory': {
        'version': {
            'type': 'integer'
        }  # TODO: also check that always: value == 1
    },
    'optional': {
        'formatters': {
            'type': 'dictionary',
            'strict_keys_set': False,
            'allowed': [
                {
                    'type': 'dictionary',
                    'optional': {
                        'format': {'type': 'not_empty_string'},
                        'datefmt': {'type': 'not_empty_string'}  # TODO: check value is valid for time.strftime()
                    }
                },
                custom_logging_object
            ]
        },
        'filters': {
            'type': 'dictionary',
            'strict_keys_set': False,
            'allowed': [
                {
                    'type': 'dictionary',
                    'optional': {
                        'name': {'type': 'not_empty_string'}
                    }
                },
                custom_logging_object
            ]
        },
        'handlers': {
            'type': 'dictionary',
            'strict_keys_set': False,
            'allowed': [
                {
                    'type': 'dictionary',
                    'mandatory': {
                        'class': {'type': 'not_empty_string'}   # TODO: check the valid class name
                    },
                    'optional': {
                        'level': {'type': 'not_empty_string'},  # TODO: check it is valid level from logging module
                        'formatter': {'type': 'not_empty_string'},  # TODO: check if it is a key of formatters dict
                        'filters': {
                            'type': 'list',
                            'allowed': {'type': 'not_empty_string'}  # TODO: check if it is a key of filters dict
                        }
                    },
                    'strict_keys_set': False
                },
                custom_logging_object
            ]
        },
        'loggers': {
            'type': 'dictionary',
            'strict_keys_set': False,
            'allowed': {
                'type': 'dictionary',
                'optional': {
                    'propagate': {'type': 'boolean'},
                    'level': {'type': 'not_empty_string'},  # TODO: check it is valid level from logging module
                    'filters': {
                        'type': 'list',
                        'allowed': {'type': 'not_empty_string'}  # TODO: check if it is a key of filters dict
                    },
                    'handlers': {
                        'type': 'list',
                        'allowed': {'type': 'not_empty_string'}  # TODO: check if it is a key of handlers dict
                    }
                }
            }
        },
        'root': {
            'type': 'dictionary',
            'optional': {
                'level': {'type': 'not_empty_string'},  # TODO: check it is valid level from logging module
                'filters': {
                    'type': 'list',
                    'allowed': {'type': 'not_empty_string'}  # TODO: check if it is a key of filters dict
                },
                'handlers': {
                    'type': 'list',
                    'allowed': {'type': 'not_empty_string'}  # TODO: check if it is a key of handlers dict
                }
            }
        },
        'incremental': {'type': 'boolean'},
        'disable_existing_loggers': {'type': 'boolean'},
    },
}
