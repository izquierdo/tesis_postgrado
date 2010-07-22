import collections
import cPickle
import logging

import options

class VariableSet:
    def __init__(self):
        self._vars = collections.defaultdict(self._id_generator().next)
        self._reverse = {}

    def _id_generator(self):
        id = 0

        while True:
            id += 1
            yield id

    def __contains__(self, item):
        return item in self._vars

    def __getitem__(self, key):
        val = self._vars[key]

        if val not in self._reverse:
            self._reverse[val] = key

        return val
    
    def __len__(self):
        return len(self._vars)

    def __iter__(self):
        return self._vars.iterkeys()

    def by_type(self, t):
        """
        The type of a variable is the value of its first element.
        """

        return [v for v in self._vars.iterkeys() if v[0] == t]

    def reverse(self, val):
        if val < 0:
            return "-" + str(self._reverse[abs(val)])

        return str(self._reverse[val])

    def get(self, *args):
        return self._vars.get(args)

class Theory:
    def __init__(self):
        self.vs = VariableSet()
        self._clauses = collections.defaultdict(list)

    def add_clause(self, clause, type = None, weight = 0):
        """
        Add a clause to this theory, optionally specifying its weight.

        If an element of clause isn't in the variable set (vs), LookupError is
        raised. If clause contains None, then the clause is silently discarded.
        """

        for v in clause:
            if abs(v) < 1 or abs(v) > len(self.vs):
                raise LookupError

        if None in clause:
            # fail silently
            return

        if options.debug:
            logging.debug(map(lambda e : self.vs.reverse(e), clause))

        self._clauses[type].append(clause)

    def clauses(self, type):
        return self._clauses[type]

    def all_clauses(self):
        clauses = [c for cl in self._clauses.itervalues() for c in cl]
        return clauses

    def write_unweighted_cnf(self, file):
        """
        Write the unweighted theory to a file-like object in the DIMACS CNF
        format.
        """

        varn = len(self.vs)

        clauses = self.all_clauses()
        clsn = len(clauses)

        print >> file, "p cnf {vars} {clauses}".format(vars=varn, clauses=clsn)

        for clause in clauses:
            print >> file, "{clause} 0".format(clause=" ".join(map(str,clause)))

    def write_weighted_cnf(self, file):
        pass

def import_theory(file):
    return cPickle.load(file)

def export_theory(theory, file):
    cPickle.dump(theory, file)
