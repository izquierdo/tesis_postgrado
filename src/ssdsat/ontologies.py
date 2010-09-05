import logging
from itertools import product
from tempfile import NamedTemporaryFile

from ply import lex, yacc

import qrp.parsing

class Ontology:
    def __init__(self, specs):
        self.specs = specs

    def __repr__(self):
        return "Ontology({0})".format(self.specs)

################################################################################
# Ontology parsing
################################################################################

# Lexer

tokens = (
    "CONSTANT",
    "VARIABLE",
    "SPEC",
    "LPAR",
    "RPAR",
    "COMMA",
)

#TODO integers shouldn't be used for predicate names
t_CONSTANT = r"\d+|[a-z]\w*"
t_VARIABLE = r"[A-Z]\w*"
t_SPEC = r"<="
t_LPAR = r"\("
t_RPAR = r"\)"
t_COMMA = r","

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

# Parser

def p_ontology(p):
    """
    ontology : spec_list
    """
    p[0] = Ontology(p[1])

def p_spec_list(p):
    """
    spec_list : spec_list spec
    """
    p[0] = p[1] +[p[2]]

def p_preference(p):
    """
    spec_list : spec
    """
    p[0] = [p[1]]

def p_literal_list(p):
    """
    spec : predicate SPEC predicate
    """
    p[0] = (p[1], p[3])

p_predicate = qrp.parsing.p_predicate

p_argument_list = qrp.parsing.p_argument_list

p_single_argument_list = qrp.parsing.p_single_argument_list

p_argument_variable = qrp.parsing.p_argument_variable

p_argument_constant = qrp.parsing.p_argument_constant

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=0)

# Helpers

def parse(file):
    return parser.parse(file.read(), lexer=lexer)

################################################################################
# Preference parsing
################################################################################

def preference_cost_file(preflist, t, copies):
    if not preflist:
        return t

    with NamedTemporaryFile(prefix="ssdsat.", suffix=".costs", delete = False) as cost_file:
        cost_filename = cost_file.name

        print >> cost_file, len(preflist)*copies

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
