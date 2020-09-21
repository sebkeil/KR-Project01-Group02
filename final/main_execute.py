import sys
from simplification import *
from preprocessing import *
import S1 as s1
import S2 as s2
import S3 as s3
import argparse

# arguments for execution
parser = argparse.ArgumentParser(description='sudoku SAT solver')
parser.add_argument('-S1', '--sudoku1', metavar='', help='input puzzle')
parser.add_argument('-S2', '--sudoku2', metavar='', help='input puzzle')
parser.add_argument('-S3', '--sudoku3', metavar='', help='input puzzle')
call = parser.parse_args()


def main(version, input1):

    # parse arguments
    full_argments = parseargs(input1)
    argies = full_argments.copy()

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
    backtrack_counter = 0

    sys.setrecursionlimit(10 ** 8)

    # start recursive function
    if version == 'S1':
        assments, backtrack_counter = s1.solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)
    elif version == 'S2':
        while any(len(clause) == 1 for clause in argments) and validity_check:
            variables, assments = unit_propagation(variables, argments, assments, units)
            argments, assments, validity_check = simplify(argments, assments, validity_check)
        units = []
        assments, backtrack_counter = s2.solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)
    elif version == 'S3':
        while any(len(clause) == 1 for clause in argments) and validity_check:
            variables, assments = unit_propagation(variables, argments, assments, units)
            argments, assments, validity_check = simplify(argments, assments, validity_check)
        #units = []
        assments, backtrack_counter = s3.solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    return assments, message, backtrack_counter


if call.sudoku1:
    version = 'S1'
    example = call.sudoku1
if call.sudoku2:
    version = 'S2'
    example = call.sudoku2
if call.sudoku3:
    version = 'S3'
    example = call.sudoku3

if __name__ == "__main__":
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
        print('Number of backtracks:', backtrack_counter)

        i += 1

    print(tests)
    print(times)
