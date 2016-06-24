# -*- coding: utf-8 -*-
from search import search_query_position


class View(object):

    def __init__(self, display, screen):
        self.display = display
        self.screen = screen

    def addstr(self, y, x, line, attrs=None):
        self.screen.stdscr.addstr(y, x, line[:self.screen.width - 1], attrs)

    def hightlight_query(self, lineno, line, attr):
        """
        """

        for pos_x in search_query_position(line, self.screen.query):
            self.screen.stdscr.addnstr(lineno,
                                       pos_x,
                                       self.screen.query,
                                       self.screen.query_length_byte,
                                       attr)

    def render_current_page(self):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if line is not None:
                if idx == 1:
                    self.addstr(idx, 0, line, self.display.select)
                else:
                    self.addstr(idx, 0, line, self.display.normal)
            else:
                self.screen.stdscr.move(idx, 0)
                self.screen.stdscr.clrtoeol()

    def render_hightlight_query(self, default=1):
        """
        """

        for idx, line in enumerate(self.screen.current_page, start=1):
            if line is not None and self.screen.is_query():
                if idx == default:
                        self.hightlight_query(idx, line, self.display.highlight_select)
                else:
                    self.hightlight_query(idx, line, self.display.highlight_normal)

    def render_prompt(self):
        """
        """
        self.addstr(0, 0, self.screen.result_prompt, self.display.normal)

    def update(self):
        """
        """
        self.render_prompt()
        self.render_current_page()
        self.render_hightlight_query()

    def move_down(self):
        new_pos_y = self.screen.pos_y + 1
        if self.screen.is_in_display_range(new_pos_y):

            # new line
            self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
            # old line
            self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
            self.screen.pos_y = new_pos_y
        else:
            self.screen.move_next_page()
            self.update()

    def move_up(self):
        new_pos_y = self.screen.pos_y - 1
        if self.screen.is_in_display_range(new_pos_y):
            # new line
            self.screen.stdscr.chgat(new_pos_y, self.screen.pos_x, -1, self.display.select)
            # old line
            self.screen.stdscr.chgat(self.screen.pos_y, self.screen.pos_x, -1, self.display.normal)
            self.screen.pos_y = new_pos_y
        else:
            self.screen.move_prev_page()
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
