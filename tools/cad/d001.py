"""D-001 envelope details, Model 1. 1 1/2" = 1'-0" (scale 8), z up. Exterior to the right in every detail."""
import math, sys
from cadkit import Sheet
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
s = Sheet(origin=(0, 0), scale=8)


def at(x, y):
    s.ox, s.oy = x, y


def R(x, z, w, h, lw="l", fill=None):
    s.rect(x, -(z + h), w, h, layer="A-DETL", lw=lw, space="m", fill=fill)


def Ln(a, b, lw="l", dash=None):
    s.line((a[0], -a[1]), (b[0], -b[1]), layer="A-DETL", lw=lw, space="m", dash=dash)


def PL(pts, lw="l", fill=None, closed=False):
    s.pline([(x, -z) for x, z in pts], layer="A-DETL", lw=lw, space="m", fill=fill, closed=closed)


def P(x, z):
    return s.m2p(x, -z)


def batt(x, z, w, h):
    n = max(1, int(h / (w * 0.7)))
    PL([(x + (w * 0.1 if i % 2 == 0 else w * 0.9), z + i * h / (n * 2)) for i in range(n * 2 + 1)], "xf")


def wall(z0, z1, studs=True):
    """2x6 wall: GWB -6.125..-5.5, studs -5.5..0, OSB 0..0.4375, WRB, stucco to 1.375"""
    R(-6.125, z0, 0.625, z1 - z0, "f", 0.82)
    R(-5.5, z0, 5.5, z1 - z0, "f")
    if studs:
        batt(-5.1, z0 + 0.5, 4.7, z1 - z0 - 1)
    R(0, z0, 0.4375, z1 - z0, "l", 0.6)
    R(0.4375, z0, 0.06, z1 - z0, "m")
    R(0.5, z0, 0.875, z1 - z0, "l", 0.92)


def notes(items, x_text, top):
    y = top
    for (pt, t) in sorted(items, key=lambda a: -a[0][1]):
        a = P(*pt)
        s.line(a, (x_text - 0.05, y + 0.03), lw="xf")
        s.circle(a, 0.015, lw="xf", fill=0.0)
        s.text((x_text, y), t, 0.06, align="l")
        y -= 0.22


COLX = [1.6, 8.3, 14.6]
ROWY = [16.6, 8.8]
TITLE_DY = -3.25


def title(i, num, t, sub):
    c, r = i % 3, i // 3
    SL.drawing_title(s, COLX[c] - 0.6, ROWY[r] + TITLE_DY, num, "D-001", t, sub, w=6.0, scalebar=False)


# 1 WINDOW HEAD
at(COLX[0] + 1.8, ROWY[0] - 0.6)
wall(10, 26)
R(-5.5, 2.0, 5.5, 8.0, "l", 0.55); Ln((-5.5, 2), (0, 10), "xf"); Ln((-5.5, 10), (0, 2), "xf")   # header
R(-5.5, 0.5, 5.5, 1.5, "l", 0.55)
R(-6.125, 0, 0.625, 2.0, "f", 0.82)
R(-3.0, -10, 3.0, 10, "m", 0.95); Ln((-1.5, -10), (-1.5, 0), "f")                                    # window frame + glass
PL([(-0.2, 0.5), (0.5, 0.5), (2.2, 0.2), (2.2, -0.6)], "m")                                         # head flashing / drip
R(0, 0.5, 0.4375, 9.5, "l", 0.6); R(0.4375, 0.5, 0.06, 9.5, "m"); R(0.5, 1.2, 0.875, 8.8, "l", 0.92)
PL([(0.5, 1.2), (1.5, 0.9), (1.5, 1.6)], "m")                                                        # casing bead
notes([((1.2, 5), "7/8\" 3-COAT STUCCO; CASING BEAD + BACKER ROD/SEALANT"), ((0.47, 14), "2 LAYERS WRB LAPPED OVER HEAD FLASHING"),
       ((1.8, 0.3), "METAL HEAD FLASHING W/ DRIP, END DAMS"), ((-1.5, -5), "WINDOW, NAIL FIN SET IN SEALANT"),
       ((-3, 6), "4x12 HEADER (S-102)"), ((-5.8, 1), "GWB RETURN, CORNER BEAD")], COLX[0] + 2.6, 20.6)
title(0, "1", "WINDOW HEAD", "SCALE: 1\u00bd\" = 1'-0\"  TYPICAL STUCCO WALL")

