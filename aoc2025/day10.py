from re import search
from collections import deque
from z3 import Optimize, Int, Sum, sat


def parse(line):
    lights, wirings, joltage = search(r"\[(.+?)\]\s(\(.+?\))\s{(.+?)}", line).groups()
    lights = [x == "#" for x in lights]
    wirings = [
        [int(n) for n in wiring.split(",")] for wiring in wirings[1:-1].split(") (")
    ]
    joltage = [int(x) for x in joltage.split(",")]
    return lights, wirings, joltage


def press(state, wiring):
    newstate = list(state)
    for i in wiring:
        newstate[i] = not newstate[i]
    return tuple(newstate)


def jolt(state, joltage):
    newstate = list(state)
    for i in joltage:
        newstate[i] += 1
    return tuple(newstate)


def bfs(initial, target, wirings, action):
    queue = deque([(initial, 0)])
    seen = {initial}
    while queue:
        state, count = queue.popleft()
        if state == target:
            return count
        for wiring in wirings:
            newstate = action(state, wiring)
            if newstate not in seen:
                seen.add(newstate)
                queue.append((newstate, count + 1))


def part_a(data):
    total = 0
    for line in data.lines():
        lights, wirings, _ = parse(line)
        total += bfs(tuple([False] * len(lights)), tuple(lights), wirings, press)
    return total


# I feel dirty using z3 here but oh well!
# Is this cheating?
def solve_z3(target, wirings):
    opt = Optimize()
    x = [Int(f"x_{i}") for i in range(len(wirings))]
    for xi in x:
        opt.add(xi >= 0)
    for j, t in enumerate(target):
        opt.add(Sum([x[i] for i, wiring in enumerate(wirings) if j in wiring]) == t)
    opt.minimize(Sum(x))
    if opt.check() == sat:
        model = opt.model()
        return sum(int(str(model[xi])) for xi in x if model[xi] is not None)


def part_b(data):
    total = 0
    for line in data.lines():
        _, wirings, joltage = parse(line)
        total += solve_z3(joltage, wirings)
    return total
