# -*- coding: utf-8 -*-

import curses
import signal
import unicodedata
from collections import OrderedDict

from manage import ConfigLoader


class Screen(object):

    def __init__(self, ret):
        self.ret = ret
        self.conf = ConfigLoader()
        self.line_storege = OrderedDict()

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        # Invalidation Ctrl + z
        signal.signal(signal.SIGINT, lambda signum, frame: None)
        curses.raw()
        curses.noecho()
        curses.cbreak()
        curses.nonl()
        self.stdscr.keypad(True)

        self.height, self.width = self.stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self._set_input_label()

        curses.curs_set(0)

        for idx, line in enumerate(self.ret, start=1):
            adapt_line = self._adapt_line(line)
            if idx == 1:
                self.stdscr.addstr(idx, 0, adapt_line, curses.color_pair(1))
            else:
                self.stdscr.addstr(idx, 0, line)
            self.line_storege[idx] = adapt_line
        self.stdscr.move(0, 6)

        return self

    def _set_input_label(self):
        label = 'input:'
        if self.conf.input_field_label:
            label = self.conf.input_field_label
        self.stdscr.addstr(0, 0, '{}'.format(label))

    def _adapt_line(self, line):
        ea_count = len([u for u in line.decode('utf-8') if unicodedata.east_asian_width(u) in ('F', 'W')])
        unicode_diff = len(line.decode('utf-8')) - ea_count
        diff_byte = self.width - (unicode_diff + (ea_count * 2))
        max_line = line + diff_byte * " "
        return max_line[:self.width]

    def __exit__(self, exc_type, exc_value, traceback):
        curses.nl()
        curses.endwin()
