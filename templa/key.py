# -*- coding: utf-8 -*-

import curses

SP_KEYS = {
    curses.KEY_DOWN: "next_line",
    curses.KEY_UP: "prev_line",
    curses.KEY_BACKSPACE: "backspace",
    127: "backspace",
}


class KeyHandler(object):

    def __init__(self, key):
        self.key = key
        self.operate = SP_KEYS.get(key)
