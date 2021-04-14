#!/usr/bin/env python3

import sys
from typing import List

from Rectangle import calculate_MBR, calculate_Geohash
from Node import RTreeNode, RTreeEntry
from utils import distribute

node_array = []  # array that holds the nodes
node_count = 0
tree_level = 0
C = 20  # node capacity
min_C = 8  # node minimum capacity
coords_file, offsets_file, outfile = sys.argv[1:4]


def load_entries(coords_file: str, offsets_file: str) -> List[RTreeEntry]:
    leaf_entries = []
    with open(coords_file) as coords, open(offsets_file) as offsets:
        offsets_lines = offsets.readlines()
        for line in offsets_lines:
            id, startOffset, endOffset = line.rstrip("\n").split(',')
            lines_count = int(endOffset) - int(startOffset) + 1
            object_coords = []
            for _ in range(lines_count):
                x, y = coords.readline().rstrip("\n").split(',')
                object_coords.append([float(x), float(y)])
            entry = RTreeEntry(id, calculate_MBR(object_coords))
            entry.geohash = calculate_Geohash(entry.mbr)
            leaf_entries.append(entry)
        # use geohashing to sort objects and reduce empty space in the MBRs
        leaf_entries.sort(key=lambda obj: obj.geohash)
        # delete geohashes to free up some memory
        for entry in leaf_entries:
            del entry.geohash
    return leaf_entries


def construct(entries: List[RTreeEntry], curr_tree_level: int, isnonleaflevel: int):
    global node_count, node_array

    curr_level_nodes = []
    if len(entries) > C:
        entries_split = distribute(entries, min_C, C)
        for entries in entries_split:
            curr_level_nodes.append(RTreeNode(id=node_count, isnonleaf=isnonleaflevel, entries=entries))
            node_count += 1
        print(f'{len(curr_level_nodes)} nodes at level {curr_tree_level}')
        node_array += curr_level_nodes

        # create entries for next level
        # we calculate each node mbr and we create a list of RTreeEntry objects
        next_level_entries = []
        for node in curr_level_nodes:
            next_level_entries.append(RTreeEntry(entry_id=node.id, mbr=node.get_mbr()))
        curr_tree_level += 1
        construct(entries=next_level_entries, curr_tree_level=curr_tree_level, isnonleaflevel=1)
    else:
        # we reached root node
        root_node = RTreeNode(id=node_count, isnonleaf=isnonleaflevel, entries=entries)
        node_array.append(root_node)
        print(f'1 nodes at level {curr_tree_level}')


leaf_entries = load_entries(coords_file, offsets_file)

construct(entries=leaf_entries, curr_tree_level=tree_level, isnonleaflevel=0)

with open(outfile, 'w') as out:
    out.writelines(f'{str(node)}\n' for node in node_array)
