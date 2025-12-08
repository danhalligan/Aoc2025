def part_a(data):
    x = data.char_array()

    start = [i for i, c in enumerate(x[0]) if c == "S"][0]
    x[1][start] = "|"
    split_count = 0
    for row in range(2, len(x)):
        for i, c in enumerate(x[row]):
            if c == "^" and x[row - 1][i] == "|":
                x[row][i - 1] = "|"
                x[row][i + 1] = "|"
                split_count += 1
            elif x[row - 1][i] == "|":
                x[row][i] = "|"

    return split_count


def part_b(data):
    x = data.char_array()

    beams = [[0 for _ in range(len(x[0]))] for _ in range(len(x))]

    start = [i for i, c in enumerate(x[0]) if c == "S"][0]
    beams[1][start] = 1
    for row in range(2, len(x)):
        for i, c in enumerate(x[row]):
            if c == "^" and beams[row - 1][i]:
                beams[row][i - 1] += beams[row - 1][i]
                beams[row][i + 1] += beams[row - 1][i]
            elif beams[row - 1][i]:
                beams[row][i] += beams[row - 1][i]

    return sum(beams[-1])
