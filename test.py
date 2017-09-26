#!/usr/bin/env python3.6

import io
import unittest

from mg import Grammer


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
        matrix = self.grammer.build_matrix()
        self.assertEqual(matrix, expected)


if __name__ == '__main__':
    unittest.main()
