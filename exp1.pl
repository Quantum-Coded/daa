% EXP 1 - PROLOG (paste in SWISH: swish.swi-prolog.org). Case study: FAMILY & EXAM MARKS.
% Pattern to remember: FACTS -> RULES (head :- body) -> QUERIES.
% Syntax: "," = AND, ";" = OR, "\+" = NOT, "\=" = not equal, "is" = arithmetic,
%         Uppercase/_ = variable, lowercase = constant, every clause ends with ".".
% Features covered: facts, rules, conjunction, disjunction, negation, inequality,
%                   recursion, arithmetic, comparison, lists, findall, cut.

% ---------- FACTS (what we KNOW) ----------
parent(tom, bob).   parent(tom, liz).
parent(bob, ann).   parent(bob, pat).
male(tom).  male(bob).  male(pat).
female(liz). female(ann).
marks(ann, 80).  marks(pat, 45).  marks(liz, 62).      % marks(Student, Score)

% ---------- RULES (what we can INFER) ----------
father(X, Y)      :- parent(X, Y), male(X).                 % AND
mother(X, Y)      :- parent(X, Y), female(X).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).            % chaining via shared Y
sibling(X, Y)     :- parent(P, X), parent(P, Y), X \= Y.    % inequality
child(X, Y)       :- parent(Y, X).                          % reversed relation
ancestor(X, Y)    :- parent(X, Y).                          % recursion: base case
ancestor(X, Y)    :- parent(X, Z), ancestor(Z, Y).          % recursive case
childless(X)      :- (male(X) ; female(X)), \+ parent(X, _).% OR + negation
passed(S)         :- marks(S, M), M >= 50.                  % comparison
grade(S, G)       :- marks(S, M), M >= 75, !, G = distinction.  % cut: stop at first match
grade(S, G)       :- marks(S, M), M >= 50, !, G = pass.
grade(_, fail).
bonus(S, New)     :- marks(S, M), New is M + 5.             % arithmetic with "is"

% Lists
len([], 0).                                                  % length of empty list = 0
len([_|T], N) :- len(T, M), N is M + 1.                      % [Head|Tail]
my_member(X, [X|_]).
my_member(X, [_|T]) :- my_member(X, T).

% ---------- QUERIES (type in the SWISH query box) ----------
% ?- father(tom, bob).                  true
% ?- grandparent(tom, W).               W = ann ; W = pat   (press Next)
% ?- sibling(ann, S).                   S = pat
% ?- ancestor(tom, ann).                true (recursion)
% ?- childless(ann).                    true
% ?- passed(pat).                       false (45 < 50)
% ?- grade(ann, G).                     G = distinction
% ?- bonus(pat, N).                     N = 50
% ?- findall(S, passed(S), L).          L = [ann, liz]   (collect all solutions)
% ?- len([a,b,c], N).                   N = 3
% ?- my_member(b, [a,b,c]).             true

% ================= VIVA Q&A =================
% Q: What is Prolog?  A: Declarative logic-programming language; you state facts and
%    rules and the engine answers queries by inference.
% Q: Fact vs rule?  A: Fact is unconditionally true; rule (Head :- Body) is true if body is true.
% Q: What is unification?  A: Matching two terms by binding variables so they become identical.
% Q: What is backtracking?  A: If a goal fails, Prolog goes back to the last choice point
%    and tries the next alternative clause. "Next" in SWISH shows this.
% Q: What does "," / ";" / "\+" mean?  A: AND / OR / negation as failure.
% Q: What is negation as failure?  A: \+ G is true if G cannot be proved (closed-world assumption).
% Q: What is a cut (!)?  A: Commits to the current clause; prevents backtracking to later ones.
% Q: Why does ancestor need two clauses?  A: Base case stops recursion; recursive case extends it.
% Q: Difference between = and is?  A: = unifies; "is" evaluates the arithmetic expression on the right.
% Q: What is the closed-world assumption?  A: Anything not in the knowledge base is taken as false.
% Q: Inference strategy used?  A: Backward chaining, depth-first search with backtracking.
