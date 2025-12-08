def collapse_ranges(iranges):
    iranges = sorted(iranges, key=lambda x: x[0])
    merged = []
    for r in iranges:
        if not merged or merged[-1][1] < r[0] - 1:
            merged.append(tuple(r))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
    return merged


def part_a(data):
    ranges, items = data.sections()
    count = 0
    for item in items.lines():
        item = int(item)
        for r in ranges.lines():
            s, e = [int(x) for x in r.split("-")]
            if s <= item <= e:
                count += 1
                break
    return count


def part_b(data):
    ranges, _ = data.sections()
    iranges = [[int(x) for x in r.split("-")] for r in ranges.lines()]
    iranges = collapse_ranges(iranges)

    return sum(r[1] - r[0] + 1 for r in iranges)
