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

    def __init__(self, stdscr):

        self.config = LoadConfig()

        self.stdscr = stdscr
        curses.start_color()
        self._set_color()

    def _set_color(self):

        # normal line
        fg = self.config.normal_line_color.get('fg', 'white')
        bg = self.config.normal_line_color.get('bg', 'black')
        normal_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        normal_line_bg = COLORS.get(bg, curses.COLOR_BLACK)
        curses.init_pair(1, normal_line_fg, normal_line_bg)

        # select line
        fg = self.config.select_line_color.get('fg', 'white')
        bg = self.config.select_line_color.get('bg', 'blue')
        select_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        select_line_bg = COLORS.get(bg, curses.COLOR_BLUE)
        curses.init_pair(2, select_line_fg, select_line_bg)

        # markup
        markup = self.config.markup_color.get('color')
        markup_color = COLORS.get(markup, curses.COLOR_YELLOW)
        # normal line markup
        curses.init_pair(3, markup_color, normal_line_bg)
        # select line markup
        curses.init_pair(4, markup_color, select_line_bg)

    @property
    def normal(self):
        result = curses.color_pair(1)
        for key, value in self.config.normal_line_options.items():
            if value == 'True':
                result = or_(result, ATTRS.get(key))
        return result

    @property
    def select(self):
        result = curses.color_pair(2)
        for key, value in self.config.select_line_options.items():
            if value == 'True':
                result = or_(result, ATTRS.get(key))
        return result

    @property
    def markup_normal(self):
        return curses.color_pair(3)

    @property
    def markup_select(self):
        return curses.color_pair(4)
