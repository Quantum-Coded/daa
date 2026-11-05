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
