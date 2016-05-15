# -*- coding: utf-8 -*-

import curses

SP_KEYS = {
    curses.KEY_DOWN: "down",
    curses.KEY_UP: "up",
    curses.KEY_BACKSPACE: "backspace",
    127: "backspace",
}


def set_lines(stdscr, model, display):
    for lineno, line in model.current_page.items():
        if line is None:
            stdscr.move(lineno, 0)
            stdscr.clrtoeol()
        else:
            if lineno == 1:  # set first line color
                stdscr.addstr(lineno, 0, line, display.select)
            else:
                stdscr.addstr(lineno, 0, line, display.normal)


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
        # prev page render
        if self.new_pos_y == 0:
            self.model.prev_page()
            self.new_pos_y = self.model.height - 1
            set_lines(self.stdscr, self.model, self.color)
        # call last page
        elif self.model.page_number == 1:
            if 0 < self.new_pos_y:
                self.model.last_page_number()
                self.new_pos_y = len(self.model.page.keys())
                set_lines(self.stdscr, self.model, self.color)
        # move select
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.color.select)  # new line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.color.normal)      # old line

    def key_down(self):
        self.new_pos_y = self.pos_y + 1
        # next page render
        if self.model.height - 1 < self.new_pos_y:
            self.model.next_page()
            self.new_pos_y = 1
            set_lines(self.stdscr, self.model, self.color)
        # call first page
        elif None in self.model.current_page.values():
            if self.model.current_page.values().index(None) < self.new_pos_y:
                self.model.first_page_number()
                self.new_pos_y = 1
                set_lines(self.stdscr, self.model, self.color)
        # move select
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.color.select)  # new line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.color.normal)      # old line

    def key_backspace(self):
        if self.model.keyword:
            self.model.keyword = self.model.keyword[:-1]

    def update_keyword(self, key):
        self.model.keyword += curses.ascii.unctrl(key)
