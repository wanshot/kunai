# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from itertools import izip_longest as _zip
from collections import OrderedDict
import unicodedata
import locale

# Default limit
PAGE_LIMIT = 2000


class Model(object):

    def __init__(self, collections, height, width):
        self.collections = collections
        self.height = height
        self.width = width

        self.keyword = u""
        self.pages = self._create_pages()
        self.page_number = 1

    def _create_pages(self, new_collections=None):
        c = self.collections
        if isinstance(new_collections, list):  # Not use only at the update
            c = new_collections

        r = c[PAGE_LIMIT] if len(c) > PAGE_LIMIT else c

        pages = OrderedDict()
        locale.setlocale(locale.LC_ALL, '')
        for page_num, c in enumerate(_zip(*[iter(r)]*(self.height-1)), start=1):
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
        new_collections = [x for x in self.collections if self.keyword in x]
        self.pages = self._create_pages(new_collections)
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
    def is_singe_line(self):
        return True if len(self.pages.keys()) == 1 else False

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
