#!/usr/bin/env python3.6
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

    def build_related_list(self) -> list:

        def same(w1: str, w2: str) -> bool:
            diff = 0
            for i, s in enumerate(w1):
                if w2[i] != s:
                    diff += 1
                if diff > 1:
                    return False
            return diff == 1

        def _candidates(n: int, x: str, items: list) -> list:
            from_item = '0' * n
            to_item = '0' * (n + 1)
            a = bisect_left(items, from_item)
            b = bisect_left(items, to_item, lo=a)
            return [i + a for i, item in enumerate(items[a:b]) if same(x, item)]

        lines = [(len(x.strip()), x.strip()) for x in self.fd.readlines()]
        lines.sort()
        handled = []
        for l, cw in lines:
            related = _candidates(l, cw, handled)
            idx = len(self.rlist)
            for j in related:
                self.rlist[j][1].append(idx)
            self.rlist.append((cw, related))
            handled.append(cw)
        return self.rlist
