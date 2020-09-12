file = open('sudoku-rules.txt', 'r')
#print(file.read())

arguments = []

def parse_clauses(file):     #  reads in the files and returns a list of lists: 'clauses'
    first_line = file.readline().split()
    n_variables = first_line[2]
    n_clauses = first_line[3]
    clauses = []

    for line in file:
        clause = line.split()
        clause.pop(-1)
        clauses.append(clause)

    return n_variables, n_clauses, clauses

n_vars, n_clauses, clauses = parse_clauses(file)

print('The file contains {} variables and {} clauses'.format(n_vars, n_clauses))
print(clauses)

