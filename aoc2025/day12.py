def parse_regions(regions):
    for line in regions.lines():
        size, counts = line.split(": ")
        size = [int(x) for x in size.split("x")]
        counts = [int(x) for x in counts.split(" ")]
        yield {"size": size, "counts": counts}


def parse_presents(presents):
    for present in presents:
        yield [[p == "#" for p in x] for x in present.lines()[1:]]


def parse(data):
    sections = data.sections()
    presents = list(parse_presents(sections[:-1]))
    regions = list(parse_regions(sections[-1]))
    return presents, regions


def part_a(data):
    presents, regions = parse(data)
    count = 0
    for region in regions:
        area = region["size"][0] * region["size"][1]
        max_n = sum(3 * 3 * n for n in region["counts"])
        min_n = sum(
            sum(sum(x) for x in presents[i]) * n for i, n in enumerate(region["counts"])
        )
        if max_n <= area:
            count += 1
        elif min_n > area:
            continue
        else:
            raise "This puzzle is too hard for me!"
    return count
