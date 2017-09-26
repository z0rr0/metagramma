#!/usr/bin/env python3.6

import io


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

    def build_related_list(self) -> list:
        for line in self.fd:
            cw = line.strip()
            related = [i for i, item in enumerate(self.rlist) if self._compare(cw, item[0])]

            idx = len(self.rlist)
            for j in related:
                self.rlist[j][1].append(idx)
            self.rlist.append((cw, related))
        return self.rlist
