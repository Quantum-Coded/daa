import csv

P = ["P1", "P2", "P3"]
V = [[0, 0, 0] for i in range(3)]
pending = []  # messages in flight: [sender, receiver, vector]
events = []

with open("vector_events_6.csv") as f:
    data = csv.reader(f)
    next(data)

    for e, pid, act, other in data:
        p = P.index(pid)

        if act == "SEND":
            V[p][p] += 1
            pending.append([pid, other, V[p][:]])

        elif act == "RECEIVE":
            m = [x for x in pending if x[1] == pid]
            m = [x for x in m if x[0] == other] or m
            pending.remove(m[0])

            V[p] = [max(a, b) for a, b in zip(V[p], m[0][2])]
            V[p][p] += 1

        else:  # LOCAL
            V[p][p] += 1

        events.append([e, V[p][:]])
        print(e, "Vector [v1, v2, v3]:", V[p])

print("\nEvent Comparison:")
for i in range(len(events)):
    for j in range(i + 1, len(events)):
        ea, a = events[i]
        eb, b = events[j]

        if all(x <= y for x, y in zip(a, b)) and a != b:
            print(ea, "->", eb, "Causally Preceding:", a, "<", b)
        elif all(y <= x for x, y in zip(a, b)) and a != b:
            print(eb, "->", ea, "Causally Preceding:", b, "<", a)
        else:
            print(ea, "||", eb, "Concurrent")
