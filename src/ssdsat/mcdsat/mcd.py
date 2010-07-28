"""
* Types of variables generated:
    - ['v', i] -- view i is used
    - ['g', i] -- goal i is covered by a view in use
    - ['z', j, k, i] -- goal j in the query is covered by goal k of view i
    - ['t', x, y, i] -- there's a mapping between variable x of the query and
      variable y of view i

* Types of clauses ge

n: number of views
m: number of query goals
"""

#TODO check usage of varset when argset is intended!

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
    add_clauses_C9(query, views, t)
    add_clauses_C10(query, views, t)
    add_clauses_C11(query, views, t)
    add_clauses_C12(query, views, t)
    add_clauses_C13(query, views, t)
    add_clauses_C14(query, views, t)

    # C8 clauses are dependent on existing 't' variables
    add_clauses_C8(query, views, t)

    # extra clauses (not appearing in the McdSat paper)
    add_clauses_E1(query, views, t)
    add_clauses_E2(query, views, t)

    # clauses for constant handling
    add_clauses_D1(query, views, t)
    add_clauses_D2(query, views, t)
    add_clauses_D3(query, views, t)

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

    t.add_clause([t.vs['v', i] for i in xrange(0, len(views)+1)])

def add_clauses_C2(query, views, t):
    """
    Description: At most one view is used
    Formula: v_i => -v_j for 0 <= i, j <= n
    """

    logging.debug("adding clauses of type C2")

    for i, j in combinations(xrange(0, len(views)+1), r=2):
        t.add_clause([-t.vs['v', i], -t.vs['v', j]])

def add_clauses_C3(query, views, t):
    """
    Description: Null view equals null
    Formula: v_0 => -g_j for 1 <= j <= m
    """

    logging.debug("adding clauses of type C3")

    for i in xrange(len(query.body)):
        clause = [-t.vs['v', 0], -t.vs['g', i+1]]
        t.add_clause(clause)

def add_clauses_C4(query, views, t):
    """
    Description: Views are useful
    Formula: v_i => \/_{j=0}^m (g_j) for 1 <= i <= n
    """

    logging.debug("adding clauses of type C4")

    for i in xrange(1, len(views)+1):
        or_gs = [t.vs['g', j+1] for j in xrange(len(query.body))]
        clause = [-t.vs['v', i]] + or_gs
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
                clause = [-t.vs['z', j, k, i], -t.vs['z', j, l, i]]
                t.add_clause(clause)

def add_clauses_C6(query, views, t):
    """
    Description: Scope of views
    Formula: v_i => -g_j if query goal j can't be covered by view i
    """

    logging.debug("adding clauses of type C6")

    for (j, query_p) in enumerate(query.body, 1):
        for (i, v) in enumerate(views, 1):
            can_cover = False

            for p in v.body:
                mapping = query_p.unify(p)

                if mapping is None:
                    continue

                # for now, we know we can cover this goal (pending
                # the distinguished/existential checks)
                can_cover = True

                for (x, y) in mapping:
                    if query.is_distinguished(x) and v.is_existential(y):
                        # we can't cover this query goal with this view goal
                        can_cover = False
                        break

                if can_cover:
                    # found a view goal with which we can cover the query goal
                    break

            if not can_cover:
                clause = [-t.vs['v', i], -t.vs['g', j]]
                t.add_clause(clause)

def add_clauses_C7(query, views, t):
    """
    Description: Consistency
    Formula: v_i /\\ g_j <=> \\/ z_{j,k,i} for appropriate i, j, k
    """

    logging.debug("adding clauses of type C7")

    for (i, v) in enumerate(views, 1):
        for j in xrange(1, len(query.body)+1):
            or_zs = [t.vs['z', j, k, i] for k in xrange(1, len(v.body)+1)]
            imply_clause = [-t.vs['v', i], -t.vs['g', j]] + or_zs
            t.add_clause(imply_clause)

            for k in xrange(1, len(v.body)+1):
                view_clause = [-t.vs['z', j, k, i], t.vs['v', i]]
                t.add_clause(view_clause)

                goal_clause = [-t.vs['z', j, k, i], t.vs['g', j]]
                t.add_clause(goal_clause)

def add_clauses_C8(query, views, t):
    """
    Description: Dead variables
    Formula: v_i => -t_{x,y} for all x, y with y not in view i
    """

    logging.debug("adding clauses of type C8")

    for var in t.vs.by_type('t'):
        for i in xrange(len(views)+1):
            if i == var[-1]:
                # this is a mapping used for view i
                continue

            clause = [-t.vs['v', i], -t.vs[var]]
            t.add_clause(clause)

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
                    or_ts =  [-t.vs['t', x, y, i], -t.vs['t', x, yp, i]]
                    clause = [-t.vs['v', i]] + or_ts
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

            clause = [-t.vs['v', i], -t.vs['t', x, y, i]]
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

                    clause = [-t.vs['v', i], -t.vs['t', x, y, i], t.vs['g', j]]
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

                if mapping:
                    for (x, y) in mapping:
                        clause = [-t.vs['v', i], -t.vs['z', j, k, i], t.vs['t', x, y, i]]
                        t.add_clause(clause)
                else:
                    clause = [-t.vs['v', i], -t.vs['z', j, k, i]]
                    t.add_clause(clause)

