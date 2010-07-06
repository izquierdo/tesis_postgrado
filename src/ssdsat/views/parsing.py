from ply import lex, yacc

tokens = (
    "CONSTANT",
    "VARIABLE",
    "SUB",
    "LPAR",
    "RPAR",
    "COMMA",
)

t_CONSTANT = r"\d+|[a-z]\w*"
t_VARIABLE = r"[A-Z]\w*"
t_SUB = r":-"
t_LPAR = r"\("
t_RPAR = r"\)"
t_COMMA = r","

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

# When parsing starts, try to make a "chemical_equation" because it's
# the name on left-hand side of the first p_* function definition.
# The first rule is empty because I let the empty string be valid
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
    p[0] = (p[1], p[3])

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
    p[0] = (p[1], p[3])

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
    p[0] = "unavar"

def p_argument_constant(p):
    """
    argument : CONSTANT
    """
    p[0] = "unaconst"

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

yacc.yacc(debug=0)

######

import collections

def pepe(s):
    """calculates counts for each element in the chemical equation
    >>> element_counts("CH3COOH")["C"]
    2
    >>> element_counts("CH3COOH")["H"]
    4
    >>>
    """
    
    result = yacc.parse(s)
    print result
