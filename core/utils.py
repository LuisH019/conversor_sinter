import pandas as pd

def clean_float(val):
    """Garante que números inteiros não fiquem com .0 no final"""
    if pd.isna(val):
        return None
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val

def clean_dict(d: dict) -> dict:
    """Remove chaves com valores nulos (None) do dicionário"""
    return {k: v for k, v in d.items() if v is not None}
