from dragonfly import *
import srabuilder.actions
from srabuilder import rules, clipboard

import urllib.parse
import time
import uuid
import os
import tempfile

import utils, contexts
CLIP_EXE = 'pbcopy' if utils.IS_MAC else 'clip.exe'

def log_dir():
    tdir = os.path.join(tempfile.gettempdir(), "osspeak_std")
    try:
        os.mkdir(tdir)
    except FileExistsError:
        pass
    return tdir


def linux_path(win_path):
    win_path_end = win_path.replace(os.sep, "/")[2:]
    mount_root = stdlib.namespace["state"].WSL_MOUNT_ROOT
    return f"{mount_root}/c{win_path_end}"


def new_logfile_path():
    return os.path.join(log_dir(), "osspeak_log.txt")


def docker_copy(gather_cmd, num, col=0):
    res = docker(gather_cmd, lambda x: x, num, col)
    clipboard.set(res)
    keyboard.KeyPress.from_raw_text(f'echo "Copied {clipboard.get()}"').send()
    keyboard.KeyPress.from_space_delimited_string("enter").send()


def docker(gather_cmd, exec_cmd, num, col=0):
    def modify_line(line):
        return line.split()[col]

    return navigate_list(gather_cmd, exec_cmd, int(num) + 1, modify_line=modify_line)


def navigate_list(gather_cmd, num):
    with clipboard.save_current():
        tmp_clip = str(uuid.uuid4())
        clipboard.set(tmp_clip)
        assert clipboard.get() == tmp_clip
        Text(f"{gather_cmd} | {CLIP_EXE}").execute()
        Key("enter").execute()
        num = int(num)
        clip_text = clipboard.get()
        s = time.time()
        while clip_text == tmp_clip:
            time.sleep(0.01)
            clip_text = clipboard.get()
            if s + 5 < time.time():
                raise RuntimeError("navigate_list failed - clipboard never got input")
        lines = clip_text.split("\n")
        try:
            line = lines[num - 1]
        except IndexError:
            raise RuntimeError
        line = line.rstrip("\r\n")
        return line


def enter_command(cmd):
    Text(cmd).execute()
    Key("enter").execute()


def checkout_numbered_branch(num):
    branch = navigate_list("git branch", num)
    if branch.startswith("*"):
        branch = branch[1:]
    enter_command(f"git checkout {branch.lstrip()}")


def list_files_to_clipboard(num):
    line = navigate_list("ls", num)
    clipboard.set(line)


def drop(num):
    line = navigate_list("ls", num)
    enter_command(f'cd "{line}"')


def to_clipboard():
    enter_command("| {CLIP_EXE}")


def run_and_log(s):
    path = linux_path(new_logfile_path())
    keyboard.KeyPress.from_raw_text(f"{s}|& tee {path}").send()
    keyboard.KeyPress.from_space_delimited_string("enter").send()


def log_stderr():
    path = linux_path(new_logfile_path())
    keyboard.KeyPress.from_raw_text(f"|& tee {path}").send()


def last_modified_file():
    dir_path = log_dir()
    files = os.listdir(dir_path)
    paths = [os.path.join(dir_path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def read_logfile(name, lines):
    if lines is None:
        with open(name) as f:
            return f.read()
    with open(name, "rb") as f:
        return tail(f, lines)


def tail(f, lines):
    total_lines_wanted = lines
    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if block_end_byte - BLOCK_SIZE > 0:
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0, 0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b"\n")
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b"".join(reversed(blocks))
    return b"\n".join(all_read_text.splitlines()[-total_lines_wanted:]).decode("utf8")


functions = {}

values = {}


def wrap_n(fn):
    to_call = lambda **kw: fn(kw["n"])
    return Function(to_call)


basic = {
    "unzip": Text("unzip "),
    "pseudo": Text("sudo "),
    "move": Text("mv "),
    "touch": Text("touch "),
    "make deer": Text("mkdir "),
    "remove": Text("rm "),
    "source": Text("source "),
    "a p t get": Text("apt-get "),
    "install": Text("install "),
    "update": Text("update "),
    "echo": Text("echo "),
    "cd": Text("cd "),
    "list files": Text("ls | cat -n") + Key("enter"),
    "list all": Text("ls -a") + Key("enter"),
    "<n> drop": wrap_n(drop),
    "<n> copy": wrap_n(list_files_to_clipboard),
    "to clipboard": Text(f"| {CLIP_EXE}") + Key("enter"),
    "[<n>] climb": (Text("cd ..") + Text("/..") * Repeat(extra="n", count=-1))
    + Key("enter"),
    "git": Text("git "),
    "git commit": srabuilder.actions.type_and_move('git commit -m ""', left=1),
    "git push": Text("git push "),
    "git add": Text("git add "),
    "git stash": Text("git stash "),
    "git stash pop": Text("git stash pop "),
    "git checkout": Text("git checkout "),
    "git checkout new branch": Text("git checkout -b "),
    "git checkout master": Text("git checkout master") + Key("enter"),
    "git merge": Text("git merge "),
    "git checkout <n>": wrap_n(checkout_numbered_branch),
}

repeat = {"close tab": Key("cs-w")}


# def rule_builder():
#     builder = rules.RuleBuilder()
#     extras = [Choice("functions", functions), Choice("values", values), rules.num]
#     defaults = {"n": 1}
#     builder.basic.append(
#         MappingRule(
#             mapping=basic,
#             extras=extras,
#             exported=False,
#             defaults=defaults,
#             name="wsl_basic",
#         )
#     )
#     builder.repeat.append(
#         MappingRule(mapping=repeat, extras=extras, exported=False, name="wsl_repeat")
#     )
#     return builder

utils.load_commands(contexts.terminal, commands=basic, repeat_commands=repeat, extras=[Choice("functions", functions), Choice("values", values), rules.num])

# on_load() => extensions.register('terminal.wsl.py', wsl)
# is_active() => window.test('MINGW64') || window.test('evan@')

# paths := home='~' | (oh see h)='~/lp/och' | downloads='/c/users/fredere1/downloads' | projects='~/lp'

# unzip = 'unzip '
# list files = 'ls | cat -n' {enter}
# list all = 'ls -a' {enter}
# climb [<number>] = 'cd ..' + '/..' * (int($1 || 1) - 1) {enter}
# drop <number> = wsl.drop($1)
# new tab = {'ctrl shift 3'}
# close tab = {'ctrl shift w'}
# tab right = {'ctrl tab'}
# tab left = {'ctrl shift tab'}
# google <number> = wsl.search(lines=int($1))
# run with logging = wsl.run_and_log('')
# go to <paths> = 'cd ' $1 {enter}
# path <paths> = $1
# new pane right = {'alt shift +'}
# new pane down = {'alt shift -'}
# focus (right | left | up | down) = {'alt ' $1}
# copy output = wsl.to_clipboard()
# copy <number> = wsl.list_files_to_clipboard($1)
# copy location = 'pwd' wsl.to_clipboard()
# launch code = 'code .' {enter}
# source <number> = wsl.navigate_list('ls', 'source', $1)
# python <number> = wsl.navigate_list('ls', 'python', $1)
# execute <number> = wsl.navigate_list('ls', '', $1)

# pseudo = 'sudo '
# move = 'mv '
# touch = 'touch '
# make deer = 'mkdir '
# remove = 'rm '
# cd = 'cd '
# r m minus r f = 'rm -rf '