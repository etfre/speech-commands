import os
from dragonfly import *
from dragonfly.windows.win32_window import Win32Window
from srabuilder import rules
import contexts
import applications

def set_manual_app_context(**kw):
    app = kw["applications"]
    contexts.set_manual_app_context(app['title'])

def open_app(**kw):
    # just using title, executables can be finicky with aliases
    app = kw["applications"]
    index = kw["n"] - 1
    title = app.get('title', [])
    titles = title if isinstance(title, (list, tuple)) else [title]
    matches = []
    for t in titles:
        matches.extend(Win32Window.get_matching_windows(title=t))
    matches[index].set_foreground()
    # FocusWindow(title=app.get("title"), index=index).execute()


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