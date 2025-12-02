def part_a(data):
    tot = 0
    for ids in data.raw.split(","):
        s, e = [int(x) for x in ids.split("-")]
        for i in range(s, e + 1):
            x = str(i)
            if len(x) % 2 == 0 and x[: len(x) // 2] == x[len(x) // 2 :]:
                tot += i
    return tot


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def part_b(data):
    tot = 0
    for ids in data.raw.split(","):
        s, e = [int(x) for x in ids.split("-")]
        for i in range(s, e + 1):
            x = str(i)
            for pattern_length in range(1, len(x) // 2 + 1):
                if len(x) % pattern_length != 0:
                    continue
                patterns = list(chunks(x, pattern_length))
                if all(c == patterns[0] for c in patterns):
                    tot += i
                    break
    return tot
