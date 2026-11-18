import math, sys
from cadkit import Sheet, fmt_ftin, text_w
from plan_engine import (Plan, dim_chain, bubble, hex_tag, circle_tag, diamond_tag, room_tag, para, table, WALL_T)

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
s = Sheet(origin=(3.6, 19.75))
p = Plan(s, 60, 50)
F = 12.0

# ------------------------------------------------------------------ spaces (feet)
SP = p.space
# Unit A
SP("A107", "A", "A107", [(0, 0, 14, 13.5)], "PRIMARY\nBEDROOM", "A107", (7, 7.2))
SP("A108", "A", "A108", [(14, 0, 11, 8.5)], "ROLL-IN\nBATH", "A108", (21.6, 5.6))
SP("A109", "A", "A109", [(14, 8.5, 5, 5)], "WIC", "A109", (16.5, 11.6))
SP("A110", "A", "A110", [(19, 8.5, 6, 5)], "LAUNDRY", "A110", (22, 12.2), area=False)
SP("A111", "A", "A111", [(0, 13.5, 3.5, 4)], None, None)
SP("A104", "A", "AO", [(3.5, 13.5, 21.5, 4), (12, 17.5, 5, 7.5), (12, 25, 3, 3)], "HALL", "A104", (17.6, 15.7), area=False)
SP("A105", "A", "A105", [(0, 17.5, 12, 8), (6, 25.5, 6, 2.5)], "BEDROOM 2", "A105", (6, 21.4))
SP("A112", "A", "A112", [(0, 25.5, 6, 2.5)], None, None)
SP("A106", "A", "A106", [(17, 17.5, 8, 7.5)], "HALL BATH", "A106", (20.6, 22.1), area=False)
SP("A102", "A", "AO", [(0, 28, 15, 9)], "DINING", "A102", (7.5, 32.4))
SP("A103", "A", "AO", [(15, 25, 10, 12)], "KITCHEN", "A103", (19.3, 29.4))
SP("A101", "A", "AO", [(0, 37, 25, 13)], "LIVING", "A101", (11.5, 43.0))
# Unit B
SP("B107", "B", "B107", [(46, 0, 14, 13.5)], "PRIMARY\nBEDROOM", "B107", (53, 7.2))
SP("B108", "B", "B108", [(35, 0, 11, 8.5)], "PRIMARY\nBATH", "B108", (41.0, 4.4))
SP("B109", "B", "B109", [(41, 8.5, 5, 5)], "WIC", "B109", (43.5, 11.6))
SP("B110", "B", "B110", [(35, 8.5, 6, 5)], "LAUNDRY", "B110", (38, 12.2), area=False)
SP("B111", "B", "B111", [(56.5, 13.5, 3.5, 4)], None, None)
SP("B104", "B", "BO", [(35, 13.5, 21.5, 4), (43, 17.5, 5, 7.5), (45, 25, 3, 3)], "HALL", "B104", (42.4, 15.7), area=False)
SP("B105", "B", "B105", [(48, 17.5, 12, 8), (48, 25.5, 6, 2.5)], "BEDROOM 2", "B105", (54, 21.4))
SP("B113", "B", "B113", [(54, 25.5, 6, 2.5)], None, None)
SP("B106", "B", "B106", [(35, 17.5, 8, 7.5)], "HALL BATH", "B106", (39.4, 22.1), area=False)
SP("B102", "B", "BO", [(45, 28, 15, 9)], "DINING", "B102", (52.5, 32.4))
SP("B103", "B", "BO", [(35, 25, 10, 12)], "KITCHEN", "B103", (40.7, 29.4))
SP("B101", "B", "BO", [(35, 37, 15, 13)], "LIVING", "B101", (42.0, 41.6))
SP("B112", "B", "B112", [(52.5, 37, 7.5, 13), (50, 42.5, 2.5, 7.5)], "BEDROOM 3", "B112", (56.0, 41.2))
SP("B114", "B", "B114", [(50, 37, 2.5, 5.5)], None, None)
# Core (common)
SP("CH1", "C", "CH1", [(25, 0, 3, 9)], None, None)
SP("CH2", "C", "CH2", [(32, 0, 3, 9)], None, None)
SP("102", "C", "STO", [(28, 0, 4, 9), (25, 9, 10, 11)], "HOUSE\nSTORAGE", "102", (30, 14.3))
SP("CH3", "C", "CH3", [(25, 20, 3, 3.5)], None, None)
SP("CH4", "C", "CH4", [(32, 20, 3, 3.5)], None, None)
SP("ENC", "C", "ENC", [(28, 20, 4, 3.5)], None, None)
SP("100", "C", "CORE", [(25, 23.5, 10, 22.5), (25, 46, 6.75, 4)], "SHARED\nENTRY", "100", (28.6, 41.6), area=False)
SP("103", "C", "RSR", [(31.75, 46, 3.25, 4)], None, None)

p.build_walls(west_type="W2")

# ------------------------------------------------------------------ openings
D = p.door
D((27.75, 50), (31.25, 50), -1, "101")
D((31.75, 49.0), (31.75, 46.5), -1, "102")
D((28.5, 0), (31.5, 0), -1, "103")
D((25, 45.5), (25, 42.5), -1, "110")
D((10.5, 13.5), (7.5, 13.5), -1, "111")
D((14, 2.5), (14, 5.5), -1, "112")
D((14, 9.5), (14, 12.5), -1, "113")
D((20.5, 13.5), (23.5, 13.5), 1, "114", kind="bifold")
D((3.5, 14), (3.5, 17), 1, "115", kind="bifold")
D((12, 19), (12, 22), -1, "116")
D((17, 23), (17, 20), -1, "117")
D((0.75, 25.5), (5.25, 25.5), 1, "118", kind="bypass")
D((35, 45.5), (35, 42.5), 1, "120")
D((49.5, 13.5), (52.5, 13.5), -1, "121")
D((46, 2.5), (46, 5.5), 1, "122")
D((46, 9.5), (46, 12.5), 1, "123")
D((36.5, 13.5), (39.5, 13.5), 1, "124", kind="bifold")
D((56.5, 14), (56.5, 17), -1, "125", kind="bifold")
D((48, 19), (48, 22), 1, "126")
D((43, 23), (43, 20), 1, "127")
D((50, 45.5), (50, 42.5), 1, "128")
D((54.75, 25.5), (59.25, 25.5), 1, "129", kind="bypass")
D((52.5, 37.5), (52.5, 42.0), 1, "130", kind="bypass")