# 2 WINDOW SILL
at(COLX[1] + 1.8, ROWY[0] + 0.6)
wall(-14, -1.5)
R(-5.5, -1.5, 5.5, 1.5, "l", 0.55)
PL([(-5.5, 0.0), (-5.5, 0.3), (0.6, 0.3), (0.6, -1.0)], "m")                                          # sill pan
R(-3.0, 0.3, 3.0, 10, "m", 0.95); Ln((-1.5, 0.3), (-1.5, 10.3), "f")
R(-7.2, -0.3, 1.7, 0.75, "l", 0.7)                                                                   # stool
PL([(0.5, -1.0), (2.2, -1.6), (2.2, -2.4)], "m")
notes([((0.2, 0.3), "SELF-ADHERED SILL PAN, BACK DAM, UP JAMBS 6\""), ((1.5, -1.5), "SLOPED STUCCO SILL, WEEP, SEALANT JOINT"),
       ((-1.5, 6), "WINDOW, U 0.30 / SHGC 0.25"), ((-6.5, 0), "STOOL / GWB RETURN"),
       ((-2.5, -8), "2x6 SILL, R-21 BATTS"), ((0.47, -10), "WRB SHINGLED UNDER SILL PAN")], COLX[1] + 2.5, 20.6)
title(1, "2", "WINDOW SILL", "SCALE: 1\u00bd\" = 1'-0\"  BEDROOM WINDOW A, SILL 3'-0\"")

# 3 SLAB EDGE / WEEP SCREED
at(COLX[2] + 1.8, ROWY[0] + 0.9)
wall(1.5, 14)
R(-5.5, 0, 5.5, 1.5, "l", 0.62)
R(-14, -4, 14, 4, "m", 0.55); R(-14, -8, 14, 4, "xf", 0.85); Ln((-14, -4.2), (0, -4.2), "f", [3, 1.5])
R(-6, -24, 12, 20, "m", 0.55)
PL([(0, -2), (1.8, -2.4), (1.8, -0.8)], "m")
PL([(0.5, -2), (0.5, 14)], "f")
PL([(-14, -8.01), (6, -8.01), (6, -8), (12, -8.3)], "m")
for k in range(2):
    Ln((8 + k * 3, -8.3), (6 + k * 3, -10), "xf")
notes([((0, 0.75), "TREATED 2x6 SILL PLATE, ANCHOR BOLTS / STRAPS (S-201)"), ((1.6, -2.2), "WEEP SCREED 4\" MIN. ABOVE GRADE"),
       ((-8, -2), "4\" SLAB, 15-MIL VAPOR RETARDER, 4\" ABC"), ((-2, -16), "PT EDGE BEAM 12\" x 24\" (S-101)"),
       ((10, -8.2), "GRADE SLOPES AWAY 5% FOR 10'-0\""), ((-3, 8), "TERMITE TREATMENT PER AZ OPM")], COLX[2] + 3.4, 20.6)
title(2, "3", "SLAB EDGE AND WEEP SCREED", "SCALE: 1\u00bd\" = 1'-0\"  ALL EXTERIOR WALLS")

# 4 EAVE (vented)
at(COLX[0] + 2.0, ROWY[1] - 0.6)
wall(-10, 0)
R(-5.5, 0, 5.5, 3.0, "l", 0.55)
pitch = 4 / 12
zt = lambda x: 14 - x * pitch
PL([(-10, zt(-10)), (24, zt(24))], "m"); PL([(-10, zt(-10) + 0.44), (24, zt(24) + 0.44)], "l")
for k in range(-10, 22, 3):
    PL([(k, zt(k) + 0.6), (k + 1.5, zt(k + 1.5) + 2.6), (k + 3, zt(k + 3) + 0.6)], "xf")
R(22.5, zt(24) - 7.25, 1.5, 7.25, "l", 1.0)
PL([(24, zt(24) - 1), (27, zt(24) - 1), (27, zt(24) - 5), (24, zt(24) - 6)], "l")
R(1.4, zt(24) - 8, 21.1, 0.5, "f", 0.7); R(8, zt(24) - 8, 3, 0.5, "f", 0.2)
Ln((-10, 3), (0, 3), "l"); Ln((0, 3), (0, zt(0)), "l")
PL([(-8, 3.5), (-8, 12), (-2, zt(-2) - 1)], "xf")
for k in range(-10, -1, 3):
    PL([(k + 1.5 * (1 - math.cos(t)), 3.3 + 8 * math.sin(t / 2)) for t in [i * math.pi / 6 for i in range(7)]], "xf")
notes([((15, zt(15) + 1.5), "CLAY TILE, BATTENS, 2 LAYERS UNDERLAYMENT, 7/16\" OSB"), ((23.3, zt(24) - 4), "2x8 FASCIA, 5\" K-STYLE GUTTER"),
       ((9.5, zt(24) - 7.8), "CONTINUOUS SOFFIT VENT (1/150 NFA, 50% LOW)"), ((-5, 9), "BAFFLE: 1\" AIR SPACE TO DECK"),
       ((-6, 5), "R-38 BLOWN; 14\" RAISED-HEEL TRUSS"), ((-2, 1.5), "DOUBLE TOP PLATE; HURRICANE TIE (S-502)")], COLX[0] + 3.4, 12.6)
title(3, "4", "EAVE — TYPICAL (N, S, E)", "SCALE: 1\u00bd\" = 1'-0\"  VENTED SOFFIT")

