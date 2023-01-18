from dragonfly import *
from typing import List


dictation_lengths = []


def snake_case(words: List[str]):
    parsed = "_".join(words)
    return parsed


def capital_snake_case(words: List[str]):
    return snake_case(words).upper()


def camel_case(words: List[str]):
    return words[0] + "".join([x.title() for x in words[1:]])


def one_word(words: List[str]):
    return "".join(words)


def hyphen_case(words: List[str]):
    parsed = "-".join(words)
    return parsed


def capital_hyphen_case(words: List[str]):
    return hyphen_case(words).upper()


def title_case(words: List[str]):
    return "".join([x.title() for x in words])


def dictation_wrap(fn):
    return Function(lambda dictation: do_dictation(fn(dictation.split())))


def do_dictation(dictation):
    text = str(dictation)
    Text(text).execute()
    dictation_lengths.append(len(text))


def do_formatted_dictation(dictation):
    formatted_output = str(dictation)
    formatted_output += " "
    Text(formatted_output).execute()
    dictation_lengths.append(len(formatted_output))


def undo_dictation():
    if dictation_lengths:
        Key("backspace:" + str(dictation_lengths.pop())).execute()


def load_grammar():
    grammar = Grammar("dictation")
    mapping = {
        "dictate <dictation>": Function(lambda dictation: do_dictation(dictation)),
        "dictate capital <dictation>": Function(
            lambda dictation: do_dictation(dictation)
        ),
        "word <dictation>": dictation_wrap(one_word),
        "cobra <dictation>": dictation_wrap(snake_case),
        "cobra capital <dictation>": dictation_wrap(capital_snake_case),
        "hyphen <dictation>": dictation_wrap(hyphen_case),
        "hyphen capital <dictation>": dictation_wrap(capital_hyphen_case),
        "camel <dictation>": dictation_wrap(camel_case),
        "title <dictation>": dictation_wrap(title_case),
        "retry that": Function(undo_dictation),
    }

    extras = [Dictation("dictation")]
    grammar.add_rule(
        MappingRule(name="dictation_command_rule", mapping=mapping, extras=extras)
    )
    grammar.load()
