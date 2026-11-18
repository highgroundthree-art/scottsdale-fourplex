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


# ---------------------------------------------------------------- clipped enlarged views
def _clip_poly(pts, xmin, ymin, xmax, ymax):
    def clip(poly, inside, inter):
        out = []
        for i in range(len(poly)):
            cur, prev = poly[i], poly[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(inter(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(inter(prev, cur))
        return out

    def ix(x):
        return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / ((b[0] - a[0]) or 1e-9))

    def iy(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / ((b[1] - a[1]) or 1e-9), y)
    p = list(pts)
    for inside, inter in ((lambda q: q[0] >= xmin, ix(xmin)), (lambda q: q[0] <= xmax, ix(xmax)),
                          (lambda q: q[1] >= ymin, iy(ymin)), (lambda q: q[1] <= ymax, iy(ymax))):
        if not p:
            break
        p = clip(p, inside, inter)
    return p


def _clip_seg(a, b, xmin, ymin, xmax, ymax):
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - xmin), (dx, xmax - a[0]), (-dy, a[1] - ymin), (dy, ymax - a[1])):
        if p == 0:
            if q < 0:
                return None
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
    if t0 > t1:
        return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


def clip_items(s, n0, box):
    xmin, ymin, xmax, ymax = box
    inb = lambda p: xmin <= p[0] <= xmax and ymin <= p[1] <= ymax
    out = []
    for it in s.items[n0:]:
        k = it[0]
        if k == "solid":
            p = _clip_poly(it[3], *box)
            if len(p) >= 3:
                out.append(("solid", it[1], it[2], p))
        elif k == "line":
            r = _clip_seg(it[5], it[6], *box)
            if r:
                out.append(it[:5] + r)
        elif k == "pline":
            pts, closed, fill = it[5], it[6], it[7]
            if all(inb(p) for p in pts):
                out.append(it); continue
            if closed and fill is not None:
                p = _clip_poly(pts, *box)
                if len(p) >= 3:
                    out.append(it[:5] + (p, True, fill, it[8]))
            else:
                seq = list(pts) + ([pts[0]] if closed else [])
                for a, b in zip(seq, seq[1:]):
                    r = _clip_seg(a, b, *box)
                    if r:
                        out.append(("line",) + it[1:5] + r)
        elif k == "text":
            if inb(it[2]):
                out.append(it)
        elif k in ("arc", "circle"):
            if inb(it[5]):
                out.append(it)
        else:
            out.append(it)
    s.items[n0:] = out


def enlarged(s, level, win, at, scale=24, screen=False):
    """Draw window win=(x0,y0,x1,y1) in feet of the level plan with its top-left at paper point at."""
    sc0 = s.scale
    s.scale = scale
    ox, oy = at[0] - win[0] * 12 / scale, at[1] + win[1] * 12 / scale
    n0 = len(s.items)
    if screen:
        p = bg(s, level, (ox, oy), names=False)
    else:
        s.ox, s.oy = ox, oy
        ns = {"__name__": "bg", "__S__": s}
        code = _source(level).replace("s = Sheet(origin=(3.6, 19.75))", "s = __S__")
        import sys as _sys
        argv = _sys.argv; _sys.argv = ["bg", "/tmp"]
        try:
            exec(compile(code, SRC[level], "exec"), ns)
        finally:
            _sys.argv = argv
        p = ns["p"]
    s.ox, s.oy = ox, oy
    a = s.m2p(win[0] * 12, win[1] * 12); b = s.m2p(win[2] * 12, win[3] * 12)
    clip_items(s, n0, (a[0], b[1], b[0], a[1]))
    s.rect(a[0], b[1], b[0] - a[0], a[1] - b[1], layer="A-ANNO-SYMB", lw="xf", dash="CENTER")
    return p
