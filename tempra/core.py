# -*- coding: utf-8 -*-

import sys
import curses
import locale
from .screen import Screen

locale.setlocale(locale.LC_ALL, '')


class Deploy(object):

    def __init__(self, func,  **kwargs):
        self.ret = func()
        self.value = None

        self.s = Screen(self.ret)
        self.y, self.x = 0, 6

        while True:
            key = self.s.stdscr.getch()
            if key == ord("q"):
                break

            if key == curses.KEY_DOWN:
                if self.y == 0:
                    self.y = self.y + 1
                else:
                    try:
                        self.s.stdscr.addstr(self.y+1, 0, self.s.line_storege[self.y], curses.color_pair(1))
                        self.s.stdscr.addstr(self.y, 0, self.s.line_storege[self.y-1])
                        self.y = self.y + 1
                    except IndexError:
                        pass

            if key == curses.KEY_UP:
                if self.y == 1:
                    pass
                else:
                    try:
                        self.s.stdscr.addstr(self.y-1, 0, self.s.line_storege[self.y-2], curses.color_pair(1))
                        self.s.stdscr.addstr(self.y, 0, self.s.line_storege[self.y-1])
                        self.y = self.y-1
                    except IndexError:
                        pass

            if key == ord("a"):
                self.value = self.s.line_storege[self.y]
                break
#                 self._action(self.s.line_storege[self.y])

        print self.value
        return self._action(self.value)

    def _action(self, line):
        sys.stdout.write(line)


def deploy(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Deploy(args[0], **kwargs)

    # def inner(obj):
    #     obj = Deploy(obj)
    #     return obj
    # return inner
