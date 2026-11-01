# AISC exam cheat-sheet (run: `python expXX.py`, Exp1 in SWISH)
| Exp | File | One-line idea to remember |
|---|---|---|
| 1 | exp1.pl | facts -> rules (`:-`, `,`=AND, `;`=OR, `\+`=NOT) -> queries |
| 2a | exp2a_uninformed.py | depth-limited DFS in a loop: limit 0, 1, 2, ... = IDDFS |
| 2b | exp2b_informed.py | heap on f = g + h (misplaced tiles) |
| 3 | exp3_peas_agent.py | PEAS comment + `if status==Dirty: Suck` reflex agent |
| 4 | exp4_mp_adder.py | mp(x,w,t); AND(1,1,t2) OR(1,1,t1) NAND(-1,-1,t-1); XOR=AND(OR,NAND) |
| 5 | exp5_perceptron.py | if y!=t: w+=alpha*t*x ; b+=alpha*t |
| 6 | exp6_backprop.py | forward -> delta_out=(t-y)y(1-y) -> delta_hid=(d@W.T)z(1-z) -> update |
| 7 | exp7_som_lvq.py | SOM: move winner toward x. LVQ: toward if class matches else away |
| 8 | exp8_associative_memory.py | Hebb W=sum outer; recall sgn(W@x); BAM both ways (W, W.T) |
| 9 | exp9_fuzzy_sets_relations.py | max/min ops; composition max_j min(R,S) |
| 10 | exp10_fuzzy_controller.py | Antecedent/Consequent -> MFs -> Rules -> ControlSystemSimulation |
| 11 | exp11_anfis.py / .ipynb | MF -> rule product -> normalise -> lstsq consequents + gradient premise |
