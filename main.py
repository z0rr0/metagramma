#!/usr/bin/env python3

import argparse
import io
import json
import sys

from mg import Grammer, time_decorator


@time_decorator
def main(ifd: io.TextIOBase, sfd: io.TextIOBase, output: io.TextIOBase) -> None:
    if ifd:
        # init
        grammer = Grammer(ifd)
        rlist = grammer.build_related_list()
        json.dump(rlist, output)
    elif sfd:
        rlist = json.load(sfd)
    else:
        raise ValueError('set init or source file')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='metagramma tool')
    parser.add_argument(
        '-i',
        dest='init_file',
        type=argparse.FileType('r'),    
        help='init dictionary file'
    )
    parser.add_argument(
        '-d',
        dest='db',
        type=argparse.FileType('r'),
        help='prepared JSON file'
    )
    parser.add_argument(
        '-o',
        dest='output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output file'
    )

    args, _ = parser.parse_known_args()
    main(args.init_file, args.db, args.output)
