def nbs(pt):
    return [
        pt + 1,
        pt - 1,
        pt + 1j,
        pt - 1j,
        pt + 1 + 1j,
        pt + 1 - 1j,
        pt - 1 + 1j,
        pt - 1 - 1j,
    ]


def part_a(data):
    g = data.grid()
    count = 0
    for pt in g.keys():
        if sum(g.get(n, ".") == "@" for n in nbs(pt)) < 4 and g[pt] == "@":
            count += 1
    return count


def part_b(data):
    g = data.grid()
    removed = 0
    count = 1
    while count > 0:
        count = 0
        for pt in g.keys():
            if sum(g.get(n, ".") == "@" for n in nbs(pt)) < 4 and g[pt] == "@":
                count += 1
                g[pt] = "."
        removed += count
    return removed
