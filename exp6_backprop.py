# EXP 6 - BACKPROPAGATION: 2 inputs -> 2 hidden -> 1 output, sigmoid, one example, no numpy.
import math

def sig(a):                       # sigmoid: squashes any number into 0..1
    return 1 / (1 + math.exp(-a))

# one training example: study hours = 0.8, attendance = 0.9, target = 1 (Pass)
x1, x2, t = 0.8, 0.9, 1
lr = 0.5

# weights (vXY = input X -> hidden Y, w1/w2 = hidden -> output)
v11, v21 = 0.5, 0.4               # into hidden 1
v12, v22 = -0.3, 0.8              # into hidden 2
w1, w2 = 0.2, -0.5                # into output

for epoch in range(1, 4):         # 3 epochs
    # ---- 1) FORWARD PROPAGATION ----
    h1 = sig(x1 * v11 + x2 * v21)         # hidden 1 = sig(x1*v11 + x2*v21)
    h2 = sig(x1 * v12 + x2 * v22)         # hidden 2 = sig(x1*v12 + x2*v22)
    y = sig(h1 * w1 + h2 * w2)            # output   = sig(h1*w1 + h2*w2)

    # ---- 2) ERROR ----
    error = t - y                         # error = target - output
    E = 0.5 * error ** 2                  # squared error E = 1/2 (t - y)^2

    # ---- 3) BACKPROPAGATION (deltas) ----
    d_out = error * y * (1 - y)           # output delta = error * y*(1-y)
    d_h1 = d_out * w1 * h1 * (1 - h1)     # hidden delta = d_out * weight * h*(1-h)
    d_h2 = d_out * w2 * h2 * (1 - h2)

    # ---- 4) UPDATE WEIGHTS: w = w + lr * delta * input ----
    w1 += lr * d_out * h1
    w2 += lr * d_out * h2
    v11 += lr * d_h1 * x1
    v21 += lr * d_h1 * x2
    v12 += lr * d_h2 * x1
    v22 += lr * d_h2 * x2

    print("epoch", epoch, "h1", h1, "h2", h2, "y", y, "error", error, "E", E)
    print("d_out", d_out, "d_h1", d_h1, "d_h2", d_h2)

# ================= VIVA Q&A =================
# Q: What is backpropagation?  A: Supervised algorithm that propagates the output error
#    backwards to compute each weight's gradient and reduce the error via gradient descent.
# Q: Why sigmoid?  A: Differentiable and squashes to (0,1); derivative is y(1-y), cheap to compute.
# Q: Output delta formula?  A: (t - y) * y * (1 - y).
# Q: Hidden delta formula?  A: (sum of next-layer delta * weight) * z * (1 - z).
# Q: Weight update rule?  A: w_new = w_old + learning_rate * delta * input.
# Q: Role of learning rate?  A: Step size; too high -> oscillates/diverges, too low -> slow.
# Q: What is an epoch?  A: One full pass through all training patterns.
# Q: Why hidden layer?  A: Lets the net learn non-linear problems (e.g. XOR) a perceptron cannot.
# Q: Why random initial weights?  A: Equal weights make hidden neurons learn identical things (symmetry).
# Q: Overfitting?  A: Net memorises training data and does badly on unseen data; fix with test split, more data.
# Q: Error function used?  A: Squared error E = 0.5 * (t - y)^2, reported as MSE.
