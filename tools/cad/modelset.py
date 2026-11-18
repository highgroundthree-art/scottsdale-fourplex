"""Model 2 and Model 3 model-specific sheets. usage: python3 modelset.py out 2|3 [sheet ...]"""
import math, sys
from reportlab.lib.colors import Color
from cadkit import Sheet
import cadkit
from gen_floor import View, window_rows
from views import vc_m2, vc_m3, vc_m3c
import sheetlib as SL
from plan_engine import table, para, dim_chain, bubble
import sheetkit
from sheetkit import Draw, notes, tbl, RED, BLUE, GREEN, ORANGE, NC, NC2, TOPY

OUT, M = sys.argv[1], int(sys.argv[2])
ONLY = set(sys.argv[3:])
F = 12.0
GRAY, TGRAY = Color(0.62, 0.62, 0.62), Color(0.45, 0.45, 0.45)
DATE = "2026-11-18"

# ============================================================== model data
if M == 2:
    INFO = dict(model_line="MODEL 2 — TOWNHOMES + SUITE", lot_line="LOT: ±66' x 152' DEEP (ASSUMED)", projno="SF-M2")
    NAME = "MODEL 2 — TOWNHOMES + OWNER SUITE"
    VIEWS = {"g": (vc_m2(1), 1, "GROUND FLOOR", 101), "u": (vc_m2(2), 2, "UPPER FLOOR", 201)}
    LAY_ALL = [("u", (1.6, 22.9), 64), ("g", (1.6, 14.75), 64)]
    LAY_G = [("g", (1.6, 22.9), 64)]
    LAY_U = [("u", (1.6, 22.9), 64)]
    ORIENT = "PLAN ROTATED: NORTH TO THE RIGHT, STREET (SOUTH) TO THE LEFT"
    FACE = {"N": "WEST", "S": "EAST", "W": "SOUTH (STREET)", "E": "NORTH (REAR)"}
    UNITS = {"A": dict(t="2 BR / 2 BA flat, Type A", sf=1008, lv="g"), "B": dict(t="Owner townhome + suite, 5 BR / 3.5 BA", sf=2240, lv="g"),
             "C": dict(t="3 BR / 2.5 BA townhome", sf=1232, lv="g"), "D": dict(t="3 BR / 2.5 BA townhome", sf=1232, lv="g")}
    BLDGS = [dict(name="FOURPLEX", w=102, d=28, views=("g", "u"), stories=2)]
    GFA = 5712
    LOT = (66, 152)
    TYPEA, TYPEB = "A", ""
else:
    INFO = dict(model_line="MODEL 3 — BIG HOUSE + CASITA", lot_line="LOT: 80' x 125' + REAR ALLEY", projno="SF-M3")
    NAME = "MODEL 3 — BIG HOUSE + CARRIAGE-HOUSE CASITA"
    VIEWS = {"g": (vc_m3(1), 1, "MAIN HOUSE — GROUND", 101), "u": (vc_m3(2), 2, "MAIN HOUSE — UPPER", 201),
             "c1": (vc_m3c(1), 1, "CARRIAGE HOUSE — LEVEL 1 GARAGES", 151), "c2": (vc_m3c(2), 2, "CARRIAGE HOUSE — LEVEL 2 CASITA D", 251),
             "c3": (vc_m3c(3), 3, "CARRIAGE HOUSE — LEVEL 3 LOFT", 351)}
    LAY_ALL = [("u", (1.6, 22.9), 64), ("g", (1.6, 14.0), 64), ("c2", (14.6, 22.9), 96), ("c1", (14.6, 18.9), 96), ("c3", (14.6, 14.9), 96)]
    LAY_G = [("g", (1.6, 22.9), 64), ("c1", (14.6, 22.9), 96)]
    LAY_U = [("u", (1.6, 22.9), 64), ("c2", (14.6, 22.9), 96), ("c3", (14.6, 18.9), 96)]
    ORIENT = "NORTH UP; ALLEY AT THE NORTH, STREET AT THE SOUTH"
    FACE = {"N": "NORTH", "S": "SOUTH", "W": "WEST", "E": "EAST"}
    UNITS = {"A": dict(t="2 BR / 2 BA flat, Type A", sf=1040, lv="g"), "B": dict(t="2 BR / 2 BA flat, Type B", sf=1040, lv="g"),
             "C": dict(t="Owner unit, entire upper floor, 4–5 BR / 3 BA", sf=2300, lv="u"), "D": dict(t="Casita over garages, 3–4 BR", sf=1500, lv="c2")}
    BLDGS = [dict(name="MAIN HOUSE", w=60, d=40, views=("g", "u"), stories=2), dict(name="CARRIAGE HOUSE", w=48, d=24, views=("c1", "c2", "c3"), stories=3)]
    GFA = 4800 + 1152 * 2 + 576
    LOT = (80, 125)
    TYPEA, TYPEB = "A", "B"

