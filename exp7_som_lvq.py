# EXP 7 - (a) Kohonen SOM  (b) LVQ  (one small worked example each)


#for both kohonen and lvq
def dist(w, x):                      # squared Euclidean distance
    d = 0
    for i in range(len(x)):
        d += (w[i] - x[i]) ** 2
    return d

# ================= 7(a) KOHONEN SOM (unsupervised) =================
# Winner = neuron with smallest distance.   Update: w = w + alpha * (x - w)
X = [[1, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 1]]
W = [[0.2, 0.4, 0.6, 0.8],           # neuron 0
     [0.9, 0.7, 0.5, 0.3]]           # neuron 1
alpha = 0.6

for epoch in range(1, 4):
    print("SOM epoch", epoch, " alpha =", alpha)
    for x in X:
        d0 = dist(W[0], x)
        d1 = dist(W[1], x)
        if d0 < d1:
            win = 0
        else:
            win = 1

        # move the winner toward x:  w = w + alpha * (x - w)
        for i in range(4):
            W[win][i] = W[win][i] + alpha * (x[i] - W[win][i])

        print("x =", x)
        print("D0 =", d0, " D1 =", d1, " -> winner = neuron", win)
        print("new weights of winner =", W[win])

    alpha = 0.5 * alpha              # decay learning rate

print("Final SOM weights:")
print("  neuron 0 =", W[0])
print("  neuron 1 =", W[1])

# ================= 7(b) LVQ (supervised) =================
# Winner same class as x -> move TOWARD:  w = w + alpha * (x - w)
# Winner different class -> move AWAY:    w = w - alpha * (x - w)
X = [[0, 0, 1, 1], [1, 0, 0, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0]]
T = [1, 2, 2, 1, 1]                  # class of each vector
alpha = 0.1

# first 2 vectors become the starting prototypes (one per class)
W = [[0, 0, 1, 1],                   # prototype 0 = X[0], class 1
     [1, 0, 0, 0]]                   # prototype 1 = X[1], class 2
C = [1, 2]                           # class of each prototype

print("\nLVQ training (vectors 3, 4, 5), alpha =", alpha)
for k in range(2, 5):                # remaining 3 vectors are used for training
    x = X[k]
    d0 = dist(W[0], x)
    d1 = dist(W[1], x)
    if d0 < d1:
        win = 0
    else:
        win = 1

    if C[win] == T[k]:               # correct class -> move toward x
        for i in range(4):
            W[win][i] = W[win][i] + alpha * (x[i] - W[win][i])
    else:                            # wrong class   -> move away from x
        for i in range(4):
            W[win][i] = W[win][i] - alpha * (x[i] - W[win][i])

    print("x =", x, " class =", T[k])
    print("D0 =", d0, " D1 =", d1, " -> winner = prototype", win, " (class", C[win], ")")
    print("new weights of winner =", W[win])

print("Final prototypes:")
print("  prototype 0 (class 1) =", W[0])
print("  prototype 1 (class 2) =", W[1])

# test: classify every vector by its nearest prototype
print("\nLVQ test")
for k in range(5):
    x = X[k]
    d0 = dist(W[0], x)
    d1 = dist(W[1], x)
    if d0 < d1:
        win = 0
    else:
        win = 1
    print("x =", x, " D0 =", d0, " D1 =", d1, " -> predicted class", C[win], " actual class", T[k])
