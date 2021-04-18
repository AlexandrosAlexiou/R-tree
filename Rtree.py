from typing import List, Iterable

from Node import RTreeNode, RTreeEntry
from utils import distribute
from Rectangle import Rectangle


class Rtree:
    """
    This class holds the Rtree data.
    Constructor needs the max and min capacity of each node.
    """

    def __init__(self, c=20, min_c=8):
        self.root = None
        self.node_array = []  # array that holds the nodes
        self.node_count = 0
        self.c = c  # node capacity
        self.min_c = min_c  # node minimum capacity

    def construct(self, entries: List[RTreeEntry], curr_tree_level: int, isnonleaflevel: int) -> None:
        """
        Construct the tree starting from the leaf entries and recursively create next level entries and nodes.
        Split entries in twenties and then create the nodes using the groups of twenties. Each twenty is a node.
        The two last nodes of each level may have less than 20 entries.
        """

        # if the entries are more than C we need to split them and create UPPER(len(entries)/C) nodes
        if len(entries) > self.c:

            # split entries to twenties and check last node's plenitude
            entries_split = distribute(entries, self.min_c, self.c)

            # create nodes from the twenties
            curr_level_nodes = []
            for entries in entries_split:
                curr_level_nodes.append(RTreeNode(id=self.node_count, isnonleaf=isnonleaflevel, entries=entries))
                self.node_count += 1
            print(f'{len(curr_level_nodes)} nodes at level {curr_tree_level}')

            # append created nodes to the global node_array
            self.node_array += curr_level_nodes

            # create entries for next level
            # we calculate each node mbr and we create a list of RTreeEntry objects
            next_level_entries = []
            for node in curr_level_nodes:
                next_level_entries.append(RTreeEntry(entry_id=node.id, mbr=node.get_mbr()))
            curr_tree_level += 1
            self.construct(entries=next_level_entries, curr_tree_level=curr_tree_level, isnonleaflevel=1)
        else:
            # we reached root node
            root_node = RTreeNode(id=self.node_count, isnonleaf=isnonleaflevel, entries=entries)
            self.root = root_node
            # append root node to the global node array
            self.node_array.append(root_node)
            print(f'1 nodes at level {curr_tree_level}')

    def rangeQuery(self, window: Rectangle, node: RTreeNode) -> Iterable[int]:
        """
        performs a range query to the tree and yields each object id that satisfies the query range
        """
        if node.isnonleaf:
            for entry in node.entries:
                if entry.mbr.intersects(window):
                    yield from self.rangeQuery(window=window, node=self.node_array[entry.entry_id])
        else:  # node is a leaf node
            for entry in node.entries:
                if entry.mbr.intersects(window):
                    yield entry.entry_id

    def kNNQuery(self, root: RTreeNode, q: (float, float), k: int):
        """
        performs a Nearest Neighbor query to the tree
        """
        import heapq as hp

        nn_obj = Rectangle(float('inf'), float('inf'), float('inf'), float('inf'))
        nn_obj_id = None
        h = []
        for entry in root.entries:
            hp.heappush(h, (entry.mbr.distance(q), entry.entry_id))

        while len(h) != 0 and self.node_array[h[0][1]].get_mbr().distance(q) < nn_obj.distance(q):
            e = hp.heappop(h)
            n = self.node_array[e[1]]
            if n.isnonleaf:
                n = self.node_array[e[1]]
                for entry in n.entries:
                    if entry.mbr.distance(q) < nn_obj.distance(q):
                        hp.heappush(h, (entry.mbr.distance(q), entry.entry_id))

            else:  # node is a leaf node
                for entry in n.entries:
                    if entry.mbr.distance(q) < nn_obj.distance(q):
                        nn_obj = entry.mbr
                        nn_obj_id = entry.entry_id

        return nn_obj_id

    def dump(self, filename: str) -> None:
        """
        dumps the tree on disk
        """
        with open(filename, 'w') as dumpfile:
            dumpfile.writelines(f'{str(node)}\n' for node in self.node_array)

    def constructFromDumpfile(self, filename: str) -> None:
        """
        parse dumped rtree file and create the tree
        """
        with open(filename, 'r') as dumpfile:
            import ast
            for line in dumpfile:
                line_eval = ast.literal_eval(line)
                isnonleaf = line_eval[0]
                node_id = line_eval[1]
                entries = line_eval[2]
                node_entries = []
                for entry in entries:
                    entry_id = entry[0]
                    mbr = entry[1]
                    node_entries.append(RTreeEntry(entry_id=entry_id, mbr=Rectangle(*mbr)))
                self.node_array.append(RTreeNode(id=node_id, isnonleaf=isnonleaf, entries=node_entries))
            self.root = self.node_array[-1]