sheetkit.COMMON.update(INFO)
sheetkit.OUT = OUT
SUF = f".{M}"


def fname(no, title):
    return f"{no}_Model{M}_{title}"


def save(s, no, file, ttl):
    sheetkit.save(s, no, f"Model{M}_{file}", ttl, pdf_title=f"{no} {ttl.replace(chr(10), ' ')} - Model {M}")


def want(no):
    return not ONLY or no in ONLY


# ============================================================== views on a sheet
def draw_view(s, key, origin, scale, screen=True):
    vc, lvl, ttl, ds = VIEWS[key]
    s.scale = scale
    s.ox, s.oy = origin
    n0 = len(s.items)
    v = View(s, vc).build()
    v.draw(lvl, ds)
    if screen:
        out = []
        for it in s.items[n0:]:
            k = it[0]
            if it[1] in ("A-ANNO-DIMS", "A-ANNO-IDEN", "A-GRID") or (it[1] == "A-AREA-IDEN" and k == "pline"):
                continue
            if k == "solid":
                out.append(("solid", "A-BKGD", 0.86, it[3]))
            elif k == "text":
                l = list(it); l[1] = "A-BKGD"; l[8] = TGRAY; out.append(tuple(l))
            else:
                l = list(it); l[1] = "A-BKGD"; l[4] = GRAY
                l[2] = "f" if l[2] in ("xh", "h", "m") else "xf"
                if k == "pline" and isinstance(l[7], float):
                    l[7] = min(0.95, 0.6 + l[7] * 0.4)
                out.append(tuple(l))
        s.items[n0:] = out
    s.scale = scale; s.ox, s.oy = origin
    v.key = key
    return v


def rooms(v):
    out = []
    for r in v.rooms:
        nm = v._room_name(r)
        if not nm or nm in ("CH",):
            continue
        out.append(dict(x=r["x"], y=r["y"], w=r["w"], h=r["h"], cx=r["x"] + r["w"] / 2, cy=r["y"] + r["h"] / 2, name=nm.replace("\n", " "), unit=r.get("unit") or "", open=r.get("open")))
    return out


def plan_sheet(layout, overlay, sheet_no, what, sub=None):
    s = sheetkit.new()
    views = []
    for (key, org, sc) in layout:
        v = draw_view(s, key, org, sc)
        s.scale = sc; s.ox, s.oy = org
        overlay(Draw(s), v)
        views.append((v, org, sc))
        s.scale = 48
        h = v.D * 12 / sc
        sl = "3/16\"" if sc == 64 else "1/8\"" if sc == 96 else "1/4\""
        SL.drawing_title(s, org[0] + 0.2, org[1] - h - 0.75, str(len(views)), sheet_no, f"{what} — {VIEWS[key][2]}",
                         f"SCALE: {sl} = 1'-0\"" + (f"   {ORIENT}" if sc == 64 and M == 2 else ""), w=min(v.W * 12 / sc + 0.2, 12.0) if sc != 64 or M != 2 else 18.0, scalebar=False)
    s.scale = 48
    return s, views


# ============================================================== generic overlays
def is_wet(n):
    return any(k in n for k in ("BATH", "POWDER", "LAUNDRY", "KITCHEN", "KITCHENETTE", "WH", "W/D"))


