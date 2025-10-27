def build_vals_insert(vals: dict):
    """
    Return ("Arg1", "Arg2", ...)
    """
    res = ", ".join(f'"{key}"' for key in vals.keys())
    return "(" + res + ")"


def build_keys_insert(vals: dict):
    """
    Return $1, $2, $3, ...
    """
    return "(" + ", ".join(f"${i + 1}" for i in range(len(vals.values()))) + ")"
