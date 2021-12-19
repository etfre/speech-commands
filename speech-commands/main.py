import os.path
import os
import threading
import time
import logging
import sys

from dragonfly import RecognitionObserver, get_engine
from dragonfly.log import setup_log
from srabuilder import sleep, environment
import srabuilder

logging.basicConfig(level=logging.INFO)
engine = srabuilder.setup_engine(silence_timeout=400, expected_error_rate_threshold=0.01, lexicon_path="..\\user_lexicon.txt")

import contexts
import mouse
import global_
import python
import firefox
import chrome
import javascript
import vscode
import vscode2
import qzdev
import visual_studio
import bash
import node_terminal
import python_terminal
import windows_terminal
import keyboard
import react
import css


# --------------------------------------------------------------------------
# Simple recognition observer class.


class Observer(RecognitionObserver):
    def on_begin(self):
        print("Speech started.")

    def on_recognition(self, words):
        print("Recognized:", " ".join(words))

    def on_failure(self):
        print("Sorry, what was that?")


def command_line_loop(engine):
    while True:
        user_input = input("> ")
        if user_input:
            time.sleep(4)
            try:
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

    map_contexts_to_builder = {
        (): global_.rule_builder(),
        (contexts.chrome,): chrome.rule_builder(),
        (contexts.bash,): bash.rule_builder()
        .merge(python_terminal.rule_builder())
        .merge(windows_terminal.rule_builder()),
        (contexts.visual_studio,): visual_studio.rule_builder(),
    }
    srabuilder.load_environment_grammars(map_contexts_to_builder)
    import _dictation

    _dictation.load_grammar()

    threading.Thread(target=command_line_loop, args=(engine,), daemon=True).start()
    srabuilder.run_engine()


if __name__ == "__main__":
    main(sys.argv[1:])
