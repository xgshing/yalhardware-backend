# apps/users/utils/mask.py
def mask_username(full_name: str) -> str:
    """
    Tanya Miller → Tanya M.
    张三丰 → 张*
    """
    if not full_name:
        return ""

    parts = full_name.strip().split(" ")
    if len(parts) == 1:
        name = parts[0]
        return name[0] + "*" if len(name) > 1 else name

    return f"{parts[0]} {parts[-1][0]}."
