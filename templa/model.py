# -*- coding: utf-8 -*-
# from .exceptions import ParseError
import re
from itertools import cycle
from collections import OrderedDict
import unicodedata


class Model(object):

    def __init__(self, list_, height, width):
        self.list_ = list_
        self.height = height
        self.width = width

        self.keyword = u''
        self.pager = self._create_pager()

    def _create_pager(self, new_list=None):
        """
        >>> model = self.Model(["hoge", "huga", "piyo"], 2)
        >>> model.pager.next()
        (1, OrderedDict([(1, 'hoge'), (2, 'huga')]))
        >>> model.pager.next()
        (2, OrderedDict([(1, 'piyo')]))
        >>> model.pager.next()
        (1, OrderedDict([(1, 'hoge'), (2, 'huga')]))
        """
        r = self.list_
        if isinstance(new_list, list):
            r = new_list

        pages = OrderedDict()
        for page_num, c in enumerate(range(0, len(r), self.height-1), start=1):
            od = OrderedDict()
            for lineno, line in enumerate(r[c:c + self.height-1], start=1):
                od[lineno] = self._adapt(line)
            pages[page_num] = od

        return cycle(pages.items())

    def update(self):
        """Update Model Pager
        """
        updated = [x for x in self.list_ if self.keyword in x]
        self.pager = self._create_pager(updated)

    def _adapt(self, line):
        ea_count = len([u for u in line.decode('utf-8') if unicodedata.east_asian_width(u) in ('F', 'W')])
        unicode_diff = len(line.decode('utf-8')) - ea_count
        diff_byte = self.width - (unicode_diff + (ea_count * 2))
        max_line = line + diff_byte * " "
        return max_line[:self.width]

    def markup(self, line):
        result = []

        if self.keyword:
            for x in re.finditer(ur"{}".format(self.keyword), line):
                result.append((x.start(), x.end()))

        return result
