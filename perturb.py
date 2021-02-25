#!/usr/bin/env python3

def read_instance(path):
    """Reads a TSPLIB-formatted TSP instance (not tour) file. """
    coordinates = []
    with open(path, "r") as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "EOF" in line or not line:
                break
            fields = line.strip().split()
            coordinates.append((float(fields[1]), float(fields[2])))
    return coordinates


def read_tour(path):
    """Reads a TSPLIB-formatted TSP tour file. """
    tour = []
    with open(path, "r") as f:
        for line in f:
            if "TOUR_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "-1" in line or "EOF" in line or not line:
                break
            fields = line.strip().split()
            tour.append((int(fields[0])))
    return tour

def apply_double_bridge(tour, indices):
    pair1, pair2 = indices
    first, second = pair1
    third, fourth = pair2
    seg1 = tour[:first + 1]
    seg2 = tour[first + 1:third + 1]
    seg3 = tour[third + 1:second + 1]
    seg4 = tour[second + 1:]
    assert(len(seg1) + len(seg2) + len(seg3) + len(seg4) == len(tour))
    if fourth < first:
        seg0 = seg1[:fourth + 1]
        seg1 = seg1[fourth + 1:]
        new_tour = seg0 + seg3 + seg2 + seg1 + seg4
    else:
        assert(fourth > second)
        seg5 = seg4[fourth - second:]
        seg4 = seg4[:fourth - second]
        new_tour = seg1 + seg4 + seg3 + seg2 + seg5
    assert(not same_tour(tour, new_tour))
    return new_tour

def distance(instance, i, j):
    # i and j are index + 1.
    i -= 1
    j -= 1
    assert(i >= 0 and j >= 0)
    dx = instance[i][0] - instance[j][0]
    dy = instance[i][1] - instance[j][1]
    return round((dx ** 2 + dy ** 2) ** 0.5)
def edge_cost(instance, edge):
    return distance(instance, edge[0], edge[1])
def tour_cost(instance, tour):
    prev = tour[-1]
    cost = 0
    for i in tour:
        cost += edge_cost(instance, (prev, i))
        prev = i
    return cost

def same_tour(t1, t2):
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            return False
    return True

import sys
import random_util

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("arguments: instance_file input_tour_path output_tour_path")
    instance_file = sys.argv[1]
    tour_path = sys.argv[2]
    output_path = sys.argv[3]
    instance = read_instance(instance_file)
    tour = read_tour(tour_path)
    indices = random_util.get_perturbation_indices(len(tour))
    print(indices)
    new_tour = apply_double_bridge(tour, indices)
    assert(len(set(new_tour)) == len(tour))
    print(f'original tour cost: {tour_cost(instance, tour)}')
    print(f'new tour cost: {tour_cost(instance, new_tour)}')

    with open(output_path, 'w') as f:
        f.write("TYPE : TOUR\n")
        f.write(f"DIMENSION : {len(new_tour)}\n")
        f.write("TOUR_SECTION\n")
        for i in new_tour:
            f.write(f"{i}\n")
        f.write("-1\n")
        f.write("EOF\n")

