# -*- coding: utf-8 -*-


class Command(object):
    """UserOperateCommand
    model < view < command
    """

    def __init__(self, templa, view, keyhandler):
        self.templa = templa
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

    def select_top_line(self):
        pass

    def select_bottom_line(self):
        pass

    def exit_templa(self):
        self.templa.cancel()

    def select_line(self):
        self.templa.finish()
