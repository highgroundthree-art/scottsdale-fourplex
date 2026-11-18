"""S-102 floor framing plan and S-103 roof framing plan, Model 1 (design intent for the structural engineer)."""
import sys
from cadkit import Sheet
from plan_engine import dim_chain, bubble, table
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
F = 12
common = dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE)


def kit(s):
    R = lambda x, y, w, h, lw="l", dash=None, fill=None, layer="S-FRAM": s.rect(x * F, y * F, w * F, h * F, layer=layer, lw=lw, space="m", dash=dash, fill=fill)
    L = lambda a, b, lw="l", dash=None, layer="S-FRAM": s.line((a[0] * F, a[1] * F), (b[0] * F, b[1] * F), layer=layer, lw=lw, space="m", dash=dash)
    T = lambda x, y, t, h=0.075, **k: s.text(s.m2p(x * F, y * F), t, h, **k)
    return R, L, T


def grids(s):
    for x, lab in ((0, "1"), (12.5, "1.5"), (25, "2"), (35, "3"), (47.5, "3.5"), (60, "4")):
        px = s.m2p(x * F, 0)[0]; py = s.m2p(0, -6 * F)[1]
        s.line((px, py - 0.2), (px, py - 0.85), layer="A-GRID", lw="xf"); bubble(s, (px, py), lab)
    for y, lab in ((0, "A"), (50, "B")):
        py = s.m2p(0, y * F)[1]; px = s.m2p(-6 * F, 0)[0]
        s.line((px + 0.2, py), (px + 0.85, py), layer="A-GRID", lw="xf"); bubble(s, (px, py), lab)
    dim_chain(s, [0, 150, 300, 420, 570, 720], 59 * F, "h", -0.3)
    dim_chain(s, [0, 720], 59 * F, "h", -0.6)
    dim_chain(s, [0, 600], 62 * F, "v", 0.45)


def walls(s, R, L):
    R(0, 0, 60, 50, "h")
    for x in (25, 35):
        R(x - 0.33, 0, 0.66, 50, "m", fill=0.5)


def span_arrow(s, L, T, x0, x1, y, txt):
    L((x0 + 0.3, y), (x1 - 0.3, y), "m")
    for x, d in ((x0 + 0.3, 1), (x1 - 0.3, -1)):
        L((x, y), (x + d * 0.9, y - 0.5), "m"); L((x, y), (x + d * 0.9, y + 0.5), "m")
    T((x0 + x1) / 2, y - 0.6, txt, 0.065, font="Helvetica-Bold")


# ============================================================ S-102
s = Sheet(origin=(3.6, 20.1))
R, L, T = kit(s)
walls(s, R, L)
# trusses @ 24" spanning E-W in each unit bay, bearing on ext wall, beam line 1.5/3.5 and W1 (each side bears its own)
for (a, b) in ((0, 12.5), (12.5, 24.67), (35.33, 47.5), (47.5, 60)):
    y = 1
    while y < 49.5:
        L((a + 0.2, y), (b - 0.2, y), "xf")
        y += 2
for (a, b, y, t) in ((0, 12.5, 30, "FT1 @ 24\""), (12.5, 24.67, 30, "FT1 @ 24\""), (35.33, 47.5, 30, "FT1 @ 24\""), (47.5, 60, 30, "FT1 @ 24\"")):
    span_arrow(s, L, T, a, b, y, t)
# bearing lines 1.5 / 3.5: flush LVL beams on posts
for x in (12.5, 47.5):
    L((x, 0.5), (x, 49.5), "h", [10, 3])
    T(x - 0.8, 10, "FB1 FLUSH BEAM / BEARING WALL", 0.06, rot=90)
    for y in (0.5, 17.5, 33, 49.5):
        R(x - 0.4, y - 0.4, 0.8, 0.8, "m", fill=0.0)
# core: stair opening + landing
R(25.4, 27.5, 9.2, 8.25, "m", [6, 3]); L((25.4, 27.5), (34.6, 35.75), "f"); L((25.4, 35.75), (34.6, 27.5), "f")
T(30, 31.9, "STAIR OPENING", 0.065, font="Helvetica-Bold")
y = 1
while y < 27:
    L((25.8, y), (34.2, y), "xf"); y += 2
y = 36.5
while y < 49.5:
    L((25.8, y), (34.2, y), "xf"); y += 2
