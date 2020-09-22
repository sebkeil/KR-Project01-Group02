from simplification import *
from heur import *


def solve(arguments, assignments, variables, backtrack, backtrack_counter, simplified_arguments, units):
    simp_arguments = arguments.copy()
    validity_check = True
    # simplify formula and check if it's unsatisfiable with chosen assignments
    sim_arguments, assignments, validity_check = simplify(simplified_arguments, assignments, validity_check)
    print('----||---- working ----||----', 'number of assignments:', len(assignments))

    # this is just unit propagation
    if validity_check:
        while any(len(clause) == 1 for clause in sim_arguments) and validity_check:
            variables, assignments, units = unit_propagation(variables, sim_arguments, assignments, units)
            sim_arguments, assignments, validity_check = simplify(sim_arguments, assignments, validity_check)

    # if no arguments left, then the formula is satisfied
    if not sim_arguments and validity_check:
        return assignments, backtrack_counter, units

    # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
    if validity_check:
        # this is the heuristic implementation
        next_lit = jw1_heuristic(variables, sim_arguments)
        if abs(next_lit) in backtrack:
            varbies = variables.copy()
            varbies.remove(abs(next_lit))
            next_lit = jw1_heuristic(varbies, sim_arguments)

        assignments.append(next_lit)
        solve(arguments, assignments, variables, backtrack, backtrack_counter, sim_arguments, units)
        return assignments, backtrack_counter, units

    # otherwise, backtrack...
    else:
        # this is necessary to see if backtracking leads to a variable which has already been backtracked on
        while len(assignments) > 1 and abs(assignments[-1]) in backtrack:
            del backtrack[backtrack.index(abs(assignments[-1]))]
            del assignments[-1]
            # this is to remove the most recently added unit literals, makes testing quicker
            while len(assignments) > 1 and assignments[-1] in units:
                del units[units.index(assignments[-1])]
                del assignments[-1]

        # if everything has been backtracked on, formula is unsatisfiable --> exits function without further ado
        if len(assignments) == 1 and len(backtrack) == 1 and abs(assignments[0]) in backtrack:
            return assignments, backtrack_counter, units

        # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
        backtrack.append(abs(assignments[-1]))
        assignments[-1] = -assignments[-1]
        backtrack_counter.append(backtrack[-1])
        print('...lots of backtracking.... nr. backtracks:', len(backtrack_counter))
        solve(arguments, assignments, variables, backtrack, backtrack_counter, simp_arguments, units)
        return assignments, backtrack_counter, units