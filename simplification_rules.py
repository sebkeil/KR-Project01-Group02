from dimacs_reader import get_variables


# if a clause contains (P or -P) it can be removed
def check_tautology(clauses):
    initial_len = len(clauses)
    for clause in clauses:
        for literal in clause:
            if -literal in clause:
                clauses.remove(clause)
    updated_len = len(clauses)
    removed_count = initial_len - updated_len
    print("{} Tautologies have been removed".format(removed_count))
    return clauses


# if there is a pure literal (occurring only positive or negative), it can be set to true (or false)
def check_pure_literal(clauses, assignments):
    variables, flat_literals = get_variables(clauses)
    assignment_counter = 0
    for clause in clauses:
        for literal in clause:
            if literal not in assignments and -literal not in flat_literals:
                assignments.append(literal)
                assignment_counter += 1
                print('{} is a pure literal and has been added to the assignments')
    if assignment_counter == 0:
        print('There are no pure literals.')
    return assignments

# if there is a unit clause (consisting of only one literal), that literal can be set to true
def check_unit_clause(clauses, assignments):
    assignment_counter = 0
    for clause in clauses:
        if len(clause) == 1:
            assignments.append(clause[0])
            print("{} is a unit clause and has been assigned ")
    if assignment_counter == 0:
        print('There are no unit clauses.')
    return assignments

#If literal L1 is true, then clause (L1 V L2 ...) is true
#If clause C1 is true, then C1 ^ C2 ^ C3... has the same value as C2 ^ C3 ^ ...
def check_clause_containing_true_literals(clause):
    # if True:
        # delete this clause
    pass

# if L1 is false, then clause (L1 v L2 v L3...) has the same value as (L2 v L3...)
def check_clause_containing_false_literals(clause):
    # if True:
        # shorten clause
    pass

# empty clause means false
def check_empty_clause(clause):
    pass

