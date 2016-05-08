# -*- coding: utf-8 -*-

import curses

SP_KEYS = {
    curses.KEY_DOWN: "down",
    curses.KEY_UP: "up",
    curses.KEY_BACKSPACE: "backspace",
    127: "backspace",
}


class KeyHandler(object):

    def __init__(self, stdscr, model,  pos_y, pos_x, page, page_num, color, key):
        self.stdscr = stdscr
        self.model = model
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.page = page
        self.page_num = page_num
        self.color = color
        self.key = SP_KEYS.get(key)

        self.new_pos_y = None
        try:
            getattr(self, '{}'.format(self.key))()
        except:
            self.update_keyword(key)

    def up(self):
        self.new_pos_y = self.pos_y - 1

#         try:
        # new line
        new_line = self.page[self.new_pos_y]
        self.stdscr.addstr(self.new_pos_y, self.pos_x, new_line, self.color.select)
        # old line
        old_line = self.page[self.pos_y]
        self.stdscr.addstr(self.pos_y, self.pos_x, old_line, self.color.normal)
#         except KeyError:
#             self.pager.next()
            # update処理
#         except TypeError:
#             pass

    def down(self):
        self.new_pos_y = self.pos_y + 1

#         try:
        # new line
        new_line = self.page[self.new_pos_y]
        self.stdscr.addstr(self.new_pos_y, self.pos_x, new_line, self.color.select)
        # old line
        old_line = self.page[self.pos_y]
        self.stdscr.addstr(self.pos_y, self.pos_x, old_line, self.color.normal)
#         except KeyError:
#             self.pager.next()
            # update処理
#         except TypeError:
#             pass

    def backspace(self):
        if self.model.keyword:
            self.model.keyword = self.model.keyword[:-1]

    def update_keyword(self, key):
        self.model.keyword += curses.ascii.unctrl(key)