Wn = p.window
for side, a, b, t in [("N", 4, 10, "A"), ("N", 50, 56, "A"),
                      ("W", 21.25, 24.25, "B"), ("W", 31, 34, "B"), ("W", 42, 45, "C"),
                      ("S", 9.5, 15.5, "D"), ("S", 39.5, 45.5, "D"), ("S", 52, 58, "A"),
                      ("E", 3.75, 9.75, "A"), ("E", 19.75, 25.75, "A"), ("E", 29.5, 35.5, "D"), ("E", 40.5, 46.5, "A")]:
    Wn(side, a, b, t)

# ------------------------------------------------------------------ fixtures & casework (model inches)
def r_(x, y, w, h, layer="A-FLOR-FIXT", lw="f", dash=None, fill=None):
    s.rect(x * F, y * F, w * F, h * F, layer=layer, lw=lw, space="m", dash=dash, fill=fill)

def L(x1, y1, x2, y2, layer="A-FLOR-FIXT", lw="f", dash=None):
    s.line((x1 * F, y1 * F), (x2 * F, y2 * F), layer=layer, lw=lw, space="m", dash=dash)

def C(x, y, r, layer="A-FLOR-FIXT", lw="f", dash=None):
    s.circle((x * F, y * F), r * F, layer=layer, lw=lw, space="m", dash=dash)

def T(x, y, t, h=0.055, layer="A-FLOR-FIXT", rot=0):
    s.text((x * F, y * F), t, h, layer=layer, space="m", valign="m", rot=rot)

def ellipse(cx, cy, rx, ry, layer="A-FLOR-FIXT"):
    pts = [((cx + rx * math.cos(a)) * F, (cy + ry * math.sin(a)) * F) for a in [i * math.pi / 18 for i in range(36)]]
    s.pline(pts, closed=True, layer=layer, lw="f", space="m")

def toilet(x, y, facing):
    """x,y = wall point at center of fixture; facing = direction bowl points ('S','N','E','W')."""
    if facing in ("S", "N"):
        sg = 1 if facing == "S" else -1
        ty = y if sg > 0 else y - 0.75
        r_(x - 0.85, ty, 1.7, 0.75)
        ellipse(x, y + sg * (0.75 + 0.95), 0.62, 0.95)
    else:
        sg = 1 if facing == "E" else -1
        tx = x if sg > 0 else x - 0.75
        r_(tx, y - 0.85, 0.75, 1.7)
        ellipse(x + sg * (0.75 + 0.95), y, 0.95, 0.62)

def lav(x, y, w, d, facing):
    r_(x, y, w, d)
    cx, cy = x + w / 2, y + d / 2
    ellipse(cx, cy, 0.55 if facing in "NS" else 0.42, 0.42 if facing in "NS" else 0.55)

def tub(x, y, w, d):
    r_(x, y, w, d, lw="l")
    s.rect((x + 0.25) * F, (y + 0.25) * F, (w - 0.5) * F, (d - 0.5) * F, layer="A-FLOR-FIXT", lw="f", space="m")
    C(x + w - 0.6, y + d / 2, 0.12)

def rollin(x, y, w, d, drain_y):
    r_(x, y, w, d, lw="l")
    L(x + 0.1, drain_y, x + w - 0.1, drain_y, lw="l")
    L(x + 0.1, drain_y + 0.25, x + w - 0.1, drain_y + 0.25, lw="f")
    T(x + w / 2, y + d / 2 - 0.3, "ROLL-IN SHOWER", 0.05)
    T(x + w / 2, y + d / 2 + 0.15, "NO CURB", 0.045)
    T(x + w / 2, drain_y - 0.25, "TRENCH DRAIN", 0.042)
    L(x + w - 0.3, y + 0.3, x + w - 0.3, y + 2.2, lw="l")  # grab bar
    r_(x + 0.15, y + 0.9, 1.3, 1.3, dash="HIDDEN")         # fold-down seat

def washer_dryer(x, y, flip=False):
    for i, lab in enumerate(("W", "D") if not flip else ("D", "W")):
        r_(x + i * 2.5, y, 2.4, 2.4)
        C(x + i * 2.5 + 1.2, y + 1.3, 0.85)
        T(x + i * 2.5 + 1.2, y + 1.3, lab, 0.06)

def wh(x, y):
    C(x, y, 0.85, lw="l"); T(x, y, "WH", 0.06)

def turning(x, y):
    C(x, y, 2.5, layer="A-ANNO-NPLT", dash="HIDDEN")

# Unit A — roll-in bath (Type A)
rollin(19.4, 0.62, 5.0, 3.2, 3.55)
toilet(15.4, 0.62, "S")
lav(14.4, 6.7, 2.4, 1.55, "N")
turning(19.6, 5.4)
L(14.45, 3.6, 14.45, 6.2, lw="l")  # grab bar side
washer_dryer(19.4, 8.85)
r_(14.4, 8.9, 0.2, 4.2, dash="HIDDEN")  # WIC shelf
L(14.4 + 1.2, 8.9, 14.4 + 1.2, 13.1, dash="HIDDEN")
wh(1.75, 15.5)
tub(17.3, 17.75, 5.0, 2.6)
toilet(21.5, 24.8, "N")
lav(17.5, 23.25, 2.0, 1.5, "S")
# bed 2 closet rod
L(0.6, 26.75, 5.4, 26.75, dash="HIDDEN")
# Kitchen A
r_(17.2, 25.2, 24.6 - 17.2, 2.0, layer="A-FLOR-CASE", lw="l")
r_(22.6, 27.2, 2.0, 7.5, layer="A-FLOR-CASE", lw="l")
L(17.2, 26.3, 24.6, 26.3, layer="A-FLOR-OVHD", dash="HIDDEN")
L(23.5, 25.2, 23.5, 34.7, layer="A-FLOR-OVHD", dash="HIDDEN")
r_(17.3, 25.3, 2.4, 2.4, lw="l"); T(18.5, 26.5, "REF", 0.055)
r_(19.95, 25.35, 2.5, 1.5); r_(20.08, 25.5, 1.08, 1.2); r_(21.28, 25.5, 1.05, 1.2); T(21.2, 27.1, "SINK", 0.045)
r_(22.6, 27.25, 2.0, 2.0, dash="HIDDEN"); T(23.6, 28.25, "DW", 0.055)
for cy in (30.75, 31.85):
    for cx in (23.15, 24.05):
        C(cx, cy, 0.35)
