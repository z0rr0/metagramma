#!/usr/bin/env python3.6
import io

from bisect import bisect_left
from datetime import datetime
from functools import wraps


def time_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = f(*args, **kwargs)
        print('duration of {}={}'.format(f.__name__, datetime.now() - start))
        return result
    return wrapper


def levenshtein_distance(a: str, b: str) -> int:
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]
    

class Grammer(object):

    def __init__(self, fd: io.TextIOBase) -> None:
        self.fd = fd
        self.matrix = []
        self.rlist = []

    @staticmethod
    def similar(w1: str, w2: str) -> bool:
        if len(w1) != len(w2) or w1 == w2:
            return False
        return levenshtein_distance(w1, w2) == 1

    @classmethod
    def _candidates(cls, x: tuple, items: list, lengths: tuple) -> list:
        b = bisect_left(lengths, x[0])
        return [k + b for k, item in enumerate(items[b:]) if cls.similar(x[1], item[1])]

    def build_related_list(self) -> list:
        self.rlist = []
        lines = [(len(x.strip()), x.strip()) for x in self.fd.readlines()]
        lengths = tuple(x[0] for x in lines)
        lines.sort()
        for i, line in enumerate(lines):
            related = self._candidates(line, lines[:i], lengths[:i])
            idx = len(self.rlist)
            for j in related:
                self.rlist[j][1].append(idx)
            self.rlist.append((line[1], related))
        return self.rlist
