from dragonfly import *
from srabuilder import rules
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
    "unzip": "unzip ",
    "pseudo": "sudo ",
    "move": "mv ",
    "touch": "touch ",
    "make deer": "mkdir ",
    "remove": "rm ",
    "source": "source ",
    "a p t get": "apt-get ",
    "install": "install ",
    "update": "update ",
    "echo": "echo ",
    "cd": "cd ",
    "list files": "ls | cat -n{enter}",
    "list all": "ls -a{enter}" ,
    "git": "git ",
    "git commit": srabuilder.actions.type_and_move('git commit -m ""', left=1),
    "git push": "git push ",
    "git add": "git add ",
    "git stash": "git stash ",
    "git stash pop": "git stash pop ",
    "git checkout": "git checkout ",
    "git checkout new branch": "git checkout -b ",
    "git checkout master": "git checkout master{enter}",
    "git merge": "git merge ",
}

extras = [Choice("functions", functions), Choice("errors", errors), Choice('headers', headers), Choice('names', names)]
utils.load_commands(contexts.terminal, commands=mapping, extras=extras)
