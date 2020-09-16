# another sudoku heuristic which I assume works quite well. Because any assignments will always eliminate some units from some
# clauses, clauses with unit literals will always appear. These are then inserted to the top of the list of variables to inspect.
# Because the initial assignments are already given for sudoku, this heuristic should work without any backtracking at all
def sudoku_heuristic(variables, clauses):
    clauses.sort(key=len)
    n = 0
    while len(getLiterals(clauses[n])) == 1:
        literals = getLiterals(clauses[n])
        if literals[0] in variables:
            variables.remove(literals[0])
        if -literals[0] in variables:
            variables.remove(-literals[0])
        variables.insert(0, literals[0])
        n += 1
    return variables
