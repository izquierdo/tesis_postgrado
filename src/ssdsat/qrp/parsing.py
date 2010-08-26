from ply import lex, yacc

from qrp.views import View, Predicate, Argument

# Lexer

tokens = (
    "CONSTANT",
    "VARIABLE",
    "SUB",
    "LPAR",
    "RPAR",
    "COMMA",
)

#TODO integers shouldn't be used for predicate names
t_CONSTANT = r"\d+|[a-z]\w*"
t_VARIABLE = r"[A-Z]\w*"
t_SUB = r":-"
t_LPAR = r"\("
t_RPAR = r"\)"
t_COMMA = r","

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

# Parser

def p_view_list(p):
    """
    view_list : view_list view
    """
    p[0] = p[1] + [p[2]]

def p_single_view_list(p):
    """
    view_list : view
    """
    p[0] = [p[1]]

def p_view(p):
    """
    view : predicate SUB predicate_list
    """
    p[0] = View(p[1], p[3])

def p_predicate_list(p):
    """
    predicate_list : predicate_list COMMA predicate
    """
    p[0] = p[1] + [p[3]]

def p_single_predicate_list(p):
    """
    predicate_list : predicate
    """
    p[0] = [p[1]]

def p_predicate(p):
    """
    predicate : CONSTANT LPAR argument_list RPAR
    """
    p[0] = Predicate(p[1], p[3])

def p_argument_list(p):
    """
    argument_list : argument_list COMMA argument
    """
    p[0] = p[1] + [p[3]]

def p_single_argument_list(p):
    """
    argument_list : argument
    """
    p[0] = [p[1]]

def p_argument_variable(p):
    """
    argument : VARIABLE
    """
    p[0] = Argument(p[1], False)

def p_argument_constant(p):
    """
    argument : CONSTANT
    """
    p[0] = Argument(p[1], True)

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=0)

# Helpers

def parse(file):
    return parser.parse(file.read(), lexer=lexer)
