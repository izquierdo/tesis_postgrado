import logging
from itertools import combinations, permutations

def rw_theory(query, views, t):
    """
    Generate and return the logical theory for query rewritings given an
    existing MCD theory for the query and views.
    """

    logging.info("[Generate RW theory]")

    rw_t = t.multicopy(len(query.body))

    add_clauses_C15(query, views, rw_t)
    add_clauses_C16(query, views, rw_t)
    add_clauses_C17(query, views, rw_t)

    add_clauses_C22(query, views, rw_t)

    return rw_t

def add_clauses_C15(query, views, t):
    """
    Description: Cover all goals
    Formula: \\/_{t=1}^m g_j^t for 1 <= j <= m
    """

    logging.debug("adding clauses of type C15")

    m = len(query.body)

    for (j, g) in enumerate(query.body, 1):
        clause = [t.vs['g', j, copy] for copy in xrange(m)]
        t.add_clause(clause)

def add_clauses_C16(query, views, t):
    """
    Description: Disjunctive covering
    Formula: g_j^t => -g_j^s for 1 <= s != t <= m
    """

    logging.debug("adding clauses of type C16")

    m = len(query.body)

    for (j, g) in enumerate(query.body, 1):
        for (si, ti) in combinations(xrange(m), r=2):
            clause = [-t.vs['g', j, ti], -t.vs['g', j, si]]
            t.add_clause(clause)

def add_clauses_C17(query, views, t):
    """
    Description: Symmetries
    Formula: g_j^t => \\/_{j=1}^{i-1} g_j^{t-1} for 1 <= i, t <= m
    """

    logging.debug("adding clauses of type C17")

    m = len(query.body)

    for (i, g) in enumerate(query.body, 1):
        for ti in xrange(1, m):
            lower = [t.vs.get('g', j, ti-1) for j in xrange(1, i)]
            clause = [-t.vs['g', i, ti]] + lower
            t.add_clause(clause)

def add_clauses_C22(query, views, t):
    """
    Description: Direct incosistency 4
    Formula: t_{x,A}^i => -t_{x,B}^j if A, B constants and i != j
    """

    logging.debug("adding clauses of type C22")

    m = len(query.body)

    allconsts = set()

    for v in views:
        allconsts.update(v.constset())

    for x in query.varset():
        for A, B in combinations(allconsts, r=2):
            for i, j in permutations(xrange(m), r=2):
                t.add_clause([-t.vs.get('t', x, A, i),
                             -t.vs.get('t', x, B, j)])

            for i in xrange(m):
                t.add_clause([-t.vs.get('t', x, A, i),
                             -t.vs.get('t', x, B, i)])
