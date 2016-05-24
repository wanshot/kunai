# -*- coding: utf-8 -*-

import curses
from search import search_keyword

SP_KEYS = {
    curses.KEY_DOWN: "down",
    curses.KEY_UP: "up",
    curses.KEY_BACKSPACE: "backspace",
    127: "backspace",
}


def update_prompt(stdscr, model):
    # TODO move view.py
    # default prompt label
    label = '%'
#     if self.conf.input_field_label:
#         label = self.conf.input_field_label

    stdscr.addstr(0, 0, '{} {}{}'.format(label,
                                         model.adapted_keyword(),
                                         model.page_info))


def update_lines(stdscr, model, display, select_num=1):
    # TODO move view.py
    for lineno, line in model.current_page.items():
        # overwrite line
        if line is None:
            stdscr.move(lineno, 0)
            stdscr.clrtoeol()
        else:
            if lineno == select_num:  # set first select line color
                stdscr.addstr(lineno, 0, line, display.select)
                stdscr.addstr(0, 15, model.keyword, display.select)
                if model.keyword:
                    for pos in search_keyword(line, model.keyword):
                        stdscr.addnstr(lineno, pos, model.keyword, len(model.keyword), display.highlight_select)
            else:
                stdscr.addstr(lineno, 0, line[:model.width-1], display.normal)
                if model.keyword:
                    for pos in search_keyword(line, model.keyword):
                        stdscr.addnstr(lineno, pos, model.keyword, len(model.keyword), display.highlight_normal)


class KeyHandler(object):

    def __init__(self, stdscr, model,  pos_y, pos_x, color, key):
        self.stdscr = stdscr
        self.model = model
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.color = color
        self.key = SP_KEYS.get(key)

        self.new_pos_y = None
        try:
            getattr(self, 'key_{}'.format(self.key))()
        except:
            self.update_keyword(key)

    def key_up(self):
        self.new_pos_y = self.pos_y - 1
        if self.new_pos_y == 0:

            # call last page
            if self.model.page_number == 1:
                self.model.move_last_page()
                self.new_pos_y = self.model.bottom_line_number
                update_lines(self.stdscr, self.model, self.color, self.model.bottom_line_number)
                update_prompt(self.stdscr, self.model)

            # prev page render
            else:
                self.model.move_prev_page()
                self.new_pos_y = self.model.height-1
                update_lines(self.stdscr, self.model, self.color)
                update_prompt(self.stdscr, self.model)

        # move select
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.color.select)  # new line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.color.normal)      # old line

    def key_down(self):
        self.new_pos_y = self.pos_y + 1

        # call first page
        if None in self.model.current_page.values():
            if self.model.current_page.values().index(None) < self.new_pos_y:
                self.model.move_first_page()
                self.new_pos_y = 1
                update_lines(self.stdscr, self.model, self.color)
                update_prompt(self.stdscr, self.model)

        # next page render
        elif self.model.height - 1 < self.new_pos_y:
            self.model.move_next_page()
            self.new_pos_y = 1
            update_lines(self.stdscr, self.model, self.color)
            update_prompt(self.stdscr, self.model)

        # move select
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.color.select)  # new line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.color.normal)      # old line

    def key_backspace(self):
        if self.model.keyword:
            self.model.keyword = self.model.keyword[:-1]

    def update_keyword(self, key):
        """stub function
        """
        # TODO use tty read character
        self.model.keyword += curses.ascii.unctrl(key).decode("utf-8")
