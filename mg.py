#!/usr/bin/env python3.6
import bisect
import io

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


def bisect_left(a: list, x: str, lo=0, hi=None) -> int:
    hi = len(a) if not hi else hi
    compare_less = lambda k, m: len(k) < len(m) or (len(k) == len(m) and k <= m)

    def bs(items: list, el: str, i, j):
        if not items[i:j]:
            return 0
        elif len(items[i:j]) == 1:
            return i if compare_less(el, items[i]) else j
        mid = len(items[i:j]) // 2
        idx = i + mid
        if compare_less(el, items[idx]):
            return bs(items, el, i, idx)
        else:
            return bs(items, el, idx, j)

    r = bs(a, x, lo, hi)
    return r
    

class Grammer(object):

    def __init__(self, fd: io.TextIOBase) -> None:
        self.fd = fd
        self.matrix = []
        self.rlist = []

    @staticmethod
    def _compare(w1: str, w2: str) -> int:
        if len(w1) == len(w2):
            if len(set(w1).intersection(set(w2))) == len(w1) - 1:
                return 1
        return 0

    def build_related_matrix(self) -> list:
        words = []
        for line in self.fd:
            words.append(line.strip())
            row = [self._compare(words[-1], w) for w in words]
            self.matrix.append(row)
            for i, r in enumerate(self.matrix[:-1]):
                r.append(row[i])
        return self.matrix

    @time_decorator
    def build_related_list2(self) -> list:
        for line in self.fd:
            cw = line.strip()
            related = [i for i, item in enumerate(self.rlist) if self._compare(cw, item[0])]

            idx = len(self.rlist)
            for j in related:
                self.rlist[j][1].append(idx)
            self.rlist.append((cw, related))
        return self.rlist

    @time_decorator
    def build_related_list(self) -> list:

        def _candidates(x: str, items: list) -> list:
            n = len(x)
            from_item = '0' * n
            to_item = '0' * (n + 1)
            a = bisect_left(items, from_item)
            b = bisect_left(items, to_item, lo=a)
            # print('x', x, n, from_item, to_item, a, b, items)
            return [i + a for i, item in enumerate(items[a:b]) if self._compare(x, item)]

        lines = sorted(self.fd.readlines(), key=lambda x: (len(x), x))
        handled = []
        for line in lines:
            cw = line.strip()
            related = _candidates(cw, handled)
            # if related:
            #     print('related', related)
            idx = len(self.rlist)
            for j in related:
                self.rlist[j][1].append(idx)
            self.rlist.append((cw, related))
            handled.append(cw)
        return self.rlist
