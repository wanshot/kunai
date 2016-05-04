# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from collections import OrderedDict
import unicodedata


class Model(object):

    def __init__(self, list_):
        self.lines = None
        self.keyword = u''

        if isinstance(list_, list):
            self.list_ = list_
            self.lines = self._create_lines()

    def _create_lines(self):
        r = OrderedDict()
        for lineno, line in enumerate(self.list_, start=1):
            if isinstance(line, str):
                line = line.decode('utf-8')
            elif isinstance(line, unicode):
                pass
            else:
                raise TypeError("Required argument hoge not str or unicode")

            r[lineno] = line

        return r

    def update(self, keyword):
        """Update Model Class
        """
        if self.keyword:
            self.keyword += keyword
        else:
            self.keyword = keyword

        r = OrderedDict()
        lineno = 1
        for line in self.lines.values():
            if self.keyword in line:
                r[lineno] = line
                lineno += 1

        self.lines = r

    def next_line(self, pos_y, pos_x, height, width, color, stdscr):
        # new line
        new_pos_y = pos_y + 1
        new_line = self._adapt_line(self.lines[new_pos_y], width)
        stdscr.addstr(new_pos_y, pos_x, new_line, color)
        # old line
        old_line = self._adapt_line(self.lines[pos_y], width)
        stdscr.addstr(pos_y, pos_x, old_line)
        return new_pos_y

    def prev_line(self, pos_y, pos_x, height, width, color, stdscr):
        # new line
        new_pos_y = pos_y - 1
        new_line = self._adapt_line(self.lines[new_pos_y], width)
        stdscr.addstr(new_pos_y, pos_x, new_line, color)
        # old line
        old_line = self._adapt_line(self.lines[pos_y], width)
        stdscr.addstr(pos_y, pos_x, old_line)
        return new_pos_y

    def _adapt_line(self, line, width):
        ea_count = len([u for u in line.decode('utf-8') if unicodedata.east_asian_width(u) in ('F', 'W')])
        unicode_diff = len(line.decode('utf-8')) - ea_count
        diff_byte = width - (unicode_diff + (ea_count * 2))
        max_line = line + diff_byte * " "
        return max_line[:width]
