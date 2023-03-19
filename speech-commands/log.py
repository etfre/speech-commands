import logging
import os.path

from logging.config import fileConfig

fileConfig(os.path.join('..', 'logging.ini'))
logger = logging.getLogger('speech-commands')
