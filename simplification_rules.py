
# if a clause contains (P or -P) it can be removed
def check_tautology(clause):
    pass

# if there is a pure literal (occurring only positive or negative)
def check_pure_literal(clause):
    pass

# if there is a unit clause (consisting of only one literal), that literal can be set to true
def check_unit_clause(clause):
    pass

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

