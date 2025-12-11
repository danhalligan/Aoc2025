from re import split
from collections import deque, defaultdict, Counter


# return adjacency list as defaultdict (needed for part b)
def parse(data):
    g = {x[0]: x[1:] for x in (split(r":*\s+", line) for line in data.lines())}
    g = defaultdict(list, g)
    return g


# Naive solution
def part_a(data):
    g = parse(data)
    q = deque([("you", 0)])
    count = 0
    while q:
        node, dist = q.popleft()
        for nb in g[node]:
            if nb == "out":
                count += 1
            else:
                q.append((nb, dist + 1))
    return count


# Topological sort based solution
def n_paths_top(adj, src, dest):
    # Build in-degrees for topological sort
    deg = Counter(nb for node in adj for nb in adj[node])
    q = deque([node for node in adj if deg[node] == 0])
    paths = defaultdict(int)
    paths[src] = 1
    while q:
        u = q.popleft()
        for v in adj[u]:
            paths[v] += paths[u]
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)
    return paths[dest]


def part_b(data):
    g = parse(data)
    print(g)
    path1 = (
        n_paths_top(g, "svr", "dac")
        * n_paths_top(g, "dac", "fft")
        * n_paths_top(g, "fft", "out")
    )
    print(path1)
    path2 = (
        n_paths_top(g, "svr", "fft")
        * n_paths_top(g, "fft", "dac")
        * n_paths_top(g, "dac", "out")
    )
    print(f"total: {path1} + {path2}")
    return path1 + path2
