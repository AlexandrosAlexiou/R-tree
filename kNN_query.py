#!/usr/bin/env python3

import sys

from Rtree import Rtree

dumpfile, kNNQueries_file, k = sys.argv[1:4]

# Instantiate the Rtree
rtree = Rtree()

# construct the Rtree from the dump file
rtree.constructFromDumpfile(dumpfile)

# open NNQueries file and perform each query to the tree
for lineno, line in enumerate(open(kNNQueries_file)):
    (x, y) = list(map(float, line.rstrip("\n").split(" ")))
    print(f'{lineno}:', rtree.kNNQuery(root=rtree.root, q=(x, y), k=int(k)))
