def join(a, b):
    return int(f"{a}{b}")


def part_a(data):
    tot = 0
    for line in data.lines():
        x = [int(i) for i in line]
        m = max(x[:-1])
        tot += join(m, max(x[x.index(m) + 1 :]))
    return tot


def find_max(x, n):
    """Maximum number that can be formed by selecting n digits from x in order."""
    if n == 1:
        return max(x)
    m = max(x[: -(n - 1)])
    return join(m, find_max(x[x.index(m) + 1 :], n - 1))


def part_b(data):
    return sum(find_max([int(i) for i in line], 12) for line in data.lines())
