def part_a(data):
    tot = 0
    for line in data.lines():
        x = [int(i) for i in line]
        m = max(x[:-1])
        best = 0
        for p, i in enumerate(x[:-1]):
            if i == m:
                r = int(str(i) + str(max(x[p + 1 :])))
                if r >= best:
                    best = r
        tot += best
    return tot


def find_max(x, n):
    """Find the maximum number that can be formed by selecting n+1 digits from x in order."""
    if n == 0:
        return max(x)
    else:
        m = max(x[:-n])
        best = 0
        for i, p in enumerate(x[:-n]):
            if p == m:
                r = find_max(x[i + 1 :], n - 1)
                if r > best:
                    best = r
        return int(str(m) + str(best))


def part_b(data):
    tot = 0
    for line in data.lines():
        tot += find_max([int(i) for i in line], 11)
    return tot
