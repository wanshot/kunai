# -*- coding: utf-8 -*-

import curses

SPECIAL_KEYS = {
    curses.KEY_DOWN      : "next_line",
    curses.KEY_UP        : "prev_line",
    curses.KEY_BACKSPACE : "backspace",
    curses.KEY_ENTER     : "enter",
    127                  : "backspace",
}


KEY_MAP = {}


class KeyHandler(object):

    def __init__(self):
        self.hold_key = None

    def handle_key(self, key):

        if self.is_special_key(key):
            self.hold_key = SPECIAL_KEYS[key]

        elif self.is_displayable_key(key):
            self.hold_key = chr(key)

        elif self.is_multibyte_key(self):
            # TODO support multibyte
            pass

    def is_displayable_key(self, key):
        return 32 <= key <= 126

    def is_multibyte_key(self, key):
        pass

    def is_special_key(self, key):
        return True if key in SPECIAL_KEYS.keys() else False
