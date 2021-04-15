from typing import List
from Node import RTreeEntry


def chunks(lst, n) -> List:
    """Yield n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def distribute(entries_to_split: List[RTreeEntry], min_c: int, C: int) -> List[List[RTreeEntry]]:
    """
    Split the entries to groups of twenties and check if last the last node has at lease min_c entries.
    If not remove elements from previous node and add them to the last node such that
    the minimum node capacity requirements is met.
    """
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
