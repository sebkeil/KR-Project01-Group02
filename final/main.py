import sys
from simplification import *
from preprocessing import *
import S1 as s1
import S2 as s2
import S3 as s3
import argparse

# here are the arguments that you want to give to the program from the terminal/command line
parser = argparse.ArgumentParser(description='sudoku SAT solver')
parser.add_argument('-S1', '--sudoku1', metavar='', help='input puzzle')
parser.add_argument('-S2', '--sudoku2', metavar='', help='input puzzle')
parser.add_argument('-S3', '--sudoku3', metavar='', help='input puzzle')

call = parser.parse_args()


def main(version, input1):

    # parse arguments
    full_argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(full_argments)

    # this is the random heuristic
    #variables = random_heuristic(variables)

    argments = tautology(full_argments)  # remove tautologies, just necessary once.

    # initialization of lists (args & assignments) and boolean (validity_check)
    validity_check = True
    assments = []
    backtrack = []
    units = []
    backtrack_counter = []

    sys.setrecursionlimit(10 ** 8)

    while any(len(clause) == 1 for clause in argments) and validity_check:
        variables, assments = unit_propagation(variables, argments, assments, units)
        argments, assments, validity_check = simplify(argments, assments, validity_check)
    units = []
    argies = argments.copy()
    # initialize variables:
    (variables1, varbsCount, varbs) = getVars(argments)
    init_assignments = assments.copy()
    assments = []

    # start recursive function
    if version == 'S1':
        assments, backtrack_counter = s1.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units)
    elif version == 'S2':
        assments, backtrack_counter = s2.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units)
    elif version == 'S3':
        assments, backtrack_counter = s3.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units)
    variables, assments = unit_propagation(variables, argments, assments, units)

    print('Number of backtracks:', backtrack_counter)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    for atoms in assments:
        init_assignments.append(atoms)

    return init_assignments, message, backtrack_counter

if call.sudoku1:
    example = call.sudoku1
    version = 'S1'
elif call.sudoku2:
    example = call.sudoku2
    version = 'S2'
elif call.sudoku3:
    example = call.sudoku3
    version = 'S3'

if __name__ == "__main__":

example = "sudoku1.txt"
if __name__ == '__main__':

    import time
    last_time = time.time()
    tests = []
    times = []

    i = 0
    while i < 1:
        assignments, message, backtrack_counter = main(version, example)
        tests.append(len(assignments))
        now_time = time.time() - last_time
        print("--- %s seconds ---" % (now_time))

        times.append(now_time)
        last_time = time.time()

        print(message, sorted(assignments, reverse=True))
        print('Number of assignments:', len(assignments))
        print('Number of backtracks:', len(backtrack_counter))

        i += 1

    print(tests)
    print(times)
