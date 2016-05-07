# -*- coding: utf-8 -*-

import sys
import curses
import locale
import signal
import threading
import curses.ascii

from manage import LoadConfig
from model import Model
from display import Display
from tty import get_ttyname, reconnect_descriptors
from key import SP_KEYS

locale.setlocale(locale.LC_ALL, '')


class TerminateLoop(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Templa(object):

    def __init__(self, ret, f):
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
        self.page = None

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
            self._set_prompt()
            self._set_lines()

        while True:
            try:
                key = self.stdscr.getch()

                if SP_KEYS.get(key):
#                   curses.erasechar()
                    self.y = self.model.key_handler(self.y,
                                                    self.x,
                                                    self.page,
                                                    self.display.select,
                                                    SP_KEYS[key],
                                                    self.stdscr)

                else:
                    if key == 127:
                        self.model.erasechar()
                        self.model.update()
                    else:
                        self.model.keyword += curses.ascii.unctrl(key)
                        self.model.update()

                    if self.model.keyword:
                        with self.global_lock:

                            if key == ord("q"):
                                break

                            if self.updating_timer is not None:
                                # clear timer
                                self.updating_timer.cancel()
                                self.updating_timer = None
                            timer = threading.Timer(self.RE_DEPICTION_DELAY, re_despiction)
                            self.updating_timer = timer
                            timer.start()

                    self.refresh_display()
            except TerminateLoop as e:
                return e.value

    def refresh_display(self):
        with self.global_lock:
            self.y, self.x = 1, 0
            self.stdscr.erase()
            self._set_prompt()
            self._set_lines()
            self.stdscr.refresh()

    def _set_lines(self):
        _, self.page = self.model.pager.next()
        for lineno, line in self.page.items():
            if lineno == 1:  # set first line color
                self.stdscr.addstr(lineno, 0, line, self.display.select)
            else:
                self.stdscr.addstr(lineno, 0, line, self.display.normal)
                # markup
                if self.model.keyword:
                    for start, end in self.model.markup(line):
                        self.stdscr.chgat(lineno, start, end, curses.color_pair(3))
        self.stdscr.move(1, 3)

    def _set_prompt(self):
        # default prompt label
        label = '%'
        if self.conf.input_field_label:
            label = self.conf.input_field_label

        self.stdscr.addstr(0, 0, '{} {}'.format(label, self.model.keyword))

#     def addstr(self, pos_y, pos_x=0, witdth, height, line, display):
        # 別のクラスに実装する
        # 他のラップする関数もまとめる
#         adapt_line = _adapt_line(line)[:self.width]


class Core(object):

    def __init__(self, func,  **kwargs):
        self.list_ = func()

        ttyname = get_ttyname()

        with open(ttyname, 'r+w') as ttyfile:

            with Templa(self.list_, reconnect_descriptors(ttyfile)) as templa:
                value = templa.loop()
            sys.exit(value)


def deploy(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Core(args[0], **kwargs)
