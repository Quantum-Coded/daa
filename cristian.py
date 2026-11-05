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
