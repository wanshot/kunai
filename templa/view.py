# -*- coding: utf-8 -*-

from search import search_query


class View(object):

    def __init__(self, stdscr, model, pos_y, pos_x, display, keyhandler=None):
        self.model = model
        self.stdscr = stdscr
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.display = display

        self.new_pos_y = 1
        self.select_value = None

        self.update()

        if keyhandler:
            try:
                getattr(self, '{}'.format(keyhandler.hold_key))()
            except:
                pass

    def _update_lines(self, line_position):
        for lineno, line in enumerate(self.model.current_page, start=1):
            # overwrite line
            if line is None:
                self.stdscr.move(lineno, 0)
                self.stdscr.clrtoeol()
            else:
                if lineno == line_position:
                    self.addstr(lineno, 0, line)
                else:
                    self.addstr(lineno, 0, line, top_line=False)

    def _hightlight_query(self, lineno, line, attr):

        for pos_x in search_query(line, self.model.query):
            self.stdscr.addnstr(lineno, pos_x, self.model.query, len(self.model.query), attr)

    def _update_prompt(self):
        # default prompt label
        label = '%'
    #     if self.conf.input_field_label:
    #         label = self.conf.input_field_label

        self.stdscr.addstr(0, 0, '{} {}{}'.format(label, self.model.prompt, self.model.pages_info))

    def _display_lines(self):
        # new line
        self.stdscr.chgat(self.new_pos_y, self.pos_x, -1, self.display.select)
#         if self.model.is_query():
#             self._hightlight_query(self.new_pos_y,
#                                    self.model.current_page[self.new_pos_y],
#                                    normal=False)
        # old line
        self.stdscr.chgat(self.pos_y, self.pos_x, -1, self.display.normal)
#         if self.model.query:
#             self._hightlight_query(self.pos_y,
#                                    self.model.current_page[self.pos_y])

    def addstr(self, y, x, line, attrs=None, top_line=True):
        if top_line:
            self.stdscr.addstr(y, x, line[:self.display.width-1], self.display.select)
            if self.model.is_query():
                self._hightlight_query(y, line, self.display.highlight_select)
        else:
            self.stdscr.addstr(y, x, line[:self.display.width-1], self.display.normal)
            if self.model.is_query():
                self._hightlight_query(y, line, self.display.highlight_normal)

    def update(self, line_position=1):
        self._update_lines(line_position)
        self._update_prompt()

    def next_line(self):

        self.new_pos_y = self.pos_y + 1

        # (last to first) call page
#         if None in self.model.current_page:
#             if self.model.current_page.index(None) < self.new_pos_y:
#                 self.model.move_first_page()
#                 self.new_pos_y = 1
#                 self.update()

        # next page render
#         elif self.model.display.height - 1 < self.new_pos_y:
#             self.model.move_next_page()
#             self.new_pos_y = 1
#             self.update()

        self._display_lines()

    def prev_line(self):
        if not self.model.is_single_line:
            self.new_pos_y = self.pos_y - 1
            if self.new_pos_y == 0:

                # (first to last) call page
                if self.model.page_number == 1:
                    self.model.move_prev_page()
                    self.new_pos_y = self.model.bottom_line_number
                    self.update(self.model.bottom_line_number)

                # prev page render
                else:
                    self.model.move_prev_page()
                    self.new_pos_y = self.model.display.height-1
                    self.update()

            self._display_lines()

    def enter(self):
        self.select_value = self.model.current_page[self.pos_y].strip()

    def backspace(self):
        if self.model.is_query():
            self.model.query = self.model.query[:-1]
            self.model.update()
