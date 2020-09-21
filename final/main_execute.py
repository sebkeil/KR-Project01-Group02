import sys
from simplification import *
from preprocessing import *
import S1 as s1
import S2 as s2
import S3 as s3
import argparse

# arguments for execution
parser = argparse.ArgumentParser(description='sudoku SAT solver')
parser.add_argument('-p','--sudoku', metavar='', help='input sudoku puzzle', required=True)
parser.add_argument('-s', '--method', metavar='', help='choose method: 1,2 or 3', required=True)
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
    if version == '1':
        assments, backtrack_counter = s1.solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)
    elif version == '2':
        while any(len(clause) == 1 for clause in argments) and validity_check:
            variables, assments = unit_propagation(variables, argments, assments, units)
            argments, assments, validity_check = simplify(argments, assments, validity_check)
        units = []
        assments, backtrack_counter = s2.solve(argies, assments, variables, backtrack, backtrack_counter, argments, units)
    elif version == '3':
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

example = call.sudoku
version = call.method
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
