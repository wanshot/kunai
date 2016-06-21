# -*- coding: utf-8 -*-
from search import search_query


class View(object):

    def __init__(self, display, screen, keyhandler=None):
        self.display = display
        self.keyhandler = keyhandler
        self.screen = screen

    def addstr(self, y, x, line, attrs=None):
        self.stdscr.addstr(y, x, line[:self.screen.width - 1], attrs)

    def hightlight_query(self, lineno, line, attr):
        """
        """

        for pos_x in search_query(line, self.screen.query):
            self.stdscr.addnstr(lineno,
                                pos_x,
                                self.screen.query,
                                len(self.screen.query_length_byte),
                                attr)

    def render_current_page(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if idx == 1:
                self.addstr(idx, 0, line, self.display.select_line)
            else:
                self.addstr(idx, 0, line, self.display.normal_line)

    def render_hightlight_query(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if idx == 1:
                self.hightlight_query(idx, line)
            else:
                self.hightlight_query(idx, line)

    def render_prompt(self):
        """
        """
        self.addstr(0, 0, self.screen.prompt)

    def update(self, operate=None):
        """
        """

        if not operate:
            self.render_prompt()
            self.render_current_page()

        elif operate == self.keyhandler.operate:
            pass

        elif operate in self.keyhandler.hoge.keys():
            self.render_prompt()
            self.render_current_page()
            self.render_hightlight_query()
