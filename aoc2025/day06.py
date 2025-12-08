from operator import add, mul
from functools import reduce


def part_a(data):
    data.lines()
    x = [line.split() for line in data.lines()]
    res = 0
    for i in range(len(x[1])):
        col = [r[i] for r in x]
        op = col[-1]
        op = {"+": add, "*": mul}[op]
        ints = [int(r) for r in col[:-1]]
        res += reduce(op, ints)
    return res


def part_b(data):
    x = data.raw.split("\n")
    s = max([len(r) for r in x])
    nums = []
    res = 0
    for i in range(s - 1, -1, -1):
        col = [r[i] for r in x if len(r) > i and not r[i] in [" ", "+", "*"]]
        if not col:
            continue
        nums += [int("".join(col))]
        if i < len(x[-1]) and x[-1][i] in ["+", "*"]:
            op = {"+": add, "*": mul}[x[-1][i]]
            res += reduce(op, nums)
            nums = []
    return res
