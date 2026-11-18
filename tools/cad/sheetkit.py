"""Shared helpers for the remaining Model 1 sheets."""
import math, sys
from reportlab.lib.colors import Color
from cadkit import Sheet
from plan_engine import table, para, dim_chain, bubble
import sheetlib as SL
from bgplan import bg

F = 12.0
DATE = "2026-11-18"
OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
COMMON = dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE)
RED = Color(0.70, 0.08, 0.08)
BLUE = Color(0.05, 0.25, 0.65)
GREEN = Color(0.05, 0.45, 0.20)
ORANGE = Color(0.80, 0.40, 0.00)
NC = 21.15     # first notes column x
NC2 = 26.55    # second notes column x
TOPY = 23.2


def new(origin=(3.6, 19.75), scale=48):
    return Sheet(origin=origin, scale=scale)


def save(s, sheet_no, file, title, pdf_title=None):
    sc, ox, oy = s.scale, s.ox, s.oy
    s.scale = 48
    SL.border_and_titleblock(s, dict(COMMON, sheet_no=sheet_no, sheet_title=title))
    s.scale, s.ox, s.oy = sc, ox, oy
    base = f"{OUT}/{sheet_no}_{file}"
    s.to_pdf(base + ".pdf", title=pdf_title or f"{sheet_no} {title.replace(chr(10), ' ')} - Model 1", author="Scottsdale Fourplex")
    s.to_dxf(base + ".dxf")
    print("wrote", base)


class Draw:
    """Model-space drawing in FEET on the current origin/scale of sheet s (y down = south)."""

    def __init__(self, s, layer="A-ANNO-SYMB", color=None):
        self.s, self.layer, self.color = s, layer, color

    def L(self, a, b, lw="l", dash=None, layer=None, color=None):
        self.s.line((a[0] * F, a[1] * F), (b[0] * F, b[1] * F), layer=layer or self.layer, lw=lw, space="m", dash=dash, color=color or self.color)

    def PL(self, pts, lw="l", dash=None, closed=False, fill=None, layer=None, color=None):
        self.s.pline([(x * F, y * F) for x, y in pts], layer=layer or self.layer, lw=lw, space="m", dash=dash, closed=closed, fill=fill, color=color or self.color)

    def R(self, x, y, w, h, lw="l", dash=None, fill=None, layer=None, color=None):
        self.PL([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw, dash, True, fill, layer, color)

    def C(self, x, y, r, lw="l", fill=None, layer=None):
        self.s.circle((x * F, y * F), r * F, layer=layer or self.layer, lw=lw, space="m", fill=fill)

    def T(self, x, y, t, h=0.065, layer=None, color=None, **k):
        self.s.text(self.s.m2p(x * F, y * F), t, h, layer=layer or "A-ANNO-TEXT", color=color or self.color, **k)

    def arrow(self, a, b, lw="l", size=0.6):
        self.L(a, b, lw)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for d in (0.45, -0.45):
            self.L(b, (b[0] - size * math.cos(ang + d), b[1] - size * math.sin(ang + d)), lw)

    def tag(self, x, y, t, h=0.06, r=0.55, color=None):
        self.s.circle(self.s.m2p(x * F, y * F), r * h / 0.06 * 0.16, layer=self.layer, lw="l", fill=1.0)
        self.s.text(self.s.m2p(x * F, y * F), t, h, layer="A-ANNO-TEXT", valign="m", font="Helvetica-Bold", color=color or self.color)

    def box(self, x, y, t, h=0.055, color=None):
        w = max(0.3, len(t) * h * 0.62 + 0.08)
        p = self.s.m2p(x * F, y * F)
        self.s.rect(p[0] - w / 2, p[1] - 0.09, w, 0.18, layer=self.layer, lw="f", fill=1.0, color=color or self.color)
        self.s.text(p, t, h, layer="A-ANNO-TEXT", valign="m", font="Helvetica-Bold", color=color or self.color)


def plan_grids(s, W=60, D=50, gx=((0, "1"), (25, "2"), (35, "3"), (60, "4")), gy=((0, "A"), (50, "B")), off=1.2):
    for x, lab in gx:
        px = s.m2p(x * F, 0)[0]; top = s.m2p(0, 0)[1]
        s.line((px, top + off - 0.2), (px, top + 0.08), layer="A-GRID", lw="xf")
        bubble(s, (px, top + off), lab)
    for y, lab in gy:
        py = s.m2p(0, y * F)[1]; lft = s.m2p(0, 0)[0]
        s.line((lft - off + 0.2, py), (lft - 0.08, py), layer="A-GRID", lw="xf")
        bubble(s, (lft - off, py), lab)


def notes(s, x, y, title, items, w=5.1, h=0.072):
    return SL.notes_list(s, x, y, title, items, w, h)


def tbl(s, x, y, title, cols, rows, w=None, h=0.066, rowh=0.165):
    w = w or sum(c[1] for c in cols)
    y = SL.head(s, x, y, title, w)
    return table(s, x, y + 0.04, cols, rows, h=h, rowh=rowh) - 0.22


def legend(s, x, y, title, items, w=5.1):
    """items: (draw_fn(x, y), text)"""
    y = SL.head(s, x, y, title, w)
    for fn, t in items:
        fn(x, y + 0.04)
        s.text((x + 0.75, y), t, 0.068, align="l")
        y -= 0.22
    return y - 0.1


def title(s, num, sheet, t, sub, x=1.35, y=3.15, w=16.0, scalebar=True):
    sc, ox, oy = s.scale, s.ox, s.oy
    s.scale = 48
    SL.drawing_title(s, x, y, num, sheet, t, sub, w=w, scalebar=scalebar)
    s.scale, s.ox, s.oy = sc, ox, oy


def north(s, x=18.6, y=3.6):
    SL.north_arrow(s, x, y)


def two_level(s, fn_ground, fn_upper, sheet, what, scale_note="SCALE: 3/16\" = 1'-0\""):
    """Stack upper (top) and ground (bottom) plans at 3/16" on one sheet."""
    s.scale = 64
    up_o, gr_o = (2.6, 22.9), (2.6, 11.9)
    p2 = bg(s, 2, up_o); s.scale = 64; s.ox, s.oy = up_o
    fn_upper(Draw(s), p2)
    s.ox, s.oy = up_o; plan_grids(s, off=0.5)
    p1 = bg(s, 1, gr_o); s.scale = 64; s.ox, s.oy = gr_o
    fn_ground(Draw(s), p1)
    s.ox, s.oy = gr_o; plan_grids(s, off=0.5)
    s.scale = 48
    SL.drawing_title(s, 2.75, 12.72, "2", sheet, f"{what} — UPPER FLOOR", scale_note, w=10.7, scalebar=False)
    SL.drawing_title(s, 2.75, 1.72, "1", sheet, f"{what} — GROUND FLOOR", scale_note, w=10.7, scalebar=False)
    SL.north_arrow(s, 14.5, 14.2); SL.north_arrow(s, 14.5, 3.2)
