# -*- coding: utf-8 -*-

import curses

SP_KEYS = {
    curses.KEY_DOWN: "next_line",
    curses.KEY_UP: "prev_line",
    curses.KEY_BACKSPACE: "backspace",
    127: "backspace",
}

KEY_MAP = {}


class KeyHandler(object):

    def __init__(self, key):
        self.ch = None
        self.operate = None

        self.handel_key(key)

    def handel_key(self, key):
        if self._is_special_key(key):
            self.operate = SP_KEYS[key]
        elif self._is_displayable_key(key):
            self.ch = chr(key)
        elif self._is_multibyte_key(self):
            # TODO support multibyte
            pass

    def _is_displayable_key(self, key):
        return 32 <= key <= 126

    def _is_multibyte_key(self, key):
        pass

    def _is_special_key(self, key):
        return True if key in SP_KEYS.keys() else False
