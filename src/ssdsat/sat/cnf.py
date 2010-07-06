import collections
import cPickle

class VariableSet:
    def __init__(self):
        self._vars = collections.defaultdict(self._id_generator().next)

    def _id_generator(self):
        id = 0

        while True:
            id += 1
            yield id

    def __contains__(self, item):
        return item in self._vars

    def __getitem__(self, key):
        return self._vars[key]
    
    def __len__(self):
        return len(self._vars)

class Theory:
    def __init__(self):
        self.vars = VariableSet()
        self._clauses = collections.defaultdict(list)

    def add_clause(self, clause, type = None):
        for v in clause:
            if v < 1 or v > len(self.vars):
                raise LookupError

        self._clauses[type].append(clause)

    def clauses(self, type):
        return self._clauses[type]

    def all_clauses(self):
        clauses = [c for clause_list in self._clauses for c in clause_list]
        return clauses

    def write_unweighted_cnf(self, file):
        """
        Write the unweighted theory to a file-like object in the DIMACS CNF
        format.
        """

        varn = len(self.vars)

        clauses = self.clauses()
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
