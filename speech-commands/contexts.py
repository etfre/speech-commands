from dragonfly import AppContext, FuncContext


PYTHON = "python"
JAVASCRIPT = "javascript"

VISUAL_STUDIO_CODE = "VISUAL_STUDIO_CODE"

language = PYTHON
manual_app_context = None

def set_manual_app_context(app_context: str):
    global manual_app_context
    manual_app_context = app_context


def set_language(lang):
    global language
    language = lang


vscode = AppContext(title="Visual Studio Code") | FuncContext(lambda *a: manual_app_context == VISUAL_STUDIO_CODE)
visual_studio = AppContext(title="Visual Studio") & ~vscode
firefox = AppContext(title="Mozilla Firefox")
chrome = AppContext(title="Google Chrome")
windows_terminal = AppContext(title="evan@")
git_bash = AppContext(title="mingw64")
stardew = AppContext(title="stardew")
bash = windows_terminal | git_bash
javascript = FuncContext(lambda *a: language == JAVASCRIPT)
python = FuncContext(lambda *a: language == PYTHON)