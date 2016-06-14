# -*- coding: utf-8 -*-
from collections import defaultdict


def search_query(line, pattern):
    """Scanning line
    """

    ret = []
    begin = 0
    position = 0

    while begin >= 0:
        begin = get_target_position(line, pattern)
        position += begin + 1
        if begin < 0:
            break
        line = line[begin+1:]
        ret.append(position-1)

    return ret


def get_target_position(line, pattern):
    """String search algorithm
    """

    m, n = len(line), len(pattern)
    if m < n:
        return -1
    skip_bad_char = defaultdict(lambda: n + 1)
    for i in range(n):
        skip_bad_char[pattern[i]] = n - i

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
            # finish
            return -1
        else:
            # skip
            pos += skip_bad_char[line[pos + n]]
    # finish
    return -1
