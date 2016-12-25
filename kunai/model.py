# -*- coding: utf-8 -*-

from pager import Paginator
from wcwidth import wcswidth


class Screen(object):

    def __init__(self, stdscr, object_list):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.pos_x = 0
        self.pos_y = 1
        if isinstance(object_list, dict):
            object_list = object_list.keys()
        self.object_list = [self.force_text(ol) for ol in object_list]
        self.current_page_number = 1
        self.query = u''
        self.paginator = Paginator(self.object_list, self.height - 1)

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
        if self.current_page.has_next():
            self.current_page_number = self.current_page.next_page_number()
        else:
            self.current_page_number = 1

        self.pos_y = 1

        return self.current_page

    def move_prev_page(self):
        if self.current_page.has_previous():
            self.current_page_number = self.current_page.previous_page_number()
        else:
            self.current_page_number = self.paginator.num_pages

        self.pos_y = len(self.current_page.object_list)

        return self.current_page

    def search_and_update(self):
        """Narrow down the target and update the value
        """
        new_object_list = [ol for ol in self.object_list if self.query in ol.decode('utf-8')]
        self.paginator = Paginator(new_object_list, self.height - 1)
        self.current_page_number = 1

    def is_within_display_range(self, position):
        """Check within display range

        :param int position: display of line number
        :return: Returns True if it is within display range
        """
        if position in range(1, len(self.current_page) + 1):
            return True
        return False

    @property
    def page_index(self):
        latest_page = 1
        if self.paginator.num_pages != 0:
            latest_page = self.paginator.num_pages
        return '[%s:%s]' % (self.current_page_number, latest_page)

    @property
    def current_page(self):
        return self.paginator.page(self.current_page_number)

    @property
    def query_byte_count(self):
        return len(self.query)

    @property
    def prompt(self):
        return self.force_text(self.query, prompt=True)

    def force_text(self, text, prompt=False):
        if isinstance(text, str):
            text = text.decode('utf-8')
        if prompt:
            text_length = wcswidth(text + self.page_index)
            ret = text + (self.width - text_length) * u' ' + self.page_index
        else:
            text_length = wcswidth(text)
            ret = text + (self.width - text_length) * u' '
        # XXX stdout = unicode -> ansii NG(maybe ansii encode fail)
        # XXX stdout = unicode -> str OK
        return ret.encode('utf-8')
