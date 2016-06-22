# -*- coding: utf-8 -*-

import curses
from config import Config

SPECIAL_KEYS = {
    curses.KEY_DOWN      : "down",
    curses.KEY_UP        : "up",
    curses.KEY_BACKSPACE : "backspace",
    curses.KEY_ENTER     : "enter",
    127                  : "backspace",
}


class KeyHandler(object):

    def __init__(self):
        self.conf = Config()
        self.keymap = self.build_keymap()
        self.hold_key = None
        self.state = None

    def build_keymap(self):
        keymap = {}

        for key, command in self.conf.keymap.items():
            if key != '__name__':
                keymap[key] = command

        return keymap

    def handle_key(self, key):

        if self.is_special_key(key):
            self.hold_key = key
            self.state = self.keymap[SPECIAL_KEYS[key]]

        elif self.is_displayable_key(key):
            self.hold_key = chr(key)
            self.state = 'input_query'

        elif self.is_multibyte_key(self):
            # TODO support multibyte
            pass

    def is_displayable_key(self, key):
        return 32 <= key <= 126

    def is_multibyte_key(self, key):
        pass

    def is_special_key(self, key):
        return True if key in SPECIAL_KEYS.keys() else False

    def debug_keyhandler(self):
        print u'hold_key:"{key}", state:"{state}"'.format(key=self.hold_key,
                                                          state=self.state)

    @property
    def is_input_query(self):
        return True if self.state == 'input_query' else False
