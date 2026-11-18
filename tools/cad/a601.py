"""A-601 door and window schedules and types, Model 1."""
import ast, re, sys
from cadkit import Sheet
from plan_engine import table, para
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"


def grab(path, name):
    src = open(path).read()
    i = src.index(f"\n{name} = [") + 1
    j = src.index("\n]", i) + 2
    return ast.literal_eval(src[i:j].split("=", 1)[1])


d1 = grab("a101_1.py", "drows"); d2 = grab("a102_1.py", "drows")
w2 = grab("a102_1.py", "wrows"); w1 = grab("a101_1.py", "wrows")
HW = {"ENTRY / CLOSER": "1", "STOREROOM": "2", "PRIVACY": "3", "PASSAGE": "4", "PULLS": "5", "LOCK / PULL": "6"}
FR = {"A": "HM, WELDED", "B": "HM, WELDED", "C": "HM, 20 MIN", "D": "WOOD", "E": "WOOD + TRACK", "F": "WOOD + TRACK", "H": "VINYL / AL"}
s = Sheet(origin=(0, 0))
cols = [("NO.", 0.42, "c"), ("LOCATION", 1.75, "l"), ("SIZE (W x H)", 1.05, "c"), ("TYPE", 0.4, "c"), ("FRAME", 0.95, "c"), ("RATING", 0.68, "c"), ("HW SET", 0.55, "c"), ("NOTES", 0.6, "c")]


def rows(dr):
    return [(n, loc, sz, t, FR.get(t, ""), r, HW.get(hw, ""), nt) for (n, loc, sz, t, r, hw, nt) in dr]


y = SL.head(s, 1.0, 23.2, "DOOR SCHEDULE — GROUND FLOOR (A-101.1)", 6.4)
y = table(s, 1.0, y + 0.04, cols, rows(d1), h=0.068, rowh=0.165)
y = SL.head(s, 7.9, 23.2, "DOOR SCHEDULE — UPPER FLOOR (A-102.1)", 6.4)
table(s, 7.9, y + 0.04, cols, rows(d2), h=0.068, rowh=0.165)

# window schedule (combined)
wc = {}
for r in w1 + w2:
    t = r[0]
    if t in wc:
        wc[t][5] = str(int(wc[t][5]) + int(r[5]))
    else:
        wc[t] = list(r)
UF = {"A": "0.30", "B": "0.30", "C": "0.30", "D": "0.30", "F": "0.30"}
wrows = [(t, r[1], r[2], r[3], "7'-0\"", r[4], r[5], "0.30 / 0.25", r[6]) for t, r in sorted(wc.items())]
wcols = [("TYPE", 0.45, "c"), ("SIZE (W x H)", 1.0, "c"), ("OPERATION", 1.2, "l"), ("SILL", 0.55, "c"), ("HEAD", 0.55, "c"), ("EGRESS", 0.6, "c"), ("QTY", 0.4, "c"), ("U / SHGC", 0.85, "c"), ("LOCATION", 1.6, "l")]
y = SL.head(s, 1.0, 17.2, "WINDOW SCHEDULE — BUILDING TOTAL", 7.2)
y = table(s, 1.0, y + 0.04, wcols, wrows, h=0.068, rowh=0.17)

