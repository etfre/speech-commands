import time
import utils
import contexts
from dragonfly import *
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules

attributes = {
    'align content': 'align-content',
    'align items': 'align-items',
    'align self': 'align-self',
    'background': 'background',
    'background color': 'background-color',
    'display': 'display',
    'flex': 'flex',
    'flex basis': 'flex-basis',
    'flex grow': 'flex-grow',
    'flex shrink': 'flex-shrink',
    'height': 'height',
    'max height': 'max-height',
    'min height': 'min-height',
    'visibility': 'visibility',
    'width': 'width',
    'z index': 'z-index',
}

values = {
    'flex box': 'flexbox',
    'grid': 'grid',
    'inherit': 'inherit',
    'none': 'none',
}

non_repeat_mapping = {
    "attribute <attributes>": '%(attributes)s: ;{left}',
    "<values>": '%(values)s',
    "<n> pixels": '%(n)spx',
}
repeat_mapping = {
}

extras = [
    Choice("attributes", attributes),
    Choice("values", values),
]
utils.load_commands(
    contexts.css,
    commands=non_repeat_mapping,
    extras=extras
)
# utils.load_commands(contexts.vscode, repeat_commands=repeat_mapping)