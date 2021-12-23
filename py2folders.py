from ast import parse, If, While, Assign, Call, BinOp, Add, Sub, Mult, Div, \
                Constant, Compare, Eq, Gt, Lt, stmt as Stmt, Expr, Name

import sys
from os import mkdir, getcwd
from shutil import rmtree
from os.path import exists, isdir

from folders_commands import F_Command, F_IF, F_WHILE, F_LET, F_PRINT, F_INPUT
from folders_expressions import F_Expr, F_Lit, F_Var, F_Eq, F_Gt, F_Lt, F_Add, F_Sub, F_Mul, F_Div
from folders_types import F_Type_Utils, F_INT, F_FLOAT, F_STRING

def transpile(path_to_pyfile: str, save_path: str = None) -> None:
    """
    Transpiles a Python source file to the Folders programming language.
    This assumes that the expressions used in Python are defined in Folders
    These include: if, while, declare, let, print, input, +, -, *, /, 
                   number or string literals, ==, and >
    """
    save_path = save_path if save_path else getcwd() + "/" + path_to_pyfile[:-3] # - .py
    with open(path_to_pyfile, "r") as py_file:
        py_ast = parse(py_file.read())
        commands = []
        for index, stmt in enumerate(py_ast.body):
            commands.append(codegen_stmt(stmt))
        if exists(save_path) and isdir(save_path):
            rmtree(save_path, ignore_errors=True)
        mkdir(save_path)
        foldergen(commands, save_path) 

def codegen_stmt(stmt: Stmt) -> F_Command:
    """
    Produces a Folders command from a Python statement.
    """
    match stmt:
        case If(test, body, _):
            f_body = [codegen_stmt(s) for s in body]
            return F_IF(codegen_expr(test), f_body)
        case While(test, body, _): 
            f_body = [codegen_stmt(s) for s in body]
            return F_WHILE(codegen_expr(test), f_body)
        case Assign(targets, value, _): 
            if len(targets) == 1:
                if isinstance(value, Call) and value.func.id == "input":
                    return F_INPUT(codegen_expr(targets[0]))
                return F_LET(targets[0].id, codegen_expr(value))
            else:
                print("Multiple assignment not supported")
        case Call(func, args, _): 
            if func.id == "print":
                if len(args) == 1:
                    return F_PRINT(codegen_expr(args[0]))
                else:
                    print("Multiple print arguments not supported")
        case Expr(value): # printing and input fall through here
            return codegen_stmt(value)
        case _:
            print("Unsupported statement:", stmt.__class__.__name__)

def codegen_expr(expr: Expr) -> F_Expr:
    """
    Produces a Folders expression from a Python expression.
    """
    match expr:
        case Constant(value): 
            return F_Lit(F_Type_Utils.ptype_to_ftype(type(value)), value)
        case Name(id, _):
            return F_Var(id)
        case Compare(left, ops, comparators): 
            if len(ops) == 1 and len(comparators) == 1:
                match ops[0]:
                    case Eq(): return F_Eq(codegen_expr(left), codegen_expr(comparators[0]))
                    case Gt(): return F_Gt(codegen_expr(left), codegen_expr(comparators[0]))
                    case Lt(): return F_Lt(codegen_expr(left), codegen_expr(comparators[0]))
                    case _: print("Unsupported comparison operator:", ops[0].__class__.__name__)
            else:
                print("Multiple comparison operators not supported")
        case BinOp(left, op, right):
            match op:
                case Add(): return F_Add(codegen_expr(left), codegen_expr(right))
                case Sub(): return F_Sub(codegen_expr(left), codegen_expr(right))
                case Mult(): return F_Mul(codegen_expr(left), codegen_expr(right))
                case Div(): return F_Div(codegen_expr(left), codegen_expr(right))
        case _:
            print("Unsupported expression:", expr.__class__.__name__)

