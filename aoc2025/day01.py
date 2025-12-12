def part_a(data):
    pos, count = 50, 0

    for line in data.lines():
        d, i = line[0], int(line[1:])
        pos = (pos + i) % 100 if d == "R" else (pos - i) % 100
        count += pos == 0

    return count


def part_b(data):
    pos, count = 50, 0

    for line in data.lines():
        d, i = line[0], int(line[1:])
        for _ in range(i):
            pos = (pos + (1 if d == "R" else -1)) % 100
            count += pos == 0

    return count
