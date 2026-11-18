"""Screened background plans of Model 1 (from a101_1.py / a102_1.py) for consultant sheets.

bg(s, level, origin) draws the walls, doors, windows and fixtures of the chosen level onto
sheet s, screened gray, with small room names. Returns the Plan (spaces etc.).
"""
from reportlab.lib.colors import Color
import cadkit
from plan_engine import Plan

F = 12.0
GRAY = Color(0.62, 0.62, 0.62)
TGRAY = Color(0.45, 0.45, 0.45)
SRC = {1: "a101_1.py", 2: "a102_1.py"}


def _source(level):
    src = open(SRC[level]).read()
    cut = src.index("# ------------------------------------------------------------------ grids")
    return src[:cut]


def bg(s, level, origin=(3.6, 19.75), names=True):
    s.ox, s.oy = origin
    n0 = len(s.items)
    ns = {"__name__": "bg", "sys": __import__("sys")}
    code = _source(level)
    # use the caller's sheet instead of a new one
    code = code.replace("s = Sheet(origin=(3.6, 19.75))", "s = __S__")
    ns["__S__"] = s
    import sys as _sys
    argv = _sys.argv
    _sys.argv = ["bg", "/tmp"]
    try:
        exec(compile(code, SRC[level], "exec"), ns)
    finally:
        _sys.argv = argv
    s.ox, s.oy = origin
    p = ns["p"]
    # screen everything drawn by the background
    out = []
    for it in s.items[n0:]:
        k = it[0]
        if k == "solid":
            out.append(("solid", "A-BKGD", 0.86, it[3]))
        elif k == "text":
            l = list(it); l[1] = "A-BKGD"; l[8] = TGRAY; out.append(tuple(l))
        else:
            l = list(it); l[1] = "A-BKGD"; l[4] = GRAY
            if l[2] in ("xh", "h", "m"):
                l[2] = "f"
            elif l[2] in ("l", "f"):
                l[2] = "xf"
            if k == "pline" and l[7] is not None and isinstance(l[7], float):
                l[7] = min(0.95, 0.6 + l[7] * 0.4)
            out.append(tuple(l))
    s.items[n0:] = out
    if names:
        for sp in p.spaces:
            if sp["name"]:
                x, y = sp["tag_at"]
                nm = sp["name"].replace("\n", " ")
                s.text(s.m2p(x * F, y * F), nm, 0.055, layer="A-BKGD", color=TGRAY)
    return p