def light(d, x, y):
    d.C(x, y, 0.42, "l", fill=1.0); d.L((x - 0.3, y - 0.3), (x + 0.3, y + 0.3), "xf"); d.L((x - 0.3, y + 0.3), (x + 0.3, y - 0.3), "xf")


def recept(d, x, y):
    d.C(x, y, 0.3, "l", fill=1.0); d.L((x - 0.1, y - 0.3), (x - 0.1, y + 0.3), "xf"); d.L((x + 0.1, y - 0.3), (x + 0.1, y + 0.3), "xf")


def unit_anchor(v, u, kinds=("LAUNDRY", "HALL", "WH", "CL")):
    rs = [r for r in rooms(v) if r["unit"] == u]
    for k in kinds:
        c = [r for r in rs if k in r["name"]]
        if c:
            r = max(c, key=lambda r: r["w"] * r["h"])
            return r["cx"], r["cy"]
    if rs:
        r = max(rs, key=lambda r: r["w"] * r["h"])
        return r["cx"], r["cy"]
    return None


def first_level_units():
    """unit -> view key where its panel / water heater sit (lowest level with that unit's laundry or largest presence)."""
    return {u: UNITS[u]["lv"] for u in UNITS}


def ov_elec(d, v):
    d.layer = "E-POWR"
    for r in rooms(v):
        if r["w"] * r["h"] < 12:
            continue
        light(d, r["cx"], r["cy"])
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        pts = [(x + 0.45, y + h / 2), (x + w - 0.45, y + h / 2), (x + w / 2, y + 0.45), (x + w / 2, y + h - 0.45)]
        if w * h < 60:
            pts = pts[:1]
        for (px, py) in pts:
            recept(d, px, py)
        if "BED" in r["name"] or r["name"].startswith("HALL") or "SUITE" in r["name"]:
            d.C(r["cx"] + 1.5, r["cy"], 0.4, "l", fill=1.0); d.T(r["cx"] + 1.5, r["cy"] + 0.17, "SD", 0.04, font="Helvetica-Bold")
    for dr in v.p.doors:
        if dr["kind"] != "swing":
            continue
        hx, hy, sx, sy = dr["h"][0] / 12, dr["h"][1] / 12, dr["st"][0] / 12, dr["st"][1] / 12
        if abs(hy - sy) < 0.01:
            px, py = sx + 0.55 * (1 if sx > hx else -1), sy + 0.55 * dr["d"]
        else:
            px, py = sx + 0.55 * dr["d"], sy + 0.55 * (1 if sy > hy else -1)
        d.T(px, py + 0.2, "S", 0.055, font="Helvetica-Bold")
    lv = first_level_units()
    for u in UNITS:
        if lv[u] == v.key:
            a = unit_anchor(v, u)
            if a:
                d.color = BLUE
                d.R(a[0] - 0.9, a[1] + 0.9, 1.8, 0.35, "m", fill=0.0); d.T(a[0], a[1] + 2.0, f"PANEL {u}", 0.055, font="Helvetica-Bold")
                d.color = None


def ov_hvac(d, v):
    d.layer = "M-DUCT"
    units_here = sorted(set(r["unit"] for r in rooms(v) if r["unit"] in UNITS))
    for u in units_here:
        rs = [r for r in rooms(v) if r["unit"] == u]
        a = unit_anchor(v, u, ("HALL", "LAUNDRY", "CL"))
        if not a:
            continue
        top_level = (UNITS[u]["lv"] == v.key and u not in ("A", "B")) or v.key in ("u", "c2")
        d.color = ORANGE
        if v.key in ("u", "c2") or (M == 2 and u != "A" and v.key == "u"):
            d.R(a[0] - 2.2, a[1] - 1.2, 4.4, 2.4, "m", fill=1.0); d.T(a[0], a[1] + 0.2, f"AHU-{u}", 0.055, font="Helvetica-Bold")
        elif (M == 3 and u in ("A", "B")) or (M == 2 and u == "A"):
            d.R(a[0] - 2.2, a[1] - 1.2, 4.4, 2.4, "m", fill=1.0); d.T(a[0], a[1] + 0.2, f"AHU-{u}", 0.055, font="Helvetica-Bold")
        for r in rs:
            if is_wet(r["name"]) and "KITCHEN" not in r["name"] or r["w"] * r["h"] < 30 or "STAIR" in r["name"]:
                continue
            cfm = int(round(r["w"] * r["h"] * 1.0 / 10.0)) * 10
            d.PL([(a[0], a[1]), (a[0], r["cy"]), (r["cx"], r["cy"])], "l")
            d.R(r["cx"] - 0.5, r["cy"] - 0.5, 1.0, 1.0, "l", fill=1.0); d.L((r["cx"] - 0.5, r["cy"] - 0.5), (r["cx"] + 0.5, r["cy"] + 0.5), "xf")
            d.T(r["cx"], r["cy"] + 1.3, f"{cfm} CFM", 0.045)
        d.color = BLUE
        for r in rs:
            if "BATH" in r["name"] or "POWDER" in r["name"] or "LAUNDRY" in r["name"]:
                d.C(r["cx"] + 1.0, r["cy"] - 1.0, 0.5, "l", fill=1.0); d.T(r["cx"] + 1.0, r["cy"] - 0.82, "E", 0.05, font="Helvetica-Bold")
        d.color = None


