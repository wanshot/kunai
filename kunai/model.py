# -*- coding: utf-8 -*-

import locale
from itertools import izip_longest as _zip
from unicodedata import east_asian_width

from wcwidth import wcswidth


def adjust_width(line, width):
    text_len = wcswidth(line)
    # ea_count = len([string for string in line_strings if east_asian_width(string) in ('F', 'W')])
    # not_ea_count = len(line_strings) - ea_count
    # diff_count = self.width - (not_ea_count + (ea_count * 2))
    # line = line_strings + diff_count * 'x'
    # return line
    ret = line + (width - text_len) * u' '
    return ret.encode('utf-8')


class Screen(object):

    def __init__(self, stdscr, request):
        if isinstance(request, dict):
            request = request.keys()
        self.request = request
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.query = u''
        self.pos_x = 0
        self.pos_y = 1
        self.pager = Pager(request, self.width, self.height)
        self.prompt = Prompt(self.query, self.width, self.pager)
        self.create_prompt()

    def create_prompt(self):
        self.prompt = Prompt(self.query, self.width, self.pager)

    def erase_query_char(self):
        if self.query:
            self.query = self.query[:-1]

    def set_query(self, query):
        """stub function
        """
        # TODO use tty read character
        # self.model.keyword += curses.ascii.unctrl(key).decode("utf-8")
        if self.query:
            self.query += query.decode('utf-8')
        else:
            self.query = query.decode('utf-8')

    def move_next_page(self):
        """Next page command
        >>> pager = Pager(map(str, range(5)), 5, 3)
        >>> print pager.current_page
        >>> ['0    ', '1    ']
        >>> pager.set_current_page(pager.next_page_number())
        >>> print pager.current_page
        >>> ['2    ', '3    ']
        >>> pager.set_current_page(pager.next_page_number())
        >>> print pager.current_page
        >>> ['4    ', None]
        >>> pager.set_current_page(pager.next_page_number())
        >>> print pager.current_page
        >>> ['0    ', '1    ']
        """
        self.pager.set_current_page(self.pager.next_page_number())
        # set top position
        self.pos_y = 1
        self.create_prompt()

    def move_prev_page(self):
        """Prev page command
        >>> pager = Pager(map(str, range(5)), 5, 3)
        >>> print pager.current_page
        >>> ['0    ', '1    ']
        >>> pager.set_current_page(pager.prev_page_number())
        >>> print pager.current_page
        >>> ['4    ', None]
        >>> pager.set_current_page(pager.prev_page_number())
        >>> print pager.current_page
        >>> ['2    ', '3    ']
        >>> pager.set_current_page(pager.prev_page_number())
        >>> print pager.current_page
        >>> ['0    ', '1    ']
        """
        self.pager.set_current_page(self.pager.prev_page_number())
        # set top position
        self.pos_y = 1
        self.create_prompt()

    def search_and_update(self):
        """
        """
        self.pos_y = 1
        # pager
        new_request = [v for v in self.request if self.query in v]
        self.pager.pages = self.pager.create_chunk_list(new_request, self.height)
        self.pager.set_current_page(self.pager.FIRST_PAGE_NUMBER)
        # prompt
        self.create_prompt()

    def is_within_display_range(self, position):
        """Check within display range
        """
        if position in range(1, self.height):
            return True
        return False

    def is_none_line(self, pos_y):
        """
        """
        if self.pager.current_page[pos_y - 1] is None:
            return True
        return False

    @property
    def current_page(self):
        return self.pager.current_page

    @property
    def query_byte_count(self):
        return len(self.query)

    @property
    def bottom_line_number(self):
        """Bottom Line Number
        """
        return len([x for x in self.pager.current_page if x is not None])

    @property
    def verbose_prompt(self):
        return self.prompt.prompt_query + self.prompt.pager_info


class Prompt(object):
    """Prompt object
    """

    def __init__(self, query, width, pager):
        self.query = query
        self.pager = pager
        self.width = width

    @property
    def prompt_query(self):
        effective_width = self.width - self.page_info_byte_count - 2
        if self.query:
            return adjust_width(self.query, self.width)[:effective_width]
        return effective_width * ' '

    @property
    def pager_info(self):
        return '[{current_page_number}:{max_pager_size}]'.format(
            current_page_number=self.pager.current_page_number,
            max_pager_size=self.pager.max_pager_size,
        )

    @property
    def page_info_byte_count(self):
        return len(self.pager_info)


class Pager(object):
    """Pager object
    """
    FIRST_PAGE_NUMBER = 1

    def __init__(self, request, width, height):
        self.height = height
        self.width = width
        self.pages = self.create_chunk_list(request, height)
        self.current_page_number = 1
        self.current_page = self._get_current_page()

    def create_chunk_list(self, request, height):
        return list(_zip(*[iter(request)] * (height - 1)))

    def next_page_number(self):
        if self.current_page_number == len(self.pages):
            return self.FIRST_PAGE_NUMBER
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

    def _get_current_page(self):
        page = []
        for line in self.pages[self.current_page_number - 1]:
            if line:
                page.append(adjust_width(line, self.width))
            else:
                page.append(None)
        return page

    def is_single_line(self):
        return True if len(self.current_page) == 1 else False

    @property
    def max_pager_size(self):
        return len(self.pages)
