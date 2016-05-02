# -*- coding: utf-8 -*-
# from .exceptions import ParseError
from collections import OrderedDict


class Model(object):

    def __init__(self, list_):
        self.lines = None
        self.keyword = u''

        if isinstance(list_, list):
            self.list_ = list_
            self.lines = self._create_lines()

    def _create_lines(self):
        r = OrderedDict()
        for lineno, line in enumerate(self.list_, start=1):
            if isinstance(line, str):
                line = line.encode('utf-8')
            elif isinstance(line, unicode):
                pass
            else:
                raise TypeError("Required argument hoge not str or unicode")

            r[lineno] = line

        return r

    def update(self, keyword):
        """Update Model Class
        """
        if self.keyword:
            self.keyword += keyword
        else:
            self.keyword = keyword

        r = OrderedDict()
        lineno = 1
        for line in self.lines.values():
            if self.keyword in line:
                r[lineno] = line
                lineno += 1

        self.lines = r