def fixtures(v):
    """(x, y, kind, unit) for plumbing fixtures from the concept SVG + room centers."""
    out = []
    for r in rooms(v):
        n = r["name"]
        if not is_wet(n):
            continue
        inside = lambda x, y: r["x"] <= x <= r["x"] + r["w"] and r["y"] <= y <= r["y"] + r["h"]
        fx = [f for f in v.d["fx"] if f["k"] == "ell" and inside(f["cx"], f["cy"])]
        for f in fx:
            out.append((f["cx"], f["cy"], "WC" if f["ry"] > 0.9 or f["rx"] > 0.9 else "LAV", r["unit"]))
        if "KITCHEN" in n:
            out.append((r["cx"], r["cy"], "KS", r["unit"]))
        if "LAUNDRY" in n or "W/D" in n:
            out.append((r["cx"], r["cy"], "CW", r["unit"]))
        if ("BATH" in n) and not fx:
            out.append((r["cx"], r["cy"], "TUB", r["unit"]))
    return out


def stacks_for(v):
    pts = fixtures(v)
    clusters = []
    for (x, y, k, u) in pts:
        for c in clusters:
            if c["u"] == u and abs(c["x"] - x) + abs(c["y"] - y) < 16:
                c["pts"].append((x, y, k)); c["x"] = sum(p[0] for p in c["pts"]) / len(c["pts"]); c["y"] = sum(p[1] for p in c["pts"]) / len(c["pts"])
                break
        else:
            clusters.append(dict(u=u, x=x, y=y, pts=[(x, y, k)]))
    return clusters


def ov_ww(d, v):
    d.layer = "P-SANR"; d.color = GREEN
    below = v.key in ("g", "c1")
    for i, c in enumerate(stacks_for(v)):
        sx, sy = c["x"], c["y"]
        for (x, y, k) in c["pts"]:
            d.PL([(x, y), (x, sy), (sx, sy)], "l", [4, 2] if below else None)
            d.C(x, y, 0.28, "l", fill=1.0); d.T(x, y + 0.8, k, 0.04)
        d.C(sx, sy, 0.45, "m", fill=0.0); d.T(sx + 1.4, sy - 0.3, f"S-{c['u']}{i + 1}", 0.05, font="Helvetica-Bold")
    d.color = None


def ov_water(d, v):
    d.layer = "P-DOMW"
    lv = first_level_units()
    whs = {}
    for u in UNITS:
        a = unit_anchor(v, u, ("WH", "LAUNDRY", "CL"))
        if a and (lv[u] == v.key or any(r["unit"] == u and is_wet(r["name"]) for r in rooms(v))):
            whs[u] = a
    for (x, y, k, u) in fixtures(v):
        if u not in whs:
            continue
        wx, wy = whs[u]
        d.color = BLUE; d.PL([(wx, wy), (wx, y - 0.15), (x, y - 0.15)], "xf")
        if k != "WC":
            d.color = RED; d.PL([(wx + 0.3, wy), (wx + 0.3, y + 0.15), (x, y + 0.15)], "xf", [4, 2])
        d.color = None; d.C(x, y, 0.25, "l", fill=1.0)
    for u, (wx, wy) in whs.items():
        if lv[u] == v.key:
            d.R(wx - 0.9, wy - 0.9, 1.8, 1.8, "m", fill=0.9); d.T(wx, wy + 0.2, f"WH-{u}", 0.045, font="Helvetica-Bold")


