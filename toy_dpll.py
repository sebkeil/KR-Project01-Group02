
import sys

import time

from dimacs_reader import get_atoms, parse_clauses

from heuristic import moms_heuristic

class NotSatisfiable(Exception):
    def __init__(self, msg):
        super().__init__(msg)      # calls init of inherited class

#most_occuring = moms_heuristic(atoms, k=2, clauses=clauses)
#print("Most Heuristic Choice: {}".format(most_occuring))


def remove_clauses_and_literals(clauses, literal):
    for clause in clauses[:]:       #  do not modify list while looping over it! -> make copy
        if literal in clause:
            clauses.remove(clause)
        elif -literal in clause:
            clause.remove(-literal)
    return clauses

def DPLL(clauses, heuristic=None):
    #print("DPLL receives clauses: {}".format(clauses))
    #print("--------------------------------")
    if clauses == []:
        print("Problem is SAT.  ")
        solution = sorted([assignment for assignment in assignments if assignment > 0])
        print("Solution: {}".format(solution))
        print(len(solution))
        return True
    elif [] in clauses:
        if atoms[iters[-1]] != atoms[-1]:
            print("{} did not work. Reversing value last assignment...".format(atoms[iters[-1]]))
            try:
                clauses.remove([])
                assignments.append(-atoms[iters[-1]])
                clauses.append([-atoms[iters[-1]]])
                DPLL(clauses)
            except NotSatisfiable:
                print("Problem is UNSAT!")
        else:
            raise NotSatisfiable("Problem is UNSAT")
    elif any(len(clause) == 1 for clause in clauses):
        for clause in clauses:
            if len(clause) == 1:
                literal = clause[0]
                if literal not in assignments and -literal not in assignments:
                    print("Appended {} to assignments.".format(literal))
                    print("--------------------------------")
                    assignments.append(literal)
                clauses = remove_clauses_and_literals(clauses, literal)
                #print("Clauses after removal: {}".format(clauses))
                #print("--------------------------------")
                DPLL(clauses)
    elif all(len(clause) > 1 for clause in clauses):
        #print("i VALUE before try = {}".format(iters))
        #print("--------------------------------")
        #while atoms[iters[-1]] not in assignments and -atoms[iters[-1]] not in assignments:
        branched_atom = atoms[iters[-1]]
        if branched_atom not in assignments and -branched_atom not in assignments:
            assignments.append(branched_atom)
            print("Appended {} to assignments. Current assignments are {}".format(branched_atom, assignments))
            print("--------------------------------")
        try:
            if heuristic=='mom':
                chosen_literal = moms_heuristic(atoms, k=2, clauses=clauses)
                print("Appended {} to the clauses based on MOMs heuristic.".format(chosen_literal))
                clauses.append([chosen_literal])
            else:
                clauses.append([atoms[iters[-1]]])
                print("Appended {} to the clauses.".format(branched_atom))
                print("--------------------------------")
        except NotSatisfiable:      # this part becomes unnecessary
            negated_atom = -branched_atom
            print("Removed {} from the clauses.".format(branched_atom))
            print("Appended {} to the clauses.".format(negated_atom))
            print("--------------------------------")
            assignments.remove(branched_atom)
            clauses.append(negated_atom)
        finally:
            iters.append(iters[-1] + 1)
            DPLL(clauses)


if __name__ == '__main__':
    file = open('practice_file8.txt', 'r')  # sudoku_test01.txt
    clauses = parse_clauses(file)
    atoms, flat_literals = get_atoms(clauses)

    sys.setrecursionlimit(10 ** 9)

    print("Atoms for this problem: {}".format(atoms))
    print("--------------------------------")
    print("--------------------------------")

    assignments = []
    iters = [0]  # catches the iterations
    backtracks = 0

    start = time.time()
    sat = DPLL(clauses, heuristic='mom')
    end = time.time()
    duration = round(end-start,4)
    print('The Algorithm took {} seconds to solve this problem.'.format(duration))

