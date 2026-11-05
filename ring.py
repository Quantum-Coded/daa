import csv

nxt = {}
active = []

with open("ring_nodes_15.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        nxt[int(r[0])] = int(r[1])

        if r[2] == "TRUE":
            active.append(int(r[0]))
        else:
            print("Detected failure of node:", r[0])

start = active[0]
cur = start
token = [start]
print("Election started by node", start)

while True:
    n = nxt[cur]

    while n not in active:  # skip failed nodes
        n = nxt[n]

    if n == start:
        break

    token.append(n)
    print("Token", token, ": node", cur, "->", n)
    cur = n

print("Token returned to initiator:", token)
print("New Leader:", max(token))
