# -*- coding: utf-8 -*-

import curses
from operator import or_
from itertools import chain

from config import Config

NORMAL_NUMBER = 1
SELECT_NUMBER = 2
NORMAL_HIGHLIGHT_NUMBER = 3
SELECT_HIGHLIGHT_NUMBER = 4

COLORS = {
    'black':   curses.COLOR_BLACK,
    'red':     curses.COLOR_RED,
    'green':   curses.COLOR_GREEN,
    'yellow':  curses.COLOR_YELLOW,
    'blue':    curses.COLOR_BLUE,
    'magenta': curses.COLOR_MAGENTA,
    'cyan':    curses.COLOR_CYAN,
    'white':   curses.COLOR_WHITE,
}

STYLE = {
    'altcharset': curses.A_ALTCHARSET,
    'blink':      curses.A_BLINK,
    'bold':       curses.A_BOLD,
    'dim':        curses.A_DIM,
    'normal':     curses.A_NORMAL,
    'standout':   curses.A_STANDOUT,
    'underline':  curses.A_UNDERLINE,
    'reverse':    curses.A_REVERSE,
}


class Display(object):

    def __init__(self):

        self.conf = Config()
        curses.start_color()
        self._set_color()

    def _set_color(self):
        """Define colors from the configuration file
        """

        # match highlight
        highlight_color = COLORS.get(self.conf.highlight_color,
                                     curses.COLOR_YELLOW)

        # normal line highlight
        fg = self.conf.normal_line_color.get('fg', 'white')
        bg = self.conf.normal_line_color.get('bg', 'black')
        normal_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        normal_line_bg = COLORS.get(bg, curses.COLOR_BLACK)
        curses.init_pair(NORMAL_NUMBER, normal_line_fg, normal_line_bg)
        curses.init_pair(NORMAL_HIGHLIGHT_NUMBER, highlight_color, normal_line_bg)

        # select line highlight
        fg = self.conf.select_line_color.get('fg', 'white')
        bg = self.conf.select_line_color.get('bg', 'blue')
        select_line_fg = COLORS.get(fg, curses.COLOR_WHITE)
        select_line_bg = COLORS.get(bg, curses.COLOR_BLUE)
        curses.init_pair(SELECT_NUMBER, select_line_fg, select_line_bg)
        curses.init_pair(SELECT_HIGHLIGHT_NUMBER, highlight_color, select_line_bg)

    def merge_option(self, colors, styles):
        """merge attrs
        :param colors: color attribute from config file
        :param styles: style attribute from config file
        :type colors: curses color_pair object
        :type styles: dict
        """
        for k, v in styles:
            if v == 'True':
                colors = or_(colors, STYLE.get(k))
        return colors

    @property
    def normal_line_attr(self):
        """set normal line attribute
        """
        return self.merge_option(curses.color_pair(NORMAL_NUMBER),
                                 self.conf.normal_line_options.items())

    @property
    def select_line_attr(self):
        """set select line attribute
        """
        return self.merge_option(curses.color_pair(SELECT_NUMBER),
                                 self.conf.select_line_options.items())

    @property
    def highlight_normal_line_attr(self):
        """set normal highlight line attribute
        """
        opts = chain(
            self.conf.normal_line_options.items(),
            self.conf.highlight_options.items())

        return self.merge_option(curses.color_pair(NORMAL_HIGHLIGHT_NUMBER),
                                 opts)

    @property
    def highlight_select_line_attr(self):
        """set select highlight line attribute
        """
        opts = chain(
            self.conf.select_line_options.items(),
            self.conf.highlight_options.items())

        return self.merge_option(curses.color_pair(SELECT_HIGHLIGHT_NUMBER),
                                 opts)
