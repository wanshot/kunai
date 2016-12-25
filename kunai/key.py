# -*- coding: utf-8 -*-

import curses
from config import Config

KUNAI_KEYS = {
    curses.KEY_DOWN      : 'down',
    curses.KEY_UP        : 'up',
    curses.KEY_BACKSPACE : 'backspace',
    curses.KEY_ENTER     : 'enter',
    127                  : 'backspace',
}


class KeyHandler(object):

    def __init__(self):
        self.conf = Config()
        self.keymap = self.build_keymap()
        self.current_key = None
        self.has_query = None
        self.command = None

    def build_keymap(self):
        """Bind config keymap with curses keymap
        """
        keymap = {}

        for key, command in self.conf.keymap.items():
            if key != '__name__':
                keymap[key] = command
            if key == 'enter':
                keymap['ctrl-m'] = command

        return keymap

    def handle_key(self, key):

        if self.has_kunai_key(key):
            self.command = self.keymap[KUNAI_KEYS[key]]
            self.has_query = False

        elif self.is_displayable_key(key):
            self.current_key = chr(key)
            self.has_query = True

        elif self.is_ctrl_masked_key(key):
            key = self.ctrl_masked_key_to_str(key)
            self.command = self.keymap[key]
            self.has_query = False

        elif self.is_utf8_multibyte_key(key):
            self.current_key = key
            self.has_query = True

    def is_displayable_key(self, key):
        return 32 <= key <= 126

    def is_utf8_multibyte_key(self, key):
        return (key & 0b11000000) == 0b11000000

    def has_kunai_key(self, key):
        """
        """
        return KUNAI_KEYS.get(key)

    def is_ctrl_masked_key(self, key):
        """

        ANSI.SYS Ctrl Key codes range
        """
        return 1 <= key <= 27

    def debug_keyhandler(self):
        print (u'current_key:{s.current_key}\n'
               u'command:{s.command}\n'
               u'has_query:{s.has_query}'.format(s=self))

    def ctrl_masked_key_to_str(self, key):
        prefix = 'ctrl-'
        # ANSY normal key start from 96 ~
        return prefix + chr(key + 96)
