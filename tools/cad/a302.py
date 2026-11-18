"""A-302 wall sections, Model 1. 1/2" = 1'-0" (scale 24), z up."""
import math, sys
from cadkit import Sheet
from plan_engine import para
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
s = Sheet(origin=(0, 0), scale=24)


def at(x, y):
    s.ox, s.oy = x, y


def R(x, z, w, h, lw="l", fill=None, layer="A-DETL"):
    s.rect(x, -(z + h), w, h, layer=layer, lw=lw, space="m", fill=fill)


def Ln(a, b, lw="l", dash=None, layer="A-DETL"):
    s.line((a[0], -a[1]), (b[0], -b[1]), layer=layer, lw=lw, space="m", dash=dash)


def PL(pts, lw="l", fill=None, closed=False):
    s.pline([(x, -z) for x, z in pts], layer="A-DETL", lw=lw, space="m", fill=fill, closed=closed)


def batt(x, z, w, h):
    n = max(1, int(h / (w * 0.7)))
    pts = []
    for i in range(n * 2 + 1):
        pts.append((x + (w * 0.1 if i % 2 == 0 else w * 0.9), z + i * h / (n * 2)))
    PL(pts, "xf")


def cross(x, z, w, h, fill=0.55):
    R(x, z, w, h, "l", fill)
    Ln((x, z), (x + w, z + h), "xf"); Ln((x, z + h), (x + w, z), "xf")


def P(x, z):
    return s.m2p(x, -z)


FF = 0.0
UFF = 128.0           # 10'-8"
PLATE = 236.0         # 19'-8"
CEIL1 = 108.0         # 9'-0"
GR = -8.0


