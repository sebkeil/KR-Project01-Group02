class heuristic:
    def __init__(self, lit: int, ratio: float):
        self.lit = lit
        self.ratio = ratio

    def __repr__(self):
        return 'literal = ' + str(self.lit) + ', ratio = ' + str(self.ratio)


# the idea of this heuristic is to rank literals based on the ratio of their polarity count
def heuristic_polarityRatio(absVarbs, varbs, varbCount): # absVarbs  = list of literals, disregarding polarity
    assignmentsRanked = []                               # varbs     = list of literals with polarity
    for varb in absVarbs:                                # varbCount = count of literals wrt. to polarity
        posVarbCount = varbCount[varbs.index(varb)]
        negVarbCount = varbCount[varbs.index(-varb)]
        if posVarbCount >= negVarbCount:
            varbRatio = posVarbCount / negVarbCount
            varbPol = varb
        else:
            varbRatio = negVarbCount / posVarbCount
            varbPol = -varb

        assignmentsRanked.append(heuristic(varbPol, varbRatio))

    return assignmentsRanked



atoms = [1,2,3,4,5,6]
clauses = [[-1,2], [1,5], [2,3,1], [3,1], [3,4,6]]

def f(clauses, literal):
    smallest_clauses_size = len(min(clauses, key=len))
    number_of_occurances = 0
    for clause in clauses:
        if len(clause) == smallest_clauses_size:
            if literal in clause or -literal in clause:
                number_of_occurances += 1
    return number_of_occurances


def moms_heuristic(atoms, k, clauses):  # atoms = argments?, k=2
    max_val = 0
    chosen_literal = None
    for atom in atoms:
        function_res = (f(clauses, atom) + f(clauses, -atom))*2**k + f(clauses, atom) * f(clauses, -atom)
        if function_res > max_val:
            max_val = function_res
            chosen_literal = atom
    return chosen_literal


most = moms_heuristic(atoms, k=2, clauses=clauses)
print(most)

