# -*- coding: utf-8 -*-
# from .exceptions import ParseError
import re
import itertools
from collections import OrderedDict
import unicodedata


class Model(object):

    def __init__(self, list_, stdscr, height, width):
        self.list_ = list_
        self.stdscr = stdscr
        self.height = height
        self.width = width

        self.keyword = u''
        self.pages = self._create_pages()
        self.page_number = 1

    def _create_pages(self, new_list=None):
        r = self.list_
        if isinstance(new_list, list):
            r = new_list

        pages = OrderedDict()
        for page_num, c in enumerate(itertools.izip_longest(*[iter(r)]*(self.height-1)), start=1):
            od = OrderedDict()
            for lineno, line in enumerate(c, start=1):
                if line is None:
                    od[lineno] = None
                else:
                    od[lineno] = self._adapt(line)
#                     od[lineno] = line
            pages[page_num] = od

        return pages

    def update(self):
        """Update Model Pager
        """
        updated = [x for x in self.list_ if self.keyword in x]
        self.pages = self._create_pages(updated)

    def next_page(self):
        """Paginator
        """
        self.page_number += 1

    def prev_page(self):
        """Paginator
        """
        self.page_number -= 1

    def first_page_number(self):
        """ Set First Page Number
        """
        self.page_number = 1

    def last_page_number(self):
        """ Set Last Page Number
        """
        self.page_number = self.pages.keys()[-1]

    @property
    def current_page(self):
        return self.pages[self.page_number]

    def _adapt(self, line):
        ea_count = len([u for u in line.decode('utf-8') if unicodedata.east_asian_width(u) in ('F', 'W')])
        unicode_diff = len(line.decode('utf-8')) - ea_count
        diff_byte = self.width - (unicode_diff + (ea_count * 2))
        max_line = line + diff_byte * " "
        return max_line[:self.width]

    def markup(self, line):
        result = []

        if self.keyword:
            for x in re.finditer(ur"{}".format(self.keyword), line):
                result.append((x.start(), x.end()))

        return result
