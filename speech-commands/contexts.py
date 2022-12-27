from dragonfly import AppContext, FuncContext
import applications
import utils

PYTHON = "python"
JAVASCRIPT = "javascript"
CPP = "cpp"
OCAML = "ocaml"

VISUAL_STUDIO_CODE = "VISUAL_STUDIO_CODE"

language = utils.env.get("language")
manual_app_context = utils.env.get("app")


def title_and_manual_context(spoken: str):
    app = applications.applications[spoken]
    title = app["title"]
    return AppContext(title=title) | FuncContext(lambda *a: manual_app_context == title)


def set_manual_app_context(app_context: str):
    global manual_app_context
    manual_app_context = app_context


def set_language(lang: str):
    global language
    language = lang


vscode = title_and_manual_context("code")
visual_studio = AppContext(title="Visual Studio") & ~vscode
text_editor = vscode | visual_studio
firefox = title_and_manual_context("firefox")
chrome = title_and_manual_context("chrome")
# windows_terminal = title_and_manual_context("evan@")
wsl_terminal = AppContext(title="evan@")
# git_bash = title_and_manual_context("mingw64")
bash = wsl_terminal
# bash = title_and_manual_context("terminal")
terminal = title_and_manual_context("terminal")
javascript = text_editor & (
    AppContext(title=".js") | AppContext(title=".ts") | FuncContext(lambda *a: language == JAVASCRIPT)
)
react = javascript
python = text_editor & (AppContext(title=".py") | FuncContext(lambda *a: language == PYTHON))
cpp = text_editor & (AppContext(title=".cpp") | FuncContext(lambda *a: language == CPP))
ocaml = text_editor & (AppContext(title=".ml") | FuncContext(lambda *a: language == OCAML))
css = text_editor & AppContext(title=".css")
