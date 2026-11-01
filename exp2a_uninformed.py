# EXP 2(a) - UNINFORMED SEARCH: Water Jug with IDDFS (Iterative Deepening DFS)
# Idea: state = (a, b) litres. Run depth-limited DFS with limit 0, 1, 2, ... until the goal is found.

CAP_A, CAP_B, TARGET = 4, 3, 2      # jug sizes and the amount we want in jug A

def next_states(a, b):
    pour_ab = min(a, CAP_B - b)      # you can only pour what fits in B
    pour_ba = min(b, CAP_A - a)
    return [(CAP_A, b), (a, CAP_B),            # fill A / fill B
            (0, b), (a, 0),                    # empty A / empty B
            (a - pour_ab, b + pour_ab),        # pour A -> B
            (a + pour_ba, b - pour_ba)]        # pour B -> A

def dls(path, limit):                # depth-limited DFS: go at most `limit` more moves
    a, b = path[-1]
    if a == TARGET:                  # goal test
        return path
    if limit == 0:                   # cutoff: stop going deeper
        return None
    for s in next_states(a, b):
        if s not in path:            # skip states on THIS path only (avoids loops)
            found = dls(path + [s], limit - 1)
            if found:
                return found
    return None

def iddfs(start=(0, 0)):
    max_depth = (CAP_A + 1) * (CAP_B + 1) - 1  # a loop-free path can't be longer than this
    for limit in range(max_depth + 1):         # the depth limit grows by 1 each round
        found = dls([start], limit)
        print("Depth limit", limit, "->", "found" if found else "not found")
        if found:
            return found                       # path

sol = iddfs()
print("Steps:", len(sol) - 1)
for s in sol:
    print(s)

# ================= VIVA Q&A =================
# Q: Uninformed search?  A: No domain knowledge/heuristic; systematically explores (BFS, DFS, IDDFS, UCS).
# Q: IDDFS?  A: DFS repeated with increasing depth limit: BFS optimality with DFS low memory.
# Q: Is IDDFS optimal/complete?  A: Complete, and optimal when every step costs the same (shallowest goal found first).
# Q: IDDFS complexity?  A: Time O(b^d), space O(b*d) (b = branching factor, d = depth of goal).
# Q: Isn't repeating the shallow levels wasteful?  A: Little; most nodes are at the deepest level, so the total stays O(b^d).
# Q: Why check the current path instead of a global seen set?  A: A global set can block a state reached deep in
#    one branch from being reached by a shorter route later, which can lose the shortest solution.
# Q: BFS vs DFS data structure?  A: BFS = queue (FIFO); DFS = stack (LIFO). IDDFS uses DFS (recursion stack).
# Q: DFS drawback?  A: Not optimal, can go infinitely deep; memory is only O(b*m).
# Q: State/operators here?  A: State = (litres in A, litres in B); operators = fill, empty, pour.
# Q: When is water-jug solvable?  A: Target is a multiple of gcd(capA, capB) and <= max capacity.
