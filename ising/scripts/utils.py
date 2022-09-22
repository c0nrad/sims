def ud_to_value(s):
    if s == 'u':
        return 1
    if s == 'd':
        return -1
    if s == "0":
        return 0
    print(s)
    raise Exception("invaluid ud")


def value_to_ud(v: int) -> str:
    if v == -1:
        return "d"
    if v == 1:
        return "u"
    if v == 0:
        return "0"
    print(v)
    raise Exception("invaluid ud")


def majority(state):
    if state.count("u") == 0 and state.count("d") == 0:
        raise Exception(state)
    if state.count("u") > state.count("d"):
        return "u"
    if state.count("u") == state.count("d"):
        return state[0]
    return "d"


def normalize_states(states):
    total = sum(states.values())
    return {k: v / total for (k, v) in states.items()}
