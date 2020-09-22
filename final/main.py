import sys
from simplification import *
from heur import *
from preprocessing import *

# initialization of lists (args & assignments) and boolean (validity_check)
validity_check = True


# function to simplify CNF with assignments and rules
def simplify(clauses, assigns, varb):

    # assign values to pure literals
    #assigns = pure_literals(clauses, varb, assigns)

    # shorten clauses
    clauses1 = shorten_clause(clauses, assigns)

    # assign TRUE to all unit clauses
    assigns, validity_check = unit_clauses(clauses1, assigns)

    # check if any clauses empty (then invalid)
    validity_check = empty_clause(clauses1, validity_check)

    # remove true clauses
    clauses2 = true_clauses(clauses1, assigns)

    return clauses2, assigns, validity_check


def solve(arguments, assignments, varb, variables, backtrack, backtrack_counter, simplified_arguments, units):
    simp_arguments = simplified_arguments.copy()

    # if no arguments left, then the formula is satisfied
    if not simp_arguments:
        return assignments, backtrack_counter
    # simplify formula and check if it's unsatisfiable with chosen assignments
    simp_arguments, assignments, validity_check = simplify(simp_arguments, assignments, varb)
    print('----||---- working ----||----', 'number of assignments:', len(assignments))

    # this is just unit propagation
    if validity_check:
        while any(len(clause) == 1 for clause in simp_arguments) and validity_check:
            variables, assignments = unit_propagation(variables, simp_arguments, assignments, units)
            simp_arguments, assignments, validity_check = simplify(simp_arguments, assignments, varb)
            simp_arguments.sort(key=len)

    for lit in variables:
        if lit not in assignments and -lit not in assignments: # go through each variable until first unassigned
                                                               # variable is found

            # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
            if validity_check:
                assignments.append(lit)
                solve(arguments, assignments, varb, variables, backtrack, backtrack_counter, simp_arguments, units)
                return assignments, validity_check, backtrack_counter

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
                    return assignments

                # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
                backtrack.append(abs(assignments[-1]))
                assignments[-1] = -assignments[-1]
                backtrack_counter += 1
                solve(arguments, assignments, varb, variables, backtrack, backtrack_counter, arguments, units)
                return assignments

    return assignments, backtrack_counter

def main(input1):

    # parse arguments
    argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(argments)

    # this is the random heuristic
    variables = random_heuristic(variables)

    argments = tautology(argments)  # remove tautologies, just necessary once.
    simplified_arguments = argments.copy()
    assments = []
    backtrack = []
    units = []
    backtrack_counter = 0
    argies = argments.copy()

    sys.setrecursionlimit(10 ** 8)

    # start recursive loop
    assments, backtrack_counter = solve(argies, assments, varbs, variables, backtrack, backtrack_counter, simplified_arguments, units)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    return assments, message, backtrack_counter

example = "sudoku1.txt"
if __name__ == '__main__':
    import time
    last_time = time.time()
    tests = []
    times = []

    i = 0
    while i < 20:
        assignments, message, backtrack_counter = main(example)
        tests.append(len(assignments))
        now_time = time.time() - last_time
        print("--- %s seconds ---" % (now_time))

        times.append(now_time)
        last_time = time.time()

        print(message, sorted(assignments, reverse=True))
        print('Number of assignments:', len(assignments))
        print('Number of backtracks:', backtrack_counter)

        i += 1

    print(tests)
    print(times)
