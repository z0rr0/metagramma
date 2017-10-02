#!/usr/bin/env python3.6

import argparse
import io
import json

from mg import Grammer


def main(ifd: io.TextIOBase, sfd: io.TextIOBase) -> None:
    if ifd:
        # init
        grammer = Grammer(ifd)
        rlist = grammer.build_related_list()
        print(json.dumps(rlist))
    elif sfd:
        rlist = json.load(sfd)
        print('kk', rlist)
    else:
        raise ValueError('set init or sorce file')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='metagramma tool')
    parser.add_argument(
        '-i',
        dest='init_file',
        type=argparse.FileType('r'),    
        help='init dictionary file'
    )
    parser.add_argument(
        '-s',
        dest='src_file',
        type=argparse.FileType('r'),
        help='source JSON file'
    )

    args, _ = parser.parse_known_args()
    main(args.init_file, args.src_file)
