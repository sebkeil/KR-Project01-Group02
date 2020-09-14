assignments = []
validity_check = True
args = []

class validityError(Exception):
        def __init__(self, clauses, assignments, validity_check):
            super(validityError, self).__init__(clauses, assignments, validity_check)
            self.args = (clauses, assignments, validity_check)

        def __str__(self):
            return repr(self.args)


class satisfiabilityERROR(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class successComputation(Exception):
    def __init__(self, assignments):
        self.assignments = assignments

    def __str__(self):
        return repr(self.assignments)


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


def getLiterals(argument):
    if argument:
        literals = argument.split(' ')
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


def pure_literals(clauses, varbs, assignments):
    for clause in clauses:
        literals = getLiterals(clause)
        for lit in literals:
            if -lit not in varbs and lit not in assignments:
                assignments.append(lit)
    return assignments


def unit_clauses(clauses, assignments, validity_check):
    for clause in clauses:
        literals = getLiterals(clause)
        if len(literals) == 1:
            if literals[0] not in assignments:
                validity_check = True
                assignments.append(literals[0])
            elif -literals[0] in assignments:
                validity_check = False
                raise satisfiabilityERROR(validity_check)

    return assignments, validity_check


def true_clauses(clauses, assignments):
    for clause in clauses:
        literals = getLiterals(clause)
        if any(item in literals for item in assignments):
            clauses.remove(clause)

    return clauses


def empty_clause(clauses, validity_check):
    for clause in clauses:
        if not clause:
            validity_check = False

    return validity_check


def shorten_clause(clauses, assignments):
    for clause in clauses:
        literals = getLiterals(clause)
        if len(literals) > 1:
            new_clause = clause
            for lit in literals:
                if -lit in assignments:
                    del literals[literals.index(lit)]
                    new_clause = [str(liters) for liters in literals]
                    sep = ' '
                    new_clause = sep.join(new_clause)
            clauses[clauses.index(clause)] = new_clause
    return clauses


# function to simplify CNF with assignments and rules
def simplify(arguments, assignments, varb, validity_check):

    # assign values to pure literals
    assignments = pure_literals(arguments, varb, assignments)

    # assign TRUE to all unit clauses
    assignments, validity_check = unit_clauses(arguments, assignments, validity_check)

    # remove true clauses
    arguments = true_clauses(arguments, assignments)

    # shorten clauses
    arguments = shorten_clause(arguments, assignments)

    validity_check = empty_clause(arguments, validity_check)

    return arguments, assignments, validity_check


def solve(arguments, assignments, varb, validity_check):
    for argument in arguments:
        literals = getLiterals(argument)
        # splitting of assignment: either the literal or its negation
        try:
            print('.')
            for lits in literals:
                if lits not in assignments and -lits not in assignments:
                    assignments.append(lits)
                arguments, assignments, validity_check = simplify(arguments, assignments, varb, validity_check)
                if not validity_check:
                    raise validityError(arguments, assignments, validity_check)

                if not arguments:
                    raise successComputation(assignments)

                assignments, message = solve(arguments, assignments, varb, validity_check)
        except validityError as e:
            assignments[-1] = -assignments[-1]
            arguments, assignments, validity_check = simplify(arguments, assignments, varb, validity_check)
            if validity_check:
                solve(arguments, assignments, varb, validity_check)
            else:
                raise satisfiabilityERROR(validity_check)
        except satisfiabilityERROR as e:
            message = 'Failure: This formula is not satisfiable'
            return assignments, message
        except successComputation as e:
            if not arguments:
                message = 'Success! This formula is satisfiable, with the following assignments: '
                return assignments, message

    return assignments, message


def main(input1):
    args = parseargs(input1)
    # initialize:
    (variables, varbsCount, varb) = getVars(args)
    args = tautology(args)  # remove tautologies, just necessary once.
    assignments = []
    validity_check = True

    # start recursive loop
    (assignments, message) = solve(args, assignments, varb, validity_check)
    return (assignments, message)

example = "sudoku_test01.txt"
if __name__ == '__main__':
    (assignments, message) = main(example)

    print(message, assignments)
    print('Number of assignments:', len(assignments))