r_(22.6, 30.05, 2.0, 2.5, lw="l"); T(21.95, 31.3, "RANGE", 0.045, rot=90)
r_(22.6, 33.05, 2.0, 1.5, dash="HIDDEN"); T(23.6, 33.8, "T/R", 0.05)
turning(19.6, 31.2)
# Unit B
tub(35.62, 0.62, 5.0, 2.6)
toilet(45.75, 7.0, "W")
lav(38.5, 6.75, 2.6, 1.55, "S")
washer_dryer(35.62, 8.85)
r_(45.4, 8.9, 0.2, 4.2, dash="HIDDEN")
L(45.4 - 1.2, 8.9, 45.4 - 1.2, 13.1, dash="HIDDEN")
wh(58.25, 15.5)
tub(35.62, 17.75, 5.0, 2.6)
toilet(37.5, 24.8, "N")
lav(40.5, 23.25, 2.0, 1.5, "S")
L(54.6, 26.75, 59.4, 26.75, dash="HIDDEN")
L(51.25, 37.6, 51.25, 41.9, dash="HIDDEN")
# Kitchen B (mirror)
r_(35.4, 25.2, 43.0 - 0.2 - 35.4, 2.0, layer="A-FLOR-CASE", lw="l")
r_(35.4, 27.2, 2.0, 7.5, layer="A-FLOR-CASE", lw="l")
L(35.4, 26.3, 42.8, 26.3, layer="A-FLOR-OVHD", dash="HIDDEN")
L(36.5, 25.2, 36.5, 34.7, layer="A-FLOR-OVHD", dash="HIDDEN")
r_(40.3, 25.3, 2.4, 2.4, lw="l"); T(41.5, 26.5, "REF", 0.055)
r_(37.55, 25.35, 2.5, 1.5); r_(37.68, 25.5, 1.08, 1.2); r_(38.88, 25.5, 1.05, 1.2); T(38.8, 27.1, "SINK", 0.045)
r_(35.4, 27.25, 2.0, 2.0, dash="HIDDEN"); T(36.4, 28.25, "DW", 0.055)
for cy in (30.75, 31.85):
    for cx in (35.95, 36.85):
        C(cx, cy, 0.35)
r_(35.4, 30.05, 2.0, 2.5, lw="l"); T(38.05, 31.3, "RANGE", 0.045, rot=90)
r_(35.4, 33.05, 2.0, 1.5, dash="HIDDEN"); T(36.4, 33.8, "T/R", 0.05)
turning(40.4, 31.2)

# Stair (west run up, landing north, east run above)
tread = 11 / 12
y_top, n = 27.5, 9
for i in range(n + 1):
    yy = y_top + i * tread
    L(25.4, yy, 29.4, yy, layer="A-FLOR-STRS", lw="f" if i < n else "l")
for i in range(n + 1):
    yy = y_top + i * tread
    L(30.6, yy, 34.6, yy, layer="A-FLOR-STRS", lw="f", dash="HIDDEN")
L(25.4, y_top, 25.4, y_top + n * tread, layer="A-FLOR-STRS", lw="l")
L(29.4, y_top, 29.4, y_top + n * tread, layer="A-FLOR-STRS", lw="l")
L(30.6, y_top, 30.6, y_top + n * tread, layer="A-FLOR-STRS", lw="f", dash="HIDDEN")
L(34.6, y_top, 34.6, y_top + n * tread, layer="A-FLOR-STRS", lw="f", dash="HIDDEN")
r_(25.4, 23.9, 9.2, 3.6, layer="A-FLOR-OVHD", dash="HIDDEN")  # landing above
L(29.75, 27.5, 29.75, 35.75, layer="A-FLOR-STRS", lw="l"); L(30.25, 27.5, 30.25, 35.75, layer="A-FLOR-STRS", lw="l")  # guards
# cut line
L(25.4, 31.9, 29.4, 30.6, layer="A-FLOR-STRS", lw="l")
# arrow up
L(27.4, 35.4, 27.4, 28.2, layer="A-FLOR-STRS", lw="f")
s.pline([(27.15 * F, 28.8 * F), (27.4 * F, 28.2 * F), (27.65 * F, 28.8 * F)], layer="A-FLOR-STRS", lw="f", space="m")
T(27.4, 36.15, "UP", 0.07, layer="A-ANNO-TEXT")
T(32.6, 32.2, "STAIR", 0.055, layer="A-ANNO-TEXT"); T(32.6, 32.75, "ABOVE", 0.055, layer="A-ANNO-TEXT")
T(30.0, 25.6, "LANDING ABOVE", 0.05, layer="A-ANNO-TEXT")
T(30, 21.75, "ENCLOSED", 0.05, layer="A-ANNO-TEXT"); T(30, 22.3, "NO STORAGE", 0.045, layer="A-ANNO-TEXT")
# chases hatch
for (x, y, w, h) in [(25, 0, 3, 9), (32, 0, 3, 9), (25, 20, 3, 3.5), (32, 20, 3, 3.5)]:
    x0, y0, x1, y1 = x + 0.45, y + 0.45, x + w - 0.3, y + h - 0.3
    k = 0.0
    while k < (x1 - x0) + (y1 - y0):
        ax, ay = x0 + k, y0
        bx, by = x0, y0 + k
        if ax > x1:
            ay += ax - x1; ax = x1
        if by > y1:
            bx += by - y1; by = y1
        L(ax, ay, bx, by, layer="A-WALL-PATT", lw="xf")
        k += 0.5
    T(x + w / 2, y + h / 2, "CH", 0.06, layer="A-ANNO-TEXT")
# fire riser
C(33.4, 48.0, 0.35, lw="l"); T(33.4, 47.1, "FIRE", 0.045, layer="A-ANNO-TEXT"); T(33.4, 49.0, "RISER", 0.045, layer="A-ANNO-TEXT")
# electric panels (recessed not in W1): show on interior partitions
for (x, y, lab) in [(14.3, 15.0, "EP-A"), (45.7, 15.0, "EP-B")]:
    pass

