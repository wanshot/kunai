# -*- coding: utf-8 -*-

import sys
import types
import curses
import locale
import signal
import threading
import subprocess
import curses.ascii

from model import Screen
from display import Display
from command import Command
from view import View
from key import KeyHandler
from parser import ExecFileParser
from tty import get_ttyname, reconnect_descriptors
from exceptions import TerminateLoop
from config import Config

locale.setlocale(locale.LC_ALL, '')


class Kunai(object):

    RE_DESPICTION_DELAY = 0.05

    def __init__(self, function_name, request, kwargs, descriptors=None):
        self.global_lock = threading.Lock()
        self.render_name = function_name
        self.request = request
        self.action_name = kwargs.get('action')
        self.args_for_action = None
        self.parser = ExecFileParser()
        self.keyhandler = KeyHandler()
        self.conf = Config()

        if descriptors is None:
            self.stdin = sys.stdin
            self.stdout = sys.stdout
            self.stderr = sys.stderr
        else:
            self.stdin = descriptors['stdin']
            self.stdout = descriptors['stdout']
            self.stderr = descriptors['stderr']

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)

        display = Display()
        screen = Screen(self.stdscr, self.request)
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
        """Exit and action or call next kunai action
        """
        curses.nl()
        curses.endwin()
        if self.action_name:
            # next action
            self.parser.pick_command(self.action_name)
            for const in self.parser.code_obj.co_consts:
                # XXX get only action method code object
                if isinstance(const, types.CodeType):
                    self.parser.set_importmodule_code(const)
                    exec(self.parser.code_obj, {
                        # set globals
                        self.render_name: self.args_for_action,
                    })
        else:
            # finish
            self.execute_command()

    def loop(self):
        # initialize
        self.view.refresh_display()
        self.updating_timer = None

        def despiction():
            self.view.search_query(self.keyhandler.current_key)

        while True:
            self.view.refresh_display()
            try:
                key = self.stdscr.getch()
                self.keyhandler.handle_key(key)
                if self.keyhandler.has_query:
                    with self.global_lock:

                        if self.updating_timer is not None:
                            # clear timer
                            self.updating_timer.cancel()
                            self.updating_timer = None
                        timer = threading.Timer(self.RE_DESPICTION_DELAY,
                                                despiction)
                        self.updating_timer = timer
                        timer.start()

                Command(self)
            except TerminateLoop as e:
                return e.value

    def finish(self, value=0):
        raise TerminateLoop(self.finish_with_exit_code(value))

    def cancel(self):
        raise TerminateLoop(self.cancel_with_exit_code())

    def finish_with_exit_code(self, value):
        if isinstance(self.request, dict):
            self.args_for_action = self.request[self.view.select_line.strip().decode('utf-8')]
        else:
            self.args_for_action = self.view.select_line
        return value

    def cancel_with_exit_code(self):
        return 1

    def execute_command(self):
        """Execute action

        kunai default action
        """
        p = subprocess.Popen(
            self.args_for_action,
            stdout=subprocess.PIPE,
            shell=True,
            executable=self.conf.shell
        )
        (output, err) = p.communicate()
        self.stdout.write(output)


class Core(object):

    def __init__(self, function, action_name=None, **kwargs):
        request = function()
        function_name = function.__name__
        ttyname = get_ttyname()

        if isinstance(request, (list, dict)):
            with open(ttyname, 'r+w') as tty_file:
                with Kunai(function_name,
                           request,
                           kwargs,
                           reconnect_descriptors(tty_file)
                           ) as kunai:
                    value = kunai.loop()
        else:
            value = u'argment is not list or dict'

        sys.exit(value)
