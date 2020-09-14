import numpy as np

def parse_literals(clause):
    if len(clause) > 0:
        literals = [int(lit) for lit in clause]
    else:
        literals = []
    return literals

def parse_clauses(file):     #  reads in the files and returns a list of lists: 'clauses'
    first_line = file.readline().split()
    n_variables = first_line[2]
    n_clauses = first_line[3]
    raw_clauses = []
    clauses = []       # contains the literals as integers

    for line in file:
        raw_clause = line.split()
        raw_clause.pop(-1)
        raw_clauses.append(raw_clause)

    for raw_clause in raw_clauses:
        clause = parse_literals(raw_clause)
        clauses.append(clause)

    return n_variables, n_clauses, clauses

def get_atoms(clauses):
    atoms = []      # all the indidivual variables that are possible (only positives)
    flat_literals = np.unique(np.array([literal for clause in clauses for literal in clause]))   # all possible assignments (positive and negative)
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in atoms:
                atoms.append(abs(literal))
    variables_count = len(atoms)
    return atoms, flat_literals


#print('The file contains {} variables and {} clauses'.format(n_vars, n_clauses))
#print(clauses)

