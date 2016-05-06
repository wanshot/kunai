# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser

# from .exceptions import ConfigLoadError
# from tempra.exceptions import ConfigLoadError

TEMPRA_ROOT_DIRECTORY = os.path.expanduser('~/.tempra/')
TEMPRA_CONF_PATH = TEMPRA_ROOT_DIRECTORY + 'temprarc'

DEFAULT_CONFIG = """
[prompt]
# DEFAULT: `> `
INPUT_FIELD_LABEL =

[normal line options]
BOLD = False
UNDERLINE = False

[select line options]
BOLD = True
UNDERLINE = True

[normal line color]
FG = white
BG = black

[select line color]
FG = white
BG = blue

[markup color]
color = yellow

"""


def make_tempra_config_file():
    if not os.path.exists(TEMPRA_ROOT_DIRECTORY):
        os.makedirs(TEMPRA_ROOT_DIRECTORY)
    with open(TEMPRA_CONF_PATH, 'w+') as file:
        file.write(DEFAULT_CONFIG)


class LoadConfig(object):

    def __init__(self):
        self._check_config()
        self._load()

    def _check_config(self):
        if not os.path.exists(TEMPRA_ROOT_DIRECTORY):
            raise IndexError('.tempra directory is not found')
        if not os.path.isfile(TEMPRA_CONF_PATH):
            raise IndexError('temprarc is not found')

    def _load(self):
        conf = SafeConfigParser()
        conf.read(TEMPRA_CONF_PATH)

        self.input_field_label = conf.get('prompt', 'INPUT_FIELD_LABEL')

        self.normal_line_color = conf._sections['normal line color']
        self.select_line_color = conf._sections['select line color']

        self.normal_line_options = conf._sections['normal line options']
        self.select_line_options = conf._sections['select line options']

        self.markup_color = conf._sections['markup color']

if __name__ == "__main__":
    make_tempra_config_file()
