class F_Command:
    pass

class F_IF(F_Command):
    __match_args__ = ("expression", "commands")
    def __init__(self, expression, commands: list[F_Command]):
        self.expression = expression
        self.commands = commands

class F_WHILE(F_Command):
    __match_args__ = ("expression", "commands")
    def __init__(self, expression, commands: list[F_Command]):
        self.expression = expression
        self.commands = commands

class F_LET(F_Command):
    __match_args__ = ("name", "expression")
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class F_PRINT(F_Command):
    __match_args__ = ("expression",)
    def __init__(self, expression):
        self.expression = expression

class F_INPUT(F_Command):
    __match_args__ = ("name",)
    def __init__(self, name):
        self.name = name