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

avg = sum(x[1] for x in times) / len(times)

print("\nAverage Clock Time:", avg)
print("Average Offset from master", times[0][0], ":", avg - times[0][1])

for x in times:
    print(x[0], "Adjustment:", avg - x[1])
