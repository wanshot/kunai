# -*- coding: utf-8 -*-

import sys
import curses
import locale
# from tempra.screen import Screen
from screen import Screen

locale.setlocale(locale.LC_ALL, '')


class Deploy(object):

    def __init__(self, func,  **kwargs):
        self.ret = func()
        self.value = None

        with Screen(self.ret) as s:
            y, x = 1, 6

            while True:
                key = s.stdscr.getch()
                if key == ord("q"):
                    break

                if key == curses.KEY_DOWN:
                    try:
                        s.stdscr.addstr(y+1, 0, s.line_storege[y+1], curses.color_pair(1))
                        s.stdscr.addstr(y, 0, s.line_storege[y])
                        y = y + 1
                    except KeyError:
                        pass

                if key == curses.KEY_UP:
                    if y == 1:
                        pass
                    else:
                        try:
                            s.stdscr.addstr(y-1, 0, s.line_storege[y-1], curses.color_pair(1))
                            s.stdscr.addstr(y, 0, s.line_storege[y])
                            y = y-1
                        except KeyError:
                            pass

                if key == ord("a"):
                    self.value = s.line_storege[y]
                    break

        if self.value:
            return self._output(self.value)

    def _output(self, value):
        sys.stdout.write(value)


def deploy(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Deploy(args[0], **kwargs)

    # def inner(obj):
    #     obj = Deploy(obj)
    #     return obj
    # return inner
