from simplification import *
from heur import random_heuristic


# function to simplify CNF with assignments and rules
def simplify(clauses, assigns, validity_check):

    # assign values to pure literals
    #assigns = pure_literals(clauses, varb, assigns)

    # remove true clauses
    clauses = true_clauses(clauses, assigns)

    # assign TRUE to all unit clauses
    assigns, validity_check = unit_clauses(clauses, assigns, validity_check)

    # shorten clauses
    clauses = shorten_clause(clauses, assigns)

    # check if any clauses empty (then invalid)
    validity_check = empty_clause(clauses, validity_check)

    return clauses, assigns, validity_check


def solve(arguments, assignments, variables, backtrack, backtrack_counter, simplified_arguments, units):
    simp_arguments = simplified_arguments.copy()
    validity_check = True
    # simplify formula and check if it's unsatisfiable with chosen assignments
    sim_arguments, assignments, validity_check = simplify(simp_arguments, assignments, validity_check)
    print('----||---- working ----||----', 'number of assignments:', len(assignments))

    # this is just unit propagation
    while any(len(clause) == 1 for clause in sim_arguments) and validity_check:
        variables, assignments = unit_propagation(variables, sim_arguments, assignments, units)
        sim_arguments, assignments, validity_check = simplify(sim_arguments, assignments, validity_check)

    # if no arguments left, then the formula is satisfied
    if not sim_arguments and validity_check:
        return assignments, backtrack_counter

    if len(assignments) == len(variables) and not validity_check and abs(assignments[-1]) not in backtrack:
        assignments[-1] = -assignments[-1]
        solve(arguments, assignments, variables, backtrack, backtrack_counter, sim_arguments, units)
        return assignments, backtrack_counter

    for next_lit in variables:
        if next_lit not in assignments and -next_lit not in assignments:
            # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
            if validity_check:

                assignments.append(next_lit)
                solve(arguments, assignments, variables, backtrack, backtrack_counter, sim_arguments, units)
                return assignments, backtrack_counter

            # otherwise, backtrack...
            else:
                print('...hang on! lots of backtracking....')

                # this is necessary to see if backtracking leads to a variable which has already been backtracked on
                while len(assignments) > 1 and abs(assignments[-1]) in backtrack:
                    del backtrack[backtrack.index(abs(assignments[-1]))]
                    del assignments[-1]
                    # this is to remove the most recently added unit literals, makes testing quicker
                    while len(assignments) > 1 and assignments[-1] in units:
                        del assignments[-1]
                        del units[-1]

                # if everything has been backtracked on, formula is unsatisfiable --> exits function without further ado
                if len(assignments) == 1 and len(backtrack) == 1 and abs(assignments[0]) in backtrack:
                    return assignments, backtrack_counter

                # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
                backtrack.append(abs(assignments[-1]))
                assignments[-1] = -assignments[-1]
                backtrack_counter += 1
                solve(arguments, assignments, variables, backtrack, backtrack_counter, arguments, units)
                return assignments, backtrack_counter
