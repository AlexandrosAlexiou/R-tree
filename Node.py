from typing import List

from Rectangle import Rectangle, calculate_MBR


class RTreeEntry:
    """
    R-Tree entry, containing the entry id which can be a node id if the node isnonleaf or an object id if the node
    is a leaf node.
    """
    def __init__(self, entry_id: int, mbr: Rectangle):
        self.entry_id = entry_id
        self.mbr = mbr
        self.geohash = None

    def __str__(self):
        return f'[{self.entry_id}, [{str(self.mbr)}]]'


class RTreeNode:
    """
    R-Tree node, containing the node id, info if the node is a leaf node and a list of entries.
    """
    def __init__(self, id: int, isnonleaf: int, entries: List[RTreeEntry]):
        self.id = id
        self.isnonleaf = isnonleaf
        self.entries = entries

    def get_mbr(self) -> Rectangle:
        coords = []
        for entry in self.entries:
            coords.append([entry.mbr.x_low, entry.mbr.y_low])
            coords.append([entry.mbr.x_high, entry.mbr.y_high])
        return calculate_MBR(coords)

    def __str__(self):
        entries_string = str(self.entries[0])
        for entry in self.entries[1:]:
            entries_string += f', {str(entry)}'

        return f'[{self.isnonleaf}, {self.id}, [{entries_string}]]'

