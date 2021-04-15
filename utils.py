from typing import List
from Node import RTreeEntry


def chunks(lst, n):
    """Yield n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def distribute(entries_to_split: List[RTreeEntry], min_c, C):
    entries_split = list(chunks(entries_to_split, C))
    last = entries_split[-1]
    if len(last) < min_c:

        remaining = min_c - len(last)
        elements = []
        for _ in range(remaining):
            elements.append(entries_split[-2].pop())
        for element in elements:
            entries_split[-1].insert(0, element)

    return entries_split
