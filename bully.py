import csv

nodes = []
alive = []

with open("bully_cluster_2.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        nodes.append(int(r[0]))

        if r[1] == "TRUE":
            alive.append(int(r[0]))
        elif r[2] == "TRUE":
            print("Coordinator failed:", r[0])

start = min(alive)
print("Initiator:", start)

for n in nodes:
    if n > start:
        print("ELECTION:", start, "->", n)

        if n in alive:
            print("OK:", n, "->", start)

leader = max(alive)
for n in alive:
    if n != leader:
        print("COORDINATOR:", leader, "->", n)
