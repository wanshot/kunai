# -*- coding: utf-8 -*-
from search import search_query_position


class View(object):

    def __init__(self, display, screen):
        self.display = display
        self.screen = screen

    def hightlight_query(self, lineno, line, attr):
        """
        """

        for pos_x in search_query_position(line, self.screen.query):
            self.screen.stdscr.addnstr(lineno,
                                       pos_x,
                                       self.screen.query,
                                       self.screen.query_byte_count,
                                       attr)

    def render_current_page(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if line is not None:
                try:
                    self.screen.stdscr.addnstr(idx, 0, line, self.screen.width)
                except:
                    pass

                if idx == self.screen.pos_y:
                    self.screen.stdscr.chgat(idx, self.screen.pos_x, -1, self.display.select)
            else:
                self.screen.stdscr.move(idx, 0)
                self.screen.stdscr.clrtoeol()

    def render_hightlight_query(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if line is not None and self.screen.query:
                if idx == self.screen.pos_y:
                    self.hightlight_query(idx, line, self.display.highlight_select)
                else:
                    self.hightlight_query(idx, line, self.display.highlight_normal)

    def render_prompt(self):
        """
        """
        self.screen.stdscr.addnstr(0, 0,
                                   self.screen.verbose_prompt,
                                   self.screen.width,
                                   self.display.normal)

    def update(self):
        """
        """
        self.render_prompt()
        self.render_current_page()
        self.render_hightlight_query()

    def move_down(self):
        new_pos_y = self.screen.pos_y + 1
        if self.screen.is_within_display_range(new_pos_y):
            if not self.screen.is_none_line(new_pos_y):
                # new line
                self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
                # old line
                self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
                # update
                self.screen.pos_y = new_pos_y
                self.render_hightlight_query()
            else:
                self.screen.move_next_page()
                self.update()
        else:
            self.screen.move_next_page()
            self.update()

    def move_up(self):
        new_pos_y = self.screen.pos_y - 1
        if self.screen.is_within_display_range(new_pos_y):
            if not self.screen.is_none_line(new_pos_y):
                # new line
                self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
                # old line
                self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
                # update
                self.screen.pos_y = new_pos_y
                self.render_hightlight_query()
        if new_pos_y == 0:
            self.screen.move_prev_page()
            # set bottom select
            self.screen.pos_y = self.screen.bottom_line_number
            self.update()

    def backspace(self):
        self.screen.erase_query_char()
        self.screen.search_and_update()
        self.refresh_display()

    def search_query(self, ch):
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