def section(kind):
    """x = 0 at the exterior face of framing; interior to the left (negative x)."""
    rated = kind == "W2"
    # soil + footing/edge beam
    PL([(-60, GR - 0.01), (40, GR)], "m")
    for k in range(10):
        Ln((-56 + k * 10, GR), (-60 + k * 10, GR - 4), "xf")
    PL([(-60, -4), (-6, -4), (-6, -24), (6, -24), (6, GR), (40, GR)], "xf")
    R(-6, -24, 12, 24, "m", 0.55)                       # edge beam 12 x 24 (below slab top)
    R(-60, -4, 54, 4, "m", 0.55)                        # 4" slab
    R(-60, -8, 54, 4, "xf", 0.85)                       # ABC
    Ln((-60, -4.2), (-6, -4.2), "f", [3, 1.5])          # vapor retarder
    # bottom plate + wall to plate
    stud = 5.5
    for (z0, z1) in ((0, CEIL1 + 0.0), (UFF, PLATE)):
        R(-stud, z0, stud, 1.5, "l", 0.55)
        R(-stud, z1 - 3, stud, 3, "l", 0.55)
        R(-stud, z0 + 1.5, stud, z1 - z0 - 4.5, "f")
        batt(-stud + 0.4, z0 + 2, stud - 0.8, z1 - z0 - 6)
        R(-stud - 0.625, z0 + 0.5, 0.625, z1 - z0 - 0.5, "f", 0.82)   # interior GWB
    # rim + floor trusses
    R(-stud, CEIL1, 1.25, UFF - CEIL1 - 1.0, "l", 0.7)                 # rim board
    R(-60, CEIL1 + 7.5, 60 - stud - 1.25 + 0, 11.875, "f")
    for xx in range(-60, -10, 8):
        Ln((xx, CEIL1 + 9), (xx + 4, CEIL1 + 7.5 + 11.875 - 1.5), "xf"); Ln((xx + 4, CEIL1 + 7.5 + 11.875 - 1.5), (xx + 8, CEIL1 + 9), "xf")
    R(-60, CEIL1 + 7.5 + 11.875, 60 - stud, 0.75, "l", 0.5)            # subfloor
    R(-60, CEIL1 - 1.25, 60 - stud - 0.625, 1.25, "f", 0.82)            # 2 layers ceiling GWB
    R(-60, CEIL1, 60 - stud - 0.625, 5.5, "xf")                         # ceiling joists zone
    # exterior skin
    sk = 0.625 if rated else 0.4375
    R(0, -2, sk, PLATE + 2, "f", 0.82 if rated else 0.6)
    R(sk, -2, 0.06, PLATE + 2, "m")
    R(sk + 0.06, -1, 0.875, PLATE + 1, "l", 0.92)
    # weep screed
    PL([(sk + 0.06, -2), (sk + 1.2, -2.5), (sk + 1.2, -1.2)], "m")
    # window at the upper floor (head 7'-0" above floor)
    for zf in (FF, UFF):
        sill, head = zf + (36 if not rated else 24), zf + 84
        R(-stud, sill - 3, stud, 3, "l", 0.55); R(-stud, head, stud, 11.25, "l", 0.55)  # sill + header
        R(-stud - 0.625, sill, stud + 0.625 + sk + 0.94, head - sill, "l", 1.0)
        R(-2.5, sill, 2.5, head - sill, "m", 0.95)
        Ln((-1.25, sill), (-1.25, head), "f")
        PL([(sk + 0.94, sill), (sk + 2.5, sill - 0.6)], "m")
    # roof: trusses with raised heel; eave 24"
    heel = 14.0
    pitch = 4 / 12
    zt = lambda x: PLATE + heel + (-x) * pitch
    PL([(-60, zt(-60)), (24, zt(24))], "m")             # top chord line
    PL([(-60, zt(-60) + 0.4375), (24, zt(24) + 0.4375)], "l")
    for k in range(-60, 24, 3):                           # tile profile
        PL([(k, zt(k) + 0.5), (k + 1.5, zt(k + 1.5) + 2.5), (k + 3, zt(k + 3) + 0.5)], "xf")
    Ln((-60, PLATE), (0, PLATE), "l")                     # bottom chord
    Ln((0, PLATE), (0, zt(0)), "l"); Ln((-30, PLATE), (0, zt(0)), "xf")
    R(22.5, zt(24) - 7.25, 1.5, 7.25, "l", 1.0)           # fascia 2x8
    PL([(24, zt(24) - 1), (28, zt(24) - 1), (28, zt(24) - 5), (24, zt(24) - 6)], "l")   # gutter
    if rated:
        R(0.06 + sk + 0.875, zt(24) - 8.0, 22.5 - (sk + 0.94), 0.625, "f", 0.82)      # 5/8 X soffit
    else:
        R(0.06 + sk + 0.875, zt(24) - 8.0, 22.5 - (sk + 0.94), 0.5, "f", 0.7)
        for xv in (8, 14):
            R(xv, zt(24) - 8.0, 3, 0.5, "f", 0.2)
    # ceiling + insulation R-38 (12")
    R(-60, PLATE - 0.625, 60 - stud, 0.625, "f", 0.82)
    for k in range(-58, -4, 4):
        PL([(k + 2 * (1 - math.cos(t)), PLATE + 0.3 + 12 * math.sin(t / 2)) for t in [i * math.pi / 6 for i in range(7)]], "xf")
    if not rated:
        PL([(-8, PLATE + 2), (-8, PLATE + 13), (-2, zt(-2) - 1)], "xf")  # baffle
    # level marks
    for z, t in ((0, "FIN. FLOOR 0'-0\""), (UFF, "UPPER FIN. FLOOR 10'-8\""), (PLATE, "TOP OF PLATE 19'-8\"")):
        a = P(-60, z)
        s.line((a[0] - 0.55, a[1]), (a[0] - 0.05, a[1]), lw="f", dash="CENTER")
        s.text((a[0] - 0.6, a[1] + 0.04), t, 0.055, align="r")
    return zt


