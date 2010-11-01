import logging
from itertools import product
from tempfile import NamedTemporaryFile

from ply import lex, yacc

class Preference:
    def __init__(self, cost, formula):
        self.cost = cost
        self.formula = formula

    def __repr__(self):
        return "Preference({0}, {1})".format(self.cost, self.formula)

class Literal:
    def __init__(self, positive, name):
        self.positive = positive
        self.name = name

    def __repr__(self):
        if self.positive:
            return self.name

        return "-" + self.name

class UnknownNameError:
    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return "Unknown name '{0}'".format(self.name)

################################################################################
# Preference parsing
################################################################################

# Lexer

tokens = (
    "NAME",
    "NEG",
    "NEWLINE",
    "INTEGER",
)

t_INTEGER = r"-?\d+"
t_NAME = r"[a-z]\w*"
t_NEG = "-"
t_NEWLINE = r"\n"

t_ignore = ' \t'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

# Parser

def p_preference_list(p):
    """
    preference_list : preference_list preference
    """
    p[0] = p[1] + [p[2]]

def p_empty_preference_list(p):
    """
    preference_list :
    """
    p[0] = []

def p_preference(p):
    """
    preference : INTEGER literal_list NEWLINE
    """
    p[0] = Preference(int(p[1]), p[2])

def p_literal_list(p):
    """
    literal_list : literal_list literal 
    """
    p[0] = p[1] + [p[2]]

def p_single_literal_list(p):
    """
    literal_list : literal
    """
    p[0] = [p[1]]

def p_positive_literal(p):
    """
    literal : NAME
    """
    p[0] = Literal(True, p[1])

def p_negative_literal(p):
    """
    literal : NEG NAME
    """
    p[0] = Literal(False, p[2])

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=0)

# Helpers

def parse(file):
    return parser.parse(file.read(), lexer=lexer)

################################################################################
# Preference handling
################################################################################

def preference_cost_file(preflist, t, copies):
    if not preflist and preflist != []:
        return None

    with NamedTemporaryFile(prefix="ssdsat.", suffix=".costs", delete = False) as cost_file:
        cost_filename = cost_file.name

        print >> cost_file, len(preflist)*copies

        #TODO aqui debe haber un issue con los copies, revisar
        for (i, p) in enumerate(preflist):
            print >> cost_file, "{0} {1}".format(t.vs['pref', i], p.cost)

    return cost_filename

def preference_clauses(query, views, preflist, t):
    if not preflist:
        return t

    (view_names, pred_names) = preference_names(views)

    add_clauses_O1(query, views, preflist, view_names, pred_names, t)
    add_clauses_O2(query, views, preflist, view_names, pred_names, t)

    return t

def preference_rw_clauses(query, views, preflist, t):
    if not preflist:
        return t

    (view_names, pred_names) = preference_names(views)

    add_clauses_O3(query, views, preflist, view_names, pred_names, t)
    add_clauses_O4(query, views, preflist, view_names, pred_names, t)

    return t

def add_clauses_O1(query, views, preflist, view_names, pred_names, t):
    """
    Using a view implies all of the predicates appearing in it are in use.
    """

    logging.debug("adding clauses of type O1")

    for (i, v) in enumerate(views, 1):
        seen = set()

        for g in v.body:
            if g.name in seen:
                continue

            seen.add(g.name)
            clause = [-t.vs['v', i], t.vs['o', g.name]]
            t.add_clause(clause)

def add_clauses_O2(query, views, preflist, view_names, pred_names, t):
    """
    Using a predicate implies at least one of the views in which it appears is in use.
    """

    logging.debug("adding clauses of type O2")

    for p in pred_names:
        clause = [-t.vs['o', p]]

        for (i, v) in enumerate(views, 1):
            if p in [g.name for g in v.body]:
                clause.append(t.vs['v', i])

        t.add_clause(clause)

def add_clauses_O3(query, views, preflist, view_names, pred_names, t):
    """
    The 'pref' variable for each preference implies the preference is enforced.
    """

    logging.debug("adding clauses of type O3")

    for (i, p) in enumerate(preflist):
        positives = [-t.vs['pref', i]]
        negatives = []

        for e in p.formula:
            if e.name in view_names:
                vartype = 'v'
                varname = view_names[e.name]
            elif e.name in pred_names:
                vartype = 'o'
                varname = e.name
            else:
                raise UnknownNameError(e.name)

            if e.positive:
                for c in xrange(len(views)):
                    positives.append(t.vs[vartype, varname, c])
            else:
                nn = [-t.vs[vartype, varname, c] for c in xrange(len(views))]
                negatives.append(nn)

        for negs in product(*negatives):
            t.add_clause(positives + list(negs))

def add_clauses_O4(query, views, preflist, view_names, pred_names, t):
    """
    A preference being enforced implies its 'pref' variable.
    """

    logging.debug("adding clauses of type O4")

    for (i, p) in enumerate(preflist):
        for e in p.formula:
            if e.name in view_names:
                vartype = 'v'
                varname = view_names[e.name]
            elif e.name in pred_names:
                vartype = 'o'
                varname = e.name
            else:
                raise UnknownNameError(e.name)

            if e.positive:
                for c in xrange(len(views)):
                    t.add_clause([-t.vs[vartype, varname, c], t.vs['pref', i]])
            else:
                clause = [t.vs['pref', i]] + [t.vs[vartype, varname, c] for c in xrange(len(views))]
                t.add_clause(clause)

def preference_names(views):
    view_names = {}
    pred_names = set()

    for (i, v) in enumerate(views, 1):
        view_names[v.head.name] = i

    for v in views:
        for g in v.body:
            pred_names.add(g.name)

    return (view_names, pred_names)

if __name__ == "__main__":
    import sys
    print parse(sys.stdin)