T(30, 12, "FT2 @ 24\" (CORE)", 0.065, font="Helvetica-Bold"); T(30, 43, "FT2 @ 24\"", 0.065, font="Helvetica-Bold")
R(28.75, 16.0, 2.5, 2.5, "l", [3, 2]); T(30, 19.4, "HATCH 202", 0.05)
for (x, y) in ((25.4, 27.5), (34.6, 27.5), (25.4, 35.75), (34.6, 35.75)):
    R(x - 0.3, y - 0.3, 0.6, 0.6, "m", fill=0.0)
T(30, 37.2, "HEADER H1 AT STAIR OPENING", 0.05)
# rim + notes
T(6.25, -1.4, "RIM BOARD 1-1/4\" LSL, ALL EXTERIOR WALLS", 0.06)
T(12.5, 51.6, "POSTS TO RIB R1 (S-101)", 0.06)
grids(s)
SL.drawing_title(s, 1.35, 3.15, "1", "S-102", "SECOND FLOOR FRAMING PLAN", "SCALE: 1/4\" = 1'-0\"   DESIGN INTENT — FINAL DESIGN BY THE STRUCTURAL ENGINEER OF RECORD", w=16.0)
SL.north_arrow(s, 18.6, 3.6)
y = SL.head(s, 21.15, 23.2, "FRAMING SCHEDULE (PRELIMINARY)", 10.6)
y = table(s, 21.15, y + 0.04, [("MARK", 0.7, "c"), ("MEMBER", 3.6, "l"), ("SPAN", 1.2, "c"), ("NOTE", 5.1, "l")], [
    ("FT1", "11-7/8\" open-web wood floor truss @ 24\" o.c.", "12'-6\"", "L/480 live, L/360 total; strongback at mid-span"),
    ("FT2", "11-7/8\" open-web wood floor truss @ 24\" o.c.", "10'-0\"", "Core, bear on W1 each side; no load to the trusses below"),
    ("FB1", "Flush LVL beam, 3-1/2\" x 11-7/8\" min.", "±16'-6\"", "Or bearing wall where the plan allows; posts to rib R1"),
    ("H1", "Header at stair opening, (2) 1-3/4\" x 11-7/8\" LVL", "9'-2\"", "Hangers each end"),
    ("RIM", "1-1/4\" x 11-7/8\" LSL rim board", "—", "Continuous; nail per S-502"),
    ("SUB", "3/4\" T&G OSB, glued and screwed", "—", "Under acoustic mat and finish (D-002/3)"),
], h=0.066, rowh=0.17) - 0.25
NOTES = [
    "Design intent only. Truss layout, member sizes, hangers and connections are designed by the Arizona-registered structural engineer and the truss manufacturer (deferred submittal).",
    "Why grid lines 1.5 and 3.5: an 11-7/8\" truss spanning 25 ft is near its limit for an STC/IIC 50 floor. A bearing line at mid-unit halves the span, keeps the 10'-8\" floor-to-floor and the 9'-0\" ceilings. Alternate: 16\" trusses clear-span, which adds 4\" to the building height (A-301.1).",
    "Each unit's floor framing bears on its own side of the double-stud W1 wall. Nothing frames across W1 (sound and fire separation).",
    "Floor trusses: nothing attached to or hung from bottom chords (independent ceiling joists, D-002/3). Duct and pipe routes through the open webs to be coordinated on X-101 before the truss order.",
    "Design loads: dead 15 psf + 10 psf ceiling; live 40 psf (residential), 100 psf at the common landing and stair (IBC Table 1607.1).",
    "Posts at FB1 run down to rib R1 in the PT slab; post bases and caps per S-502.",
]
SL.notes_list(s, 21.15, y, "FLOOR FRAMING NOTES", NOTES, 10.6)
SL.border_and_titleblock(s, dict(common, sheet_no="S-102", sheet_title="FLOOR FRAMING\nPLAN"))
base = f"{OUT}/S-102_Model1_Floor_Framing_Plan"
s.to_pdf(base + ".pdf", title="S-102 Floor Framing Plan - Model 1", author="Scottsdale Fourplex"); s.to_dxf(base + ".dxf"); print("wrote", base)

# ============================================================ S-103
s = Sheet(origin=(3.6, 20.1))
R, L, T = kit(s)
R(-2, -2, 64, 54, "l", [8, 3])
walls(s, R, L)
# common trusses spanning N-S between the ridge... hip roof: girder trusses + hip jacks
for x in range(25, 36, 2):
    L((x, -1.8), (x, 51.8), "xf")
T(30, 3.5, "T1 COMMON @ 24\"", 0.065, font="Helvetica-Bold")
for x in range(3, 25, 2):
    L((x, -1.8), (x, 51.8), "xf", [4, 2])