NOTES1 = [
    (0.0, "4\" PT SLAB ON 15-MIL VAPOR RETARDER, 4\" ABC"), (-14, "EDGE BEAM 12\" x 24\" MIN. (S-101); 18\" BELOW GRADE MIN."),
    (-2.2, "WEEP SCREED 4\" ABOVE GRADE / 2\" ABOVE PAVING"), (24, "2x6 STUDS @ 16\" O.C., R-21 BATTS (R-13 MIN. IECC)"),
    (60, "7/16\" OSB SHEATHING, 2 LAYERS GRADE D WRB, LATH"), (72, "7/8\" 3-COAT STUCCO, SAND FINISH, ELASTOMERIC COLOR COAT"),
    (95, "WINDOW: SILL PAN + HEAD FLASHING (D-001)"), (CEIL1 + 3, "F1 RATED CEILING (D-002/3)"), (CEIL1 + 13, "11-7/8\" FLOOR TRUSSES; RIM BOARD"),
    (PLATE - 4, "DOUBLE TOP PLATE; HURRICANE TIES EA. TRUSS (S-502)"), (PLATE + 6, "R-38 BLOWN; BAFFLE AT EAVE; 14\" RAISED HEEL"),
    (PLATE + 16, "CLAY TILE, 2 LAYERS UNDERLAYMENT, 7/16\" OSB"), (PLATE + 11, "VENTED SOFFIT (1/150 NFA), 5\" GUTTER"),
]
NOTES2 = [
    (0.0, "SAME SLAB AND FOOTING AS SECTION 1"), (24, "2x6 STUDS @ 16\" O.C., R-21 BATTS"), (40, "5/8\" TYPE X GWB INTERIOR, FULL HEIGHT TO DECK LINE"),
    (60, "5/8\" TYPE X GYPSUM SHEATHING (NOT OSB)"), (72, "2 LAYERS WRB, LATH, 7/8\" 3-COAT STUCCO"),
    (95, "WINDOWS B/C: 25% MAX. OPENINGS (G-002)"), (CEIL1 + 3, "F1 RATED CEILING CONTINUOUS TO W2"),
    (PLATE + 6, "NO SOFFIT VENTS IN THE WEST EAVE"), (PLATE + 11, "SOFFIT: 5/8\" TYPE X GWB, EXT. GRADE (705.2.3)"),
    (PLATE + 16, "BLOCK + FIRESTOP AT TOP OF WALL TO DECK"),
]


def labels(items, x_text):
    prev = 99
    for (z, t) in sorted(items, key=lambda a: -a[0]):
        a = P(4, z)
        yy = min(prev - 0.2, a[1] + 0.12)
        prev = yy
        s.line(a, (x_text - 0.05, yy + 0.03), lw="xf")
        s.circle(a, 0.015, lw="xf", fill=0.0)
        s.text((x_text, yy), t, 0.058, align="l")


at(4.8, 6.9); section("EXT"); labels(NOTES1, 7.2)
SL.drawing_title(s, 1.0, 4.4, "1", "A-302", "WALL SECTION — TYPICAL EXTERIOR WALL (N, S, E)", "SCALE: 1/2\" = 1'-0\"   AT A BEDROOM WINDOW, BOTH FLOORS", w=9.4, scalebar=False)
at(14.8, 6.9); section("W2"); labels(NOTES2, 17.2)
SL.drawing_title(s, 11.0, 4.4, "2", "A-302", "WALL SECTION — W2 RATED WEST WALL", "SCALE: 1/2\" = 1'-0\"   1 HOUR, FIRE SEPARATION DISTANCE 7'-0\"", w=9.4, scalebar=False)

s.scale = 48
NOTES = [
    "Wall sections show design intent. Structural sizes, hold-downs, shear wall nailing and connectors per the S-sheets.",
    "Weather-resistive barrier: two layers of Grade D paper (or one layer over a drainage mat) behind stucco, lapped shingle-style; integrate with window and door flashing (IBC 1404, 2510.6).",
    "Weep screed at the foundation plate line: 4\" min. above earth, 2\" min. above paving (IBC 2512.1.2).",
    "Slab: finish floor 8\" above finish grade; grade slopes away 5% for 10 ft (6\" fall) or to a swale (IBC 1804.4).",
    "Vented attic: 1/150 net free area split between soffit intake and high tile vents (IBC 1202.2.1). Baffles keep insulation 1\" clear of the deck. No soffit vents in the west eave (W2).",
    "Termite protection: soil treatment or bait system per IBC 2304.12.9 / Arizona OPM; treated bottom plates on the slab.",
    "Air barrier: interior GWB with sealed top and bottom plates, sealed penetrations and gasketed boxes; blower door 5 ACH50 max. (EN-001).",
    "Ceiling height 9'-0\" both floors; window heads align at 7'-0\" above finish floor all around.",
]
SL.notes_list(s, 21.15, 23.2, "WALL SECTION NOTES", NOTES, 5.1)
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="A-302", sheet_title="WALL SECTIONS"))
base = f"{OUT}/A-302_Model1_Wall_Sections"
s.to_pdf(base + ".pdf", title="A-302 Wall Sections - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
