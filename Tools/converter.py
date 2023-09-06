def str2bool(value: str) -> bool:
    v = value.lower()
    
    if v  in ("true", "1"): return True
    elif v in ("false", "0"): return False
    elif v is None: raise TypeError
    else: raise ValueError
