#!/usr/bin/env python3.6

import io


class Grammer(object):

    def __init__(self, fd: io.TextIOBase) -> None:
        self.fd = fd
        self.matrix = []

    @staticmethod
    def _compare(w1, w2):
        if len(w1) == len(w2):
            if len(set(w1).difference(set(w2))) == 1:
                return 1
        return 0

    def build_matrix(self) -> list:
        words = []
        for line in self.fd:
            words.append(line.strip())
            row = [self._compare(words[-1], w) for w in words]
            self.matrix.append(row)
            for i, r in enumerate(self.matrix[:-1]):
                r.append(row[i])
        return self.matrix