# ------------------------------------------------------------------ draw walls/openings
p.draw_walls()
p.draw_openings()

# ------------------------------------------------------------------ grids
GX = [(0, "1"), (25, "2"), (35, "3"), (60, "4")]
GY = [(0, "A"), (50, "B")]
top = s.m2p(0, 0)[1]; bot = s.m2p(0, 600)[1]; lft = s.m2p(0, 0)[0]; rgt = s.m2p(720, 0)[0]
for x, lab in GX:
    px = s.m2p(x * F, 0)[0]
    s.line((px, top + 1.55), (px, top + 0.08), layer="A-GRID", lw="xf")
    s.line((px, bot - 0.08), (px, bot - 1.55), layer="A-GRID", lw="xf")
    bubble(s, (px, top + 1.75), lab); bubble(s, (px, bot - 1.75), lab)
for y, lab in GY:
    py = s.m2p(0, y * F)[1]
    s.line((lft - 1.55, py), (lft - 0.08, py), layer="A-GRID", lw="xf")
    s.line((rgt + 0.08, py), (rgt + 1.25, py), layer="A-GRID", lw="xf")
    bubble(s, (lft - 1.75, py), lab); bubble(s, (rgt + 1.45, py), lab)

# ------------------------------------------------------------------ dimensions (model inches)
fi = lambda v: v * F
dim_chain(s, [fi(v) for v in (0, 7, 25, 30, 35, 53, 60)], 0, "h", 0.55)
dim_chain(s, [fi(v) for v in (0, 25, 35, 60)], 0, "h", 0.9)
dim_chain(s, [fi(v) for v in (0, 60)], 0, "h", 1.25)
dim_chain(s, [fi(v) for v in (0, 12.5, 25, 29.5, 35, 42.5, 55, 60)], 600, "h", -0.55)
dim_chain(s, [fi(v) for v in (0, 25, 35, 60)], 600, "h", -0.9)
dim_chain(s, [fi(v) for v in (0, 60)], 600, "h", -1.25)
dim_chain(s, [fi(v) for v in (0, 22.75, 32.5, 43.5, 50)], 0, "v", -0.55)
dim_chain(s, [fi(v) for v in (0, 13.5, 17.5, 28, 37, 50)], 0, "v", -0.9)
dim_chain(s, [fi(v) for v in (0, 50)], 0, "v", -1.25)
dim_chain(s, [fi(v) for v in (0, 6.75, 22.75, 32.5, 43.5, 50)], 720, "v", 0.55)
dim_chain(s, [fi(v) for v in (0, 50)], 720, "v", 0.9)
# interior strings
def idim_h(xs, y):
    dim_chain(s, [fi(v) for v in xs], fi(y), "h", 0.0, ext_from=None)
def idim_v(ys, x):
    dim_chain(s, [fi(v) for v in ys], fi(x), "v", 0.0)
idim_v([13.5, 17.5], 13.0)
idim_v([13.5, 17.5], 47.0)
idim_h([15, 25], 36.3)
s.text(s.m2p(fi(13.35), fi(16.9)), "42\" MIN. CLR.", 0.05, layer="A-ANNO-DIMS", align="l")

# ------------------------------------------------------------------ tags
for sp in p.spaces:
    if sp["name"]:
        area = None
        if sp["area"]:
            a = sum(w * h for (_, _, w, h) in sp["rects"])
            area = f"{int(round(a))} SF"
        room_tag(s, s.m2p(sp["tag_at"][0] * F, sp["tag_at"][1] * F), sp["name"], sp["number"], area)
# small rooms labels
for (x, y, t) in [(3.0, 27.3, "CL"), (57.0, 27.3, "CL"), (51.25, 40.2, "CL")]:
    s.text(s.m2p(x * F, y * F), t, 0.06, layer="A-AREA-IDEN", font="Helvetica-Bold", valign="m")

# door tags
for d in p.doors:
    (hx, hy), (sx, sy) = d["h"], d["st"]
    mx, my = (hx + sx) / 2, (hy + sy) / 2
    off = 20 if d["kind"] == "swing" else 14
    sd = d["d"] if d["kind"] == "swing" else 1
    if d["o"] == "h":
        c = s.m2p(mx, my - sd * off)
    else:
        c = s.m2p(mx - sd * off, my)
    OVR = {"113": (11.6, 11.0), "123": (48.4, 11.0), "112": (12.6, 4.0), "122": (47.4, 4.0),
           "114": (22.0, 15.9), "124": (38.0, 15.9), "115": (5.0, 15.5), "125": (55.0, 15.5),
           "117": (15.6, 21.5), "127": (44.4, 21.5)}
    if d["tag"] in OVR:
        c = s.m2p(OVR[d["tag"]][0] * F, OVR[d["tag"]][1] * F)
    if d["tag"] in ("101",):
        c = s.m2p(mx, my + 22)
    if d["tag"] in ("103",):
        c = s.m2p(mx, my - 22)
    circle_tag(s, c, d["tag"])
# window tags (outside face)
for w in p.windows:
    m = (w["a"] + w["b"]) / 2
    if w["side"] == "N":
        c = s.m2p(m, -16)
    elif w["side"] == "S":
        c = s.m2p(m, 600 + 16)
    elif w["side"] == "W":
        c = s.m2p(-16, m)
    else:
        c = s.m2p(720 + 16, m)
    diamond_tag(s, c, w["tag"])

# wall type tags with leaders
def wtag(xm, ym, label, dx, dy):
    a = s.m2p(xm * F, ym * F)
    b = (a[0] + dx, a[1] + dy)
    s.line(a, b, layer="A-ANNO-IDEN", lw="xf")
    hex_tag(s, (b[0] + (0.11 if dx > 0 else -0.11), b[1]), label)
hex_tag(s, s.m2p(25 * F, 2.8 * F), "W1"); hex_tag(s, s.m2p(35 * F, 2.8 * F), "W1")
hex_tag(s, s.m2p(25 * F, 47.0 * F), "W1"); hex_tag(s, s.m2p(35 * F, 47.0 * F), "W1")
hex_tag(s, s.m2p(0.35 * F, 6.0 * F), "W2"); hex_tag(s, s.m2p(0.35 * F, 38.0 * F), "W2")
hex_tag(s, s.m2p(59.7 * F, 32.5 * F + 0), "EXT".replace("EXT", "E1"))
hex_tag(s, s.m2p(20.0 * F, 49.7 * F), "E1"); hex_tag(s, s.m2p(40.0 * F, 0.3 * F), "E1")
hex_tag(s, s.m2p(14.0 * F, 7.4 * F), "P1"); hex_tag(s, s.m2p(46.0 * F, 7.4 * F), "P1")

