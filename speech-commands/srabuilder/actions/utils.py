import time
import dragonfly


def type_and_move(to_type, up=0, left=0):
    action = dragonfly.Text(to_type)
    if up:
        action += sleep(0.1)
        action += dragonfly.Key(f"up:{up}")
    if left:
        action += sleep(0.1)
        action += dragonfly.Key(f"left:{left}")
    return action


def sleep(n):
    return dragonfly.Function(lambda: time.sleep(n))


def between(*actions, n=0.1):
    if not actions:
        return
    main_action = actions[0]
    for action in actions[1:]:
        main_action += sleep(n)
        main_action += action
    return main_action


def surround(left, right):
    return between(
        dragonfly.Key("c-d"),
        dragonfly.Key("right"),
        dragonfly.Text(right),
        dragonfly.Key("left") * dragonfly.Repeat(count=len(right)),
        dragonfly.Key("c-left"),
        dragonfly.Text(left),
    )


def parse(s: str, text_fn=dragonfly.Text, key_fn=dragonfly.Key):
    if not s:
        raise RuntimeError("Can't parse empty string")
    current_text = ""
    actions = []
    is_key = False
    for i, char in enumerate(s):
        try:
            next_char = s[i + 1]
        except IndexError:
            next_char = None
        if char == "{" and next_char != "{" and not is_key:
            is_key = True
            if current_text:
                actions.append(text_fn(current_text))
                current_text = ""
        elif char == "}" and next_char != "}":
            if not is_key:
                raise RuntimeError("Unmatched } token")
            if current_text:
                actions.append(key_fn(current_text))
                current_text = ""
            is_key = False
        else:
            current_text += char
    if is_key:
        raise RuntimeError("Unmatched { token")
    if current_text:
        actions.append(text_fn(current_text))
    return between(*actions)
