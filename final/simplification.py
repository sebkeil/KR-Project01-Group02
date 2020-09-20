def tautology(clauses):
    for literals in clauses:
        for lit in literals:
            if -lit in literals:
                clauses.remove(literals)
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
            varbs.append(literals[0])

    for items in varbs:
        if -items in varbs or -items in assigns:
            validity_check = False

    return assigns, validity_check


def true_clauses(clauses, assigns):
    rem_clauses = []
    for literals in clauses:
        if any(item in literals for item in assigns):
            rem_clauses.append(literals)
    for rc in rem_clauses:
        clauses.remove(rc)

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


def unit_propagation(variables, clauses, assmts, units):
    clauses.sort(key=len)
    n = 0
    while n < len(clauses) and len(clauses[n]) == 1:
        literals = clauses[n]
        if literals[0] not in assmts and -literals[0] not in assmts:
            assmts.append(literals[0])
            units.append(literals[0])
        n += 1

    return variables, assmts