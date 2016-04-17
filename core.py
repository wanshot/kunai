# -*- coding: utf-8 -*-

import curses
import locale
from screen import Screen

locale.setlocale(locale.LC_ALL, '')


class Deploy(object):

    def __init__(self, func,  **kwargs):
        self.ret = func()
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
                    self.s.stdscr.addstr(self.y+1, 0, self.s.line_storege[self.y], curses.color_pair(1))
                    self.s.stdscr.addstr(self.y, 0, self.s.line_storege[self.y-1])
                    self.y = self.y + 1

            if key == curses.KEY_UP:
                if self.y == 0:
                    pass
                else:
                    self.s.stdscr.addstr(self.y-1, 0, self.s.line_storege[self.y-2], curses.color_pair(1))
                    self.s.stdscr.addstr(self.y, 0, self.s.line_storege[self.y-1])
                    self.y = self.y-1


def deploy(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Deploy(args[0], **kwargs)

    # def inner(obj):
    #     obj = Deploy(obj)
    #     return obj
    # return inner


@deploy
def main():
    pass
    return ["a", "b", "c"]

# main = tes(main)

if __name__ == "__main__":
    main
