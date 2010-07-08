class View:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        body_str = ",".join(map(str, self.body))
        return "{head} :- {body}".format(head = self.head, body = body_str)

class Predicate:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        args_str = ",".join(map(str, self.arguments))
        return "{name}({args})".format(name = self.name, args = args_str)

class Argument:
    def __init__(self, name, constant):
        self.name = name
        self.constant = constant

    def __repr__(self):
        return self.name
