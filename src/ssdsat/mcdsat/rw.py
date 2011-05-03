import logging
from itertools import combinations, permutations

def rw_theory(query, views, t):
    """
    Generate and return the logical theory for query rewritings given an
    existing MCD theory for the query and views.
    """

    logging.info("[Generate RW theory]")
    global m
    m = len(query.body)
    rw_t = t.multicopy(m)

    add_clauses_C15(query, views, rw_t)
    add_clauses_C16(query, views, rw_t)
    add_clauses_C17(query, views, rw_t)

    #add_clauses_C23(query, views, rw_t)
    #add_clauses_C24(query, views, rw_t)
    #add_clauses_I6(query, views, rw_t)
    #add_clauses_I7(query, views, rw_t)
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
    Formula: t_{x,A}^i => -t_{x,B}^j if A, B constants
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

def add_clauses_C23(query, views, t):
    """
    Description: Transitivity 3
    Formula: t_{y,A,i}^w0 /\\ t_{y,x,j}^w1 /\\ t_{z,x,j}^w1 => t_{z,A,i}^w0, for y, z variables in the query,
             and x variable in view j, 0 <= w0, w1 < m.
    """

    logging.debug("adding clauses of type C23")

    updated = True

    while updated:
        updated = False
        for (i, vi) in enumerate(views, 1):
          for A in vi.constset():
            for (j, vj) in enumerate(views, 1):
              for y in query.varset():
                for z in query.varset():
                  if z == y:
                    continue
                  for x in vj.varset():
                          for w0, w1 in permutations(xrange(m), r=2):
                            if t.vs.get('t',y,A,w0) and t.vs.get('t',y,x,w1) and t.vs.get('t',z,x,w1): # i, j, j
                                if not ('t', z, A, w0) in t.vs: # i
                                    updated = True                                
                                clause = [-t.vs.get('t', y, A, w0), # i
                                          -t.vs.get('t', y, x, w1), # j
                                          -t.vs.get('t', z, x, w1), # j
                                           t.vs['t', z, A, w0]]     # i
                                if not clause in t.all_clauses():
                                    t.add_clause(clause)

def add_clauses_C24(query, views, t):
    """
    Description: Transitivity 4
    Formula: t_{A,y,i}^w0 /\\ t_{x,y,i}^w0 /\\ t_{x,z,j}^w1 => t_{A,z,j}^w1, for x variable in the query,
             and y,z variables in views i and j, 0 <= w0, w1 < m.
    """

    logging.debug("adding clauses of type C24")
    logging.debug(t.vs.by_type('t'))
    updated = True

    while updated:
        updated = False
        for A in query.constset():
            for (i, vi) in enumerate(views, 1):
              for (j, vj) in enumerate(views, 1):
                for x in query.varset():
                  for y in vi.argset():
                    
                    for z in vj.argset():
                       if y == z:
                         continue
                       for w0, w1 in permutations(xrange(m), r=2):
                          if t.vs.get('t',A,y,w0) and t.vs.get('t',x,y,w0) and t.vs.get('t',x,z,w1): # i, i, j
                                if not ('t', A, z, w1) in t.vs: # j
                                    updated = True                                
                                clause = [-t.vs.get('t', A, y, w0), # i
                                          -t.vs.get('t', x, y, w0), # i
                                          -t.vs.get('t', x, z, w1), # j
                                           t.vs['t', A, z, w1]]     # j
                                if not clause in t.all_clauses():
                                    t.add_clause(clause)

def add_clauses_I6(query, views, t):
    """
    Description: Transitivity 3
    Formula: t_{w,y,i}^w0 /\\ t_{x,y,i}^w0 /\\ t_{x,z,j}^w1 => t_{w,z,j}^w1, for w, x variables in the query,
             and y, z variables in views i and j, 0 <= w0, w1 < m.
    """

    logging.debug("adding clauses of type I6")

    updated = True

    while updated:
        updated = False

        for (i, vi) in enumerate(views, 1):
          for (j, vj) in enumerate(views, 1):
            for w in query.varset():
                for x in query.varset():
                    for y in vi.argset():
                        for z in vj.argset():
                          if y == z:
                            continue
                          for w0, w1 in permutations(xrange(m), r=2):
                            if t.vs.get('t',w,y,w0) and t.vs.get('t',x,y,w0) and t.vs.get('t',x,z,w1):# i, i, j
                                if not ('t', w, z,w1) in t.vs: # j
                                    updated = True                                
                                clause = [-t.vs.get('t', w, y, w0), #i
                                          -t.vs.get('t', x, y, w0), #i
                                          -t.vs.get('t', x, z, w1), #j
                                           t.vs['t', w, z, w1]]     #j
                                if not clause in t.all_clauses():
                                    t.add_clause(clause)


def add_clauses_I7(query, views, t):
    """
    Description: Transitivity 4
    Formula: t_{y,w,i}^w0 /\\ t_{y,x,j}^w1 /\\ t_{z,x,j}^w1 => t_{z,w,i}^w0, for y, z variables in the query,
             and x, w variables in views j and i, 0 <= w0, w1 < m.
    """

    logging.debug("adding clauses of type I7")

    updated = True

    while updated:
        updated = False

        for (i, vi) in enumerate(views, 1):
          for (j, vj) in enumerate(views, 1):
            for w in vi.argset():
                for x in vj.argset():
                    for y in query.varset():
                        for z in query.varset():
                            if y == z:
                                continue
                            for w0, w1 in permutations(xrange(m), r=2):
                              if t.vs.get('t',y,w,w0) and t.vs.get('t',y,x,w1) and t.vs.get('t',z,x,w1): # i, j, j
                                  if not ('t', z, w, w0) in t.vs: # i
                                      updated = True                                
                                  clause = [-t.vs.get('t', y, w, w0),  # i
                                            -t.vs.get('t', y, x, w1), # j
                                            -t.vs.get('t', z, x, w1),  # j
                                            t.vs['t', z, w, w0]]       # i
                                  if not clause in t.all_clauses():
                                      t.add_clause(clause)


