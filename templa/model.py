# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from itertools import izip_longest as _zip
from collections import OrderedDict
from unicodedata import east_asian_width
import locale

# Default limit
PAGE_LIMIT = 2000


class Pager(object):


class Prompt(object):
    pass

class Pager(object):
    """
    """
    FIRST_PAGE_NUMBER = 1

    def __init__(self, order, display):
        self.display = display
        self.order = order
        self.pages = self._create_pages(order)
        self.current_page_number = 1
        self.current_page = self._get_current_page()
        self.query = None

    def create_pages(self, order):
        return list(_zip(*[iter(order)]*(self.display.height-1)))

    def next_page_number(self):
        if self.current_page_number == len(self.pages):
            return 1
        else:
            return self.current_page_number + 1

    def prev_page_number(self):
        if self.current_page_number == 1:
            return len(self.pages)
        else:
            return self.current_page_number - 1

    def set_current_page(self, number):
        locale.setlocale(locale.LC_ALL, '')
        self.current_page_number = number
        if self.pages:
            self.current_page = self._get_current_page()
        else:
            self.current_page = []

    def _to_adapt_width(self, line_strings):
        """ Adapt Line of string
        line: Unicode
        """
        ea_count = len([string for string in line_strings if east_asian_width(string) in ('F', 'W')])
        not_ea_count = len(line_strings) - ea_count
        diff_count = self.display.width - (not_ea_count + (ea_count * 2))
        line = line_strings + diff_count * " "
        return line[:self.display.width]

    def _get_current_page(self):
        ret = []
        for v in self.pages[self.current_page_number - 1]:
            if v:
                ret.append(self._to_adapt_width(v))
        return ret

    def is_query(self):
        return True if self.query else False

    def is_single_line(self):
        return True if len(self.current_page) == 1 else False

    @property
    def pages_info(self):
        """Display Page info
        """
        return "[{}:{}]".format(self.current_page_number, len(self.pages))

    @property
    def prompt(self):
        """Display query
        """
        query_width = self.display.width - len(self.pages_info) - 2
        if self.query:
            return self._to_adapt_width(self.query)[:query_width]
        return query_width * " "

    @property
    def bottom_line_number(self):
        """Bottom Line Number
        """
        return max([idx for idx, x in enumerate(self.current_page, start=1) if x])
