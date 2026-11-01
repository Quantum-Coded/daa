# EXP 9 - FUZZY RELATIONS: Max-Min and Max-Product composition.
# R relates X -> Y, S relates Y -> Z. Plain Python, matrices are lists of rows.

R = [[1.0, .35, .05],
     [.4, .95, .4],
     [.05, .35, 1.0]]
S = [[1.0, .3, .05],
     [.55, .85, .25],
     [.85, .3, .05]]
n = 3

# T[i][k] = max over j of min(R[i][j], S[j][k])   <- max-min
# T[i][k] = max over j of R[i][j] * S[j][k]       <- max-product
print("Max-Min  R o S:")
for i in range(n):
    for k in range(n):
        print("T[", i, "][", k, "] =", max(min(R[i][0], S[0][k]),
                                           min(R[i][1], S[1][k]),
                                           min(R[i][2], S[2][k])))

print("\nMax-Prod R o S:")
for i in range(n):
    for k in range(n):
        print("T[", i, "][", k, "] =", max(R[i][0] * S[0][k],
                                           R[i][1] * S[1][k],
                                           R[i][2] * S[2][k]))

# ================= VIVA Q&A =================
# Q: Fuzzy set?  A: Each element has a membership degree in [0,1] instead of just in/out.
# Q: Crisp vs fuzzy?  A: Crisp membership is only 0 or 1.
# Q: Fuzzy relation?  A: Fuzzy subset of a Cartesian product X x Y, i.e. a matrix of memberships.
# Q: Max-min composition?  A: T(x,z) = max over y of min(R(x,y), S(y,z)).
# Q: Max-product composition?  A: T(x,z) = max over y of R(x,y)*S(y,z).
# Q: Use of composition?  A: Chain relations to infer indirect links (occupancy -> action -> availability).
# Q: Union / intersection / complement?  A: max(A,B) / min(A,B) / 1 - A.
# Q: Fuzzy vs probability?  A: Fuzzy = degree of truth (vagueness); probability = likelihood of an event.
