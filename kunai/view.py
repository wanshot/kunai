# -*- coding: utf-8 -*-
from search import search_query_position


class View(object):

    def __init__(self, display, screen):
        self.display = display
        self.screen = screen

    def _hightlight_query(self, lineno, line, attr):
        """Highlight matching results in search string

        :params int lineno: Line number
        :params str line: String per line
        :params attr: Attributes of the string to be displayed
        """

        for pos_x in search_query_position(line, self.screen.query):
            self.screen.stdscr.addnstr(lineno,
                                       pos_x,
                                       self.screen.query,
                                       self.screen.query_byte_count,
                                       attr)

    def render_current_page(self):
        """Display current page
        """
        for idx, line in enumerate(self.screen.current_page, start=1):
            self.screen.stdscr.addnstr(idx, 0, line, self.screen.width - 1)
            if idx == self.screen.pos_y:
                self.screen.stdscr.chgat(idx,
                                         self.screen.pos_x,
                                         -1,
                                         self.display.select_line_attr)

    def render_hightlight_query(self):
        """Highlight the query and display it
        """
        for idx, line in enumerate(self.screen.current_page, start=1):
            if line is not None and self.screen.query:
                if idx == self.screen.pos_y:
                    self._hightlight_query(
                        idx,
                        line,
                        self.display.highlight_select_line_attr)
                else:
                    self._hightlight_query(
                        idx,
                        line,
                        self.display.highlight_normal_line_attr)

    def render_prompt(self):
        """Display prompt
        """
        self.screen.stdscr.addnstr(0, 0,
                                   self.screen.prompt,
                                   self.screen.width,
                                   self.display.normal_line_attr)

    def update(self):
        """Update display
        """
        self.render_prompt()
        self.render_current_page()
        self.render_hightlight_query()

    def move_down(self):
        new_pos_y = self.screen.pos_y + 1
        if self.screen.is_within_display_range(new_pos_y):
            # new line
            self.screen.stdscr.chgat(new_pos_y,
                                     self.screen.pos_x,
                                     -1,
                                     self.display.select_line_attr)
            # old line
            self.screen.stdscr.chgat(self.screen.pos_y,
                                     self.screen.pos_x,
                                     -1,
                                     self.display.normal_line_attr)
            # update
            self.screen.pos_y = new_pos_y
            self.render_hightlight_query()
        else:
            self.screen.move_next_page()
            self.update()

    def move_up(self):
        new_pos_y = self.screen.pos_y - 1
        if self.screen.is_within_display_range(new_pos_y):
            # new line
            self.screen.stdscr.chgat(new_pos_y,
                                     self.screen.pos_x,
                                     -1,
                                     self.display.select_line_attr)
            # old line
            self.screen.stdscr.chgat(self.screen.pos_y,
                                     self.screen.pos_x,
                                     -1,
                                     self.display.normal_line_attr)
            # update
            self.screen.pos_y = new_pos_y
            self.render_hightlight_query()
        else:
            self.screen.move_prev_page()
            # set bottom select
            self.update()

    def backspace(self):
        """Erase one character from the input character string
        """
        self.screen.erase_query_char()
        self.screen.search_and_update()
        self.refresh_display()

    def search_query(self, ch):
        """Enter a character string to search
        """
        self.screen.set_query(ch)
        self.screen.search_and_update()
        self.refresh_display()

    def refresh_display(self):
        self.screen.stdscr.erase()
        self.update()
        self.screen.stdscr.refresh()

    @property
    def select_line(self):
        return self.screen.current_page[self.screen.pos_y - 1]
