from typing import List
from Rectangle import Rectangle


class RTreeEntry:
    """
    R-Tree entry, containing the entry id which can be a node id if the node isnonleaf or an object id if the node
    is a leaf node.
    """
    def __init__(self, entry_id: int, mbr: Rectangle):
        self.entry_id = entry_id
        self.mbr = mbr

    def __str__(self):
        return f'[{self.entry_id}, [{str(self.mbr)}]]'


class RTreeNode:
    """
    R-Tree node, containing the node id, info if the node is a leaf node and a list of entries.
    """
    def __init__(self, node_id: int, isnonleaf: int, entries: List[RTreeEntry]):
        self.node_id = node_id
        self.isnonleaf = isnonleaf
        self.entries = entries

    def __str__(self):
        entries_string = str(self.entries[0])
        for entry in self.entries[1:]:
            entries_string += f', {str(entry)}'

        return f'[{self.isnonleaf}, {self.node_id}, [{entries_string}]]'

