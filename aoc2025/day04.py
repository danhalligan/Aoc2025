def nbs(pt):
    return [pt + dx + dy * 1j for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx or dy]


def accessible(g, pt):
    return g[pt] == "@" and sum(g.get(n, ".") == "@" for n in nbs(pt)) < 4


def part_a(data):
    g = data.grid()
    return sum(accessible(g, pt) for pt in g)


def part_b(data):
    g = data.grid()
    removed = 0
    while True:
        rm = [pt for pt in g if accessible(g, pt)]
        if not rm:
            break
        for pt in rm:
            g[pt] = "."
        removed += len(rm)
    return removed
