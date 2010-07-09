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

from sat.cnf import Theory
from itertools import combinations

def mcd_theory(query, views):
    t = Theory()

    add_clauses_C1(query, views, t)
    add_clauses_C2(query, views, t)
    add_clauses_C3(query, views, t)
    add_clauses_C4(query, views, t)
    add_clauses_C5(query, views, t)
    add_clauses_C6(query, views, t)

    return t

def add_clauses_C1(query, views, t):
    """
    Description: At least one view is used
    Formula: \/_{i=0}^n (v_i)
    """

    t.add_clause([t.vs["v", i] for i in xrange(0, len(views)+1)])

def add_clauses_C2(query, views, t):
    """
    Description: At most one view is used
    Formula: v_i => -v_j for 0 <= i, j <= n
    """

    for i, j in combinations(xrange(0, len(views)+1), r=2):
        t.add_clause([-t.vs["v", i], -t.vs["v", j]])

def add_clauses_C3(query, views, t):
    """
    Description: Null view equals null
    Formula: v_0 => -g_j for 1 <= j <= m
    """

    for i in xrange(len(query.body)):
        clause = [t.vs["v", 0], -t.vs["g", i+1]]
        t.add_clause(clause)

def add_clauses_C4(query, views, t):
    """
    Description: Views are useful
    Formula: v_i => \/_{j=0}^m (g_j) for 1 <= i <= n
    """

    for i in xrange(1, len(views)+1):
        clause = [-t.vs["v", i]] + [t.vs["g", j+1] for j in xrange(len(query.body))]
        t.add_clause(clause)

def add_clauses_C5(query, views, t):
    """
    Description: Subgoals are covered at most once
    Formula: z_{j,k,i} => -z_{j,l,i} for appropriate i, j, k, l with k != l
    """

    for j in xrange(1, len(query.body)+1):
        for (i, v) in enumerate(views):
            for k, l in combinations(xrange(1, len(v.body)+1), r=2):
                clause = [-t.vs["z", j, k, i+1], -t.vs["z", j, l, i+1]]
                t.add_clause(clause)

def add_clauses_C6(query, views, t):
    """
    Description: Scope of views
    Formula: v_i => -g_j if query goal j can't be covered by view i
    """

    for (j, query_pred) in enumerate(query.body):
        for (i, v) in enumerate(views):
            can_cover = False

            for view_pred in v.body:
                if view_pred.name == query_pred.name and view_pred.arity == query_pred.arity:
                    can_cover = True
                    break

            if not can_cover:
                print "can't cover with view %d the goal %d" % (i+1, j+1)
                clause = [-t.vs["v", i+1], -t.vs["g", j+1]]
                t.add_clause(clause)
