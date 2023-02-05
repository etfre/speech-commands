import os
from dragonfly import *
from dragonfly.windows import Window
from srabuilder import rules
import contexts
import applications
import utils

def set_manual_app_context(**kw):
    app = kw["applications"]
    contexts.set_manual_app_context(app['title'])

def open_app(**kw):
    import time
    # just using title, executables can be finicky with aliases
    app = kw["applications"]
    target_count = kw["n"]
    title = app.get('title', [])
    titles = title if isinstance(title, (list, tuple)) else [title]
    match_count = 0
    for win in Window.get_all_windows():
        win_title = win.title.lower()
        for title in titles:
            if title in win_title:
                match_count += 1
                if target_count == match_count:
                    win.set_foreground()
                    return
                break


def start_app(**kw):
    exe = kw["applications"]["executable"]
    if exe == 'cmd.exe':
        os.system('start cmd.exe')
    else:
        StartApp(exe).execute()


non_repeat_mapping = {
    "[<n>] open <applications>": Function(open_app),
    "start <applications>": Function(start_app),
    "using <applications>": Function(set_manual_app_context),
    "using default": Function(lambda: contexts.set_manual_app_context(None)),
    "maximize window": Function(lambda: Window.get_foreground().maximize()),
    "minimize window": Function(lambda: Window.get_foreground().minimize()),
    "restore window": Function(lambda: Window.get_foreground().restore()),
    "close window": Function(lambda: Window.get_foreground().close()),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("applications", applications.applications), rules.num]
    defaults = {"n": 1}
    builder.basic.append(
        MappingRule(
            mapping=non_repeat_mapping,
            extras=extras,
            exported=False,
            defaults=defaults,
            name="windows",
        )
    )
    return builder

utils.load_commands(
    commands=non_repeat_mapping,
    extras=[Choice("applications", applications.applications), rules.num],
    defaults={"digits": 1},
)
