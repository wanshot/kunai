# -*- coding: utf-8 -*-

import curses
from operator import or_

from manage import LoadConfig

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


class Display(object):

    def __init__(self, stdscr, fg=None, bg=None, markup=None, select=None):

        self.config = LoadConfig()

        self.fg_color = curses.COLOR_WHITE
        if fg is not None:
            self.fg_color = COLORS[fg]
        self.bg_color = curses.COLOR_BLACK
        if bg is not None:
            self.bg_color = COLORS[bg]
        self.markup_color = curses.COLOR_YELLOW
        if markup is not None:
            self.markup_color = COLORS[markup]
        self.select_color = curses.COLOR_BLUE
        if select is not None:
            self.select_color = COLORS[select]

        self.stdscr = stdscr
        curses.start_color()

        # normal line
        curses.init_pair(1, self.fg_color, self.bg_color)
        # select line
        curses.init_pair(2, self.fg_color, self.select_color)
        # markup select line
        curses.init_pair(3, self.markup_color, self.select_color)
        # markup normal line
        curses.init_pair(4, self.markup_color, self.bg_color)

    @property
    def normal(self):
        return curses.color_pair(1)

    @property
    def select(self):
        if not self.config.under_line:
            pass
        return or_(curses.color_pair(2), curses.A_UNDERLINE)

    @property
    def markup_select(self):
        return curses.color_pair(3) | curses.A_UNDERLINE

    @property
    def markup_normal(self):
        return curses.color_pair(4)
