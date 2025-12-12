def part_a(data):
    tot = 0
    for line in data.lines():
        x = [int(i) for i in line]
        m = max(x[:-1])
        tot += int(f"{m}{max(x[x.index(m) + 1 :])}")
    return tot


def find_max(x, n):
    """Maximum number that can be formed by selecting n+1 digits from x in order."""
    if n == 0:
        return max(x)
    m = max(x[:-n])
    return int(f"{m}{find_max(x[x.index(m) + 1:], n - 1)}")


def part_b(data):
    return sum(find_max([int(i) for i in line], 11) for line in data.lines())
