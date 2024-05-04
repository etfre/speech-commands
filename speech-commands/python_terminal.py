from dragonfly import *
from srabuilder import rules
import utils, contexts


basic = {
    "python": "python3 ",
    "pip": "pip ",
    "pip install": "pip install ",
    "pip freeze": "pip freeze > requirements.txt {enter}",
    "activate virtual": "source bin/activate {enter}",
    "create virtual": "python3 -m venv . {enter}",
    "flask run": "python -m flask run {enter}",
}


utils.load_commands(contexts.iterm2, basic)
