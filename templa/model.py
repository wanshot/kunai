# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from itertools import izip_longest as _zip
from collections import OrderedDict
from unicodedata import east_asian_width
import locale

# Default limit
PAGE_LIMIT = 2000


class Model(object):

    def __init__(self, collections, display):
        self.display = display
        self.collections = collections
        self.source = self._create_source(collections)
        self.current_page_number = 1
        self.current_page = [self._to_adapt_width(v) for v in self.source[self.current_page_number - 1] if v]
        self.query = None

    def _create_source(self, collections):
        return list(_zip(*[iter(collections)]*(self.display.height-1)))

    def _next_page_number(self):
        if self.current_page_number == len(self.source):
            return 1
        else:
            return self.current_page_number + 1

    def _prev_page_number(self):
        if self.current_page_number == 1:
            return len(self.source)
        else:
            return self.current_page_number - 1

    def _update(self, number):
        locale.setlocale(locale.LC_ALL, '')
        self.current_page_number = number
        self.current_page = [self._to_adapt_width(v) for v in self.source[self.current_page_number - 1] if v]

    def move_next_page(self):
        """ API
        >>> _list = [u"hoge", u"huga", u"piyo", u'templa', u'sushi']
        >>> model = Model(_list, 5, 3)  # width, height
        >>> print model.current_page  # [u'hoge ', u'huga ']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'piyo ', u'templa']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'sushi']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        self._update(self._next_page_number())

    def move_prev_page(self):
        """ API
        >>> _list = [u"hoge", u"huga", u"piyo", u'templa', u'sushi']
        >>> model = Model(_list, 5, 3)
        >>> print model.current_page  # [u'hoge ', u'huga ']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'sushi']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'piyo ', u'templa']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        self._update(self._prev_page_number())

    def update(self):
        """ API
        >>> _list = [u"hoge", u"huga", u"piyo"]
        >>> model = Model(_list, 5, 3) # width, height
        >>> model.query = "h"
        >>> model.update()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        new_collections = [v for v in self.collections if self.query in v]
        self.source = self._create_source(new_collections)
        self._update(1)

    @property
    def model_info(self):
        """Display Page info
        """
        return u"[{}:{}]".format(self.current_page_number, len(self.source) - 1)

    @property
    def prompt(self):
        """Display query
        """
        if self.query:
            query_width = self.display.width - len(self.model_info)
            return self._to_adapt_width(self.query)[:query_width-2]
        return ""

    def _to_adapt_width(self, line_strings):
        """ Adapt Line of string
        line: Unicode
        """
        ea_count = len([string for string in line_strings if east_asian_width(string) in ('F', 'W')])
        not_ea_count = len(line_strings) - ea_count
        diff_count = self.display.width - (not_ea_count + (ea_count * 2))
        line = line_strings + diff_count * " "
        return line[:self.display.width]

    @property
    def is_single_line(self):
        return True if len(self.current_page) == 1 else False

    @property
    def bottom_line_number(self):
        """Bottom Line Number
        """
        return max([idx for idx, x in enumerate(self.current_page, start=1) if x])

    def is_query(self):
        return True if self.query else False


if __name__ == "__main__":
    _list = [u"hoge", u"huga", u"piyo", u'templa', u'sushi']
    model = Model(_list, 5, 3)
    print model.current_page
    model.move_prev_page()
    print model.current_page
    model.move_prev_page()
    print model.current_page
    model.move_prev_page()
    print model.current_page
