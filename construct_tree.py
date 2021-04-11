#!/usr/bin/env python3

import sys
from Object import Object
from Node import RTreeNode, RTreeEntry

leaf_entries = []
node_array = []  # array that holds the nodes
node_count = 0
tree_level = 0


def chunks(lst, n):
    """Yield n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_objects(coords_file, offsets_file):
    objects = []  # object array
    with open(coords_file) as coords, open(offsets_file) as offsets:
        offsets_lines = offsets.readlines()
        for line in offsets_lines:
            id, startOffset, endOffset = line.rstrip("\n").split(',')
            lines_count = int(endOffset) - int(startOffset) + 1
            object_coords = []
            for _ in range(lines_count):
                x, y = coords.readline().rstrip("\n").split(',')
                object_coords.append([float(x), float(y)])
            object = Object(id, object_coords)
            object.calculate_geohash()
            objects.append(object)
        # use geohashing to sort objects and reduce empty space in the MBRs later
        objects.sort(key=lambda object: object.geohash)
        # delete geohashes after the sort to free up memory and create entries
        for object in objects:
            leaf_entries.append(RTreeEntry(object.id, object.mbr))


load_objects(*sys.argv[1:])

entries_split = list(chunks(leaf_entries, 20))

for entries in entries_split:
    node_array.append(RTreeNode(node_id=node_count, isnonleaf=0, entries=entries))
    node_count += 1

print(*node_array, sep='\n')

# x = '[ "A","B","C" , " D"]'
# x = ast.literal_eval(x)
# print(x)
