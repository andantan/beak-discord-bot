def str2bool(value: str) -> bool:
    true_values = ("true", "1")
    false_values = ("false", "0")

    value = value.lower()

    if value in true_values:    return True
    elif value in false_values: return False
    elif value is None:         raise TypeError
    else:                       raise ValueError