# ---- door type elevations at 1/2" = 1'-0"  (1 ft = 0.5 in)
K = 0.5
def door_type(x0, y0, tag, w, h, kind, cap):
    s.rect(x0, y0, w * K, h * K, lw="m")
    if kind == "flush":
        pass
    elif kind == "lite":
        s.rect(x0 + 0.3 * K, y0 + 4.2 * K, (w - 0.6) * K, 3.2 * K, lw="f")
    elif kind == "bypass":
        s.line((x0 + w * K / 2, y0), (x0 + w * K / 2, y0 + h * K), lw="f")
        s.line((x0, y0 + h * K + 0.05), (x0 + w * K, y0 + h * K + 0.05), lw="f")
    elif kind == "bifold":
        for f in (0.25, 0.5, 0.75):
            s.line((x0 + w * K * f, y0), (x0 + w * K * f, y0 + h * K), lw="xf" if f != 0.5 else "f")
    elif kind == "slider":
        s.line((x0 + w * K / 2, y0), (x0 + w * K / 2, y0 + h * K), lw="f")
        s.rect(x0 + 0.25 * K, y0 + 0.4 * K, w * K / 2 - 0.35 * K, h * K - 0.65 * K, lw="xf")
        s.rect(x0 + w * K / 2 + 0.1 * K, y0 + 0.4 * K, w * K / 2 - 0.35 * K, h * K - 0.65 * K, lw="xf")
        s.text((x0 + w * K * 0.75, y0 + h * K / 2), "← OPER.", 0.055)
        s.text((x0 + w * K * 0.25, y0 + h * K / 2), "FIXED", 0.055)
    elif kind == "louver":
        for i in range(6):
            yy = y0 + 0.4 + i * 0.12
            s.line((x0 + 0.15, yy), (x0 + w * K - 0.15, yy), lw="xf")
    s.text((x0 + w * K / 2, y0 - 0.22), f"W {w}'-0\"" if float(w).is_integer() else f"W {int(w)}'-{int(round((w % 1) * 12))}\"", 0.06)
    yy = y0 - 0.42
    for ln in cap:
        s.text((x0 + w * K / 2, yy), ln, 0.058); yy -= 0.12


y0 = 10.3
SL.head(s, 1.0, 15.3, "DOOR TYPES  ·  1/2\" = 1'-0\"", 13.3)
x = 1.1
for tag, w, h, kind, cap in [
        ("A", 3.5, 8, "lite", ["INSULATED FIBERGLASS", "1/2 LITE, TEMPERED", "ENTRY 101 / EXT."]),
        ("B", 2.5, 6.67, "louver", ["HOLLOW METAL", "RISER ROOM 102", "SIGN 'FIRE RISER'"]),
        ("C", 3, 8, "flush", ["SOLID-CORE WOOD 1¾\"", "20 MIN, S-LABEL", "UNIT ENTRY"]),
        ("D", 3, 8, "flush", ["SOLID-CORE WOOD 1¾\"", "FLUSH, PAINT GRADE", "INTERIOR"]),
        ("E", 5, 8, "bypass", ["BYPASS, SOLID-CORE", "TOP-HUNG TRACK", "CLOSETS"]),
        ("F", 3, 8, "bifold", ["BI-FOLD (2) 1'-6\"", "SOLID-CORE, LOUVER", "AT WH (COMB. AIR)"]),
        ("H", 6, 8, "slider", ["SLIDING GLASS DOOR", "TEMPERED LOW-E", "U 0.30 / SHGC 0.25"])]:
    door_type(x, y0, tag, w, h, kind, cap)
    s.text((x + w * K / 2, y0 + h * K + 0.3), f"TYPE {tag}", 0.085, font="Helvetica-Bold")
    x += w * K + 0.55

