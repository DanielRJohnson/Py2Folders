# Py2Folders
A partial-transpiler that converts a subset of Python to the Folders esoteric programming language

### Folders
[Folders](https://danieltemkin.com/Esolangs/Folders/) is an [esoteric programming language](https://esolangs.org/wiki/Esoteric_programming_language) created by [Daniel Temkin](https://danieltemkin.com/) where the instructions are represented completely by the structure of folders. That is, there are **NO FILES**. The names of the folders and any files within are **COMPLETELY IGNORED**. For example, the Hello World of Folders can be found in [this file](https://github.com/DanielRJohnson/Py2Folders/blob/main/hello_world_structure.txt).

### The Transpiler
Py2Folders transpiles a subset of Python's source code constructs into Folders "source code". Why I mention a subset is that not every Python construct can be directly translated. So, this begs a large question:

### What's Allowed?
Statements:
1. If
2. While
3. Single Assignment
4. Printing a Single Expression
5. Input

Expressions (May not be nested):
1. Variable
2. Add
3. Subtract
4. Multiply
5. Divide
6. Num and Str Literals
7. Equals
8. Greater Than
9. Less Than

If your .py file adheres to these large restrictions, it can be transpiled.

### Usage
1. Clone this Repo
2. Create your Python file to transpile
3. run `Python3 <path_to_pyfile>` which will create a new directory `<pyfile without .py>` in the same folder
4. (Optional) Install [Folders.py](https://github.com/SinaKhalili/Folders.py) and run `Folders <generated folder>`

Congrats! You have translated your Python source file to a construct of entirely folders that *still runs*.
