#!/usr/bin/env python3

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
        return seg0 + seg3 + seg2 + seg1 + seg4
    else:
        assert(fourth > second)
        seg5 = seg4[fourth - second:]
        seg4 = seg4[:fourth - second]
        return seg1 + seg2 + seg3 + seg4 + seg5

import sys
import random_util

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("arguments: input_tour_path output_tour_path")
    tour_path = sys.argv[1]
    output_path = sys.argv[2]
    tour = read_tour(tour_path)
    indices = random_util.get_perturbation_indices(len(tour))
    new_tour = apply_double_bridge(tour, indices)
    assert(len(set(new_tour)) == len(tour))
    with open(output_path, 'w') as f:
        f.write("TYPE : TOUR\n")
        f.write(f"DIMENSION : {len(new_tour)}\n")
        f.write("TOUR_SECTION\n")
        for i in new_tour:
            f.write(f"{i}\n")
        f.write("-1\n")
        f.write("EOF\n")

