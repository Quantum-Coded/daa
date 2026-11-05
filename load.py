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
