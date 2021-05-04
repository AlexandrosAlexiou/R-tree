# Spatial queries using an R-tree

Construction and usage of an R-tree index to answer spatial queries.

## Object coordinates
There are two input files, coords.txt and offsets.txt. The first contains point coordinates in the form `x, y`. The second contains entries of the form `id, startOffset, endOffset` where id is the unique identifier of a polygonal object and startOffset (respectively endOffset) is the number of the line in the coords.txt file that the coordinates start (respectively end).

## Range queries
Rqueries.txt contains the coordinates of the query window in the form `x_low y_low x_high y_high`. Every line is a query window.

## K - Nearest neighbor queries
NNqueries.txt constains the coordinates of the query point in the form of `x y`. Every line is a query point.

## Usage

* **R-tree construction**
```python
from Rtree import Rtree
from utils import load_entries

coords_file, offsets_file, outfile = "./data/coords.txt", "./data/offsets.txt", "./data/Rtree.txt"

# Instantiate the Rtree
rtree = Rtree()

# Load entries from the data files using the utils
leaf_entries = load_entries(coords_file, offsets_file)

# start the construction passing the leaf entries
rtree.construct(entries=leaf_entries, curr_tree_level=0, isnonleaflevel=0)

# dump the tree
rtree.dump(outfile)
```


* **Range queries**
```python
from Rtree import Rtree
from Rectangle import Rectangle

dumpfile, queries_file = "./data/Rtree.txt", "./data/Rqueries.txt"

# Instantiate the Rtree
rtree = Rtree()

# construct the Rtree from the dump file
rtree.constructFromDumpfile(dumpfile)

# open queries file and perform each range query to the tree
for lineno, line in enumerate(open(queries_file)):
    x_low, y_low, x_high, y_high = list(map(float, line.rstrip("\n").split(" ")))
    window_query = Rectangle(x_low=x_low, x_high=x_high, y_low=y_low, y_high=y_high)
    results = list(rtree.rangeQuery(node=rtree.root, window=window_query))
    # print query results
    print(f"{lineno} ({len(results)}): {str(results)[1:-1]}")
```


* **K - Nearest neighbor queries**
```python
from Rtree import Rtree

dumpfile, kNNQueries_file = "./data/Rtree.txt", "./data/NNqueries.txt"
k = 10

# Instantiate the Rtree
rtree = Rtree()

# construct the Rtree from the dump file
rtree.constructFromDumpfile(dumpfile)

# open NNQueries file and perform each query to the tree
for lineno, line in enumerate(open(kNNQueries_file)):
    (x, y) = list(map(float, line.rstrip("\n").split(" ")))
    results = list(rtree.kNNQuery(root=rtree.root, q=(x, y), k=k))
    # print query results
    print(f'{lineno}: {str(results)[1:-1]}')
```


## API
- `Rtree.construct(self, entries: List[RTreeEntry], curr_tree_level: int, isnonleaflevel: int)`
    * Recursively constructs the tree with the Bulk Loading technique.

- `Rtree.rangeQuery(self, node: RTreeNode, window: Rectangle)`
    * Yields the ids of the objects that satisfy the range of the query window given the root node of the tree and the window.

- `Rtree.kNNQuery(self, root: RTreeNode, q: (float, float), k: int)`
    * Yields k nearest neighbors to the point q.

<div style="page-break-after: always;"></div>

## Tests

From the project's root folder, execute `tests.py`.

### References:

* [R-tree](https://en.wikipedia.org/wiki/R-tree)
* [Z-order curve](https://en.wikipedia.org/wiki/Z-order_curve)
* [Nearest neighbor search](https://en.wikipedia.org/wiki/Nearest_neighbor_search)
