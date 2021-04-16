#!/usr/bin/env python3

import sys

from Rtree import Rtree
from utils import load_entries

coords_file, offsets_file, outfile = sys.argv[1:4]

# Instantiate the Rtree
rtree = Rtree()

# Load entries from the data files using the utils
leaf_entries = load_entries(coords_file, offsets_file)

# start the construction passing the leaf entries
rtree.construct(entries=leaf_entries, curr_tree_level=0, isnonleaflevel=0)

# dump the tree
rtree.dump(outfile)

