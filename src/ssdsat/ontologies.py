import logging
from itertools import product
from tempfile import NamedTemporaryFile

from ply import lex, yacc

import qrp.parsing

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

class Ontology:
    def __init__(self, spec_list):
        tc = set()

        for a, b in spec_list:
            tc.add((a, b, ()))

        # transitive closure

        while True:
            new = set()

            for (spec_a, spec_b) in product(tc, repeat=2):
                if spec_a == spec_b:
                    continue

                spec_c = self._join(spec_a, spec_b)
    
                if spec_c is not None:
                    new.add(spec_c)

            pre_len = len(tc)
            tc.update(new)
            pos_len = len(tc)

            if pre_len == pos_len:
                break

        self.specs = tc

    def _join(self, spec_a, spec_b):
        (child_a, parent_a, binding_a) = spec_a
        (child_b, parent_b, binding_b) = spec_b

        if not parent_a.name == child_b.name:
            return None
        
        if not parent_a.arity == child_b.arity:
            return None

        equals_set = {}

        for x, y in list(binding_a) + list(binding_b) + zip(parent_a.arguments, child_b.arguments):
            if x not in equals_set and y not in equals_set:
                equals_set[x] = equals_set[y] = set([x, y])
            elif x not in equals_set:
                equals_set[y].add(x)
                equals_set[x] = equals_set[y]
            elif y not in equals_set:
                equals_set[x].add(y)
                equals_set[y] = equals_set[x]
            elif equals_set[x] is not equals_set[y]:
                equals_set[x].update(equals_set[y])
                equals_set[y] = equals_set[x]

        seen = set()

        for x in equals_set:
            if x in seen:
                continue

            for y in equals_set[x]:
                seen.add(y)

            if len([var for var in equals_set[x] if var.constant]) > 1:
                return None

        return (child_a, parent_b, tuple(zip(parent_a.arguments, child_b.arguments)))

    def __repr__(self):
        return "Ontology({0})".format(self.specs)

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    import sys
    print parse(sys.stdin)
