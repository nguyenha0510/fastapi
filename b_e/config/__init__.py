import os
from b_e.helpers.config_utils import load_config
import logging.config

print("Loading config")

logging_config = os.path.join(os.path.dirname(__file__),
                              '../logging.conf')

config_file = os.path.join(os.path.dirname(__file__),
                           '../config.yaml')
config = None
if os.path.isfile(config_file):
    config = load_config(config_file)

logging.config.fileConfig(logging_config, disable_existing_loggers=False)
root_logger = logging.getLogger()
root_logger.handlers = []
log = logging.getLogger('action')
log.propagate = False

print("Config loaded successfully!")
