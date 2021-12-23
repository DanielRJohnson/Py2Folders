class F_Expr:
    pass

class F_Var(F_Expr):
    __match_args__ = ("name",)
    def __init__(self, name):
        self.name = name

class F_Add(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Sub(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Mul(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Div(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Lit(F_Expr):
    __match_args__ = ("type", "value")
    def __init__(self, type, value):
        self.type = type
        self.value = value

class F_Eq(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Gt(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right

class F_Lt(F_Expr):
    __match_args__ = ("left", "right")
    def __init__(self, left, right):
        self.left = left
        self.right = right