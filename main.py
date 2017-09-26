#!/usr/bin/env python3.6

import argparse
import io
import sys

from mg import Grammer


def main(fd: io.TextIOBase) -> None:
    grammer = Grammer(fd)
    matrix = grammer.build_matrix()
    # print(matrix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='metagramma tool')
    parser.add_argument(
        '-f',
        dest='src_file',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='source dictionary file'
    )

    args, _ = parser.parse_known_args()
    main(args.src_file)
