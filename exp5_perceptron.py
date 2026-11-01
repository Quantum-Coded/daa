# EXP 5 - SINGLE-LAYER PERCEPTRON, AND function (bipolar: +1 / -1)
# yin = b + w1*x1 + w2*x2 ; y = +1 if yin >= theta else -1
# Learning rule (only when y != t):  w = w + alpha*t*x ;  b = b + alpha*t
# Trained on ONE example only

x1, x2, t = 1, -1, -1          # the single example
w1, w2, b = 0, 0, 0            # initial weights and bias
alpha, theta = 1, 0

yin = b + w1*x1 + w2*x2        # net input
# output
if yin >= theta:
    y = 1
else:
    y = -1

print("yin =", yin, " y =", y, " t =", t)

if y != t:                     # wrong -> update
    w1 = w1 + alpha * t * x1
    w2 = w2 + alpha * t * x2
    b  = b  + alpha * t
    print("Wrong, updated")
else:
    print("Correct, no update")

print("w1 =", w1, " w2 =", w2, " b =", b)

# ================= VIVA Q&A =================
# Q: Perceptron?  A: Single-layer neuron with learnable weights; output = step(w.x + b).
# Q: Learning rule?  A: If output != target: w += alpha*t*x, b += alpha*t (no change when correct).
# Q: Role of bias/threshold?  A: Shifts the decision boundary away from the origin.
# Q: Convergence theorem?  A: Converges in finite steps if data are linearly separable.
# Q: Can it learn XOR?  A: No, not linearly separable -> needs a multilayer network.
# Q: Why bipolar?  A: Symmetric +-1 values make updates occur for both classes.
# Q: Epoch?  A: One pass over all training patterns.
# Q: Supervised or unsupervised?  A: Supervised (needs targets).
