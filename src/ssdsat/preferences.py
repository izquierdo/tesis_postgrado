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

t_INTEGER = r"\d+"
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
# Preference parsing
################################################################################

def preference_clauses(query, views, preflist, t):
    view_names = set([v.head.name for v in views])
    pred_names = set()

    for v in views:
        for g in v.body:
            pred_names.add(g.name)

    for p in preflist:
        clause = []

        for e in p.formula:
            if e.name in view_names:
                pass
            elif e.name in pred_names:
                pass
            else:
                raise UnknownNameError(e.name)

        #t.add_clause([-t.vs['v', i], -t.vs['v', j]])

    return t

if __name__ == "__main__":
    import sys
    print parse(sys.stdin)
