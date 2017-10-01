#!/usr/bin/env python3.6

import io
import unittest

from mg import Grammer, bisect_left


class HelpersTestCase(unittest.TestCase):

    def test_bisect(self):
        items = sorted(
            [
                'a',
                'b',
                'd',
                'aa',
                'ac',
                'bb'
            ],
            key=lambda c: (len(c), c)
        )
        values = (
            ('a', 0, []),
            ('b', 0, []),
            ('ab', 0, []),
            ('b', 1, items),
            ('c', 2, items),
            ('aa', 3, items),
            ('ab', 4, items),
            ('aaa', 6, items),
        )
        for x, i, a in values:
            j = bisect_left(a, x)
            self.assertEqual(i, j, 'invalid {}!={}, x={} a={}'.format(i, j, x, a))


class GrammerTestCase(unittest.TestCase):

    def setUp(self):
        fd = io.StringIO()
        fd.writelines([
            'abcd\n',
            'abce\n',
            'abfe\n',
            'abcdf\n',
            'abcde\n',
        ])
        fd.seek(0)
        self.grammer = Grammer(fd)

    def test_build(self):
        expected = [
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
        ]
        matrix = self.grammer.build_related_matrix()
        self.assertEqual(matrix, expected)


if __name__ == '__main__':
    unittest.main()
