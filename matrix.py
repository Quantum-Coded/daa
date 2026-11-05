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
