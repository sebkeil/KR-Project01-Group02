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



def mom_heuristic(flat_literals):
    positive_literals = [literal for literal in flat_literals if literal > 0]
    most_occuring_literal = max(set(positive_literals), key=positive_literals.count)
    return most_occuring_literal