def heads(v):
    pts = []
    for r in rooms(v):
        if r["w"] * r["h"] < 24:
            continue
        nx, ny = max(1, math.ceil(r["w"] / 14)), max(1, math.ceil(r["h"] / 14))
        for i in range(nx):
            for j in range(ny):
                pts.append((r["x"] + r["w"] * (i + 0.5) / nx, r["y"] + r["h"] * (j + 0.5) / ny))
    return pts


def ov_fp(d, v):
    d.layer = "F-SPRN"
    for (x, y) in heads(v):
        d.C(x, y, 0.35, "l", fill=1.0); d.L((x - 0.35, y), (x + 0.35, y), "xf"); d.L((x, y - 0.35), (x, y + 0.35), "xf")
    d.color = RED
    W, D = v.W, v.D
    d.PL([(1.0, D / 2), (W - 1.0, D / 2)], "m")
    for x in range(4, int(W), 12):
        d.PL([(x, 1.0), (x, D - 1.0)], "l")
    d.color = None


def ov_rcp(d, v):
    d.layer = "A-CLNG"
    for r in rooms(v):
        if r["w"] * r["h"] < 12:
            continue
        light(d, r["cx"], r["cy"])
        d.box(r["cx"], r["cy"] + 1.5, "9'-0\"" if v.key not in ("c3",) else "SLOPED", 0.042)


def segs_of(v, types):
    return [sg for sg in v.p.segs if sg[4] in types]


def seg_pts(sg):
    o, f, a, b, t = sg
    return (((f / 12, a / 12), (f / 12, b / 12)) if o == "v" else ((a / 12, f / 12), (b / 12, f / 12)))


def ov_xco(d, v):
    for sg in segs_of(v, ("W1",)):
        (x0, y0), (x1, y1) = seg_pts(sg)
        d.R(min(x0, x1) - 0.5, min(y0, y1) - 0.5, abs(x1 - x0) + 1.0, abs(y1 - y0) + 1.0, "f", dash=[3, 2], color=RED)
    for q in v.chases_red:
        d.R(q["x"], q["y"], q["w"], q["h"], "m", fill=0.8)
    for i, c in enumerate(stacks_for(v)):
        d.C(c["x"], c["y"], 0.45, "m", fill=0.0)
    ov_hvac(d, v)


def ov_shear(d, v):
    d.layer = "S-SHWL"; d.color = RED
    for sg in segs_of(v, ("EXT", "W1", "W3")):
        (x0, y0), (x1, y1) = seg_pts(sg)
        if abs(x1 - x0) + abs(y1 - y0) < 4:
            continue
        d.L((x0, y0), (x1, y1), "h")
        for (hx, hy) in ((x0, y0), (x1, y1)):
            d.PL([(hx - 0.4, hy), (hx, hy - 0.4), (hx + 0.4, hy), (hx, hy + 0.4)], "m", closed=True, fill=0.0)
        d.box((x0 + x1) / 2, (y0 + y1) / 2, "SW3" if sg[4] == "W1" else "SW1", 0.04)
    d.color = None


def ov_acc(d, v):
    d.color = BLUE
    for u in (TYPEA, TYPEB):
        if not u:
            continue
        rs = [r for r in rooms(v) if r["unit"] == u]
        if rs and v.key == "g":
            r = max(rs, key=lambda r: r["w"] * r["h"])
            d.T(r["cx"], r["cy"] + 2.2, f"UNIT {u} — TYPE {'A' if u == TYPEA else 'B'}", 0.08, font="Helvetica-Bold")
            for (x, y, rad) in v.turns:
                d.C(x, y, rad, "l")
    if v.key != "g":
        d.T(v.W / 2, v.D / 2, "NOT COVERED: UPPER LEVELS / MULTISTORY UNITS WITHOUT AN ELEVATOR", 0.07, font="Helvetica-Bold")
    d.color = None


