from typing import List

from Node import RTreeEntry
from Rectangle import calculate_MBR, calculate_Geohash


def load_entries(coords_file: str, offsets_file: str) -> List[RTreeEntry]:
    """
    Create and return the leaf entries using the input files.
    Leaf entries are all the objects of the first level of the tree
    that will be split in twenties and will be packed into nodes.
    """
    entries = []
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
            entries.append(entry)
        # use geohashing to sort objects and reduce empty space in the MBRs
        entries.sort(key=lambda obj: obj.geohash)
        # delete geohashes to free up some memory
        for entry in entries:
            del entry.geohash
    return entries


def chunks(lst, n) -> List:
    """Yield n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def distribute(entries_to_split: List[RTreeEntry], min_c: int, c: int) -> List[List[RTreeEntry]]:
    """
    Split the entries to groups of twenties and check if last the last node has at lease min_c entries.
    If not remove elements from previous node and add them to the last node such that
    the minimum node capacity requirements is met.
    """
    entries_split = list(chunks(entries_to_split, c))
    last = entries_split[-1]
    if len(last) < min_c:

        remaining = min_c - len(last)
        elements = []
        for _ in range(remaining):
            elements.append(entries_split[-2].pop())
        for element in elements:
            entries_split[-1].insert(0, element)

    return entries_split
