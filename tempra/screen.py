# -*- coding: utf-8 -*-

import curses
import signal
import unicodedata
from .manage import ConfigLoader


class Screen(object):

    def __init__(self, ret):
        self.conf = ConfigLoader()

#     def __enter__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        # Invalidation Ctrl + z
        signal.signal(signal.SIGINT, lambda signum, frame: None)
        curses.raw()
        curses.noecho()
        curses.cbreak()
        curses.nonl()
        self.stdscr.keypad(1)

        self.height, self.width = self.stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self._set_input_area()

        curses.curs_set(0)

        self.line_storege = []
        for idx, line in enumerate(ret, start=1):
            adapt_line = self._adapt_line(line)
            self.stdscr.addstr(idx, 0, line)
            self.line_storege.append(adapt_line)
        self.stdscr.move(0, 6)

    def _set_input_area(self):
        label = 'input:'
        if self.conf.input_field_label:
            label = self.conf.input_field_label
        self.stdscr.addstr(0, 0, '{}'.format(label))

    def _adapt_line(self, line):
        unicodelize = line.decode('utf-8')
        picked = len([u for u in unicodelize if unicodedata.east_asian_width(u) in ('F', 'W')])
        unicode_diff = len(unicodelize) - picked
        max_line = unicode_diff + (picked * 2)
        diff_byte = self.width - max_line
        return line + diff_byte * " "

    def __exit__(self, exc_type, exc_value, traceback):
        curses.nl()
        curses.endwin()
