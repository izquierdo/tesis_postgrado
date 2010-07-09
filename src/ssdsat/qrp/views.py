class View:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        body_str = ",".join(map(str, self.body))
        return "{head} :- {body}".format(head = self.head, body = body_str)

    def varset(self):
        s = set()

        s.update([a for a in self.head.arguments if not a.constant])
        s.update([a for g in self.body for a in g.arguments if not a.constant])

        return s

    def is_existential(self, a):
        return a not in self.head.arguments

class Predicate:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        args_str = ",".join(map(str, self.arguments))
        return "{name}({args})".format(name = self.name, args = args_str)

    arity = property(lambda self : len(self.arguments))

class Argument:
    def __init__(self, name, constant):
        self.name = name
        self.constant = constant

    def __repr__(self):
        return self.name