# ---- window types
SL.head(s, 1.0, 8.25, "WINDOW TYPES  ·  1/2\" = 1'-0\"  ·  VIEWED FROM THE EXTERIOR", 13.3)
x = 1.1; y0 = 4.9
import math
for tag, w, h, kind, cap in [("A", 6, 4, "hs", ["HORIZONTAL SLIDER", "SILL 3'-0\"", "EGRESS: 5.7 SF NET"]), ("B", 3, 5, "sh", ["SINGLE HUNG", "SILL 2'-0\"", "EGRESS AT BED 2"]),
                             ("C", 3, 4, "sh", ["SINGLE HUNG", "SILL 3'-0\"", ""]), ("D", 6, 5, "hs", ["HORIZONTAL SLIDER", "SILL 2'-0\"", "TEMPERED (< 18\" A.F.F.)"]),
                             ("F", 3, 5, "arch", ["FIXED, ARCH TOP", "SILL 2'-0\"", "TEMPERED (AT STAIR)"])]:
    s.rect(x - 0.08, y0 - 0.08, w * K + 0.16, h * K + 0.16, lw="l")
    s.rect(x, y0, w * K, h * K, lw="m")
    if kind == "hs":
        s.line((x + w * K / 2, y0), (x + w * K / 2, y0 + h * K), lw="l")
        s.text((x + w * K * 0.25, y0 + h * K / 2), "→", 0.12)
    elif kind == "sh":
        s.line((x, y0 + h * K / 2), (x + w * K, y0 + h * K / 2), lw="l")
        s.text((x + w * K / 2, y0 + h * K * 0.25), "↑", 0.12)
    elif kind == "arch":
        pts = [(x + w * K / 2 + w * K / 2 * math.cos(a / 20 * math.pi), y0 + (h - 1.5) * K + w * K / 2 * math.sin(a / 20 * math.pi) * 0.66) for a in range(21)]
        s.pline(pts, lw="l")
    s.text((x + w * K / 2, y0 + h * K + 0.25), f"TYPE {tag}", 0.085, font="Helvetica-Bold")
    s.text((x + w * K / 2, y0 - 0.25), f"{w}'-0\" x {h}'-0\"", 0.06)
    yy = y0 - 0.42
    for ln in cap:
        s.text((x + w * K / 2, yy), ln, 0.058); yy -= 0.12
    x += w * K + 0.75

# ---- hardware sets + notes
HWS = [
    "SET 1 — ENTRY: 3 hinges (ball bearing, NRP at exterior), lever entry lockset with deadbolt (single-cylinder; thumbturn inside, no key needed to exit, IBC 1010.2.4), closer, kick plate, wide-angle viewer, smoke gasket at unit doors, stop. Accessible units: levers, 5 lbf max., closer sweep 5 sec.",
    "SET 2 — STOREROOM: 3 hinges, storeroom lever (always locked outside, free egress inside), closer at 102, sign. Knox box for 102 per fire marshal.",
    "SET 3 — PRIVACY: 3 hinges, privacy lever with emergency release, wall stop.",
    "SET 4 — PASSAGE: 3 hinges (pair for bi-folds: pivot hardware), passage lever or pulls, stop.",
    "SET 5 — BYPASS: top-hung track, floor guide, recessed pulls.",
    "SET 6 — SLIDER: keyed lock outside / thumb latch inside, secondary foot bolt, screen, low-profile sill (Unit A: ½\" max., accessible).",
]
y = SL.notes_list(s, 21.15, 23.2, "HARDWARE SETS", HWS, 5.1)
NOTES = [
    "Door sizes are nominal leaf sizes; rough openings per manufacturer. All interior doors 8'-0\" tall to match the 9'-0\" ceilings.",
    "Clear width at every door on an accessible route and every door in Unit A: 32\" min. with the door open 90°, maneuvering clearances per A117.1 404.2.4. Unit B (Type B): 31¾\" nominal clear min. at user-passage doors.",
    "Rated doors: labeled door and frame assemblies, self-closing and positive-latching (IBC 716). Do not field-cut or add hardware that voids the label.",
    "Safety glazing: all door glass, the stair window F, and window glass within 18\" of the floor or 24\" of a door edge (IBC 2406.4).",
    "Windows: dual-pane low-E, vinyl or fiberglass frames, NFRC labeled, U 0.30 max. and SHGC 0.25 max. (better than the IECC 2021 CZ 2B prescriptive U 0.40). Color and grille pattern per the elevations.",
    "Emergency escape openings: 5.7 SF net clear (5.0 SF at grade floor), 24\" min. clear height, 20\" min. clear width, sill 44\" max. Window opening control devices are not used.",
    "Install windows and doors with sill pan flashing, head flashing and WRB integration per D-001.",
    "Door 101 and unit entry doors get a doorbell, an address/unit sign, and a light outside (E-101).",
]
SL.notes_list(s, 26.55, 23.2, "DOOR AND WINDOW NOTES", NOTES, 5.25)
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="A-601", sheet_title="DOOR + WINDOW\nSCHEDULES"))
base = f"{OUT}/A-601_Model1_Door_and_Window_Schedules"
s.to_pdf(base + ".pdf", title="A-601 Door and Window Schedules - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
