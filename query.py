#!/usr/bin/env python3

import ast

nodes = []
with open("./data/Rtree.txt", "r") as Rtree_file:
    lines = Rtree_file.readlines()
    for line in lines:
        nodes.append(ast.literal_eval(line))

print(len(nodes[0]))
