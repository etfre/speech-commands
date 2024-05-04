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


non_repeat_mapping: dict[str, ActionBase | str] = {
    "[<n>] open <applications>": Function(open_app),
    "start <applications>": Function(start_app),
    "using <applications>": Function(set_manual_app_context),
    "using default": Function(lambda: contexts.set_manual_app_context(None)),
    "window maximize": Function(lambda: Window.get_foreground().maximize()),
    "window minimize": Function(lambda: Window.get_foreground().minimize()),
    "window restore": Function(lambda: Window.get_foreground().restore()),
    "window close": Function(lambda: Window.get_foreground().close()),
}

if utils.IS_MAC:
    non_repeat_mapping['next window'] = "{w-`}"
    non_repeat_mapping['previous  window'] = "{ws-`}"

utils.load_commands(
    commands=non_repeat_mapping,
    extras=[Choice("applications", applications.applications), rules.num],
    defaults={"digits": 1},
)
