def part_a(data):
    tot = 0
    for ids in data.raw.split(","):
        s, e = [int(x) for x in ids.split("-")]
        for i in range(s, e + 1):
            x = str(i)
            if len(x) % 2 == 0 and x[: len(x) // 2] == x[len(x) // 2 :]:
                tot += i
    return tot


def part_b(data):
    tot = 0
    for ids in data.raw.split(","):
        s, e = [int(x) for x in ids.split("-")]
        for i in range(s, e + 1):
            x = str(i)
            for pattern_length in range(1, len(x) // 2 + 1):
                if len(x) % pattern_length == 0:
                    pattern = x[:pattern_length]
                    if x == pattern * (len(x) // pattern_length):
                        tot += i
                        break
    return tot
