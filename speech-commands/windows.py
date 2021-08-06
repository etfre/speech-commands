from dragonfly import *
from srabuilder import rules

applications = {
    "firefox": {
        "title": "mozilla firefox",
        "executable": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    },
    "code": {
        "title": "visual studio code",
        "executable": "C:\\Users\\evfre\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe",
    },
    "visual studio": {
        "title": "microsoft visual studio",
        "executable": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\IDE\\devenv.exe",
    },
    "chrome": {
        "title": "google chrome",
        "executable": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    },
    "terminal": {"title": "evan@", "executable": "wt.exe"},
    "command prompt": {"title": "command prompt"},
    "powershell": {"title": "windows powershell"},
    "git bash": {
        "title": "mingw64",
        "executable": "C:\\Program Files\\Git\\git-bash.exe",
    },
}


def open_app(**kw):
    # just using title, executables can be finicky with aliases
    app = kw["applications"]
    index = kw["n"] - 1
    FocusWindow(title=app.get("title"), index=index).execute()


def start_app(**kw):
    StartApp(kw["applications"]["executable"]).execute()


non_repeat_mapping = {
    "[<n>] open <applications>": Function(open_app),
    "start <applications>": Function(start_app),
    "maximize window": Function(lambda: Window.get_foreground().maximize()),
    "minimize window": Function(lambda: Window.get_foreground().minimize()),
    "restore window": Function(lambda: Window.get_foreground().restore()),
    "close window": Function(lambda: Window.get_foreground().close()),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("applications", applications), rules.num]
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