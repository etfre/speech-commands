import os.path
import os
# delete so dragonfly doesn't think we're on linux for mac
try:
    del os.environ['DISPLAY']
except KeyError:
    pass
import threading
import time
import logging
import subprocess
import sys

from dragonfly import RecognitionObserver, get_engine
from dragonfly.log import setup_log
from srabuilder import sleep, environment
import srabuilder

logging.basicConfig(level=logging.INFO)
engine = srabuilder.setup_engine(silence_timeout=400, expected_error_rate_threshold=0.01, lexicon_path=os.path.join("..", "user_lexicon.txt"))

import contexts
import global_
import mouse
import python
import cpp
import firefox
import chrome
import iterm2
import javascript
import vscode
import vscode2
import visual_studio
import bash
import node_terminal
import python_terminal
import windows_terminal
import vscode_javascript
import vscode_ocaml 
import vscode_python
import react
import windows
import applescript
import css


# --------------------------------------------------------------------------
# Simple recognition observer class.


class Observer(RecognitionObserver):

    def on_recognition(self, words):
        print("Recognized:", " ".join(words))

# try:
#     import readline
# except:
#     pass #readline not available

def run_applescript(script: str):
    res = subprocess.run(['osascript', '-e', script, '-s', 's'], stdout=subprocess.PIPE, text=True).stdout.rstrip()
    return res

def command_line_loop(engine: get_engine):
    script = '''
    tell application "System Events"
        get id of first application process whose ¬
            frontmost is true
    end tell
    '''
    script2 = '''
    tell application "System Events" to tell application process id "577677"
        try
            get properties of window 1
        on error errmess
            log errmess
        end try
    end tell
    '''
    script3 = '''
    global appIds
    tell application "System Events"
        set appIds to id of every application process whose ¬
            background only is false
    end tell
    return appIds
    '''
    to_run = script2
    while True:
        s = time.time()
        res = run_applescript(to_run)
        e = time.time()
        print('run_applescript', res, e-s)

        s = time.time()
        res2 = applescript.AppleScript(to_run).run()
        e = time.time()
        print('applescript.AppleScript', res2, e-s)
        print('')

        time.sleep(5)
        continue
        user_input = input("> ").strip()
        if user_input:
            time.sleep(4)
            try:
                print('mimic ', user_input)
                engine.mimic(user_input)
            except Exception as e:
                print(e)


# --------------------------------------------------------------------------
# Main event driving loop.


def main(args):


    # Register a recognition observer
    observer = Observer()
    observer.register()
    sleep.load_sleep_wake_grammar(True)
    import _dictation
    _dictation.load_grammar()
    # threading.Thread(target=command_line_loop, args=(engine,), daemon=True).start()
    srabuilder.run_engine()


if __name__ == "__main__":
    main(sys.argv[1:])
