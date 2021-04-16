#!/usr/bin/env python3
import sys

from Rtree import Rtree

dumpfile, queries_file = sys.argv[1:3]

rtree = Rtree()

rtree.constructFromDumpfile(dumpfile)
