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
# Ontology handling
################################################################################

if __name__ == "__main__":
    import sys
    print parse(sys.stdin)
