# EXP 8: Hopfield (8a) and BAM (8b) - simple version, no numpy

# activation: 1 if value >= 0 else -1
def activation(v):
    if v >= 0:
        return 1
    return -1

# ================= 8(a) AUTO-ASSOCIATIVE (Hopfield) =================
p1 = [1, 1, 1, 1]
p2 = [-1, 1, 1, -1]

# Step 1: w1 = p1(T) * p1  (column x row = 4x4 table)
w1 = [[0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]]
for i in range(4):
    for j in range(4):
        w1[i][j] = p1[i] * p1[j]

# Step 2: w2 = p2(T) * p2
w2 = [[0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]]
for i in range(4):
    for j in range(4):
        w2[i][j] = p2[i] * p2[j]

# Step 3: W = w1 + w2
W = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
for i in range(4):
    for j in range(4):
        W[i][j] = w1[i][j] + w2[i][j]

print("w1 =", w1)
print("w2 =", w2)
print("W  =", W)

# Step 4: test a vector x:  y = x * W, then apply the activation
# y is compared with 'expected' (the stored pattern x should give back)
def test(x, expected):
    y = [0, 0, 0, 0]
    for j in range(4):
        total = 0
        for i in range(4):
            total = total + x[i] * W[i][j]
        y[j] = activation(total)
    print("x =", x, " y =", y, " ->", "correct" if y == expected else "wrong")

# Step 5: test the stored patterns (y should equal x)
test(p1, p1)
test(p2, p2)

# Step 6: add noise to p1 (flip the first bit); y should still come back as p1
noisy = [-1, 1, 1, 1]
test(noisy, p1)

# ================= 8(b) BAM (hetero-associative) =================
# Training data: each row is one pair.  X (inputs) is linked to Y (outputs).
#      x1  x2  x3  x4
X = [[ 1,  1, -1, -1],      # pair 1
     [-1,  1,  1, -1]]      # pair 2

#      y1  y2  y3
Y = [[ 1, -1,  1],          # pair 1
     [-1,  1,  1]]          # pair 2

# Step 1: start with all weights = 0  (4 inputs x 3 outputs)
W = [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]

# Step 2: Hebb rule, one pair at a time:  w_new = w_old + x * y
for p in range(2):                  # 2 pairs
    for i in range(4):              # inputs  x1..x4
        for j in range(3):          # outputs y1..y3
            W[i][j] = W[i][j] + X[p][i] * Y[p][j]
    print("after pair", p + 1, ": W =", W)

# Step 3: forward recall  y = x * W  (X -> Y), then activation
def forward(x, expected):
    y = [0, 0, 0]
    for j in range(3):
        total = 0
        for i in range(4):
            total = total + x[i] * W[i][j]
        y[j] = activation(total)
    print("X =", x, " Y =", y, " ->", "correct" if y == expected else "wrong")

# Step 4: backward recall  x = y * W(T)  (Y -> X), then activation
def backward(y, expected):
    x = [0, 0, 0, 0]
    for i in range(4):
        total = 0
        for j in range(3):
            total = total + y[j] * W[i][j]
        x[i] = activation(total)
    print("Y =", y, " X =", x, " ->", "correct" if x == expected else "wrong")

# Step 5: test both directions for each pair
for p in range(2):
    forward(X[p], Y[p])
    backward(Y[p], X[p])

# Step 6: add noise to pair 1 input (flip x4); Y should still come back as pair 1
forward([1, 1, -1, 1], Y[0])

# ================= VIVA Q&A =================
# Q: Associative memory?  A: Stores patterns and recalls them from partial/noisy cues (content-addressable).
# Q: Auto vs hetero-associative?  A: Auto: pattern with itself; hetero: pattern A with a different pattern B.
# Q: Hebb rule?  A: Weights = sum of outer products of stored patterns: W = sum(p p^T).
# Q: Why zero the diagonal in Hopfield?  A: No self-connections; keeps energy descent stable.
# Q: BAM?  A: Two-layer hetero-associative net; W = sum(a b^T); recall forward (a W) and backward (b W^T).
# Q: Why bipolar?  A: Gives better orthogonality and correct Hebbian cancellation.
# Q: Hopfield capacity?  A: About 0.15 N patterns for N neurons.
# Q: Too many patterns?  A: Crosstalk -> spurious states and wrong recall.
# Q: Activation?  A: Bipolar threshold: +1 if net >= 0 else -1.
