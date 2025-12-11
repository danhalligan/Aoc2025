from aoc2025.aoc import Puzzle
from itertools import combinations, pairwise


def area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def part_a(data):
    locations = data.int_array(",")
    return max(area(p1, p2) for p1, p2 in combinations(locations, 2))


# OK so the locations are in an order that traces out the perimeter.
# So we can just take pairs of points to find the straight perimeter lines.
# We want to avoid any rectangles that overlap one of the lines.
def find_valid_rectangles(locations):
    for (x, y), (u, v) in combinations(locations, 2):
        x, u = sorted((x, u))
        y, v = sorted((y, v))
        a = area((x, y), (u, v))
        fail = False
        for (p, q), (r, s) in pairwise(locations + [locations[0]]):
            p, r = sorted((p, r))
            q, s = sorted((q, s))
            if all((x < r, u > p, y < s, v > q)):
                fail = True
                break
        if not fail:
            yield a


def part_b(data):
    locations = data.int_array(",")
    return max(find_valid_rectangles(locations))