def exits(v):
    out = []
    W, D = v.p.W / 12, v.p.D / 12
    for dr in v.p.doors:
        hx, hy = dr["h"][0] / 12, dr["h"][1] / 12
        sx, sy = dr["st"][0] / 12, dr["st"][1] / 12
        on_edge = (abs(hy) < 0.6 and abs(sy) < 0.6) or (abs(hy - D) < 0.6 and abs(sy - D) < 0.6) or (abs(hx) < 0.6 and abs(sx) < 0.6) or (abs(hx - W) < 0.6 and abs(sx - W) < 0.6)
        if on_edge:
            out.append(((hx + sx) / 2, (hy + sy) / 2))
    return out


def ov_life(d, v):
    d.color = RED
    for sg in segs_of(v, ("W1",)):
        (x0, y0), (x1, y1) = seg_pts(sg)
        d.L((x0, y0), (x1, y1), "xh")
    ex = exits(v)
    for (x, y) in ex:
        d.C(x, y, 0.6, "m", fill=1.0); d.T(x, y + 0.2, "EX", 0.045, font="Helvetica-Bold")
    d.color = BLUE
    worst = {}
    for u in sorted(set(r["unit"] for r in rooms(v) if r["unit"] in UNITS)):
        rs = [r for r in rooms(v) if r["unit"] == u]
        far = max(((r["x"] + 0.5, r["y"] + 0.5) for r in rs) , key=lambda p: min(abs(p[0] - e[0]) + abs(p[1] - e[1]) for e in ex) if ex else 0)
        if ex:
            e = min(ex, key=lambda e: abs(far[0] - e[0]) + abs(far[1] - e[1]))
            L = abs(far[0] - e[0]) + abs(far[1] - e[1])
            if v.key in ("u", "c2", "c3"):
                L += 40
            d.PL([far, (far[0], e[1]), e], "m", [5, 2]); d.C(far[0], far[1], 0.45, "m", fill=0.0)
            d.T((far[0] + e[0]) / 2, e[1] - 0.8 if e[1] > far[1] else e[1] + 1.2, f"{u}: {L:.0f}'", 0.05, font="Helvetica-Bold")
            worst[u] = L
    d.color = None
    v.travel = worst


# ============================================================== plan-overlay sheets
def notes_col(s, title, items, x=None, y=None, w=None):
    if M == 2:
        x = x or 1.0; y = y or 8.0; w = w or 9.6
    else:
        x = x or NC; y = y or TOPY; w = w or 10.6
    return notes(s, x, y, title, items, w)


