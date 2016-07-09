# -*- coding: utf-8 -*-

import sys
import curses
import locale
import signal
import threading
import curses.ascii

from model import Screen
from display import Display
from command import Command
from view import View
from key import KeyHandler
from action import Actions
from parser import ExecFileParser
from tty import get_ttyname, reconnect_descriptors
from exceptions import TerminateLoop

locale.setlocale(locale.LC_ALL, '')


class Templa(object):

    RE_DESPICTION_DELAY = 0.05

    def __init__(self, ret, parser, descriptors=None):
        self.global_lock = threading.Lock()
        self.ret = ret
        self.parser = parser
        self.args_for_action = None
        self.keyhandler = KeyHandler()

        if descriptors is None:
            self.stdin = sys.stdin
            self.stdout = sys.stdout
            self.stderr = sys.stderr
        else:
            self.stdin = descriptors["stdin"]
            self.stdout = descriptors["stdout"]
            self.stderr = descriptors["stderr"]

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)

        display = Display()
        screen = Screen(self.stdscr, self.ret)
        self.view = View(display, screen)

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
        exec self.parser.code_obj

    def loop(self):
        # initialize
        self.view.refresh_display()
        self.updating_timer = None

        def despiction():
            self.view.search_query(self.keyhandler.hold_key)

        while True:
            try:
                key = self.stdscr.getch()
                self.keyhandler.handle_key(key)
                if self.keyhandler.is_input_query:
                    with self.global_lock:

                        if self.updating_timer is not None:
                            # clear timer
                            self.updating_timer.cancel()
                            self.updating_timer = None
                        timer = threading.Timer(self.RE_DESPICTION_DELAY,
                                                despiction)
                        self.updating_timer = timer
                        timer.start()

                Command(self, self.view, self.keyhandler.state)
            except TerminateLoop as e:
                return e.value, self.args_for_action

    def finish(self, value=0):
        raise TerminateLoop(self.finish_with_exit_code(value))

    def cancel(self):
        raise TerminateLoop(self.cancel_with_exit_code())

    def finish_with_exit_code(self, value):
        self.args_for_action = self.view.select_line
        return value

    def cancel_with_exit_code(self):
        return 1


class Core(object):

    def __init__(self, func,  **kwargs):
        self.collections = func()
        self.action_name = kwargs.get('default_action')
        self.parser = ExecFileParser()
        ttyname = get_ttyname()
        self.action = Actions()

        self.parser.pick_command(self.action_name)

        with open(ttyname, 'r+w') as tty_file:

            with Templa(self.collections, self.parser, reconnect_descriptors(tty_file)) as templa:
                value, args_for_action = templa.loop()

#         self._run_action(args_for_action)
        sys.exit(value)

#     def _run_action(self, args_for_action):
#         sys.stdout.close()
#         exec self.parser.code_obj
