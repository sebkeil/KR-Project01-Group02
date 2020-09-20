import sys
import py2exe
from simplification import *
from heur import *
from preprocessing import *


# function to simplify CNF with assignments and rules
def simplify(clauses, assigns, validity_check):

    # assign values to pure literals
    #assigns = pure_literals(clauses, varb, assigns)

    # shorten clauses
    clauses1 = shorten_clause(clauses, assigns)

    # assign TRUE to all unit clauses
    assigns, validity_check = unit_clauses(clauses1, assigns, validity_check)

    # check if any clauses empty (then invalid)
    validity_check = empty_clause(clauses1, validity_check)

    # remove true clauses
    clauses2 = true_clauses(clauses1, assigns)

    return clauses2, assigns, validity_check


def solve(arguments, assignments, variables, backtrack, backtrack_counter, simplified_arguments, units):
    simp_arguments = simplified_arguments.copy()
    validity_check = True
    # simplify formula and check if it's unsatisfiable with chosen assignments
    simp_arguments, assignments, validity_check = simplify(simp_arguments, assignments, validity_check)
    print(time.time()-last_time, 'seconds  ', '----||---- working ----||----', 'number of assignments:', len(assignments))

    # this is just unit propagation
    if validity_check:
        while any(len(clause) == 1 for clause in simp_arguments) and validity_check:
            variables, assignments = unit_propagation(variables, simp_arguments, assignments, units)
            simp_arguments, assignments, validity_check = simplify(simp_arguments, assignments, validity_check)

    if 542 in assignments and 543 in assignments:
        print('poop')

    # if no arguments left, then the formula is satisfied
    if not simp_arguments and validity_check:
        return assignments, backtrack_counter

    if len(assignments) == len(variables)-1:# and not validity_check and abs(assignments[-1]) not in backtrack:
        assignments[-1] = -assignments[-1]
        solve(arguments, assignments, variables, backtrack, backtrack_counter, simp_arguments, units)
        return assignments, backtrack_counter

    for next_lit in variables:
        if next_lit not in assignments and -next_lit not in assignments:
            # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
            if validity_check:

                assignments.append(next_lit)
                solve(arguments, assignments, variables, backtrack, backtrack_counter, simp_arguments, units)
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

    #return assignments, backtrack_counter

def main(input1):

    # parse arguments
    argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(argments)

    # this is the random heuristic
    #variables = random_heuristic(variables)

    argments = tautology(argments)  # remove tautologies, just necessary once.

    # initialization of lists (args & assignments) and boolean (validity_check)
    validity_check = True
    assments = []
    backtrack = []
    units = []
    backtrack_counter = 0


    sys.setrecursionlimit(10 ** 8)

    while any(len(clause) == 1 for clause in argments) and validity_check:
        variables, assments = unit_propagation(variables, argments, assments, units)
        argments, assignments, validity_check = simplify(argments, assments, validity_check)
    units = []
    argies = argments.copy()

    # start recursive loop
    assments, backtrack_counter = solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    return assments, message, backtrack_counter

example = "C:\\Users\marto\Desktop\sudoku1.txt"
if __name__ == '__main__':
    import time
    last_time = time.time()
    tests = []
    times = []

    i = 0
    while i < 1:
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
