# EXP 10 - FUZZY LOGIC CONTROLLER (Mamdani), pure Python (no libraries)
# Case study: Fan speed from temperature & humidity.  (Swap names for any case.)
# Steps: 1 membership fn  2 fuzzify  3 rules  4 aggregate  5 defuzzify (centroid)


# 1) Triangular membership function: 0 at a, 1 at b, 0 at c
def tri(x, a, b, c):
    if x < a or x > c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)    # rising edge
    else:
        return (c - x) / (c - b)    # falling edge


# Crisp inputs
temp = 32
hum = 70

# 2) Fuzzification: crisp value -> membership degree of each label
cold = tri(temp, 0, 0, 20)
warm = tri(temp, 10, 20, 30)
hot = tri(temp, 20, 40, 40)

low = tri(hum, 0, 0, 50)
mid = tri(hum, 0, 50, 100)
high = tri(hum, 50, 100, 100)

# 3) Rules: IF a AND b THEN c   (AND = min, OR = max)
slow_strength = max(cold, low)      # IF cold OR low humidity  THEN slow
medium_strength = min(warm, mid)    # IF warm AND mid humidity THEN medium
fast_strength = max(hot, high)      # IF hot OR high humidity  THEN fast

# 4) Inference + aggregation: clip each output triangle at its rule strength,
#    then combine the clipped shapes with max
# 5) Defuzzification: centroid = sum(x * mu) / sum(mu)
numerator = 0
denominator = 0
for x in range(101):
    slow = min(slow_strength, tri(x, 0, 0, 50))
    medium = min(medium_strength, tri(x, 0, 50, 100))
    fast = min(fast_strength, tri(x, 50, 100, 100))
    mu = max(slow, medium, fast)
    numerator += x * mu
    denominator += mu

print("Fan speed =", round(numerator / denominator, 2), "%")

# ================= VIVA Q&A =================
# Q: FLC blocks?  A: Fuzzifier, rule base, inference engine, defuzzifier.
# Q: Mamdani vs Sugeno?  A: Mamdani output is a fuzzy set (needs defuzzification); Sugeno output is a function/constant.
# Q: Fuzzification?  A: Converting crisp input to membership degrees.
# Q: Defuzzification methods?  A: Centroid (default), bisector, mean/smallest/largest of maximum.
# Q: AND / OR in rules?  A: min / max (scikit-fuzzy default).
# Q: Membership function types?  A: Triangular, trapezoidal, Gaussian, bell.
# Q: Antecedent vs consequent?  A: Input variable (IF part) vs output variable (THEN part).
# Q: Why fuzzy control?  A: Handles imprecise/linguistic knowledge without an exact mathematical model.
