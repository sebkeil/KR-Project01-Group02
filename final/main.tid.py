import sys
import random
import argparse

# here are the arguments that you want to give to the program from the terminal/command line
parser = argparse.ArgumentParser(description='sudoku SAT solver')
parser.add_argument('-s','--sudoku', metavar='', help='input sudoku puzzle', required=True)
# parser.add_argument('-m', '--method', type=int, metavar='', help='choose method (1,2,3...)') #this still cannot be used
call = parser.parse_args()

# initialization of lists (args & assignments) and boolean (validity_check)
assigns = []
validity_check = True
args = []


def unit_propagation(variables, clauses, assmts):
    clauses.sort(key=len)
    n = 0
    while n < len(clauses) and len(clauses[n]) == 1:
        literals = clauses[n]
        if literals[0] in variables:
            variables.remove(literals[0])
        if -literals[0] in variables:
            variables.remove(-literals[0])
        variables.insert(0, literals[0])
        n += 1

    return variables, assmts


def random_heuristic(variables):
    random.shuffle(variables)
    flip = 1
    for varb in variables:
        if flip == 1:
            variables[variables.index(varb)] = -varb
        flip = -flip
    random.shuffle(variables)

    return variables


def parseargs(inputfile):
    file = open(inputfile, "r")
    rules = file.read()
    lines = rules.split('\n')
    for line in lines:
        if line.startswith('c'):
            continue
        elif line.startswith('p'):
            info = line.split(' ')
            numVarbs = info[2]  # these two could be interesting for evaluating heuristics and hardness
            numClauses = info[3]  # <--
        else:
            line = line[:-2]
            arg = getLiterals(line)
            args.append(arg)

    return args


def getLiterals(clause):
    if clause:
        literals = clause.split(' ')
        literals = [int(lit) for lit in literals]
    else:
        literals = []
    return literals


def getVars(args):
    #  initialize variables
    varbs = []
    varbsCount = []

    for literals in args:
        for lit in literals:
            # for each literal in a clause, see if the integer has already been added to variable list
            # important to see if a specific value is a pure literal or if there are any unit clauses
            if lit not in varbs:
                varbs.append(lit)
                varbsCount.append(1)
            else:
                varbsCount[varbs.index(lit)] += 1

    variablesList = [abs(variables) for variables in varbs]
    variablesList = list(set(variablesList))
    return variablesList, varbsCount, varbs


def tautology(clauses):
    for literals in clauses:
        for lit in literals:
            if -lit in literals:
                clauses.remove(clause)
                return clauses

    return clauses


def pure_literals(clauses, varbs, assigns):
    for literals in clauses:
        for lit in literals:
            if -lit not in varbs and lit not in assigns:
                assigns.append(lit)
    return assigns


def unit_clauses(clauses, assigns):
    varbs = []
    validity_check = True
    for literals in clauses:
        if len(literals) == 1:
            item = literals[0]
            varbs.append(item)
            if -literals[0] in assigns:
                validity_check = False

    for items in varbs:
        if -items in varbs:
            validity_check = False

    return assigns, validity_check


def true_clauses(clauses, assigns):
    rem_clauses = []
    for literals in clauses:
        if any(item in assigns for item in literals):
            rem_clauses.append(literals)
    for rc in rem_clauses:
        clauses.remove(rc)
    del rem_clauses
    return clauses


def empty_clause(clauses, validity_check):
    for clause in clauses:
        if not clause:
            validity_check = False

    return validity_check


def shorten_clause(clauses, assigns):
    for literals in clauses:
        keep_lits = []
        if len(literals) > 1:
            for lit in literals:
                if -lit not in assigns:
                    keep_lits.append(lit)
            if keep_lits:
                new_clause = [liters for liters in keep_lits]
            else:
                new_clause = []

            clauses[clauses.index(literals)] = new_clause
    return clauses


# function to simplify CNF with assignments and rules
def simplify(clauses, assigns, varb):

    # assign values to pure literals
    assigns = pure_literals(clauses, varb, assigns)

    # shorten clauses
    clauses1 = shorten_clause(clauses, assigns)

    # assign TRUE to all unit clauses
    assigns, validity_check = unit_clauses(clauses1, assigns)

    # check if any clauses empty (then invalid)
    validity_check = empty_clause(clauses1, validity_check)

    # remove true clauses
    clauses2 = true_clauses(clauses1, assigns)

    return clauses2, assigns, validity_check


def solve(arguments, assignments, varb, variables, backtrack, backtrack_counter, simplified_arguments):
    simp_arguments = simplified_arguments.copy()
    assments = assignments.copy() # make a copy of assignments
                                  # because python passes references and values to new variables

    #args = arguments.copy() # copy for same reason
    simp_arguments, assments, validity_check = simplify(simp_arguments, assments, varb) # simplify formula and check if it's
                                                                              # unsatisfiable with chosen assignments
    # this is just unit propagation
    variables, assments = unit_propagation(variables, simp_arguments, assments)

    # if no arguments left, then the formula is satisfied
    if not simp_arguments:
        return assments, validity_check, backtrack_counter

    for lit in variables:
        if lit not in assments and -lit not in assments: # go through each variable until first unassigned
                                                               # variable is found
            print('----||---- working ----||----', 'number of assignments:', len(assments))

            # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
            if validity_check:
                assments.append(lit)
                assments, validity_check, backtrack_counter = solve(arguments, assments, varb, variables, backtrack, backtrack_counter, simp_arguments)
                return assments, validity_check, backtrack_counter

            # otherwise, backtrack...
            else:
                print('...hang on! lots of backtracking....')
                while len(assments) > 1 and abs(assments[-1]) in backtrack: # this is necessary to see if backtracking
                                                                            # leads to a variable which has already been
                                                                            # backtracked on
                    del backtrack[backtrack.index(abs(assments[-1]))]
                    del assments[-1]

                # if everything has been backtracked on, formula is unsatisfiable --> exits function without further ado
                if len(assments) == 1 and len(backtrack) == 1 and abs(assments[0]) in backtrack:
                    return assignments, validity_check, backtrack_counter

                # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
                backtrack.append(abs(assments[-1]))
                assments[-1] = -assments[-1]
                backtrack_counter += 1
                assments, validity_check, backtrack_counter = solve(arguments, assments, varb, variables, backtrack, backtrack_counter, arguments)

            return assments, validity_check, backtrack_counter

def main(input1):

    # parse arguments
    argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(argments)
    variables = random_heuristic(variables)
    argments = tautology(argments)  # remove tautologies, just necessary once.
    simplified_arguments = argments.copy()
    assments = []
    backtrack = []
    backtrack_counter = 0
    argies = argments.copy()

    sys.setrecursionlimit(10 ** 8)

    # start recursive loop
    assments, validity_check, backtrack_counter = solve(argies, assments, varbs, variables, backtrack, backtrack_counter, simplified_arguments)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    return assments, message, backtrack_counter



if __name__ == '__main__':

    import time
    start_time = time.time()

    (assignments, message, backtrack_counter) = main(call.sudoku)

    print(message, sorted(assignments, reverse=True))
    print('Number of assignments:', len(assignments))
    print('Number of backtracks:', backtrack_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
