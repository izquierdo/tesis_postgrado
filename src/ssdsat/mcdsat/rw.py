import logging
from itertools import combinations

def rw_theory(query, views, t):
    """
    Generate and return the logical theory for query rewritings given an
    existing MCD theory for the query and views.
    """

    logging.debug("generating RW theory")

    rw_t = t.multicopy(len(query.body))

    add_clauses_C15(query, views, rw_t)
    add_clauses_C16(query, views, rw_t)
    add_clauses_C17(query, views, rw_t)

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
