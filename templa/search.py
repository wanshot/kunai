# -*- coding: utf-8 -*-
from collections import defaultdict


def search_keyword(line, pattern):
    beg = sunday_algorithm(line, pattern)
    end = beg + len(pattern)
    return beg, end


def sunday_algorithm(line, pattern):
    m, n = len(line), len(pattern)
    if m < n:
        return -1
    bad_char_jump = defaultdict(lambda: n + 1)
    for i in range(n):
        bad_char_jump[pattern[i]] = n - i
    pos = 0
    while pos <= m - n:
        i, j = pos, 0
        while j < n and line[i] == pattern[j]:
            i += 1
            j += 1
        if j == n:
            # match
            return pos
        elif pos == m - n:
            return -1
        else:
            # skip
            pos += bad_char_jump[line[pos + n]]
    return -1