def add_clauses_C13(query, views, t):
    """
    Description: 1-1 on existential vars
    Formula: v_i /\\ t_{x,y} => -t_{xp,y} for x existential in the query, xp
    in the query and y in view i
    """

    logging.debug("adding clauses of type C13")

    for (i, v) in enumerate(views, 1):
        for x in query.varset():
            if not query.is_existential(x):
                continue

            for xp in query.varset():
                if x == xp:
                    continue

                for y in v.varset():
                    clause = [-t.vs['v', i], -t.vs['t', x, y, i],
                            -t.vs['t', xp, y, i]]
                    t.add_clause(clause)


def add_clauses_C14(query, views, t):
    """
    Description: If the view has no existential variables, the MCD covers at
    most one goal.
    Formula: v_i /\\ g_j => -g_k if v_i has no existential variables
    """

    logging.debug("adding clauses of type C14")

    for (i, v) in enumerate(views, 1):
        if len(v.existential_varset()) == 0:
            for j, k in combinations(xrange(1, len(query.body)+1), r=2):
                clause = [-t.vs['v', i], -t.vs['g', j], -t.vs['g', k]]
                t.add_clause(clause)

def add_clauses_E1(query, views, t):
    """
    Description: Remove unnecesary mappings
    Formula: t_{x,y} /\\ v_i => (\/ z_{j,k,i} for j, k where mapping t_{x,y} is
    needed)
    """

    logging.debug("adding clauses of type E1")

    needed = {}

    for (i, v) in enumerate(views, 1):
        for (k, p) in enumerate(v.body, 1):
            for (j, g) in enumerate(query.body, 1):
                mapping = g.unify(p)

                if mapping:
                    for (x, y) in mapping:
                        needed.setdefault((-t.vs['v', i], -t.vs['t', x, y, i]), []).append(t.vs['z', j, k, i])

    for ((v_var, t_var), z_vars) in needed.iteritems():
        t.add_clause([v_var, t_var] + z_vars)

def add_clauses_E2(query, views, t):
    """
    Description: Null view is useless
    Formula: -v_0
    """

    logging.debug("adding clauses of type E2")

    t.add_clause([-t.vs['v', 0]])



def add_clauses_D1(query, views, t):
    """
    Description: Direct inconsistency 1
    Formula: t_{x,A} => -t_{x,B} if A, B are constants
    """
    #TODO efficient implementation

    logging.debug("adding clauses of type D1")

    for (va, vb) in combinations(t.vs.by_type('t'), r=2):
        (xa, A, na) = (va[1], va[2], va[3])
        (xb, B, nb) = (vb[1], vb[2], vb[3])

        if xa == xb and na == nb and A.constant and B.constant and A != B:
            print va
            print vb
            clause = [-t.vs[va], -t.vs[vb]]
            t.add_clause(clause)

def add_clauses_D2(query, views, t):
    """
    Description: Direct inconsistency 2
    Formula: t_{A,x} => -t_{B,x} if A, B are constants
    """
    #TODO efficient implementation

    logging.debug("adding clauses of type D2")

    for (va, vb) in combinations(t.vs.by_type('t'), r=2):
        (A, xa, na) = (va[1], va[2], va[3])
        (B, xb, nb) = (vb[1], vb[2], vb[3])

        if xa == xb and na == nb and A.constant and B.constant and A != B:
            clause = [-t.vs[va], -t.vs[vb]]
            t.add_clause(clause)

def add_clauses_D3(query, views, t):
    """
    Description: Direct inconsistency 3
    Formula: -t_{A,B} if A, B are constants and A != B
    """
    #TODO efficient implementation

    logging.debug("adding clauses of type D3")

    for var in t.vs.by_type('t'):
        (A, B) = (var[1], var[2])

        if A.constant and B.constant and A != B:
            clause = [-t.vs[var]]
            t.add_clause(clause)

def add_clauses_D4(query, views, t):
    """
    Description: Transitivity 1
    Formula: t_{A,y} /\\ t_{x,y} /\\ t_{x,z} => t_{A,z} if A is a constant
    """

    #print "clausulas S4  v_i /\\ t_{A,y} /\\ t_{x,y} /\\ t_{x,z} => t_{A,z}"
    #pprint.pprint(d4)
    #print "clausulas S5  v_i /\\ t_{y,A} /\\ t_{y,x} /\\ t_{z,x} => t_{z,A}"
    #pprint.pprint(d5)
