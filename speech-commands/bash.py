from dragonfly import *
import srabuilder.actions
from srabuilder import rules, clipboard

import urllib.parse
import time
import uuid
import os
import tempfile

import utils, contexts

CLIP_EXE = "pbcopy" if utils.IS_MAC else "clip.exe"


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
    "(p w d) | present working directory": "pwd{enter}",
    "unzip": "unzip ",
    "pseudo": "sudo ",
    "move": "mv ",
    "touch": "touch ",
    "tail": "tail ",
    "make deer": "mkdir ",
    "echo": "echo ",
    "remove": "rm ",
    "source": "source ",
    "a p t get": "apt-get ",
    "install": "install ",
    "update": "update ",
    "echo": "echo ",
    "cd": "cd ",
    "cat": "cat ",
    "list files": "ls | cat -n{enter}",
    "list all [files]": "ls -a{enter}",
    "<n> drop": wrap_n(drop),
    "<n> copy": wrap_n(list_files_to_clipboard),
    "to clipboard": f"| {CLIP_EXE} {{enter}}",
    "[<n>] climb": (Text("cd ..") + Text("/..") * Repeat(extra="n", count=-1))
    + Key("enter"),
    "git": "git ",
    "git commit": 'git commit -m ""{left}',
    "git push": "git push ",
    "git add": "git add ",
    "git stash": "git stash ",
    "git stash pop": "git stash pop ",
    "git checkout": "git checkout ",
    "git checkout new branch": "git checkout -b ",
    "git checkout master": "git checkout master{enter}",
    "git checkout main": "git checkout main{enter}",
    "git merge": "git merge ",
    "up stream": "upstream",
    "origin": "origin",
    "docker": "docker ",
    "compose": "compose ",
    "docker ((p s) | processes)": "docker ps ",
    "docker all ((p s) | processes)": "docker ps -a",
    "docker compose up": "docker compose up ",
    "docker compose down": "docker compose down {enter}",
    "docker compose run": "docker compose run",
    "git checkout <n>": wrap_n(checkout_numbered_branch),
}

repeat = {"close tab": Key("cs-w")}

utils.load_commands(contexts.bash, commands=basic, repeat_commands=repeat)
