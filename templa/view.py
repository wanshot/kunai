# -*- coding: utf-8 -*-
from search import search_query


class View(object):

    def __init__(self, display, screen):
        self.display = display
        self.screen = screen

    def addstr(self, y, x, line, attrs=None):
        self.screen.stdscr.addstr(y, x, line[:self.screen.width - 1], attrs)

    def hightlight_query(self, lineno, line, attr):
        """
        """

        for pos_x in search_query(line, self.screen.query):
            self.screen.stdscr.addnstr(lineno,
                                       pos_x,
                                       self.screen.query,
                                       len(self.screen.query_length_byte),
                                       attr)

    def render_current_page(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if idx == 1:
                self.addstr(idx, 0, line, self.display.select)
            else:
                self.addstr(idx, 0, line, self.display.normal)

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
        self.addstr(0, 0, self.screen.result_prompt, self.display.normal)

    def update(self):
        """
        """
        self.render_prompt()
        self.render_current_page()

    def move_up(self):
        new_pos_y = self.screen.pos_y + 1
        # new line
        self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
        # old line
        self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
        self.screen.pos_y = new_pos_y

    def move_down(self):
        new_pos_y = self.screen.pos_y - 1
        # new line
        self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
        # old line
        self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
        self.screen.pos_y = new_pos_y

    def refresh_display(self):
        self.screen.stdscr.erase()
        self.update()
        self.screen.stdscr.refresh()
