from ply import lex, yacc

class Preference:
    def __init__(self, cost, formula):
        self.cost = cost
        self.formula = formula

class BinOp:
    def __init__(self, p, q):
        self.p = p
        self.q = q

class OrPref(BinOp):
    pass

class AndPref(BinOp):
    pass

class ImplyPref(BinOp):
    pass

################################################################################
# Preference parsing
################################################################################

# Lexer

tokens = (
    "INTEGER",
    "NAME",
    "LOR",
    "LAND",
    "IMPLY",
    "NEG",
)

t_INTEGER = r"\d+"
t_NAME = r"[a-z]\w*"
t_LOR = r"\\/"
t_LAND = r"/\\"
t_IMPLY = "=>"
t_NEG = "-"

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

# Parser

def p_preference_list(p):
    """
    preference_list : preference_list preference
    """
    p[0] = p[1] + [p[2]]

def p_single_preference_list(p):
    """
    preference_list : preference
    """
    p[0] = [p[1]]

def p_preference(p):
    """
    preference : INTEGER formula
    """
    p[0] = Preference(p[1], p[2])

def p_formula_lor(p):
    """
    formula : literal LOR literal
    """
    p[0] = OrPref(p[1], p[3])

def p_formula_land(p):
    """
    formula : literal LAND literal
    """
    p[0] = AndPref(p[1], p[3])

def p_formula_imply(p):
    """
    formula : literal IMPLY literal
    """
    p[0] = ImplyPref(p[1], p[3])

def p_literal_positive(p):
    """
    literal : NAME
    """
    p[0] = (1, p[1])

def p_literal_negative(p):
    """
    literal : NEG NAME
    """
    p[0] = (-1, p[1])

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=0)

# Helpers

def parse(file):
    return parser.parse(file.read(), lexer=lexer)

if __name__ == "__main__":
    import sys
    print yacc.parse(sys.stdin.read())
