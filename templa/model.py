# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from itertools import izip_longest as _zip
from collections import OrderedDict
from unicodedata import east_asian_width
import locale

# Default limit
PAGE_LIMIT = 2000


class Screen(object):

    def __init__(self, stdscr, order):
        self.stdscr = stdscr
        self.order = order
        self.height, self.width = stdscr.getmaxyx()
        self.query = u''
        self.pos_x = 0
        self.pos_y = 1
        self.initialize()

    def initialize(self):
        self.create_pager()
        self.create_prompt()

    def create_prompt(self):
        self.prompt = Prompt(self.query, self.width, self.pager.info)

    def create_pager(self):
        self.pager = Pager(self.order, self.height, self.width)

    def is_query(self):
        return True if self.query else False

    def erase_query_char(self):
        self.query = self.query[:-1]

    def set_query(self, query):
        """stub function
        """
        # TODO use tty read character
        # self.model.keyword += curses.ascii.unctrl(key).decode("utf-8")
        if self.is_query:
            if self.query == u'':
                self.query = query.decode("utf-8")
            else:
                self.query += query.decode("utf-8")

    def move_next_page(self):
        """Command
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
        self.pager.set_current_page(self.pager.next_page_number())
        self.pos_y = 1

    def move_prev_page(self):
        """Command
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
        self.pager.set_current_page(self.pager.prev_page_number())
        self.pos_y = 1

    def search_and_update(self):
        """
        >>> _list = [u"hoge", u"huga", u"piyo"]
        >>> model = Model(_list, 5, 3) # width, height
        >>> model.query = "h"
        >>> model.update()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        self.pos_y = 1
        # pager
        new_order = [v for v in self.order if self.query in v]
        self.pager.pages = self.pager.create_pages(new_order, self.height)
        self.pager.set_current_page(self.pager.FIRST_PAGE_NUMBER)
        # prompt
        self.create_prompt()

    def is_in_display_range(self, position):
        if position in range(1, self.height):
            return True
        return False

    @property
    def current_page(self):
        return self.pager.current_page

    @property
    def query_length_byte(self):
        # XXX
        return len(self.query)

    @property
    def bottom_line_number(self):
        """Bottom Line Number
        """
        return len([x for x in self.pager.current_page if x])

    @property
    def result_prompt(self):
        return self.prompt.prompt_query() + self.prompt.pager_info()


class Prompt(object):
    """
    """

    def __init__(self, query, width, pager_info):
        self.query = query
        self.info = pager_info
        self.width = width

    def pager_info(self):
        return "[{}:{}]".format(self.info['current_page'], self.info['max_page'])

    def pager_info_length_byte(self):
        return len(self.pager_info())

    def prompt_query(self):
        effective_width = self.width - self.pager_info_length_byte() - 2
        if self.query:
            return self._to_adapt_width(self.query)[:effective_width]
        return effective_width * " "

    def _to_adapt_width(self, line_strings):
        """ Adapt Line of string
        line: Unicode
        """
        ea_count = len([string for string in line_strings if east_asian_width(string) in ('F', 'W')])
        not_ea_count = len(line_strings) - ea_count
        diff_count = self.width - (not_ea_count + (ea_count * 2))
        line = line_strings + diff_count * " "
        return line[:self.width]


class Pager(object):
    """
    """
    FIRST_PAGE_NUMBER = 1

    def __init__(self, order, height, width):
        self.width = width
        self.pages = self.create_pages(order, height)
        self.current_page_number = 1
        self.current_page = self._get_current_page()

    def create_pages(self, order, height):
        return list(_zip(*[iter(order)]*(height-1)))

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
        diff_count = self.width - (not_ea_count + (ea_count * 2))
        line = line_strings + diff_count * " "
        return line[:self.width]

    def _get_current_page(self):
        ret = []
        for v in self.pages[self.current_page_number - 1]:
            if v:
                ret.append(self._to_adapt_width(v))
            else:
                ret.append(v)

        return ret

    def is_single_line(self):
        return True if len(self.current_page) == 1 else False

    @property
    def info(self):
        return {
            'max_page': len(self.pages),
            'current_page': self.current_page_number,
        }
