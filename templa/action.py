# -*- coding: utf-8 -*-
import sys


class Actions(object):

    def _check_func(self):
        """check functions
        """
        # TODO raise duplicate func_name
        pass

    def execute(self, ret, func=None):
        if func is None:
            self.output_to_stdout(ret)
        else:
            getattr(self, func.__name__)(ret)

    def output_to_stdout(self, ret):
        """default action
        """
        sys.stdout.write(ret)
