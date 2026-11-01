# EXP 2(b) - INFORMED SEARCH: A* on the 8-puzzle
# f(n) = g(n) + h(n)   g = moves made so far, h = misplaced tiles (0 = blank)
import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
START = (1, 2, 3, 0, 4, 6, 7, 5, 8)

def h(s):                                    # heuristic: tiles not in goal place
    misplaced = 0                            # counter for wrongly placed tiles
    for i in range(9):                       # check each of the 9 positions
        tile = s[i]
        if tile == 0:                        # ignore the blank
            continue
        if tile != GOAL[i]:                  # tile is not where the goal wants it
            misplaced += 1
    return misplaced

def neighbours(s):
    result = []                              # collect all next boards here
    z = s.index(0)                          # blank position in the flat tuple (where the 0 is)
    r, c = divmod(z, 3)                      # 3x3 grid, returns quotient, remainder
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:      # stay inside the 3x3 board
            t = list(s)
            n = nr * 3 + nc                  # flatten
            t[z], t[n] = t[n], t[z]          # slide tile into the blank
            result.append(tuple(t))          # add this board to the list
    return result                            # give back all boards at once

def astar(start):
    pq = [(h(start), 0, start, [start])]    # (f, g, state, path) - heap pops smallest f
    best = {start: 0}                        # cheapest g seen per state
    while pq:
        f, g, s, path = heapq.heappop(pq)
        if s == GOAL:
            return path
        for n in neighbours(s):
            if n not in best or g + 1 < best[n]:
                best[n] = g + 1
                heapq.heappush(pq, (g + 1 + h(n), g + 1, n, path + [n]))

solution = astar(START)                      # list of boards from start to goal

step_number = 0
for board in solution:
    print("Step", step_number)
    print(board[0], board[1], board[2])      # first row
    print(board[3], board[4], board[5])      # second row
    print(board[6], board[7], board[8])      # third row
    print()                                  # blank line between steps
    step_number += 1

# ================= VIVA Q&A =================
# Q: Informed search?  A: Uses a heuristic h(n) estimating cost to goal (A*, greedy best-first).
# Q: A* evaluation function?  A: f(n) = g(n) + h(n).
# Q: g and h?  A: g = actual cost from start; h = estimated cost to goal.
# Q: Heuristic used?  A: Misplaced tiles (Manhattan distance is stronger).
# Q: Admissible heuristic?  A: Never overestimates true cost; guarantees A* is optimal.
# Q: Greedy best-first vs A*?  A: Greedy uses only h (fast, not optimal); A* uses g + h (optimal).
# Q: Why a priority queue (heap)?  A: Always expand the node with smallest f.
# Q: Is every 8-puzzle solvable?  A: No; only half of states (even inversion count for this goal).
# Q: Drawback of A*?  A: Stores all nodes in memory: exponential space.
