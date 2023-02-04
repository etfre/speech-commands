import uuid
import time
from dragonfly import *


digitMap = {
    "zero": 0,
    "one": 1,
    "too": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

nonZeroDigitMap = {
    "one": 1,
    "too": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_numrep(rep):
    first, rest = rep
    numstr = str(first) + "".join(str(d) for d in rest)
    return int(numstr)


numrep = Sequence(
    [Choice(None, nonZeroDigitMap), Repetition(Choice(None, digitMap), min=0, max=10)],
    name="n",
)
num = Modifier(numrep, parse_numrep)
digitsrep = Repetition(Choice(None, digitMap), name="digits", min=1, max=16)
digits = Modifier(digitsrep, lambda rep: "".join(map(str, rep)))


def alternative(elements, name=None):
    alternatives = []
    for item in elements:
        elem = item
        if isinstance(item, Rule):
            elem = RuleRef(rule=item)
        alternatives.append(elem)
    return Alternative(alternatives, name=name)


release = Key("shift:up, ctrl:up, alt:up")


class RepeatRule(CompoundRule):
    pass


def new_repeat_rule(repeat):
    spec = f"[<n>] <repeat>"
    extras = [repeat, num]
    name = "something"
    rule = RepeatRule(spec=spec, extras=extras, name=name, exported=False)
    return rule


def new_basic_rule(elem):
    return BasicRule(element=elem, name=str(uuid.uuid4()))


def module_rule(rule=None, repeat_rule=None):
    pass


class RuleBuilder:
    def __init__(self, basic=None, repeat=None):
        self.basic = []
        self.repeat = []

    def to_rule(self):
        alt = alternative(self.repeat, name="repeat")
        rep = new_repeat_rule(alt)
        basic = alternative(self.basic + [rep], name="basic")
        ccr_elem = Repetition(basic, min=1, max=16)
        return RootRule(element=ccr_elem)

    def merge(self, other):
        self.basic.extend(other.basic)
        self.repeat.extend(other.repeat)
        return self


def yield_actions(node):
    actor = node.actor
    if isinstance(actor, (Literal, Modifier)):
        yield node.value()
    elif isinstance(actor, (RuleRef, Compound, Optional, Sequence, Alternative)):
        for child in node.children:
            yield from yield_actions(child)
    elif isinstance(actor, Rule):
        rule = actor
        if isinstance(rule, RepeatRule):
            assert len(node.children) == 1
            result = list(yield_actions(node.children[0]))
            if len(result) == 1:
                yield result[0]
            elif result:
                count, action = result
                if count > 1:
                    yield action * Repeat(count=count)
                else:
                    yield action
                yield release
        else:
            yield node.value()
    else:
        raise NotImplementedError(f"{node}")


class RootRule(BasicRule):

    exported = True

    def _process_recognition(self, node, extras):  # @UnusedVariable
        rep = node.children[0]
        for child in rep.children:
            for action in yield_actions(child):
                action.execute()
                # sleep to avoid typing out of order. Might want to
                # make this configurable for latency-sensitive applications like games
                time.sleep(0.05)


class ParsedRule(MappingRule):
    def __init__(self, mapping, text_fn=Text, key_fn=Key, **kwargs):
        import srabuilder.actions

        parsed_mapping = {}
        for k, v in mapping.items():
            parsed_mapping[k] = srabuilder.actions.parse(v, text_fn=text_fn, key_fn=key_fn) if isinstance(v, str) and not isinstance(v, Text) else v
        super().__init__(mapping=parsed_mapping, exported=False, **kwargs)