# -*- coding: utf-8 -*-
import curses
from search import search_keyword


class View(object):

    def __init__(self, stdscr, model, pos_y, pos_x, display, keyhandler=None):
        self.model = model
        self.stdscr = stdscr
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.display = display

        self.new_pos_y = None

        if keyhandler:
            try:
                getattr(self, '{}'.format(keyhandler.operate))()
            except:
                self.update_keyword(keyhandler.key)

    def _update_line(self, select_num):
        for lineno, line in self.model.current_page.items():
            # overwrite line
            if line is None:
                self.stdscr.move(lineno, 0)
                self.stdscr.clrtoeol()
            else:
                if lineno == select_num:  # set first select line color
                    self.stdscr.addstr(lineno, 0, line, self.display.select)
                    if self.model.keyword:
                        self._hightlight_keyword(lineno, line, normal=False)
                else:
                    self.stdscr.addstr(lineno, 0, line[:self.model.width-1],
                                       self.display.normal)
                    if self.model.keyword:
                        self._hightlight_keyword(lineno, line, normal=True)

    def _hightlight_keyword(self, lineno, line, normal=True):
        if normal:
            attr = self.display.highlight_normal
        else:
            attr = self.display.highlight_select

        for pos in search_keyword(line, self.model.keyword):
            self.stdscr.addnstr(lineno, pos, self.model.keyword,
                                len(self.model.keyword), attr)

    def _display_line(self):
        # new line
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.display.select)
        # old line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.display.normal)

    def _update_prompt(self):
        # default prompt label
        label = '%'
    #     if self.conf.input_field_label:
    #         label = self.conf.input_field_label

        self.stdscr.addstr(0, 0, '{} {}{}'.format(label,
                                                  self.model.adapted_keyword(),
                                                  self.model.page_info))

    def update(self, select_num=1):
        self._update_line(select_num)
        self._update_prompt()

    def next_line(self):
        self.new_pos_y = self.pos_y + 1

        # (last to first) call page
        if None in self.model.current_page.values():
            if self.model.current_page.values().index(None) < self.new_pos_y:
                self.model.move_first_page()
                self.new_pos_y = 1
                self.update()

        # next page render
        elif self.model.height - 1 < self.new_pos_y:
            self.model.move_next_page()
            self.new_pos_y = 1
            self.update()

        self._display_line()

    def prev_line(self):
        self.new_pos_y = self.pos_y - 1
        if self.new_pos_y == 0:

            # (first to last) call page
            if self.model.page_number == 1:
                self.model.move_last_page()
                self.new_pos_y = self.model.bottom_line_number
                self.update(self.model.bottom_line_number)

            # prev page render
            else:
                self.model.move_prev_page()
                self.new_pos_y = self.model.height-1
                self.update()

        self._display_line()

    def backspace(self):
        if self.model.keyword:
            self.model.keyword = self.model.keyword[:-1]

    def update_keyword(self, key):
        """stub function
        """
        # TODO use tty read character
        self.model.keyword += curses.ascii.unctrl(key).decode("utf-8")
