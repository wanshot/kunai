# -*- coding: utf-8 -*-

import sys
import curses
import locale
import signal
import threading
import curses.ascii

from config import LoadConfig
from model import Model
from display import Display
from view import View
from key import KeyHandler
from tty import get_ttyname, reconnect_descriptors

__all__ = (
    "fry",
)

locale.setlocale(locale.LC_ALL, '')


class TerminateLoop(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Templa(object):

    def __init__(self, ret, f=None):
        self.global_lock = threading.Lock()
        self.ret = ret
        self.conf = LoadConfig()
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
        self.height, self.width = self.stdscr.getmaxyx()
        curses.curs_set(0)

        self.display = Display(self.stdscr)
        self.model = Model(self.ret, self.height, self.width)

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

    # http://docs.python.jp/2/library/threading.html#timer-objects
    RE_DEPICTION_DELAY = 0.05

    def loop(self):
        # initialize
        self.refresh_display()
        self.updating_timer = None

        def re_despiction():
            view = View(self.stdscr, self.model, self.y, self.x, self.display)
            view.update()

        while True:
            try:
                key = self.stdscr.getch()
                keyhandler = KeyHandler(key)
                view = View(self.stdscr, self.model, self.y, self.x,
                            self.display, keyhandler)

                if view.new_pos_y:
                    self.y = view.new_pos_y
                else:
                    self.model = view.model
                    self.model.update()

                    if self.model.keyword:
                        with self.global_lock:

                            if key == ord("q"):
                                break

                            if self.updating_timer is not None:
                                # clear timer
                                self.updating_timer.cancel()
                                self.updating_timer = None
                            timer = threading.Timer(self.RE_DEPICTION_DELAY,
                                                    re_despiction)
                            self.updating_timer = timer
                            timer.start()

                    self.refresh_display()
            except TerminateLoop as e:
                return e.value

    def refresh_display(self):
        with self.global_lock:
            self.y, self.x = 1, 0
            self.stdscr.erase()
            view = View(self.stdscr, self.model, self.y, self.x, self.display)
            view.update()
            self.stdscr.refresh()


class Core(object):

    def __init__(self, func,  **kwargs):
        self.collections = func()

        ttyname = get_ttyname()

        with open(ttyname, 'r+w') as ttyfile:

            with Templa(self.collections, reconnect_descriptors(ttyfile)) as templa:
                value = templa.loop()
            sys.exit(value)


def fry(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Core(args[0], **kwargs)
