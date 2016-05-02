# -*- coding: utf-8 -*-

import sys
import curses
import locale
import codecs

from build import Templa
from tty import get_ttyname, reconnect_descriptors

locale.setlocale(locale.LC_ALL, '')


def read_input(filename):

    if filename:
        stream = codecs.getreader(locale.getpreferredencoding())(open(filename, "r"), "replace")
    else:
        stream = codecs.getreader(locale.getpreferredencoding())(sys.stdin, "replace")

    stream.close()


class Core(object):

    def __init__(self, func,  **kwargs):
        self.list_ = func()

        ###########
        self.stdscr = curses.initscr()
        self.stdscr.addstr(0, 0, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        ###########

        ttyname = get_ttyname()

        with open(ttyname, 'r+w') as ttyfile:

            with Templa(self.list_, reconnect_descriptors(ttyfile)) as templa:
                value = templa.loop()
            sys.exit(value)


def deploy(*args, **kwargs):

    if len(args) == 1 and callable(args[0]):
        return Core(args[0], **kwargs)
