# ============================================================
# EXP 1: rpc
# ============================================================
import csv, json

#RPC
def processData(x):
    return x * 2

#RMI
class Server:
    def processData(self, x):
        return x * 2

server = Server()
choice = input("Enter 1 for RPC or 2 for RMI: ")

with open("rpc_calls_1.csv") as f:
    data = csv.reader(f)
    next(data)#skip header

    for r in data:
        #Client Annouces Call
        print("\n[DISPATCH]", r[1], "invoking", r[2], "at", r[4])

        #Client Packs the request
        packet = json.dumps({"method": r[2], "param": int(r[3])})  # marshal
        print("[MARSHAL]", packet)

        #Server unpacks the request
        d = json.loads(packet)
        x = d["param"]  # unmarshal on server
        print("[SERVER EXECUTION] Processing parameter:", x)

        #Execution
        if choice == "1":
            result = processData(x)
        else:
            result = server.processData(x)
        print("[RETURN] Result:", result)


# ============================================================
# EXP 2: multithreading
# ============================================================
import csv
import threading
import time

lock = threading.Lock() #mutex
done = [] #shared data


def work(r):
    print("Started:", r[1], r[0])
    time.sleep(int(r[2]) / 1000) #simulate work

    print("Waiting for lock:", r[1])
    with lock: #wait for avl, then append and release lock
        print("Lock acquired:", r[1])
        done.append(r[0])
    print("Lock released:", r[1])


threads = []

with open("tasks_4.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        t = threading.Thread(target=work, args=(r,))
        t.start()
        threads.append(t)

for t in threads:
    t.join()

print("Completed tasks:", done)


# ============================================================
# EXP 3: lamport
# ============================================================
import csv

clock = {}     # current clock of each process
sent = {}      # (sender, receiver) -> timestamps of messages not yet received
events = []

with open("events_7.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        event_id, process_id, event_type, message_to, initial_clock = r
        L = max(clock.get(process_id, 0), int(initial_clock))

        if event_type == "SEND":
            clock[process_id] = L + 1
            sent.setdefault((process_id, message_to), []).append(clock[process_id])
            print(event_id, "SEND: L =", L, "+ 1 =", clock[process_id])

        elif event_type == "RECEIVE":
            # for RECEIVE, message_to holds the sender
            msg = sent[(message_to, process_id)].pop(0)
            clock[process_id] = max(L, msg) + 1
            print(event_id, "RECEIVE: L = max(", L, ",", msg, ") + 1 =", clock[process_id])

        else:  # LOCAL
            clock[process_id] = L + 1
            print(event_id, "LOCAL: L =", L, "+ 1 =", clock[process_id])

        events.append((clock[process_id], process_id, event_id))

print("\nTotal Causal Order:")
for timestamp, process_id, event_id in sorted(events):
    print(event_id, process_id, "Timestamp:", timestamp)


# ============================================================
# EXP 4: cristian
# ============================================================
import csv

with open("cristian_clocks_8.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        t0, ts, t1 = int(r[1]), int(r[2]), int(r[3])

        rtt = t1 - t0
        est = ts + rtt / 2
        drift = est - t1

        print("\nClient:", r[0])
        print("RTT = T1 - T0 =", rtt)
        print("Estimated Server Time = T_server + RTT/2 =", est)
        print("Drift / Offset Adjustment:", drift)
        print("Adjusted Client Time:", t1 + drift)


# ============================================================
# EXP 5: berkely
# ============================================================
import csv

times = []

print("Polled node times:")
with open("node_clocks_3.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        print(r[0], r[1])

        if r[2] == "FALSE":
            times.append([r[0], int(r[1])])
        else:
            print("Outlier discarded:", r[0])

total = 0
for x in times:
    total = total + x[1]

avg = total / len(times)

print("\nAverage Clock Time:", avg)
print("Average Offset from master", times[0][0], ":", avg - times[0][1])

for x in times:
    print(x[0], "Adjustment:", avg - x[1])


# ============================================================
# EXP 6: vector
# ============================================================
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


# ============================================================
# EXP 7: ring
# ============================================================
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


# ============================================================
# EXP 8: bully
# ============================================================
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


# ============================================================
# EXP 9: load
# ============================================================
import csv

workers = ["W1", "W2", "W3"]
load = [0, 0, 0]
jobs = [0, 0, 0]
i = 0

mode = "LC"  # "RR" = Round Robin, "LC" = Least Connections

with open("workload_5.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        w = i % 3 if mode == "RR" else jobs.index(min(jobs))

        load[w] += int(r[1])
        jobs[w] += 1
        i += 1

        print(r[0], "assigned to", workers[w])
        print("Current Load:", load)

print("\nFinal Summary:")
for i in range(3):
    print(workers[i], "Jobs:", jobs[i], "Load:", load[i])


# ============================================================
# EXP 10: matrix
# ============================================================
import csv
import threading

A = []

with open("matrix_22.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        A.append([int(x) for x in r[1:]])

n = len(A)
B = A if n == len(A[0]) else [list(c) for c in zip(*A)]  # A x A, or A x A^T if not square
C = [None] * n


def work(i):
    C[i] = [sum(a * b for a, b in zip(A[i], col)) for col in zip(*B)]
    print("Worker", i, "partial dot products:", C[i])


print("MASTER SCATTERING")
for i in range(n):
    print("Row", i, "->", "Worker", i, A[i])

threads = []
for i in range(n):
    t = threading.Thread(target=work, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("MASTER GATHERING")
for row in C:
    print(row)