def foldergen(commands: list[F_Command], path: str, varmap: dict[str, int] = {}, is_expr: bool = False) -> None:
    """
    Creates Folders source code from a list of Folders Commands
    """
    for index, F_Construct in enumerate(commands): 
        command_path = path + "/" + str(index) + " - " + F_Construct.__class__.__name__
        if not is_expr: mkdir(command_path)
        match F_Construct: # could be expr or type on recursive call
            case F_IF(test, body):
                declpath = command_path + "/" + str(index) + "0ifdecl"
                testpath = command_path + "/" + str(index) + "1iftest"
                bodypath = command_path + "/" + str(index) + "2ifbody"
                mkdir(declpath)
                mkdir(testpath)
                mkdir(bodypath)
                # If = 0 folders
                foldergen([test], testpath, varmap, is_expr=True)
                foldergen(body, bodypath, varmap)
            case F_WHILE(test, body):
                declpath = command_path + "/" + str(index) + "0whiledecl"
                testpath = command_path + "/" + str(index) + "1whiletest"
                bodypath = command_path + "/" + str(index) + "2whilebody"
                mkdir(declpath)
                mkdir(testpath)
                mkdir(bodypath)
                # While = 1 folder
                mkdir(declpath + "/0")
                foldergen([test], testpath, varmap, is_expr=True)
                foldergen(body, bodypath, varmap)
            case F_LET(name, expr):
                declpath = command_path + "/" + str(index) + "0letdecl"
                namepath = command_path + "/" + str(index) + "1letname"
                exprpath = command_path + "/" + str(index) + "2letexpr"
                mkdir(declpath)
                mkdir(namepath)
                mkdir(exprpath)
                # Let = 3 Folders
                for i in range(3):
                    mkdir(declpath + "/" + str(i))
                # variable names are in number of folders
                if name not in varmap:
                    varmap[name] = len(varmap)
                # create N folders where N is the corresponding variable name
                for i in range(varmap[name]):
                    mkdir(namepath + "/" + str(i))
                foldergen([expr], exprpath, varmap, is_expr=True)
            case F_PRINT(expr):
                declpath = command_path + "/" + str(index) + "0printdecl"
                exprpath = command_path + "/" + str(index) + "1printexpr"
                mkdir(declpath)
                mkdir(exprpath)
                # Print = 4 Folders
                for i in range(4):
                    mkdir(declpath + "/" + str(i))
                foldergen([expr], exprpath, varmap, is_expr=True)
            case F_INPUT(expr):
                declpath = command_path + "/" + str(index) + "0inputdecl"
                exprpath = command_path + "/" + str(index) + "1inputexpr"
                mkdir(declpath)
                mkdir(exprpath)
                # Input = 5 Folders
                for i in range(5):
                    mkdir(declpath + "/" + str(i))
                foldergen([expr], exprpath, varmap, is_expr=True)
            case F_Var(name):
                declpath = path + "/" + str(index) + "0vardecl"
                namepath = path + "/" + str(index) + "1varname"
                mkdir(declpath)
                mkdir(namepath)
                # Variable = 0 Folders
                # variable names are in number of folders
                if name not in varmap:
                    varmap[name] = len(varmap)
                for i in range(varmap[name]):
                    mkdir(namepath + "/" + str(i))
            case F_Add(left, right):
                declpath = path + "/" + str(index) + "0adddecl"
                leftpath = path + "/" + str(index) + "1addleft"
                rightpath = path + "/" + str(index) + "2addright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Add = 1 Folder
                mkdir(declpath + "/0")
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Sub(left, right):
                declpath = path + "/" + str(index) + "0subdecl"
                leftpath = path + "/" + str(index) + "1subleft"
                rightpath = path + "/" + str(index) + "2subright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Sub = 2 Folders
                for i in range(2):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Mul(left, right):
                declpath = path + "/" + str(index) + "0muldecl"
                leftpath = path + "/" + str(index) + "1mullleft"
                rightpath = path + "/" + str(index) + "2mullright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Mul = 3 Folders
                for i in range(3):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Div(left, right):
                declpath = path + "/" + str(index) + "0divdecl"
                leftpath = path + "/" + str(index) + "1divleft"
                rightpath = path + "/" + str(index) + "2divright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Div = 4 Folders
                for i in range(4):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Lit(type, value):
                declpath = path + "/" + str(index) + "0litdecl"
                typepath = path + "/" + str(index) + "1littype"
                valuepath = path + "/" + str(index) + "2litvalue"
                mkdir(declpath)
                mkdir(typepath)
                mkdir(valuepath)
                # Lit = 5 Folders
                for i in range(5):
                    mkdir(declpath + "/" + str(i))
                # Make # of folders corresponding to the type
                for i in range(F_Type_Utils.type_to_num_folders[type]):
                    mkdir(typepath + "/" + str(i))
                # Literals are represented in hex, 4 folders is a hex digit that is 1 / 0 if it has a folder
                # Strings are a folder containing these literals
                if type == F_STRING:
                    for char_idx, char in enumerate(value):
                        charpath = valuepath + "/" + str(char_idx) + char
                        mkdir(charpath)
                        bits = bin(ord(char))[2:] # cut off the 0b
                        # extend the string to be a multiple of 4
                        while not ((len(bits) & (len(bits)-1) == 0) and len(bits) >= 8):
                            bits = "0" + bits
                        for i in range(len(bits) // 4):
                            mkdir(charpath + "/hexchar" + str(i))
                        for index, bit in enumerate(bits): 
                            mkdir(charpath + "/hexchar" + str(index // 4) + "/" + str(index))
                            if bit == "1":
                                mkdir(charpath + "/hexchar" + str(index // 4) + "/" + str(index) + "/" + bit)
                elif type == F_INT:
                    bits = bin(value)[2:] # cut off the 0b
                    # extend the string to be a power of 2
                    while not ((len(bits) & (len(bits)-1) == 0) and len(bits) >= 8):
                        bits = "0" + bits
                    for i in range(len(bits) // 4):
                        mkdir(valuepath + "/hexchar" + str(i))
                    for index, bit in enumerate(bits): 
                        mkdir(valuepath + "/hexchar" + str(index // 4) + "/" + str(index))
                        if bit == "1":
                            mkdir(valuepath + "/hexchar" + str(index // 4) + "/" + str(index) + "/" + bit)
                elif type == F_FLOAT:
                    bits = F_Type_Utils.float_binary(value)
                    # extend the string to be a power of 2
                    while not ((len(bits) & (len(bits)-1) == 0) and len(bits) >= 8):
                        bits = "0" + bits
                    for i in range(len(bits) // 4):
                        mkdir(valuepath + "/hexchar" + str(i))
                    for index, bit in enumerate(bits): 
                        mkdir(valuepath + "/hexchar" + str(index // 4) + "/" + str(index))
                        if bit == "1":
                            mkdir(valuepath + "/hexchar" + str(index // 4) + "/" + str(index) + "/" + bit)
                else:
                    raise ValueError("Internal Error Occurred, Unknown literal type")
            case F_Eq(left, right):
                declpath = path + "/" + str(index) + "0eqdecl"
                leftpath = path + "/" + str(index) + "1eqleft"
                rightpath = path + "/" + str(index) + "2eqright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Eq = 6 Folders
                for i in range(6):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Gt(left, right):
                declpath = path + "/" + str(index) + "0gtdecl"
                leftpath = path + "/" + str(index) + "1gtleft"
                rightpath = path + "/" + str(index) + "2gtright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Gt = 7 Folders
                for i in range(7):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case F_Lt(left, right):
                declpath = path + "/" + str(index) + "0ltdecl"
                leftpath = path + "/" + str(index) + "1ltleft"
                rightpath = path + "/" + str(index) + "2ltright"
                mkdir(declpath)
                mkdir(leftpath)
                mkdir(rightpath)
                # Lt = 8 Folders
                for i in range(8):
                    mkdir(declpath + "/" + str(i))
                foldergen([left], leftpath, varmap, is_expr=True)
                foldergen([right], rightpath, varmap, is_expr=True)
            case _:
                raise ValueError("Internal Error Occurred, Unhandled case in foldergen.")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 py2folders.py <path_to_pyfile> <save_path>?")
        sys.exit(1)
    path_to_pyfile = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) == 3 else None
    transpile(path_to_pyfile, save_path)
    exit(0)