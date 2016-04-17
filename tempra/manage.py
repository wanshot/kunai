# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser

from .exceptions import ConfigLoadError

TEMPRA_ROOT_DIRECTORY = os.path.expanduser('~/.tempra/')
TEMPRA_CONF_PATH = TEMPRA_ROOT_DIRECTORY + 'temprarc'

DEFAULT_CONFIG = """
[views]
# DEFAULT: `Input:`
# INPUT_FIELD_LABEL =
"""


def make_tempra_config_file():
    if not os.path.exists(TEMPRA_ROOT_DIRECTORY):
        os.makedirs(TEMPRA_ROOT_DIRECTORY)
    with open(TEMPRA_CONF_PATH, 'w+') as file:
        file.write(DEFAULT_CONFIG)


class ConfigLoader(object):

    def __init__(self):
        self._check_config()
        self._load_config()

    def _check_config(self):
        if not os.path.exists(TEMPRA_ROOT_DIRECTORY):
            raise ConfigLoadError('.tempra directory is not found')
        if not os.path.isfile(TEMPRA_CONF_PATH):
            raise ConfigLoadError('temprarc is not found')

    def _load_config(self):
        conf = SafeConfigParser()
        conf.read(TEMPRA_CONF_PATH)
        self.input_field_label = conf.get('views', 'INPUT_FIELD_LABEL')


if __name__ == "__main__":
    make_tempra_config_file()
