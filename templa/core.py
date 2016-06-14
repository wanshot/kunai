# -*- coding: utf-8 -*-

import sys
import curses
import locale
import signal
import threading
import curses.ascii

from config import Config
from model import Model
from display import Display
from view import View
from key import KeyHandler
from action import Actions
from tty import get_ttyname, reconnect_descriptors
from exceptions import TerminateLoop

locale.setlocale(locale.LC_ALL, '')


class Templa(object):

    def __init__(self, ret, action_name, f=None):
        self.global_lock = threading.Lock()
        self.ret = ret
        self.action_name = action_name
        self.action = Actions()
        self.keyhandler = KeyHandler()
        self.conf = Config()
        self.y, self.x = 1, 0

        if f is None:
            self.stdin = sys.stdin
            self.stdout = sys.stdout
            self.stderr = sys.stderr
        else:
            self.stdin = f["stdin"]
            self.stdout = f["stdout"]
            self.stderr = f["stderr"]

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)

        self.display = Display(self.stdscr)
        self.model = Model(self.ret, self.display)

        # Invalidation Ctrl + z
        signal.signal(signal.SIGINT, lambda signum, frame: None)
        self.stdscr.keypad(True)

        curses.raw()
        curses.noecho()
        curses.cbreak()
        curses.nonl()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        curses.nl()
        curses.endwin()
        self.action.output_to_stdout("test")
        # TODO action

    # http://docs.python.jp/2/library/threading.html#timer-objects
    RE_DESPICTION_DELAY = 0.05

    def loop(self):
        # initialize
        self.refresh_display()
        self.updating_timer = None

        def despiction():
            self.y, self.x = 1, 0
            self.keyhandler.handle_key(self.key)
            self.view = View(self.stdscr, self.model, self.y, self.x, self.display, self.keyhandler)
            self.view.update()
            self.model = self.view.model
            self.model.update()
            self.stdscr.refresh()

        while True:
            try:
                self.key = self.stdscr.getch()
                # if self.model.is_search():
                # 入力文字
                if self.keyhandler.is_displayable_key(self.key):
                    with self.global_lock:

                        if self.key == ord("q"):
                            break

                        if self.updating_timer is not None:
                            # clear timer
                            self.updating_timer.cancel()
                            self.updating_timer = None
                        timer = threading.Timer(self.RE_DESPICTION_DELAY,
                                                despiction)
                        self.updating_timer = timer
                        timer.start()

                self.refresh_display(self.key)
            except TerminateLoop as e:
                return e.value

    def refresh_display(self, key=None):
        self.stdscr.erase()
        self.keyhandler.handle_key(key)
        self.view = View(self.stdscr, self.model, self.y, self.x, self.display, self.keyhandler)
        self.view.update()
        self.y = self.view.new_pos_y
        self.stdscr.refresh()

    def finish(self, value=0):
        raise TerminateLoop(self.finish_with_exit_code(value))

    def cancel(self):
        raise TerminateLoop(self.cancel_with_exit_code())

    def finish_with_exit_code(self, value):
        self.args_for_action = self.view.select_value
        return value

    def cancel_with_exit_code(self):
        return 1


class Core(object):

    def __init__(self, func,  **kwargs):
        self.collections = func()
        action = kwargs.get('default_action')
        ttyname = get_ttyname()

        with open(ttyname, 'r+w') as ttyfile:

            with Templa(self.collections, action, reconnect_descriptors(ttyfile)) as templa:
                value = templa.loop()
            sys.exit(value)
