from dragonfly import AppContext, FuncContext


PYTHON = "python"
JAVASCRIPT = "javascript"

language = PYTHON


def set_language(lang):
    global language
    language = lang


vscode = AppContext(title="Visual Studio Code")
visual_studio = AppContext(title="Visual Studio") & ~vscode
firefox = AppContext(title="Mozilla Firefox")
chrome = AppContext(title="Google Chrome")
windows_terminal = AppContext(title="evan@")
git_bash = AppContext(title="mingw64")
stardew = AppContext(title="stardew")
bash = windows_terminal | git_bash
javascript = FuncContext(lambda *a: language == JAVASCRIPT)
python = FuncContext(lambda *a: language == PYTHON)