from sat.cnf import Theory
from itertools import product

def mcd_theory(query, views):
    t = Theory()

    add_clauses_C1(query, views, t)
    add_clauses_C2(query, views, t)
    add_clauses_C3(query, views, t)
    add_clauses_C4(query, views, t)

    return t

def add_clauses_C1(query, views, t):
    """
    Description: At least one view is used
    Formula: \/_{i=0}^n (v_i)
    """

    t.add_clause([t.vs["v", i] for i in xrange(0, len(views)+1)])

def add_clauses_C2(query, views, t):
    for i, j in product(xrange(0, len(views)+1), repeat=2):
        if i != j:
            t.add_clause([-t.vs["v", i], -t.vs["v", j]])

def add_clauses_C3(query, views, t):
    for i in xrange(len(query.body)):
        clause = [t.vs["v", 0], -t.vs["g", i+1]]
        t.add_clause(clause)

def add_clauses_C4(query, views, t):
    """
    Description: Views are useful
    Formula: v_i => \/_{j=0}^m (g_j) for 1 <= i <= n
    """

    for i in xrange(1, len(views)+1):
        clause = [t.vs["v", i]] + [t.vs["g", j+1] for j in xrange(len(query.body))]
        t.add_clause(clause)
