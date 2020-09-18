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




  def MomsHeuristic(self, clauses):
    """MOMS variable ordering heuristic."""
    if not clauses: return None
    moms = {}
    max = 0
    max_lit = 0
    min_len = len(clauses[0])
    for i in xrange(len(clauses)):
      if len(clauses[i]) < min:
        min_len = len(clauses[i])
    for j in xrange(len(clauses)):
      # Increment for clauses with min len
      if len(clauses[j]) == min_len:
        for lit in clauses[j]:
          if lit in moms:
            moms[lit] += 1
          else:
            moms[lit] = 1
          if moms[lit] > max:
            max = moms[lit]
            max_lit = lit
    if max_lit == 0:
      raise Exception, "MOMS algorithm error"
    return max_lit
