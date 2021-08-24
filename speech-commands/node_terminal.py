from dragonfly import *
from srabuilder import rules

import urllib.parse
import time
import uuid
import os
import contexts
import tempfile
import utils



def enter_command(cmd):
    Text(cmd).execute()
    Key("enter").execute()


basic = {
    "node": "node ",
    "n p m": "npm ",
    "n p m install": "npm install ",
    "n p m start": "npm start ",
    "n p m run": "npm run ",
}

utils.load_commands(contexts.bash, basic)