# 5 EAVE (rated west)
at(COLX[1] + 2.0, ROWY[1] - 0.6)
R(-6.125, -10, 0.625, 13, "f", 0.82); R(-5.5, -10, 5.5, 10, "f"); batt(-5.1, -9.5, 4.7, 9)
R(0, -10, 0.625, 10 + 13, "f", 0.82); R(0.625, -10, 0.06, 10, "m"); R(0.69, -10, 0.875, 10, "l", 0.92)
R(-5.5, 0, 5.5, 3.0, "l", 0.55)
PL([(-10, zt(-10)), (24, zt(24))], "m"); PL([(-10, zt(-10) + 0.44), (24, zt(24) + 0.44)], "l")
for k in range(-10, 22, 3):
    PL([(k, zt(k) + 0.6), (k + 1.5, zt(k + 1.5) + 2.6), (k + 3, zt(k + 3) + 0.6)], "xf")
R(22.5, zt(24) - 7.25, 1.5, 7.25, "l", 1.0)
R(1.6, zt(24) - 8, 20.9, 0.625, "f", 0.82)
R(0, 3, 1.5, zt(0) - 3, "l", 0.55)
Ln((-10, 3), (0, 3), "l")
notes([((15, zt(15) + 1.5), "TILE ROOF AS DETAIL 4"), ((10, zt(24) - 7.7), "5/8\" TYPE X EXT. GYPSUM SOFFIT, NO VENTS"),
       ((0.7, 8), "SOLID BLOCKING + FIRESTOP TO DECK"), ((0.3, -6), "5/8\" TYPE X SHEATHING CONTINUES TO SOFFIT"),
       ((-3, -5), "W2: 1 HR BOTH SIDES (D-002/2)"), ((23.3, zt(24) - 4), "FASCIA 2x8, GUTTER")], COLX[1] + 3.4, 12.6)
title(4, "5", "EAVE — RATED WEST WALL (W2)", "SCALE: 1\u00bd\" = 1'-0\"  IBC 705.2.3, FSD 7'-0\"")

# 6 THRESHOLD AT SLIDER / ACCESSIBLE ENTRY
at(COLX[2] + 1.8, ROWY[1] + 0.2)
R(-14, -4, 18, 4, "m", 0.55); R(-14, -8, 18, 4, "xf", 0.85)
R(-14, 0, 12, 0.375, "l", 0.4)
PL([(-2, 0), (2, 0), (2, 0.5), (-1, 0.5), (-2, 0.375)], "m", 0.6)
R(-1.5, 0.5, 3.0, 12, "m", 0.95)
R(4, -4.5, 9, 4, "m", 0.85)
PL([(4, -0.5), (13, -0.7)], "l")
PL([(-2.2, -0.2), (2.2, -0.2), (2.2, -0.6), (3.8, -0.9)], "m")
notes([((0, 0.5), "THRESHOLD 1/2\" MAX. HIGH, BEVELED 1:2 (A117.1 404.2.5)"), ((-8, 0.2), "FINISH FLOOR (LVP / TILE)"),
       ((2.6, -0.5), "SILL PAN UNDER THRESHOLD, SLOPE TO EXTERIOR"), ((9, -0.6), "PATIO SLAB 1/2\" BELOW FLOOR, 2% AWAY"),
       ((-6, -2), "SLAB RECESSED 1-1/2\" AT DOOR (S-101)"), ((0, 8), "SLIDER 119/131 OR ENTRY 101")], COLX[2] + 3.4, 11.4)
title(5, "6", "ACCESSIBLE THRESHOLD", "SCALE: 1\u00bd\" = 1'-0\"  DOORS 101, 119, 131 (ZERO-STEP)")

s.scale = 48
NOTES = [
    "Stucco system per ASTM C926 / C1063: 7/8\" three-coat, galvanized expanded metal lath over two layers of Grade D WRB; control joints at 144 SF max. panels and at every floor line (horizontal expansion joint at the band).",
    "Flashing sequence: sill pan first, window set in sealant, jamb flashing, head flashing, then the upper WRB lapped over the head flashing. Water must always run out, never behind.",
    "Sealant: backer rod and polyurethane or silicone at all frame-to-stucco joints; no caulk-only joints.",
    "Every window and door: pre-install sill pan with end dams and back dam. Window opening rough sizes per the manufacturer.",
    "Air sealing: foam or sealant around window and door frames at the interior; seal the bottom plate to the slab with sill gasket.",
    "Accessible thresholds at doors 101, 119, 131 and the unit A entry: 1/2\" max. height, changes over 1/4\" beveled 1:2; exterior slab 1/2\" below finish floor, sloped 2% away.",
]
SL.notes_list(s, 21.15, 23.2, "ENVELOPE NOTES", NOTES, 5.1)
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="D-001", sheet_title="ENVELOPE\nDETAILS"))
base = f"{OUT}/D-001_Model1_Envelope_Details"
s.to_pdf(base + ".pdf", title="D-001 Envelope Details - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
