import sys

# initialization of lists (args & assignments) and boolean (validity_check)
assigns = []
validity_check = True
args = []


# Exception: this exception class occurs in the Recursive Loop (solve() function). An exception of this kind occurs if
# if an assignment (the most recently added assignment) results in an invalid argument. This means that the current list
# of assignments cannot satisfy the formula and backtracking is necessary
class validityError(Exception):
    def __init__(self, validity_check):
        self.value = validity_check

    def __str__(self):
        return repr(self.value)


# Exception: this exception occurs if the validity check
class satisfiabilityERROR(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class successComputation(Exception):
    def __init__(self, assigns):
        self.assigns = assigns

    def __str__(self):
        return repr(self.assigns)


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
            args.append(line)
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

    for clause in args:
        literals = getLiterals(clause)
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
    for clause in clauses:
        literals = getLiterals(clause)
        for lit in literals:
            if -lit in literals:
                clauses.remove(clause)
                return clauses

    return clauses


def pure_literals(clauses, varbs, assigns):
    for clause in clauses:
        literals = getLiterals(clause)
        for lit in literals:
            if -lit not in varbs and lit not in assigns:
                assigns.append(lit)
    return assigns


def unit_clauses(clauses, assigns):
    varbs = []
    validity_check = True
    for clause in clauses:
        literals = getLiterals(clause)
        if len(literals) == 1:
            item = literals[0]
            varbs.append(item)
            if -literals[0] in assigns:
                validity_check = False

    for items in varbs:
        if -items in varbs:
            validity_check = False
            #elif literals[0] in assigns:
            #    del clauses[clauses.index(clause)]

    return assigns, validity_check


def true_clauses(clauses, assigns):
    rem_clauses = []
    for clause in clauses:
        literals = getLiterals(clause)
        if any(item in assigns for item in literals):
            rem_clauses.append(clause)
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
    for clause in clauses:
        keep_lits = []
        literals = getLiterals(clause)
        if len(literals) > 1:
            for lit in literals:
                if -lit not in assigns:
                    keep_lits.append(lit)
            if keep_lits:
                new_clause = [str(liters) for liters in keep_lits]
                sep = ' '
                new_clause = sep.join(new_clause)
            clauses[clauses.index(clause)] = new_clause
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


def solve(arguments, assignments, varb, variables, backtrack, backtrack_counter):

    assments = assignments.copy() # make a copy of assignments
                                  # because python passes references and values to new variables

    args = arguments.copy() # copy for same reason
    simp_arguments, assments, validity_check = simplify(args, assments, varb) # simplify formula and check if it's
                                                                              # unsatisfiable with chosen assignments
    # if no arguments left, then the formula is satisfied
    if not simp_arguments:
        return assments, validity_check

    for lit in variables:
        if lit not in assignments and -lit not in assignments: # go through each variable until first unassigned
                                                               # variable is found
            print('----||---- working ----||----')

            # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
            if validity_check:
                assments.append(lit)
                assments, validity_check, backtrack_counter = solve(simp_arguments, assments, varb, variables, backtrack, backtrack_counter)
                return assments, validity_check, backtrack_counter

            # otherwise, backtrack...
            else:
                while len(assments) > 1 and abs(assments[-1]) in backtrack: # this is necessary to see if backtracking
                    print('...hang on! lots of backtracking....')           # leads to a variable which has already been
                    del assments[-1]                                        # backtracked on
                    del backtrack[-1]
                    backtrack_counter += 1

                # if everything has been backtracked on, formula is unsatisfiable --> exits function without further ado
                if len(assments) == 1 and len(backtrack) == 1 and abs(assments[0]) in backtrack:
                    return assignments, validity_check, backtrack_counter

                # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
                backtrack.append(abs(assments[-1]))
                assments[-1] = -assments[-1]
                backtrack_counter += 1
                assments, validity_check, backtrack_counter = solve(arguments, assments, varb, variables, backtrack, backtrack_counter)

            return assments, validity_check, backtrack_counter

def main(input1):
    # parse arguments
    argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varb) = getVars(argments)
    argments = tautology(argments)  # remove tautologies, just necessary once.
    assments = []
    backtrack = []
    backtrack_counter = 0
    argies = argments.copy()

    sys.setrecursionlimit(10 ** 8)

    # start recursive loop
    assments, validity_check, backtrack_counter = solve(argies, assments, varb, variables, backtrack, backtrack_counter)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    return assments, message, backtrack_counter


example = "C:\\Users\marto\Desktop\practice_file8.txt"
if __name__ == '__main__':
    import time
    start_time = time.time()
    (assignments, message, backtrack_counter) = main(example)

    print(message, assignments)
    print('Number of assignments:', len(assignments))
    print('Number of backtracks:', backtrack_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
