import csv

clock = {}
pending = []  # messages in flight: [sender, receiver, timestamp]
events = []

with open("events_7.csv") as f:
    data = csv.reader(f)
    next(data)

    for r in data:
        event_id, process_id, event_type, message_to, initial_clock = r
        L = max(clock.get(process_id, 0), int(initial_clock))

        if event_type == "SEND":
            clock[process_id] = L + 1
            pending.append([process_id, message_to, clock[process_id]])
            print(event_id, "SEND: L =", L, "+ 1 =", clock[process_id])

        elif event_type == "RECEIVE":
            m = [x for x in pending if x[1] == process_id]
            m = [x for x in m if x[0] == message_to] or m
            pending.remove(m[0])

            clock[process_id] = max(L, m[0][2]) + 1
            print(event_id, "RECEIVE: L = max(", L, ",", m[0][2], ") + 1 =", clock[process_id])

        else:  # LOCAL
            clock[process_id] = L + 1
            print(event_id, "LOCAL: L =", L, "+ 1 =", clock[process_id])

        events.append((clock[process_id], process_id, event_id))

print("\nTotal Causal Order:")
for timestamp, process_id, event_id in sorted(events):
    print(event_id, process_id, "Timestamp:", timestamp)
