# -*- coding: utf-8 -*-


class Command(object):
    """User operate command
    Model < View < Command
    """

    def __init__(self, kunai):
        self.kunai = kunai
        self.view = kunai.view
        if not kunai.keyhandler.has_query:
            getattr(self, kunai.keyhandler.command)()

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

    def exit_kunai(self):
        self.kunai.cancel()

    def select_line(self):
        self.kunai.finish()
