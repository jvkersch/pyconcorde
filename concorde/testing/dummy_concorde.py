#!/usr/bin/env python

import argparse
import os
import stat
import sys
import textwrap


def main():
    # print CLI args
    print(sys.argv[1:])

    # parse arguments
    p = argparse.ArgumentParser()
    p.add_argument("fname")
    args, unknown = p.parse_known_args()

    # write dummy sol file
    sol_fname = os.path.splitext(args.fname)[0] + ".sol"
    with open(sol_fname, "wt") as fp:
        fp.write("5\n")
        fp.write("0 1 2 3 4\n")


if __name__ == "__main__":
    main()