# section marks
def section(x_ft_or_none, y_ft_or_none, num, sheet_ref):
    if y_ft_or_none is not None:
        py = s.m2p(0, y_ft_or_none * F)[1]
        for xx, side in ((lft - 2.3, -1), (rgt + 2.05, 1)):
            s.line((xx - side * 0.0, py), (xx - side * 0.55, py), layer="A-ANNO-SYMB", lw="m")
            s.circle((xx, py), 0.2, layer="A-ANNO-SYMB", lw="l", fill=1.0)
            s.line((xx - 0.2, py), (xx + 0.2, py), layer="A-ANNO-SYMB", lw="xf")
            s.text((xx, py + 0.05), num, 0.08, layer="A-ANNO-SYMB", font="Helvetica-Bold")
            s.text((xx, py - 0.13), sheet_ref, 0.058, layer="A-ANNO-SYMB")
            s.pline([(xx - 0.2, py), (xx, py - 0.32), (xx + 0.2, py)], layer="A-ANNO-SYMB", lw="l", fill=0.1, closed=True)
    else:
        px = s.m2p(x_ft_or_none * F, 0)[0]
        for yy, side in ((top + 2.3, 1), (bot - 2.3, -1)):
            s.circle((px, yy), 0.2, layer="A-ANNO-SYMB", lw="l", fill=1.0)
            s.line((px - 0.2, yy), (px + 0.2, yy), layer="A-ANNO-SYMB", lw="xf")
            s.text((px, yy + 0.05), num, 0.08, layer="A-ANNO-SYMB", font="Helvetica-Bold")
            s.text((px, yy - 0.13), sheet_ref, 0.058, layer="A-ANNO-SYMB")
            s.pline([(px - 0.2, yy), (px + 0.32, yy), (px, yy + 0.2)], layer="A-ANNO-SYMB", lw="l", fill=0.1, closed=True)
            s.line((px, yy - side * 0.2), (px, yy - side * 0.55), layer="A-ANNO-SYMB", lw="m")
section(None, 22.5, "1", "A-301")
section(27.5, None, "2", "A-301")

# enlarged plan callouts
def callout(x, y, w, h, num, ref, at):
    s.rect(x * F, y * F, w * F, h * F, layer="A-ANNO-SYMB", lw="f", space="m", dash=[6, 3])
    a = s.m2p(at[0] * F, at[1] * F)
    c = (a[0] + at[2], a[1] + at[3])
    s.line(a, (c[0] - 0.18, c[1] - 0.06), layer="A-ANNO-SYMB", lw="xf")
    s.circle(c, 0.18, layer="A-ANNO-SYMB", lw="l", fill=1.0)
    s.line((c[0] - 0.18, c[1]), (c[0] + 0.18, c[1]), layer="A-ANNO-SYMB", lw="xf")
    s.text((c[0], c[1] + 0.04), num, 0.075, layer="A-ANNO-SYMB", font="Helvetica-Bold")
    s.text((c[0], c[1] - 0.12), ref, 0.052, layer="A-ANNO-SYMB")
callout(14.25, 0.75, 10.4, 7.6, "3", "A-402", (24.65, 7.7, -0.3, 0.0))
callout(15.2, 25.2, 9.55, 11.6, "1", "A-401", (15.2, 36.8, 0.3, -0.3))

# north arrow + drawing title
nx, ny = 17.6, 4.3
s.circle((nx, ny), 0.38, layer="A-ANNO-SYMB", lw="l")
s.pline([(nx, ny + 0.55), (nx - 0.17, ny - 0.25), (nx, ny - 0.08), (nx + 0.17, ny - 0.25)], closed=True, layer="A-ANNO-SYMB", lw="l", fill=0.08)
s.text((nx, ny + 0.62), "N", 0.13, layer="A-ANNO-SYMB", font="Helvetica-Bold")
tx, ty = 1.35, 4.05
s.circle((tx + 0.35, ty + 0.2), 0.32, layer="A-ANNO-TEXT", lw="m", fill=1.0)
s.line((tx + 0.03, ty + 0.2), (tx + 0.67, ty + 0.2), layer="A-ANNO-TEXT", lw="f")
s.text((tx + 0.35, ty + 0.28), "1", 0.15, font="Helvetica-Bold")
s.text((tx + 0.35, ty + 0.03), "A-101.1", 0.07)
s.text((tx + 0.85, ty + 0.27), "GROUND FLOOR PLAN — MODEL 1 STACKED BIG HOUSE", 0.19, font="Helvetica-Bold", align="l")
s.line((tx + 0.85, ty + 0.18), (tx + 13.0, ty + 0.18), layer="A-ANNO-TEXT", lw="h")
s.text((tx + 0.85, ty - 0.02), "SCALE: 1/4\" = 1'-0\"      UNITS A + B  ·  COMMON CORE  ·  GROSS 3,000 SF THIS LEVEL", 0.09, align="l")
# scale bar
sbx, sby = tx + 9.6, ty - 0.08
for i in range(4):
    s.rect(sbx + i * 0.25, sby, 0.25, 0.06, layer="A-ANNO-TEXT", lw="xf", fill=0.1 if i % 2 == 0 else 1.0)
s.rect(sbx + 1.0, sby, 1.0, 0.06, layer="A-ANNO-TEXT", lw="xf", fill=1.0)
for v, lab in ((0, "0"), (0.5, "2'"), (1.0, "4'"), (2.0, "8'")):
    s.text((sbx + v, sby + 0.1), lab, 0.06)

# ------------------------------------------------------------------ notes columns
X1, X2, YT = 21.15, 26.55, 23.2
H = 0.075

def head(x, y, t, w=5.1):
    s.text((x, y), t, 0.1, font="Helvetica-Bold", align="l")
    s.line((x, y - 0.06), (x + w, y - 0.06), lw="l")
    return y - 0.24

