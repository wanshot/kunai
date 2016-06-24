# -*- coding: utf-8 -*-


class TemplaCommand(object):

    def __init__(self, view, keyhandler):
        self.view = view
        self.execute(keyhandler)

    def execute(self, keyhandler):
        if keyhandler == 'input_query':
            pass
        else:
            # XXX
            getattr(self, keyhandler)()

    def move_next_page(self):
        self.view.screen.move_next_page()
        self.view.update()

    def move_prev_page(self):
        self.view.screen.move_prev_page()
        self.view.update()

    def move_up(self):
        self.view.move_up()

    def move_down(self):
        self.view.move_down()

    def backword_word(self):
        self.view.backspace()

    def select_top(self):
        pass

    def select_bottom(self):
        pass

    def select_line(self):
        pass