for x in range(37, 60, 2):
    L((x, -1.8), (x, 51.8), "xf", [4, 2])
T(13, 12, "T2 STEP-DOWN HIP TRUSSES @ 24\"", 0.065, font="Helvetica-Bold"); T(47, 12, "T2 STEP-DOWN HIP TRUSSES @ 24\"", 0.065, font="Helvetica-Bold")
for x in (24.67, 35.33):
    L((x, -1.8), (x, 51.8), "h")
    T(x + (-0.8 if x < 30 else 0.8), 40, "G1 HIP GIRDER (ON W1)", 0.06, rot=90)
for (a, b) in (((-2, -2), (25, 25)), ((-2, 52), (25, 25)), ((62, -2), (35, 25)), ((62, 52), (35, 25)), ((25, 25), (35, 25))):
    L(a, b, "m", [10, 3])
T(30, 24.2, "RIDGE", 0.065, font="Helvetica-Bold")
T(5, 36, "J1 JACKS", 0.065); T(55, 36, "J1 JACKS", 0.065)
# attic draftstop at W1, attic access
for (x, y) in ((8, 15.5), (52, 15.5)):
    R(x - 1.1, y - 1.25, 2.2, 2.5, "m", fill=0.85); T(x, y + 2.3, "ATTIC ACCESS 22x30", 0.05)
# loggia
R(22.5, 50, 15, 7, "m"); T(30, 54.2, "LOGGIA: 2x RAFTERS @ 24\" ON 4x12 BEAM, (2) 6x6 POSTS", 0.055)
grids(s)
SL.drawing_title(s, 1.35, 3.15, "1", "S-103", "ROOF FRAMING PLAN", "SCALE: 1/4\" = 1'-0\"   HIP ROOF 4:12, ENGINEERED TRUSSES @ 24\" O.C. — DESIGN INTENT", w=16.0)
SL.north_arrow(s, 18.6, 3.6)
y = SL.head(s, 21.15, 23.2, "ROOF FRAMING SCHEDULE (PRELIMINARY)", 10.6)
y = table(s, 21.15, y + 0.04, [("MARK", 0.7, "c"), ("MEMBER", 3.6, "l"), ("SPAN", 1.2, "c"), ("NOTE", 5.1, "l")], [
    ("T1", "Common truss, 4:12, 14\" raised heel, @ 24\"", "50'-0\" + eaves", "Core zone; interior bearing on W1 only if the designer uses it"),
    ("T2", "Step-down hip trusses @ 24\"", "50'-0\"", "Flat-top hip system, end set by girder G1"),
    ("G1", "Hip girder truss (multi-ply)", "50'-0\"", "Bears on the W1 walls and the exterior walls; hangers per mfr."),
    ("J1", "Hip jacks / corner jacks", "varies", "On the hip girders, 24\" o.c."),
    ("DECK", "7/16\" OSB, H-clips, 8d @ 6/12", "—", "Roof diaphragm per S-201"),
], h=0.066, rowh=0.17) - 0.25
NOTES = [
    "Design intent. Final truss layout, girders, hangers and bracing by the truss manufacturer, reviewed by the structural engineer (deferred submittal).",
    "Design loads: roof dead 15 psf + 12 psf clay tile (27 psf total top chord); roof live 20 psf; bottom chord 10 psf + R-38; wind 115 mph Vult, exposure C (verify with ASCE 7 Hazard Tool for the parcel); Seismic Design Category B (verify).",
    "Clay tile adds weight: confirm the tile manufacturer's weight and use it in the truss design.",
    "Uplift: hurricane tie at every truss to the top plate; straps at girders to posts or hold-downs per S-201.",
    "W1 walls rise to the roof deck and divide the attic (D-002/4). The truss designer must not run a top or bottom chord through W1; trusses are split at each W1.",
    "Permanent truss bracing per the truss design drawings and BCSI-B3. Temporary bracing per BCSI-B1.",
    "No HVAC equipment in the attic above the bottom chord load assumed; condensers at grade.",
]
SL.notes_list(s, 21.15, y, "ROOF FRAMING NOTES", NOTES, 10.6)
SL.border_and_titleblock(s, dict(common, sheet_no="S-103", sheet_title="ROOF FRAMING\nPLAN"))
base = f"{OUT}/S-103_Model1_Roof_Framing_Plan"
s.to_pdf(base + ".pdf", title="S-103 Roof Framing Plan - Model 1", author="Scottsdale Fourplex"); s.to_dxf(base + ".dxf"); print("wrote", base)
