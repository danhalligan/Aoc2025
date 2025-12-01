def part_a(data):
    pos, count = 50, 0

    for line in data.lines():
        d, i = line[0], line[1:]
        i = int(i)
        pos += i if d == "R" else -i
        pos %= 100
        if pos == 0:
            count += 1

    return count


def part_b(data):
    pos, count = 50, 0

    for line in data.lines():
        d, i = line[0], line[1:]
        i = int(i)
        for p in range(i):
            pos += 1 if d == "R" else -1
            pos %= 100
            if pos == 0:
                count += 1

    return count
