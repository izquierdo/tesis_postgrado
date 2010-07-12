"""
* Types of variables generated:
    - ["v", i] -- view i is used
    - ["g", i] -- goal i is covered by a view in use
    - ["z", j, k, i] -- goal j in the query is covered by goal k of view i
    - ["t", x, y, i] -- there's a mapping between variable x of the query and
      variable y of view i

* Types of clauses ge

n: number of views
m: number of query goals
"""

import logging

from sat.cnf import Theory
from itertools import combinations

def mcd_theory(query, views):
    """
    Generate and return the logical theory for an MCD given a query and a
    list of views.
    """

    logging.debug("generating MCD theory")

    t = Theory()

    add_clauses_C1(query, views, t)
    add_clauses_C2(query, views, t)
    add_clauses_C3(query, views, t)
    add_clauses_C4(query, views, t)
    add_clauses_C5(query, views, t)
    add_clauses_C6(query, views, t)
    add_clauses_C7(query, views, t)
    add_clauses_C8(query, views, t)
    add_clauses_C9(query, views, t)
    add_clauses_C10(query, views, t)
    add_clauses_C11(query, views, t)
    add_clauses_C12(query, views, t)

    return t

def mcd_from_model(t):
    """
    """

def add_clauses_C1(query, views, t):
    """
    Description: At least one view is used
    Formula: \/_{i=0}^n (v_i)
    """

    logging.debug("adding clauses of type C1")

    t.add_clause([t.vs["v", i] for i in xrange(0, len(views)+1)])

def add_clauses_C2(query, views, t):
    """
    Description: At most one view is used
    Formula: v_i => -v_j for 0 <= i, j <= n
    """

    logging.debug("adding clauses of type C2")

    for i, j in combinations(xrange(0, len(views)+1), r=2):
        t.add_clause([-t.vs["v", i], -t.vs["v", j]])

def add_clauses_C3(query, views, t):
    """
    Description: Null view equals null
    Formula: v_0 => -g_j for 1 <= j <= m
    """

    logging.debug("adding clauses of type C3")

    for i in xrange(len(query.body)):
        clause = [-t.vs["v", 0], -t.vs["g", i+1]]
        t.add_clause(clause)

def add_clauses_C4(query, views, t):
    """
    Description: Views are useful
    Formula: v_i => \/_{j=0}^m (g_j) for 1 <= i <= n
    """

    logging.debug("adding clauses of type C4")

    for i in xrange(1, len(views)+1):
        or_gs = [t.vs["g", j+1] for j in xrange(len(query.body))]
        clause = [-t.vs["v", i]] + or_gs
        t.add_clause(clause)

def add_clauses_C5(query, views, t):
    """
    Description: Subgoals are covered at most once
    Formula: z_{j,k,i} => -z_{j,l,i} for appropriate i, j, k, l with k != l
    """

    logging.debug("adding clauses of type C5")

    for j in xrange(1, len(query.body)+1):
        for (i, v) in enumerate(views, 1):
            for k, l in combinations(xrange(1, len(v.body)+1), r=2):
                clause = [-t.vs["z", j, k, i], -t.vs["z", j, l, i]]
                t.add_clause(clause)

def add_clauses_C6(query, views, t):
    """
    Description: Scope of views
    Formula: v_i => -g_j if query goal j can't be covered by view i
    """

    logging.debug("adding clauses of type C6")

    for (j, query_p) in enumerate(query.body, 1):
        for (i, v) in enumerate(views, 1):
            #TODO use Predicate.unify here instead
            can_cover = False

            for p in v.body:
                if p.name == query_p.name and p.arity == query_p.arity:
                    can_cover = True
                    break

            if not can_cover:
                clause = [-t.vs["v", i], -t.vs["g", j]]
                t.add_clause(clause)

def add_clauses_C7(query, views, t):
    """
    Description: Consistency
    Formula: v_i /\\ g_j <=> \\/ z_{j,k,i} for appropriate i, j, k
    """

    logging.debug("adding clauses of type C7")

    for (i, v) in enumerate(views, 1):
        for j in xrange(1, len(query.body)+1):
            or_zs = [t.vs["z", j, k, i] for k in xrange(1, len(v.body)+1)]
            imply_clause = [-t.vs["v", i], -t.vs["g", j]] + or_zs
            t.add_clause(imply_clause)

            for k in xrange(1, len(v.body)+1):
                view_clause = [-t.vs["z", j, k, i], t.vs["v", i]]
                t.add_clause(view_clause)

                goal_clause = [-t.vs["z", j, k, i], t.vs["g", j]]
                t.add_clause(goal_clause)

def add_clauses_C8(query, views, t):
    """
    Description: Dead variables
    Formula: v_i => -t_{x,y} for all x, y with y not in view i
    """

    logging.debug("adding clauses of type C8")

    print "UNIMPLEMENTED!!!"
    pass

def add_clauses_C9(query, views, t):
    """
    Description: Head homomorphism
    Formula: v_i /\\ t_{x,y} => -t{x,yp} for all existential y, yp in view i
    """

    logging.debug("adding clauses of type C9")

    for x in query.varset():
        for (i, v) in enumerate(views, 1):
            for y, yp in combinations(v.varset(), r=2):
                if v.is_existential(y) and v.is_existential(yp):
                    or_ts =  [-t.vs["t", x, y, i], -t.vs["t", x, yp, i]]
                    clause = [-t.vs["v", i]] + or_ts
                    t.add_clause(clause)

def add_clauses_C10(query, views, t):
    """
    Description: Distinguished
    Formula: v_i => -t_{x,y} for x distinguished in the query and y existential
    in view i
    """

    logging.debug("adding clauses of type C10")

    for (i, v) in enumerate(views, 1):
        for y in v.varset():
            if not v.is_existential(y):
                continue

            for x in query.varset():
                if query.is_existential(x):
                    continue

            clause = [-t.vs["v", i], -t.vs["t", x, y, i]]
            t.add_clause(clause)

def add_clauses_C11(query, views, t):
    """
    Description: Existential
    Formula: v_i /\\ t_{x,y} => g_j for existential y in view i and goals j
    that contain existential x in the query
    """

    logging.debug("adding clauses of type C11")

    for (i, v) in enumerate(views, 1):
        for y in v.varset():
            if not v.is_existential(y):
                continue

            for x in query.varset():
                if not query.is_existential(x):
                    continue

                for (j, g) in enumerate(query.body, 1):
                    if x not in g.arguments:
                        continue

                    clause = [-t.vs["v", i], -t.vs["t", x, y, i], t.vs["g", j]]
                    t.add_clause(clause)

def add_clauses_C12(query, views, t):
    """
    Description: Matching
    Formula: v_i /\\ z_{j,k,i} => t_{x,y} for x and y that must match if goal j
    in the query is covered by goal k in view i
    """

    logging.debug("adding clauses of type C12")

    for (i, v) in enumerate(views, 1):
        for (k, p) in enumerate(v.body, 1):
            for (j, g) in enumerate(query.body, 1):
                mapping = g.unify(p)

                if not mapping:
                    continue

                for (x, y) in mapping:
                    clause = [-t.vs["v", i], -t.vs["z", j, k, i], t.vs["t", x, y, i]]
                    t.add_clause(clause)
