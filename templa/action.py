# -*- coding: utf-8 -*-
import sys
import subprocess


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
        subprocess.check_output(ret.strip(), shell=True, stderr=subprocess.STDOUT)
#         sys.stdout.write(ret)
#         sys.stdout.write('\n')
