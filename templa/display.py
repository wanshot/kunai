# -*- coding: utf-8 -*-

import curses
from operator import or_
from itertools import chain

from config import Config

COLORS = {
    "black":   curses.COLOR_BLACK,
    "red":     curses.COLOR_RED,
    "green":   curses.COLOR_GREEN,
    "yellow":  curses.COLOR_YELLOW,
    "blue":    curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan":    curses.COLOR_CYAN,
    "white":   curses.COLOR_WHITE,
}

ATTRS = {
    "altcharset": curses.A_ALTCHARSET,
    "blink":      curses.A_BLINK,
    "bold":       curses.A_BOLD,
    "dim":        curses.A_DIM,
    "normal":     curses.A_NORMAL,
    "standout":   curses.A_STANDOUT,
    "underline":  curses.A_UNDERLINE,
    "reverse":    curses.A_REVERSE,
}


NORMAL_LINE = 1
SELECT_LINE = 2
NORMAL_LINE_HL = 3
SELECT_LINE_HL = 4


class Display(object):

    def __init__(self, stdscr):

        self.conf = Config()

        self.stdscr = stdscr
        curses.start_color()
        self._set_color()

    def _set_color(self):

        # normal line
        fg = self.conf.normal_line_color.get('fg', 'white')
        bg = self.conf.normal_line_color.get('bg', 'black')
        normal_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        normal_line_bg = COLORS.get(bg, curses.COLOR_BLACK)
        curses.init_pair(NORMAL_LINE, normal_line_fg, normal_line_bg)
        # select line
        fg = self.conf.select_line_color.get('fg', 'white')
        bg = self.conf.select_line_color.get('bg', 'blue')
        select_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        select_line_bg = COLORS.get(bg, curses.COLOR_BLUE)
        curses.init_pair(SELECT_LINE, select_line_fg, select_line_bg)

        # sting match
        highlight_color = COLORS.get(self.conf.highlight_color,
                                     curses.COLOR_YELLOW)
        # normal line highlight
        curses.init_pair(NORMAL_LINE_HL, highlight_color, normal_line_bg)
        # select line highlight
        curses.init_pair(SELECT_LINE_HL, highlight_color, select_line_bg)

    def merge_option(self, ret, opts):
        """ make ATTRS
        """
        for k, v in opts:
            if v == 'True':
                ret = or_(ret, ATTRS.get(k))
        return ret

    @property
    def normal(self):
        return self.merge_option(curses.color_pair(NORMAL_LINE),
                                 self.conf.normal_line_options.items())

    @property
    def select(self):
        return self.merge_option(curses.color_pair(SELECT_LINE),
                                 self.conf.select_line_options.items())

    @property
    def highlight_normal(self):
        opts = chain(
            self.conf.normal_line_options.items(),
            self.conf.highlight_options.items())

        return self.merge_option(curses.color_pair(NORMAL_LINE_HL), opts)

    @property
    def highlight_select(self):
        opts = chain(
            self.conf.select_line_options.items(),
            self.conf.highlight_options.items())

        return self.merge_option(curses.color_pair(SELECT_LINE_HL), opts)
