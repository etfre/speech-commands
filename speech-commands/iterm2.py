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
    "tab close": "{wa-w}",
}

repeat = {
    "higher": "{w-pageup}",
    "lower": "{w-pagedown}",
}

utils.load_commands(contexts.iterm2, basic, repeat_commands=repeat)