y = head(X1, YT, "GENERAL NOTES — FLOOR PLANS")
notes = [
    "Do not scale drawings. Exterior dimensions are to outside face of exterior wall finish; interior dimensions are to centerline of partitions; grid lines are at outside face of exterior walls and centerline of W1 walls, unless noted otherwise.",
    "Wall types per legend this sheet. W1 and W2 are 1-hour fire-resistance-rated assemblies (G-005). Run W1 continuous from top of slab to underside of roof deck; seal all penetrations with a listed firestop system (D-002).",
    "Building is fully sprinklered per NFPA 13R. Provide interconnected smoke alarms in each sleeping room, outside each sleeping area and on each story; CO alarms per IFC 915.",
    "Every bedroom has an emergency escape and rescue opening: 5.0 SF min. net clear at grade floor, 24\" min. clear height, 20\" min. clear width, sill 44\" max. A.F.F. (IBC 1031).",
    "Unit A is an ICC A117.1-2009 Type A unit; Unit B is a Type B unit. Maintain clear floor spaces and 5'-0\" turning circles shown dashed. Unit A doors: lever hardware, 32\" min. clear opening, zero-step thresholds.",
    "Unit entry doors 110 and 120: 20-minute, self-closing, positive-latching, smoke- and draft-control (S-label). Confirm corridor reading of the shared entry with plan review (G-005).",
    "No plumbing, recessed boxes or ductwork in W1 walls. Wet rooms stack over wet rooms; drains and vents run in chases CH. Do not cut or notch joists, trusses or beams (X-101).",
    "Kitchens: pull-out trash and recycling compartment with two 7-gallon bins (T/R) per Scottsdale IBC 1211. Range hoods recirculating or ducted up into the soffit; no hood duct through W1.",
    "Provide 2x blocking for grab bars at every toilet, tub and shower. Unit A: install grab bars and a fold-down shower seat.",
    "Window sizes are nominal; verify rough openings with the manufacturer. West wall (W2, 7'-0\" to lot line): unprotected openings limited to 45 SF per story; 42 SF shown.",
    "Common stair: 4'-0\" clear runs, 7\" max. risers, 11\" min. treads, handrails both sides at 34\"–38\", 42\" guards at the well. Verify riser count against final floor-to-floor height.",
    "Ceiling height 9'-0\" A.F.F. unless noted. Gross floor area this level 3,000 SF; Units A and B 1,250 SF each.",
]
for i, n in enumerate(notes, 1):
    y = para(s, X1, y, n, 5.1, H, num=f"{i}.")

y -= 0.12
y = head(X1, y, "WALL TYPES")
wall_legend = [
    ("W1", 0.32, "UNIT SEPARATION — 1 HR. Double 2x4 @ 16\" o.c. with 1\" air space, 3½\" batts each stud row, 5/8\" Type X GWB each face (UL U341, verify). ±9½\". To roof deck."),
    ("W2", 0.32, "EXTERIOR — 1 HR, RATED BOTH SIDES (west wall, 7'-0\" to lot line). 2x6 @ 16\", 5/8\" Type X exterior gypsum sheathing, WRB, 7/8\" three-coat stucco, R-21 batts, 5/8\" Type X GWB."),
    ("E1", 0.62, "EXTERIOR. 2x6 @ 16\", 7/16\" OSB, WRB, 7/8\" three-coat stucco, R-21 batts, 1/2\" GWB."),
    ("P1", 0.70, "INTERIOR PARTITION. 2x4 @ 16\", 1/2\" GWB each face; moisture-resistant board at wet walls, cement board at tub and shower surrounds."),
]
for tag, g, txt in wall_legend:
    s.rect(X1, y - 0.12, 0.42, 0.18, layer="A-ANNO-TEXT", lw="l", fill=g)
    hex_tag(s, (X1 + 0.7, y - 0.03), tag)
    y = para(s, X1 + 0.95, y, txt, 4.15, H)

