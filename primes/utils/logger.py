import os
import logging.config
import json


def setup_logging(default_path='primes/conf/logging.json',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """Reads configuration for the logger from a json file.
    
    See: http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python

    Keyword Arguments:
        default_path -- the path to the json config file.
        default_level -- the default level of logging for all loggers.
        env_key -- environment variable for logging config location.
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
