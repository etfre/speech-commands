from dragonfly import AppContext, FuncContext
import applications

PYTHON = "python"
JAVASCRIPT = "javascript"

VISUAL_STUDIO_CODE = "VISUAL_STUDIO_CODE"

language = None
manual_app_context = None

def title_and_manual_context(spoken: str):
    app = applications.applications[spoken]
    title = app['title']
    return AppContext(title=title) | FuncContext(lambda *a: manual_app_context == title)

def set_manual_app_context(app_context: str):
    global manual_app_context
    manual_app_context = app_context


def set_language(lang):
    global language
    language = lang

vscode = title_and_manual_context("code")
qzdev = title_and_manual_context("q z dev")
visual_studio = AppContext(title="Visual Studio") & ~vscode
firefox = title_and_manual_context("firefox")
chrome = title_and_manual_context("chrome")
# windows_terminal = title_and_manual_context("evan@")
# git_bash = title_and_manual_context("mingw64")
# bash = windows_terminal | git_bash
bash = title_and_manual_context("terminal")
javascript = vscode & (AppContext(title=".js") | AppContext(title=".ts") | FuncContext(lambda *a: language == JAVASCRIPT))
react = javascript & (AppContext(title=".jsx") | AppContext(title=".tsx")) 
python = vscode & (AppContext(title=".py") | FuncContext(lambda *a: language == PYTHON))
css = vscode & AppContext(title=".css")