# column 2: schedules
y2 = head(X2, YT, "DOOR SCHEDULE", 5.25)
DCOLS = [("NO.", 0.38, "c"), ("LOCATION", 1.42, "l"), ("SIZE", 0.95, "c"), ("TYPE", 0.38, "c"), ("RATING", 0.6, "c"), ("HARDWARE", 0.82, "l"), ("NOTE", 0.7, "l")]
drows = [
    ("101", "SHARED ENTRY", "3'-6\" x 8'-0\"", "A", "—", "ENTRY / CLOSER", "1,2"),
    ("102", "FIRE RISER", "2'-6\" x 6'-8\"", "B", "—", "STOREROOM", "3"),
    ("103", "HOUSE STORAGE", "3'-0\" x 6'-8\"", "A", "—", "STOREROOM", "4"),
    ("110", "UNIT A ENTRY", "3'-0\" x 8'-0\"", "C", "20 MIN S", "ENTRY / CLOSER", "1,5"),
    ("111", "A PRIMARY BEDROOM", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", "1"),
    ("112", "A ROLL-IN BATH", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", "1"),
    ("113", "A WIC", "3'-0\" x 8'-0\"", "D", "—", "PASSAGE", "1"),
    ("114", "A LAUNDRY", "(2) 1'-6\" x 8'-0\"", "F", "—", "PASSAGE", "1"),
    ("115", "A WATER HEATER", "(2) 1'-6\" x 8'-0\"", "F", "—", "PASSAGE", "1,6"),
    ("116", "A BEDROOM 2", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", "1"),
    ("117", "A HALL BATH", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", "1"),
    ("118", "A BED 2 CLOSET", "(2) 2'-6\" x 8'-0\"", "E", "—", "PULLS", ""),
    ("120", "UNIT B ENTRY", "3'-0\" x 8'-0\"", "C", "20 MIN S", "ENTRY / CLOSER", "5"),
    ("121", "B PRIMARY BEDROOM", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", ""),
    ("122", "B PRIMARY BATH", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", ""),
    ("123", "B WIC", "3'-0\" x 8'-0\"", "D", "—", "PASSAGE", ""),
    ("124", "B LAUNDRY", "(2) 1'-6\" x 8'-0\"", "F", "—", "PASSAGE", ""),
    ("125", "B WATER HEATER", "(2) 1'-6\" x 8'-0\"", "F", "—", "PASSAGE", "6"),
    ("126", "B BEDROOM 2", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", ""),
    ("127", "B HALL BATH", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", ""),
    ("128", "B BEDROOM 3", "3'-0\" x 8'-0\"", "D", "—", "PRIVACY", ""),
    ("129", "B BED 2 CLOSET", "(2) 2'-6\" x 8'-0\"", "E", "—", "PULLS", ""),
    ("130", "B BED 3 CLOSET", "(2) 2'-6\" x 8'-0\"", "E", "—", "PULLS", ""),
]
y2 = table(s, X2, y2 + 0.04, DCOLS, drows, h=0.066, rowh=0.15)
y2 -= 0.12
for t in ["TYPES: A insulated fiberglass, exterior, 1¾\"; B hollow metal; C solid-core wood 1¾\", 20-min label; D solid-core wood flush, 1¾\"; E bypass, solid-core; F bi-fold, solid-core.",
          "NOTES: 1 Type A unit / accessible route: lever hardware, 32\" clear, max. 5 lbf opening force, ½\" max. threshold. 2 Zero-step entry. 3 Sign \"FIRE RISER\"; access per Scottsdale Fire. 4 Exterior, swings out. 5 Self-closing, smoke gasketing. 6 Combustion/make-up air per IFGC if gas option."]:
    y2 = para(s, X2, y2, t, 5.25, 0.068)
y2 -= 0.06
y2 = head(X2, y2, "WINDOW SCHEDULE", 5.25)
WCOLS = [("TYPE", 0.42, "c"), ("SIZE (W x H)", 0.98, "c"), ("OPERATION", 1.02, "l"), ("SILL A.F.F.", 0.72, "c"), ("EGRESS", 0.58, "c"), ("QTY", 0.38, "c"), ("LOCATION", 1.15, "l")]
wrows = [
    ("A", "6'-0\" x 4'-0\"", "HORIZ. SLIDER", "2'-6\"", "YES", "6", "BEDROOMS"),
    ("B", "3'-0\" x 5'-0\"", "SINGLE HUNG", "2'-0\"", "BED 2", "2", "WEST (W2)"),
    ("C", "3'-0\" x 4'-0\"", "SINGLE HUNG", "3'-0\"", "—", "1", "WEST (W2)"),
    ("D", "6'-0\" x 5'-0\"", "HORIZ. SLIDER", "2'-0\"", "—", "3", "LIVING / DINING"),
]
y2 = table(s, X2, y2 + 0.04, WCOLS, wrows, h=0.066, rowh=0.15)
y2 -= 0.12
y2 = para(s, X2, y2, "Dual-pane low-E vinyl or fiberglass, U-factor 0.40 max., SHGC 0.25 max. (IECC 2021, climate zone 2B). Safety glazing where required by IBC 2406. Egress windows: verify net clear opening with the manufacturer.", 5.25, 0.068)

y2 -= 0.06
y2 = head(X2, y2, "DESIGN-DEVELOPMENT COORDINATION (CHANGES FROM CONCEPT REV 1.4)", 5.25)
dd = [
    ("a.", "Bedroom doors 111 and 121 now swing into the bedrooms, not into the 4'-0\" hall."),
    ("b.", "Stair: 4'-0\" landing across both runs at the north end; chases CH at the landing shortened to 3'-6\"."),
    ("c.", "House storage 102 gets exterior door 103 on the rear wall; the old door under the landing had no headroom and is deleted."),
    ("d.", "OPEN — Site plan shows rear patios but no door from Units A/B. Confirm converting window A at each primary bedroom to a 6'-0\" sliding door."),
]
for n, t in dd:
    y2 = para(s, X2, y2, t, 5.25, 0.068, num=n)


# ---- symbols legend (col 1)
y -= 0.1
y = head(X1, y, "SYMBOLS")
sym = [
    (lambda c: circle_tag(s, c, "110"), "DOOR TAG \u2014 SEE DOOR SCHEDULE"),
    (lambda c: diamond_tag(s, c, "A"), "WINDOW TAG \u2014 SEE WINDOW SCHEDULE"),
    (lambda c: hex_tag(s, c, "W1"), "WALL TYPE TAG \u2014 SEE WALL TYPES"),
    (lambda c: bubble(s, c, "2", r=0.13), "GRID LINE"),
    (lambda c: (s.circle(c, 0.13, layer="A-ANNO-SYMB", lw="l", fill=1.0), s.line((c[0]-0.13, c[1]), (c[0]+0.13, c[1]), layer="A-ANNO-SYMB", lw="xf"), s.pline([(c[0]-0.13, c[1]), (c[0], c[1]-0.22), (c[0]+0.13, c[1])], layer="A-ANNO-SYMB", lw="l", fill=0.1, closed=True)), "BUILDING SECTION (NUMBER / SHEET)"),
    (lambda c: (s.circle(c, 0.13, layer="A-ANNO-SYMB", lw="l", fill=1.0), s.line((c[0]-0.13, c[1]), (c[0]+0.13, c[1]), layer="A-ANNO-SYMB", lw="xf")), "ENLARGED PLAN CALLOUT (NUMBER / SHEET)"),
    (lambda c: s.circle(c, 0.13, layer="A-ANNO-NPLT", lw="f", dash="HIDDEN"), "5'-0\" TURNING SPACE (TYPE A / TYPE B)"),
    (lambda c: s.line((c[0]-0.2, c[1]), (c[0]+0.2, c[1]), layer="A-FLOR-OVHD", lw="f", dash="HIDDEN"), "OVERHEAD / ABOVE (CABINETS, LANDING)"),
]
col = 0
yy0 = y
for i, (fn, label) in enumerate(sym):
    cx = X1 + 0.2 + (i % 2) * 2.6
    cy = yy0 - (i // 2) * 0.34
    fn((cx, cy - 0.02))
    s.text((cx + 0.28, cy - 0.05), label, 0.062, align="l")
y = yy0 - ((len(sym) + 1) // 2) * 0.34 - 0.1
y = head(X1, y, "ROOM TAG")
room_tag(s, (X1 + 0.6, y - 0.12), "ROOM NAME", "A101", "000 SF", h=0.08)
s.text((X1 + 1.3, y - 0.12), "Room number: unit letter + level + room. Areas are measured to wall centerlines and rounded.", 0.062, align="l")

# ---- area summary (col 2)
y2 -= 0.08
y2 = head(X2, y2, "AREA SUMMARY \u2014 GROUND FLOOR", 5.25)
ACOLS = [("SPACE", 2.45, "l"), ("BEDS / BATHS", 0.9, "c"), ("ACCESSIBILITY", 1.2, "c"), ("GROSS SF", 0.7, "c")]
arows = [("UNIT A (FLAT, OWNER OR RENTAL)", "2 BR / 2 BA", "TYPE A", "1,250"),
         ("UNIT B (FLAT, RENTAL)", "3 BR / 2 BA", "TYPE B", "1,250"),
         ("COMMON CORE (ENTRY, STAIR, STORAGE)", "\u2014", "ACCESSIBLE ROUTE", "500"),
         ("TOTAL THIS LEVEL", "", "", "3,000")]
y2 = table(s, X2, y2 + 0.04, ACOLS, arows, h=0.066, rowh=0.15)

# ------------------------------------------------------------------ border + title block
s.rect(0.5, 0.375, 35.25, 23.25, layer="A-ANNO-TTLB", lw="xh")
TB = 32.15
s.line((TB, 0.375), (TB, 23.625), layer="A-ANNO-TTLB", lw="h")
tw = 35.75 - TB
yy = 23.625
def tb_box(hgt, lines, title=None, big=None):
    global yy
    y0 = yy - hgt
    s.line((TB, y0), (35.75, y0), layer="A-ANNO-TTLB", lw="l")
    ty = yy - 0.18
    if title:
        s.text((TB + 0.12, ty), title, 0.062, font="Helvetica-Bold", align="l", color=None)
        ty -= 0.18
    for (t, h, f) in lines:
        s.text((TB + 0.12, ty), t, h, font=f, align="l")
        ty -= h * 1.6
    yy = y0
    return y0

tb_box(1.25, [("", 0.12, "Helvetica"), ("SCOTTSDALE", 0.2, "Helvetica-Bold"), ("FOURPLEX", 0.2, "Helvetica-Bold"), ("DIGNITY-BASED ATTAINABLE HOUSING", 0.068, "Helvetica")])
tb_box(1.0, [("MODEL 1 — STACKED BIG HOUSE", 0.085, "Helvetica-Bold"), ("SOUTH SCOTTSDALE, ARIZONA", 0.075, "Helvetica"), ("PARCEL / ADDRESS: TBD", 0.075, "Helvetica"), ("LOT: 80' x 125' TYPICAL", 0.075, "Helvetica")], "PROJECT")
tb_box(0.95, [("________________________", 0.075, "Helvetica"), ("", 0.075, "Helvetica"), ("________________________", 0.075, "Helvetica")], "OWNER / DEVELOPER")
tb_box(0.95, [("________________________", 0.075, "Helvetica"), ("", 0.075, "Helvetica"), ("________________________", 0.075, "Helvetica")], "ARCHITECT OF RECORD")
tb_box(0.95, [("STRUCTURAL: TBD", 0.068, "Helvetica"), ("MEP / FIRE PROTECTION: TBD", 0.068, "Helvetica"), ("CIVIL: TBD", 0.068, "Helvetica")], "CONSULTANTS")
# seal box
y0 = tb_box(3.0, [], "SEAL")
s.rect(TB + 0.5, y0 + 0.35, tw - 1.0, 2.2, layer="A-ANNO-TTLB", lw="f", dash="HIDDEN")
s.text((TB + tw / 2, y0 + 1.62), "DESIGN DEVELOPMENT", 0.1, font="Helvetica-Bold")
s.text((TB + tw / 2, y0 + 1.40), "NOT FOR CONSTRUCTION", 0.1, font="Helvetica-Bold", color=None)
s.text((TB + tw / 2, y0 + 1.15), "Not for permit, bidding or", 0.068)
s.text((TB + tw / 2, y0 + 1.02), "construction until sealed by", 0.068)
s.text((TB + tw / 2, y0 + 0.89), "an Arizona-registered", 0.068)
s.text((TB + tw / 2, y0 + 0.76), "design professional.", 0.068)
tb_box(1.05, [("2021 IBC · GROUP R-2 · TYPE V-B", 0.068, "Helvetica"), ("NFPA 13R · 1-HR UNIT SEPARATIONS", 0.068, "Helvetica"), ("CITY OF SCOTTSDALE AMENDMENTS", 0.068, "Helvetica"), ("ICC A117.1-2009 (TYPE A + TYPE B)", 0.068, "Helvetica")], "CODE BASIS")
# revisions
y0 = tb_box(1.55, [], "ISSUES / REVISIONS")
rv = [("1.4", "2026-11-14", "CONCEPT COORDINATION"), ("DD-1", "2026-11-17", "DESIGN DEVELOPMENT")]
ry = y0 + 1.15
for a, b, c_ in rv:
    s.text((TB + 0.12, ry), a, 0.066, align="l", font="Helvetica-Bold"); s.text((TB + 0.55, ry), b, 0.066, align="l"); s.text((TB + 1.35, ry), c_, 0.066, align="l")
    ry -= 0.17
for t in range(3):
    s.line((TB + 0.12, ry + 0.06), (35.6, ry + 0.06), layer="A-ANNO-TTLB", lw="xf"); ry -= 0.17
y0 = tb_box(1.25, [("PROJECT NO.   SF-M1", 0.068, "Helvetica"), ("DATE            2026-11-17", 0.068, "Helvetica"), ("SCALE           1/4\" = 1'-0\"", 0.068, "Helvetica"), ("DRAWN / CHK   — / —", 0.068, "Helvetica")], "")
y0 = tb_box(1.0, [("GROUND FLOOR", 0.14, "Helvetica-Bold"), ("PLAN", 0.14, "Helvetica-Bold")], "SHEET TITLE")
# sheet number fills rest
s.text((TB + 0.12, yy - 0.2), "SHEET", 0.062, font="Helvetica-Bold", align="l")
s.text((TB + tw / 2, 0.375 + 0.75), "A-101.1", 0.42, font="Helvetica-Bold")

s.to_pdf(f"{OUT}/A-101.1_Model1_Ground_Floor_Plan.pdf", title="A-101.1 Ground Floor Plan - Model 1", author="Scottsdale Fourplex")
s.to_dxf(f"{OUT}/A-101.1_Model1_Ground_Floor_Plan.dxf")
print("done", len(s.items), "entities")