PLANS = {
    "X-101": ("MEP COORDINATION PLAN", LAY_ALL, ov_xco, "MEP COORDINATION\nPLAN", [
        "W1 unit separation walls (red bands) carry no pipes, ducts, boxes or recessed items; services cross units only through listed firestop systems at chases.",
        "Each unit has its own HVAC, water heater, panel and meters; nothing is shared between units except the fire sprinkler main and the house panel.",
        "Ducts in floor-truss space above rated F1 ceilings get ceiling radiation dampers at every opening; upper-level ducts run in the attic, R-8, sealed and tested.",
        "Plumbing stacks (black dots) stack wet rooms over wet rooms; branch routes coordinated with floor-truss webs before the truss order.",
        "Design intent for the engineers of record; confirm all routes on their drawings."]),
    "P-101": ("WASTE AND VENT PLAN", LAY_ALL, ov_ww, "WASTE AND VENT\nPLAN", [
        "Design intent. Fixture branches (green) to stacks S-xn; dashed = below slab (ground level), solid = in floor trusses (upper levels).",
        "PVC/ABS Sch. 40 DWV; cast iron in shared chases is the quiet alternate. Vent each stack through the roof; no air admittance valves.",
        "Building sewer 4\" to the street (C-103), cleanouts at each stack base and at the building exit.",
        "Sleeve all below-slab lines through PT slab beams before the pour (S-101)."]),
    "P-102": ("DOMESTIC WATER PLAN", LAY_ALL, ov_water, "DOMESTIC WATER\nPLAN", [
        "Design intent. Blue: cold, red dashed: hot from each unit's heat pump water heater WH-x (50 gal, PEX home-run manifold).",
        "One City meter, PRV if over 80 psi, unit submeters and shutoffs at the service entry; each unit has a main shutoff at its water heater.",
        "Water heaters in pans with T&P and pan drains to the exterior; louvered closet doors for heat pump air."]),
    "FP-101": ("FIRE SPRINKLER LAYOUT", LAY_ALL, ov_fp, "FIRE SPRINKLER\nLAYOUT", [
        "NFPA 13R design intent; final layout and hydraulics by a licensed sprinkler contractor (deferred submittal).",
        "Residential quick-response heads, one per room and closet over 24 SF, baths over 55 SF; attic heads only if Scottsdale requires.",
        "Riser with control valve, flow switch and exterior bell at the fire service entry; FDC location per the Fire Marshal."]),
    "A-701": ("REFLECTED CEILING PLAN", LAY_ALL, ov_rcp, "REFLECTED\nCEILING PLANS", [
        "Ceilings 9'-0\" unless noted; floor/ceilings between stacked units are the F1 1-hour assembly (G-005, D-002/3).",
        "Surface LED fixtures centered in rooms; no recessed cans in rated ceilings.",
        "Attic access 22x30 at each upper unit hall; insulated, weatherstripped hatch."]),
    "S-201": ("SHEAR WALL PLAN (DESIGN INTENT)", LAY_ALL, ov_shear, "SHEAR WALL\nPLAN", [
        "Light-frame wood shear walls with OSB; exterior walls SW1 and unit separation walls SW3. Design by the structural engineer of record (ASCE 7, SDPWS).",
        "Preliminary criteria: wind 115 mph Vult exposure C; SDC B (verify for parcel). Hold-downs (diamonds) at shear wall ends to the PT slab.",
        "SW3 sheathing placed so the W1 double-stud acoustic/fire design is unchanged (D-002/1)."]),
    "G-004": ("ACCESSIBILITY PLAN", LAY_ALL, ov_acc, "ACCESSIBILITY\nPLAN", [
        "Four or more dwelling units: Fair Housing Act / IBC 1107 covered dwellings are the ground-floor flats in this building without an elevator.",
        f"Provided: Unit {TYPEA} Type A" + (f", Unit {TYPEB} Type B." if TYPEB else ". Multistory townhomes B, C, D are not covered (no elevator)."),
        "Accessible route from the public walk and the van stall to each covered unit entry; thresholds 1/2\" max.; turning circles shown.",
        "Details on D-003; mounting heights 15\"–48\"."]),
    "E-101": ("GROUND LEVEL POWER AND LIGHTING", LAY_G, ov_elec, "GROUND LEVEL\nELECTRICAL PLAN", [
        "Design intent. Receptacles per NEC 210.52, GFCI/AFCI per 210.8 and 210.12, tamper-resistant; surface LED fixtures; smoke/CO alarms interconnected.",
        "Unit panels 125A (200A for the owner unit if the load calc requires, E-301) with surge protection; meters at the meter center (E-201)."]),
    "E-102": ("UPPER LEVEL POWER AND LIGHTING", LAY_U, ov_elec, "UPPER LEVEL\nELECTRICAL PLAN", [
        "Design intent. Same standards as E-101. Upper units: wiring in floor trusses and attic; no boxes in W1 walls.",
        "Smoke alarms in every bedroom, outside sleeping areas and on each level; CO alarms per IFC 915."]),
    "M-101": ("GROUND LEVEL HVAC", LAY_G, ov_hvac, "GROUND LEVEL\nHVAC PLAN", [
        "Design intent. One heat pump system per unit (Manual J/S/D by the mechanical engineer); registers sized at about 1 CFM/SF as placeholders.",
        "Ground-level ducts in the floor-truss space above rated ceilings with ceiling radiation dampers; condensers on pads at grade.",
        "Bath fans (E) ducted to the exterior; primary bath fan runs continuously for whole-house ventilation (IMC 403.3.2)."]),
    "M-102": ("UPPER LEVEL HVAC", LAY_U, ov_hvac, "UPPER LEVEL\nHVAC PLAN", [
        "Design intent. Upper-level AHUs on attic platforms with 30\" service space, light and receptacle; ducts R-8, sealed, leakage tested.",
        "No duct crosses a W1 draftstop between attics."]),
    "G-005": ("LIFE SAFETY PLAN", LAY_ALL, ov_life, "RATED ASSEMBLIES\n+ LIFE SAFETY", None),
}


