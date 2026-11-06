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
