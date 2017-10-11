#!/usr/bin/env python3

import tempfile
import unittest

from mg import Grammer, levenshtein_distance


class GrammerTestCase(unittest.TestCase):

    def test_related_list(self):
        items = [
            'ab\n',
            'ba\n',
            'be\n',
            'abc\n',
            'abe\n',
            'afe\n',
            'wxyy\n',
            'wyxy\n',
            'wyyy\n',
        ]
        fd = tempfile.TemporaryFile(mode='w+')
        fd.writelines(items)
        fd.seek(0)
        grammer = Grammer(fd)

        result = [
            ('ab', []),
            ('ba', [2]),
            ('be', [1]),
            ('abc', [4]),
            ('abe', [3, 5]),
            ('afe', [4]),
            ('wxyy', [8]),
            ('wyxy', [8]),
            ('wyyy', [6, 7]),
        ]
        rlist = grammer.build_related_list()
        fd.close()
        self.assertEqual(rlist, result)


class HelpersTestCase(unittest.TestCase):

    def test_levenshtein_distance(self):
        items = (
            (('', ''), 0),
            (('ab', 'ba '), 2),
            (('azcde', 'abcde'), 1),
            (('abcde', 'abcde'), 0),
            (('юяяя', 'яяяф'), 2),
        )
        for args, n in items:
            self.assertEqual(levenshtein_distance(*args), n, args)


if __name__ == '__main__':
    unittest.main()
