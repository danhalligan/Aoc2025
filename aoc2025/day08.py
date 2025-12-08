from math import sqrt


def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def get_distances(locations):
    distances = {
        (i, j): distance(p1, p2)
        for i, p1 in enumerate(locations)
        for j, p2 in enumerate(locations)
        if i < j
    }
    return sorted(distances.items(), key=lambda x: x[1])


def part_a(data, limit=1000):
    locations = data.int_array(",")
    distances = get_distances(locations)
    circuits = []
    for idx, ((i, j), d) in enumerate(distances):
        if idx == limit:
            break
        involved = [c for c in circuits if i in c or j in c]
        if any(i in c and j in c for c in involved):
            continue
        if len(involved) == 2:
            new_circuit = involved[0] | involved[1]
            circuits.remove(involved[0])
            circuits.remove(involved[1])
            circuits.append(new_circuit)
        elif len(involved) == 1:
            involved[0].update([i, j])
        else:
            circuits.append(set([i, j]))

    lens = sorted(len(x) for x in circuits)[-3:]
    return lens[0] * lens[1] * lens[2]


def part_b(data, limit=None):
    locations = data.int_array(",")
    distances = get_distances(locations)
    circuits = []
    for (i, j), d in distances:
        # Find all circuits containing i or j
        involved = [c for c in circuits if i in c or j in c]
        if any(i in c and j in c for c in involved):
            continue
        if len(involved) == 2:
            new_circuit = involved[0] | involved[1]
            circuits.remove(involved[0])
            circuits.remove(involved[1])
            circuits.append(new_circuit)
        elif len(involved) == 1:
            involved[0].update([i, j])
        else:
            circuits.append(set([i, j]))
        if len(circuits) == 1 and len(circuits[0]) == len(locations):
            return locations[i][0] * locations[j][0]