def build_plan_sheet(no):
    what, lay, ov, tb, nts = PLANS[no]
    sheet_no = no + (SUF if no in ("P-101", "P-102") else "")
    s, views = plan_sheet(lay, ov, sheet_no, what)
    if no == "G-005":
        trav = {}
        for (v, _, _) in views:
            trav.update(getattr(v, "travel", {}))
        rows = [(u, UNITS[u]["t"], f"{trav.get(u, 0):.0f} ft", "125 ft (single exit, sprinklered)" if M == 3 and u in "ABC" else "125 ft", "YES" if trav.get(u, 0) <= 125 else "CHECK") for u in sorted(UNITS)]
        x = 1.0 if M == 2 else NC
        y = 8.0 if M == 2 else TOPY
        y = tbl(s, x, y, "EXIT ACCESS TRAVEL (MOST REMOTE POINT TO EXIT, INCL. 40 FT FOR STAIRS ON UPPER LEVELS)", [("UNIT", 0.6, "c"), ("TYPE", 3.4, "l"), ("TRAVEL", 1.0, "c"), ("LIMIT", 2.6, "c"), ("OK", 0.7, "c")], rows, w=8.3)
        y = tbl(s, x if M == 3 else 10.6, y if M == 3 else 8.0, "RATED ASSEMBLIES (SEE D-002)", [("TAG", 0.6, "c"), ("ASSEMBLY", 3.0, "l"), ("RATING", 0.8, "c"), ("BASIS", 2.6, "l")], [
            ("W1", "Unit separation wall, double stud", "1 HR", "UL U341 / GA WP 3820, STC 55"),
            ("F1", "Floor/ceiling between stacked units", "1 HR", "UL L528 / GA FC 5512, STC/IIC 50"),
            ("E1", "Exterior wall (FSD 10 ft min.)", "0 HR", "Table 602"),
            ("DS", "Attic draftstop at W1", "—", "IBC 718.4"),
            ("DR", "Doors from units to shared areas", "20 MIN", "Self-closing, S-label")], w=7.0)
        nts = ["Red: 1-hour W1 walls. EX: exits to the exterior. Blue dashed: exit access travel from the most remote point.",
               "Sprinklered throughout (NFPA 13R). Smoke and CO alarms per IFC 907.2.11 / 915. No building fire alarm required (under 16 units, 2–3 stories).",
               "Each unit has direct exterior exits; upper levels reach them by stairs inside the unit (Model 2) or by the private/common stair (Model 3)."]
        notes(s, (1.0 if M == 2 else NC), (y if M == 3 else 4.5), "LIFE SAFETY NOTES", nts, 9.6 if M == 2 else 10.6)
    else:
        notes_col(s, f"{what} — NOTES", nts)
    save(s, sheet_no, {"X-101": "MEP_Coordination_Plan", "P-101": "Waste_and_Vent_Plan", "P-102": "Domestic_Water_Plan", "FP-101": "Fire_Sprinkler_Layout",
                       "A-701": "Reflected_Ceiling_Plans", "S-201": "Shear_Wall_Plan", "G-004": "Accessibility_Plan", "E-101": "Ground_Floor_Electrical_Plan",
                       "E-102": "Upper_Floor_Electrical_Plan", "M-101": "Ground_Floor_HVAC_Plan", "M-102": "Upper_Floor_HVAC_Plan",
                       "G-005": "Rated_Assemblies_Life_Safety"}[no], tb)


if __name__ == "__main__":
    for no in PLANS:
        if want(no) or want(no + SUF):
            build_plan_sheet(no)
