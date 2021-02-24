#!/usr/bin/env python3

import random

def get_perturbation_indices(n):
    """Returns a pair of a pair of indices representing a double-bridge perturbation.
    Each pair represents 2 edges removed in a non-sequential 2-opt move.
    An index i represents the edge from i to i+1.
    """
    assert(n > 4) # minimum of 5 edges to perform a non-trivial perturbation.
    first = random.randrange(n)
    # there must be a gap of at least one edge between first and this edge.
    # there are 3 edges that cannot be chosen, first, first + 1, and first - 1.
    second = random.randrange(n - 3)
    second = (first + 2 + second) % n

    # normalize first to be min and second to be max.
    pair = (first, second)
    first = min(pair)
    second = max(pair)

    # get third edge, in between first and second.
    assert(second - first > 1)
    third = random.randrange(first + 1, second)
    excluded_edges = second - first + 1
    available_edges = n - excluded_edges

    # get fourth edge outside of first and second edge.
    fourth = random.randrange(available_edges)
    fourth = (second + 1 + fourth) % n

    index_set = set([first, second, third, fourth])
    if len(index_set) != 4:
        print([first, second, third, fourth])
    assert(len(index_set) == 4)

    assert(third - first > 0)
    assert(second - third > 0)
    assert(fourth > second or fourth < first)

    return ((first, second), (third, fourth))

if __name__ == "__main__":
    for i in range(100):
        print(get_perturbation_indices(10))
