from dragonfly import *
import utils
import contexts

functions = {
}

errors = {
    "(assert|assertion) error": "AssertionError",
    "key error": "KeyError",
    "exception": "Exception",
    "import error": "ImportError",
    "index error": "IndexError",
    "not implemented error": "NotImplementedError",
    "oh s error": "OSError",
    "run time error": "RuntimeError",
    "type error": "TypeError",
    "value error": "ValueError",
}

headers = {
    'standard': "std",
    'vector': "vector",
    'map': "map",
    'memory': "memory",
    'b s l': "bsl",
    '(out stream) | (stream out)': "ostream",
    '(in stream) | (stream in)': "istream",
    'eye oh stream': "iostream",
}

names = {
    'vector': "vector",
    'map': "map",
    'string': "string",
    'see out': "cout",
    'end line': "endl",
}

mapping = {
    "int": "int ",
    "float": "float ",
    "double": "double ",
    "include": "#include ",
    "raise": "raise ",
    "using": "using ",
    "name space": "namespace ",
    "include <headers>": "#include <%(headers)s>",
    "name <headers>": "%(headers)s",
    "<headers> <names>": "%(headers)s::%(names)s",
    "name <names>": "%(names)s",
    "standard": "std::",
    "b s l": "bsl::",
    "assign": " = ",
    "compare": " == ",
    "(out stream) | (stream out)": " << ",
    "(in stream) | (stream in)": " >> ",
    "return": "return ;{left}",
    "break": "break;",
    "continue": "continue;",
    "not": "!",
    "stand": " && ",
    "store": " || ",
    "new scope": "{{}}{left}{enter}",
    "<errors>": "%(errors)s",
    "if statement": "if () {{}}{left}{enter}{up}",
    "else statement": "else {{}}{left}{enter}",
    "if else statement": "if () {{}}{left}{enter}{down}{c-enter}else {{}}{left}{enter}{up:4}{end}{left:3}",
    "else if statement": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "for loop": "for (int i = 0; i < ; i++) {{}}{left}{enter}{up}{end}{left:8}",
    "for each loop": "for (r) {{}}{left}{enter}{up}{end}{left:8}",
    "while loop": "while () {{}}{left}{enter}{up}{end}{left:3}",
    "try catch": "try{{}}{left}{enter}",
    "true": "true",
    "false": "false",
    "null": "null",
    "auto": "auto",
    "ref": "&",
    "d ref": "*",
    "call <names>": "%(names)s(){left}",
    "string": '""{left}',
    "angles": "<>",
    "header guard": "#ifndef {enter}#define {enter:4}#endif{up:5}{end}{ca-down}"
}

extras = [Choice("functions", functions), Choice("errors", errors), Choice('headers', headers), Choice('names', names)]
utils.load_commands(contexts.cpp, commands=mapping, extras=extras)
