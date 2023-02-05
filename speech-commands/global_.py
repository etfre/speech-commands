from dragonfly import *
import time
from dragonfly.windows.clipboard import Clipboard

import os
import contexts
import windows
import utils
from srabuilder import rules, clipboard

def paste_clipboard_lines(n=1):
    spl = clipboard.get().split(os.linesep)
    if not spl:
        return
    with clipboard.save_current():
        to_paste = os.linesep.join(spl[-int(n):])
        clipboard.set(to_paste)
        Key('c-v').execute()
        time.sleep(0.1)
    

basic_mapping = {
    "language javascript": Function(lambda: contexts.set_language(contexts.JAVASCRIPT)),
    "language python": Function(lambda: contexts.set_language(contexts.PYTHON)),
    "language see plus plus": Function(lambda: contexts.set_language(contexts.CPP)),
    "language oh camel": Function(lambda: contexts.set_language(contexts.OCAML)),
    "(clear | reset) language": Function(lambda: contexts.set_language(None)),
    "launch wsl": Text("wsl.exe") + Key("enter"),
    "type clipboard": Function(utils.type_clipboard),
    "paste <n> (line | lines)": Function(paste_clipboard_lines),
}

repeat = {
    "alt tab": '{alt:down}{tab}',
}

utils.load_commands(None, basic_mapping)
utils.load_commands(None, repeat_commands=repeat)
