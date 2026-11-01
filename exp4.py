# EXP 4(a)(b) - HALF / FULL ADDER with McCulloch-Pitts neurons
# MP neuron: output 1 if (sum of input*weight) >= threshold else 0.
# AND : weights (1,1) threshold 2 | OR : weights (1,1) threshold 1
# XOR is not linearly separable, so build it from 2 layers:  XOR = (A OR B) AND NOT(A AND B)
# NOT(A AND B) as ONE neuron: weights (-1,-1), threshold -1  (fires unless both are 1)

def mp(x, w, t):
    total = 0
    for i in range(len(x)):
        total = total + x[i] * w[i]    # input * its weight
    if total >= t:
        return 1                       # neuron fires
    else:
        return 0                       # neuron does not fire

def AND(a, b): return mp([a, b], [1, 1], 2)
def OR(a, b):  return mp([a, b], [1, 1], 1)
def NAND(a, b): return mp([a, b], [-1, -1], -1)
def XOR(a, b): return AND(OR(a, b), NAND(a, b))      # hidden layer = OR, NAND

def half_adder(a, b):
    return XOR(a, b), AND(a, b)                      # sum, carry

def full_adder(a, b, cin):
    s1, c1 = half_adder(a, b)                        # first half adder
    s, c2 = half_adder(s1, cin)                      # second half adder
    return s, OR(c1, c2)                             # carry = c1 OR c2

print("HALF ADDER\nA B | S C")
for a in (0, 1):
    for b in (0, 1):
        print(a, b, "|", *half_adder(a, b))

print("\nFULL ADDER\nA B Cin | S Cout")
for a in (0, 1):
    for b in (0, 1):
        for c in (0, 1):
            print(a, b, c, " |", *full_adder(a, b, c))

# ================= VIVA Q&A =================
# Q: McCulloch-Pitts neuron?  A: Binary-threshold neuron: fires (1) if weighted input sum >= threshold, else 0.
# Q: Are MP weights learned?  A: No, fixed and set by hand.
# Q: AND / OR thresholds?  A: Weights (1,1): AND threshold 2, OR threshold 1.
# Q: Why can one neuron not do XOR?  A: XOR is not linearly separable; needs hidden layer (OR, NAND -> AND).
# Q: Half adder outputs?  A: Sum = A XOR B, Carry = A AND B.
# Q: Full adder?  A: Sum = A xor B xor Cin; Cout = (A and B) or (Cin and (A xor B)); two half adders + OR.
# Q: Excitatory vs inhibitory?  A: Positive weight vs negative weight inputs.
