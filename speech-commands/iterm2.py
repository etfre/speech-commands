import dragonfly as df

import contexts
import utils


basic = {
    "new horizontal": "{ws-d}",
    "new vertical": "{w-d}",
    "pane up": "{wa-up}",
    "pane right": "{wa-right}",
    "pane down": "{wa-down}",
    "pane left": "{wa-left}",
    "close pane": "{w-w}",
}

repeat = {
    "higher": "{w-pageup}",
    "lower": "{w-pagedown}",
    "tab new": "{w-t}",
    "tab close": "{wa-w}",
    "tab left": "{sw-[}",
    "tab right": "{sw-]}",
}

utils.load_commands(contexts.iterm2, basic, repeat_commands=repeat)