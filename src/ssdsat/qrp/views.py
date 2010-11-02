class View:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        body_str = ",".join(map(str, self.body))
        return "{head} :- {body}".format(head = self.head, body = body_str)

    def argset(self):
        s = set()

        s.update([a for a in self.head.arguments])
        s.update([a for g in self.body for a in g.arguments])

        return s

    def varset(self):
        s = set()

        s.update([a for a in self.head.arguments if not a.constant])
        s.update([a for g in self.body for a in g.arguments if not a.constant])

        return s

    def constset(self):
        s = set()

        s.update([a for a in self.head.arguments if a.constant])
        s.update([a for g in self.body for a in g.arguments if a.constant])

        return s

    def existential_varset(self):
        return set([v for v in self.varset() if self.is_existential(v)])

    def is_distinguished(self, a):
        return a in self.head.arguments or a.constant

    def is_existential(self, a):
        return not self.is_distinguished(a)

class Predicate:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        args_str = ",".join(map(str, self.arguments))
        return "{name}({args})".format(name = self.name, args = args_str)

    arity = property(lambda self : len(self.arguments))

    def unify(self, other, ontology = None):
        if self.name == other.name and self.arity == other.arity:
            return zip(self.arguments, other.arguments)

        if ontology:
            for (child, parent, binding) in ontology.specs:
                if self.name != parent.name or self.arity != parent.arity:
                    continue

                if other.name != child.name or other.arity != child.arity:
                    continue

                l = []
                mapped_child = {}

                for (i, arg) in enumerate(child.arguments):
                    if arg.constant:
                        l.append((arg, other.arguments[i]))
                    else:
                        mapped_child.setdefault(arg, set()).add(other.arguments[i])

                for (i, arg) in enumerate(parent.arguments):
                    # if ontology is correct, arg should always be a key in mapped_child
                    if arg.constant:
                        l.append((self.arguments[i], arg))
                    else:
                        for newarg in mapped_child[arg]:
                            l.append((self.arguments[i], newarg))

                #TODO faltan variables que aparecen en child.arguments pero no en self.arguments

                return l

        return None

class Argument:
    def __init__(self, name, constant):
        self.name = name
        self.constant = constant

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.constant == other.constant

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.name,self.constant))
