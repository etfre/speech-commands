from dragonfly import AppContext, FuncContext
import applications
import utils

PYTHON = "python"
JAVASCRIPT = "javascript"
CPP = "cpp"
OCAML = "ocaml"

VISUAL_STUDIO_CODE = "VISUAL_STUDIO_CODE"

language: str | None = utils.env.get("language")
manual_app_context = utils.env.get("app")


def title_and_manual_context(spoken: str):
    app = applications.applications[spoken]
    title = app["title"]
    return AppContext(title=title) | FuncContext(lambda *a: manual_app_context == title)


def set_manual_app_context(app_context: str):
    global manual_app_context
    manual_app_context = app_context


def set_language(lang: str | None):
    global language
    language = lang


vscode = title_and_manual_context("code")
visual_studio = AppContext(title="Visual Studio") & ~vscode
text_editor = vscode | visual_studio
firefox = title_and_manual_context("firefox")
chrome = title_and_manual_context("chrome")

wsl_terminal = AppContext(title="evan@")
iterm2 = AppContext(title="iterm2 terminal")
bash = wsl_terminal | iterm2

javascript = text_editor & (AppContext(title=".js") | AppContext(title=".ts"))
typescript = text_editor & AppContext(title=".ts")
react = javascript
python = text_editor & (AppContext(title=".py") | FuncContext(lambda *a: language == PYTHON))
cpp = text_editor & (AppContext(title=".cpp") | FuncContext(lambda *a: language == CPP))
ocaml = text_editor & (AppContext(title=".ml") | FuncContext(lambda *a: language == OCAML))
css = text_editor & AppContext(title=".css")
