# EXP 3 - PEAS / PAGE + SIMPLE REFLEX AGENT.  Case study: Vacuum cleaner agent.
#
# PEAS (agent):                         PAGE (for a goal-based/learning agent):
#  P erformance: clean squares, less    P ercepts : location + dirty/clean
#                time/energy            A ctions  : Left, Right, Suck
#  E nvironment: 2 rooms A and B        G oals    : all rooms clean
#  A ctuators  : wheels, suction        E nvironment: two-room world
#  S ensors    : dirt sensor, location
#
# Simple reflex agent = ONLY if-then rules on the CURRENT percept (no memory).

def reflex_agent(location, status):
    if status == "Dirty":
        return "Suck"
    return "Right" if location == "A" else "Left"

world = {"A": "Dirty", "B": "Dirty"}     # environment state
loc = "A"                                # agent starts in room A
for step in range(4):
    action = reflex_agent(loc, world[loc])           # percept -> action
    print(f"Step {step}: at {loc}, sees {world[loc]} -> {action}")
    if action == "Suck":
        world[loc] = "Clean"                         # action changes environment
    elif action == "Right":
        loc = "B"
    else:
        loc = "A"
print("Final world:", world)

# ================= VIVA Q&A =================
# Q: What is an agent?  A: Anything that perceives its environment via sensors and acts via actuators.
# Q: What is PEAS?  A: Performance measure, Environment, Actuators, Sensors.
# Q: What is PAGE?  A: Percepts, Actions, Goals, Environment.
# Q: Simple reflex agent?  A: Chooses action from the current percept only, using condition-action rules.
# Q: Its limitation?  A: No memory; fails in partially observable environments, can loop forever.
# Q: Other agent types?  A: Model-based reflex, goal-based, utility-based, learning agent.
# Q: Rational agent?  A: Picks the action maximising expected performance measure given its percepts.
# Q: Vacuum-world properties?  A: Fully observable (here), deterministic, discrete, static, single agent.
