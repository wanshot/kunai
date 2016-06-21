# -*- coding: utf-8 -*-


class TemplaCommand(object):

    def __init__(self, screen, view):
        self.screen = screen
        self.view = view

    def move_next_page(self):
        return self.screen.move_next_page()

    def move_prev_page(self):
        return self.screen.move_prev_page()

    def move_top(self):
        pass

    def move_down(self):
        pass

    def backword_word(self):
        pass

    def select_top(self):
        pass

    def select_bottom(self):
        pass

    def select_line(self):
        pass
