#!/usr/bin/env python3

import sys

from Rtree import Rtree
from Rectangle import Rectangle

dumpfile, queries_file = sys.argv[1:3]

# Instantiate the Rtree
rtree = Rtree()

# construct the Rtree from the dump file
rtree.constructFromDumpfile(dumpfile)

for lineno, line in enumerate(open(queries_file)):
    x_low, y_low, x_high, y_high = list(map(float, line.rstrip("\n").split(" ")))
    window_query = Rectangle(x_low=x_low, x_high=x_high, y_low=y_low, y_high=y_high)
    results = list(rtree.range_query(node=rtree.root, window=window_query))
    print(f"{lineno} ({len(results)}): {str(results)[1:-1]}")

