# -*- coding: utf-8 -*-
# from .exceptions import ParseError
import re
import itertools
from collections import OrderedDict
import unicodedata
import locale


class Model(object):

    def __init__(self, list_, stdscr, height, width):
        self.list_ = list_
        self.stdscr = stdscr
        self.height = height
        self.width = width

        self.keyword = u""
        self.pages = self._create_pages()
        self.page_number = 1

    def _create_pages(self, new_list=None):
        r = self.list_
        if isinstance(new_list, list):  # Not use only at the update
            r = new_list

        pages = OrderedDict()
        locale.setlocale(locale.LC_ALL, '')
        for page_num, c in enumerate(itertools.izip_longest(*[iter(r)]*(self.height-1)), start=1):
            od = OrderedDict()
            for lineno, line in enumerate(c, start=1):
                if line is None:
                    od[lineno] = None
                else:
                    od[lineno] = self._adapt(line).encode(locale.getpreferredencoding())
            pages[page_num] = od

        return pages

    def update(self):
        """Update Pages
        """
        updated = [x for x in self.list_ if self.keyword in x]
        self.pages = self._create_pages(updated)
        self.page_number = 1

    def move_next_page(self):
        """Set Next Page Number
        """
        self.page_number += 1

    def move_prev_page(self):
        """Set Prev Page Number
        """
        self.page_number -= 1

    def move_first_page(self):
        """Set First Page Number
        """
        self.page_number = 1

    def move_last_page(self):
        """Set Last Page Number
        """
        self.page_number = max(self.pages.keys())

    @property
    def last_page_number(self):
        """Last Page Number
        """
        if self.pages:
            return max(self.pages.keys())
        else:
            return 1

    @property
    def current_page(self):
        """Curent Page Data
        """
        if self.pages:
            return self.pages[self.page_number]
        else:
            return {}

    @property
    def bottom_line_number(self):
        """Bottom Line Number
        """
        return max([idx for idx, x in enumerate(self.current_page.values(), start=1) if x])

    @property
    def page_info(self):
        """Display Page info
        """
        return u"[{}:{}]".format(self.page_number, self.last_page_number)

    def adapted_keyword(self):
        """Display Keyword
        """
        keyword_width = self.width - len(self.page_info)
        return self._adapt(self.keyword)[:keyword_width-2]

    def _adapt(self, line):
        """ Adapt Line of string
        line: Unicode
        """
        ea = len([u for u in line if unicodedata.east_asian_width(u) in ('F', 'W')])
        not_ea = len(line) - ea
        diff = self.width - (not_ea + (ea * 2))
        line_width = line + diff * " "
        return line_width[:self.width]

    def markup(self, line):
        result = []

        if self.keyword:
            for x in re.finditer(ur"{}".format(self.keyword), line):
                result.append((x.start(), x.end()))

        return result
