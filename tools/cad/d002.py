"""D-002 rated assembly and firestop details, Model 1. Details at 1 1/2" = 1'-0" (scale 8) and 3" = 1'-0" (scale 4)."""
import math, sys
from cadkit import Sheet
from plan_engine import para
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
s = Sheet(origin=(0, 0), scale=8)


FLIP = [False]


def at(x, y, scale=8, flip=False):
    s.ox, s.oy, s.scale = x, y, scale
    FLIP[0] = flip


def fy(y, h=0):
    return -(y + h) if FLIP[0] else y


def R(x, y, w, h, lw="l", fill=None, layer="A-DETL"):
    s.rect(x, fy(y, h), w, h, layer=layer, lw=lw, space="m", fill=fill)


def Ln(a, b, lw="l", dash=None, layer="A-DETL"):
    s.line((a[0], fy(a[1])), (b[0], fy(b[1])), layer=layer, lw=lw, space="m", dash=dash)


def batt(x, y, w, h, vertical=True):
    """insulation squiggle inside a rectangle (model inches)."""
    pts = []
    if vertical:
        n = int(h / (w * 0.6)) + 1
        for i in range(n * 4 + 1):
            t = i / 4
            yy = y + t * (h / n)
            xx = x + (w * 0.15 if i % 4 in (0,) else w * 0.85 if i % 4 == 2 else w * 0.5)
            pts.append((xx, yy))
    else:
        n = int(w / (h * 0.6)) + 1
        for i in range(n * 4 + 1):
            t = i / 4
            xx = x + t * (w / n)
            yy = y + (h * 0.15 if i % 4 == 0 else h * 0.85 if i % 4 == 2 else h * 0.5)
            pts.append((xx, yy))
    s.pline([(a, fy(b)) for a, b in pts], layer="A-DETL-INSL", lw="xf", space="m")


def leader(p, txt_xy, txt, h=0.07):
    """p in model inches, txt_xy in paper inches."""
    a = s.m2p(p[0], fy(p[1]))
    s.line(a, (txt_xy[0] - 0.05, txt_xy[1] + 0.03), layer="A-ANNO-TEXT", lw="xf")
    s.circle(a, 0.02, layer="A-ANNO-TEXT", lw="xf", fill=0.0)
    s.text(txt_xy, txt, h, align="l")


def gwb(x, y, w, h):
    R(x, y, w, h, "f", 0.82)


def P(x, y):
    return s.m2p(x, fy(y))


# ---------------------------------------------------------------- 1. W1 plan section (3" = 1'-0")
at(2.4, 19.7, 4)
# staggered studs on 2x6 plate, 5.5" plate, 5/8 GWB both sides + RC one side
X0 = 0
# real build: from left face: GWB 5/8, RC 1/2, plate 5.5, GWB 5/8
xL = 0.0
gwb(xL, 0, 0.625, 16); xL += 0.625
R(xL, 0, 0.5, 16, "xf"); s.text(s.m2p(xL + 0.25, -0.8), "RC", 0.05); xL += 0.5
R(xL, 0, 5.5, 16, "f")
for i, y in enumerate((1, 7, 13)):
    left = i % 2 == 0
    R(xL + (0 if left else 2.0), y, 3.5, 1.5, "l", 0.55)
    s.line(s.m2p(xL + (0 if left else 2.0), y), s.m2p(xL + (3.5 if left else 5.5), y + 1.5), layer="A-DETL", lw="xf")
    s.line(s.m2p(xL + (0 if left else 2.0), y + 1.5), s.m2p(xL + (3.5 if left else 5.5), y), layer="A-DETL", lw="xf")
batt(xL + 0.6, 0.3, 4.3, 15.4)
xL += 5.5
gwb(xL, 0, 0.625, 16); xL += 0.625
for yy in (0, 16):
    Ln((-0.5, yy), (xL + 0.5, yy), "xf", [3, 2])
s.text(s.m2p(-5, 8), "UNIT", 0.07, font="Helvetica-Bold"); s.text(s.m2p(xL + 1.5, -1.8), "CORE OR UNIT", 0.07, font="Helvetica-Bold", align="l")
for i, (pt, t) in enumerate([((0.3, 2.5), "5/8\" TYPE X GWB, JOINTS TAPED"), ((0.9, 4.5), "RESILIENT CHANNEL @ 24\" O.C. (ONE SIDE ONLY)"),
        ((2.5, 7.7), "STAGGERED 2x4 STUDS @ 16\" O.C. EACH SIDE"), ((4.5, 1.5), "2x6 TOP + BOTTOM PLATES"),
        ((4.0, 11), "3\u00bd\" BATTS, WOVEN BETWEEN STUDS"), ((7.0, 15), "5/8\" TYPE X GWB, JOINTS TAPED")]):
    leader(pt, (5.0, 19.45 - i * 0.3), t, 0.065)
SL.drawing_title(s, 1.0, 14.8, "1", "D-002", "W1 UNIT SEPARATION WALL — PLAN SECTION", "SCALE: 3\" = 1'-0\"   1 HOUR (UL U341 OR EQUAL) · STC 55", w=9.6, scalebar=False)
for t, yy in (("UNIT C/A SIDE  ←", 19.7), ("→  SHARED ENTRY / UNIT SIDE", 19.7)):
    pass

# ---------------------------------------------------------------- 2. W2 exterior wall plan section (3" = 1'-0")
at(12.2, 19.7, 4)
xL = 0
gwb(xL, 0, 0.625, 16); xL += 0.625
R(xL, 0, 5.5, 16, "f")
for y in (1, 13):
    R(xL, y, 5.5, 1.5, "l", 0.55)
    s.line(s.m2p(xL, y), s.m2p(xL + 5.5, y + 1.5), layer="A-DETL", lw="xf"); s.line(s.m2p(xL, y + 1.5), s.m2p(xL + 5.5, y), layer="A-DETL", lw="xf")
batt(xL + 0.5, 2.8, 4.5, 10.0)
xL += 5.5
gwb(xL, 0, 0.625, 16); xL += 0.625
R(xL, 0, 0.06, 16, "m"); xL += 0.06
R(xL, 0, 0.875, 16, "l", 0.92)
for k in range(8):
    s.line(s.m2p(xL + 0.1, k * 2 + 0.3), s.m2p(xL + 0.78, k * 2 + 1.2), layer="A-DETL", lw="xf")
xL += 0.875
s.text(s.m2p(-5, 8), "UNIT", 0.07, font="Helvetica-Bold"); s.text(s.m2p(xL + 1.5, -1.8), "EXTERIOR — 7'-0\" TO LOT LINE", 0.065, font="Helvetica-Bold", align="l")
for i, (pt, t) in enumerate([((0.3, 3), "5/8\" TYPE X GWB INTERIOR"), ((3.5, 7), "2x6 STUDS @ 16\" O.C., R-21 BATTS"),
        ((6.4, 5), "5/8\" TYPE X GYPSUM SHEATHING, EXTERIOR GRADE"), ((6.75, 10), "2 LAYERS GRADE D WRB + LATH"), ((7.3, 14), "7/8\" 3-COAT CEMENT STUCCO")]):
    leader(pt, (15.4, 18.85 - i * 0.3), t, 0.065)
SL.drawing_title(s, 11.2, 14.8, "2", "D-002", "W2 EXTERIOR WALL, WEST — PLAN SECTION", "SCALE: 3\" = 1'-0\"   1 HOUR BOTH SIDES (UL U356 OR EQUAL) · FSD 7'-0\"", w=9.6, scalebar=False)

# ---------------------------------------------------------------- 3. F1 floor/ceiling (1 1/2" = 1'-0")
at(1.4, 8.3, 8, flip=True)
W = 60
z = 0
R(0, z, W, 0.625, "f", 0.82); R(0, z + 0.625, W, 0.625, "f", 0.82); z += 1.25      # 2 layers GWB
R(0, z, W, 0.5, "xf"); z += 0.5                                                 # RC
for x in range(0, W, 16):
    R(x + 1, z, 1.5, 5.5, "l", 0.55)
batt(0.2, z + 0.4, W - 0.4, 3.5, vertical=False)
z += 5.5
R(0, z, W, 1.0, "xf")                                                  # air gap
z += 1.0
zt = z
R(0, z, W, 11.875, "f")
for x in range(0, W - 4, 24):
    R(x + 2, z, 3.5, 1.5, "l", 0.55); R(x + 2, z + 11.875 - 1.5, 3.5, 1.5, "l", 0.55)
k = 0
for xx in range(0, W - 6, 6):
    a = (xx, z + 1.5); b = (xx + 6, z + 11.875 - 1.5)
    if k % 2:
        a, b = (xx, z + 11.875 - 1.5), (xx + 6, z + 1.5)
    Ln(a, b, "xf"); k += 1
z += 11.875
R(0, z, W, 0.75, "l", 0.6); z += 0.75
R(0, z, W, 0.25, "xf", 0.3); z += 0.25
R(0, z, W, 0.5, "l", 0.9); z += 0.5
# leaders: note this view's model y grows down on paper, so text goes to the right
lx = 1.4 + W / 8 + 0.4
for (yy, t) in [(z - 0.25, "FINISH FLOOR (LVP OR TILE) ON 1/4\" ACOUSTIC MAT"),
                (z - 0.9, "3/4\" T&G OSB SUBFLOOR, GLUED + SCREWED"),
                (zt + 6, "11⅞\" OPEN-WEB FLOOR TRUSS @ 24\" O.C. (S-102)"),
                (zt - 0.5, "1\" AIR SPACE — NOTHING ATTACHED TO THE TRUSSES"),
                (6, "INDEPENDENT 2x6 CEILING JOISTS @ 16\" O.C., R-19"),
                (1.5, "RESILIENT CHANNEL @ 16\" O.C."),
                (0.6, "2 LAYERS 5/8\" TYPE X GWB, JOINTS STAGGERED")]:
    p = P(W - 4, yy)
    s.line(p, (lx - 0.05, p[1]), layer="A-ANNO-TEXT", lw="xf")
    s.text((lx, p[1] - 0.025), t, 0.06, align="l")
SL.drawing_title(s, 1.0, 6.9, "3", "D-002", "F1 FLOOR / CEILING BETWEEN UNITS", "SCALE: 1½\" = 1'-0\"   1 HOUR (UL L528 / GA FC 5512 OR EQUAL) · STC 50 / IIC 50", w=9.6, scalebar=False)

# ---------------------------------------------------------------- 4. W1 at roof: draftstop (1 1/2" = 1'-0")
at(14.0, 9.9, 12, flip=True)
# roof deck sloping, truss top chords both sides; wall rises to deck
deck = lambda x: 30 - 0 * x
Ln((-30, 34), (36, 22), "m"); Ln((-30, 35), (36, 23), "l")      # OSB deck (4:12-ish shown)
Ln((-30, 35), (36, 23), "f")
for x in (-28, -4, 20):
    zz = 34 - (x + 30) * 12 / 66
    R(x, 0, 1.5, zz - 0.3, "l", 1.0) if False else None
# ceiling line both sides
gwb(-30, -0.625, 26.5, 0.625); gwb(6.3, -0.625, 30, 0.625)
# wall: 2 layers studs w/ GWB both sides to deck
top = lambda x: 34 - (x + 30) * 12 / 66
for xx, w_ in ((-3.5, 0.625), (5.5, 0.625)):
    gwb(xx, -24, w_, top(xx) - (-24) - 0.4)
R(-2.875, -24, 8.375, 24 + top(1.3) - 0.6, "f")
R(-2.875, -0.0, 8.375, 1.5, "l", 0.55)            # double top plates? (plate at ceiling for lower part)
R(-2.875, 1.5, 8.375, 1.5, "l", 0.55)
batt(-2.3, -23, 7.2, 22)
for i, (pt, t) in enumerate([((1.3, top(1.3) - 0.5), "LISTED HEAD-OF-WALL JOINT AT THE DECK (715)"), ((-3.2, 14), "W1 CONTINUES TO THE UNDERSIDE OF THE DECK"),
        ((6.0, 10), "5/8\" TYPE X GWB BOTH SIDES IN THE ATTIC (718.4)"), ((1.3, 2.2), "DOUBLE TOP PLATE AT CEILING LINE"), ((22, -0.3), "CEILING: 5/8\" TYPE X GWB, R-38 ABOVE"), ((1.3, -12), "W1 BELOW: SEE DETAIL 1")]):
    leader(pt, (17.6, 12.9 - i * 0.3), t, 0.065)
s.text(P(-17, 16), "ATTIC A / C", 0.07, font="Helvetica-Bold"); s.text(P(22, 14), "ATTIC CORE", 0.07, font="Helvetica-Bold")
s.text(P(-17, -10), "UNIT C", 0.07, font="Helvetica-Bold"); s.text(P(22, -10), "LOFT 202", 0.07, font="Helvetica-Bold")
SL.drawing_title(s, 11.2, 6.9, "4", "D-002", "W1 AT ROOF — ATTIC DRAFTSTOP", "SCALE: 1\" = 1'-0\"   NO OPENINGS IN THE DRAFTSTOP; ATTIC ACCESS EACH SIDE", w=9.6, scalebar=False)

# ---------------------------------------------------------------- 5. firestop schedule table
from plan_engine import table
s.scale = 48
y = SL.head(s, 1.0, 6.1, "5  ·  THROUGH-PENETRATION FIRESTOP SCHEDULE (IBC 714) — USE A LISTED SYSTEM FOR EACH CONDITION", 19.8)
rows = [
    ("F1 floor", "Copper / PEX water pipe ≤ 1\"", "Listed F/T-rated system, e.g. UL F-C-1xxx / F-C-2xxx series", "F 1 HR, T 1 HR"),
    ("F1 floor", "PVC / ABS DWV ≤ 4\"", "Intumescent collar or wrap system for plastic pipe, UL F-C-2xxx", "F 1 HR"),
    ("F1 floor", "Cast iron DWV in chases (alt.)", "Mineral wool + sealant, UL F-C-1xxx", "F 1 HR"),
    ("F1 ceiling", "Supply / return ducts", "Listed ceiling radiation damper in the rated ceiling (717.6.2)", "1 HR"),
    ("F1 ceiling", "Light fixtures, boxes", "Surface-mounted only; boxes listed for rated ceilings or protected with fire-rated enclosures", "—"),
    ("W1 / W2", "Electrical cable (NM) through wall", "Avoid in W1. Where unavoidable: listed system W-L-3xxx", "F 1 HR"),
    ("W2", "Exterior penetrations (hose bib, vents)", "Listed system W-L-xxxx; no dryer or bath vents in W2", "F 1 HR"),
    ("Top of W1", "Head-of-wall joint to deck", "Listed joint system HW-D-xxxx", "1 HR"),
]
table(s, 1.0, y + 0.04, [("LOCATION", 1.4, "l"), ("PENETRATING ITEM", 3.4, "l"), ("SYSTEM (BASIS OF DESIGN)", 11.0, "l"), ("RATING", 4.0, "c")], rows, h=0.068, rowh=0.17)

NOTES = [
    "Details show the basis of design. Any substitute assembly or firestop must be a tested, listed system of equal or greater rating; submit the listing with the shop drawings.",
    "Rated assemblies are inspected before cover. Firestop installer to be trained by the manufacturer; label each firestop with the system number, installer and date.",
    "Keep W1 free of plumbing, ducts, recessed boxes and medicine cabinets. Back-to-back outlets are not allowed in W1; offset 24\" min. where any box occurs in a rated wall (714.4.2).",
    "F1: nothing is attached to, hung from or penetrates the floor-truss bottom chords; the ceiling joists span independently. Plumbing in F1 runs in chases CH1–CH4 (X-101).",
    "Resilient channel: install per the listing with screws into the channel only; any screw into the framing short-circuits the sound isolation.",
    "Acoustic sealant at the perimeter of every GWB layer in W1 and F1 (both faces), and at all penetrations.",
    "W2 eave: soffit within the 7'-0\" fire separation distance framed with 1-hour protection (5/8\" Type X GWB under the rafter tails) or fire-retardant-treated wood per IBC 705.2.3; no soffit vents in the west eave.",
    "Mark rated walls in the attic: 'FIRE AND/OR SMOKE BARRIER — PROTECT ALL OPENINGS', 3\" letters, every 30 ft (703.5).",
]
SL.notes_list(s, 21.15, 23.2, "DETAIL NOTES", NOTES, 5.1)
TEST = [
    "Field sound testing (ASTM E336 / E1007) of one W1 wall and one F1 floor before move-in: FSTC 45 and FIIC 45 minimum (IBC 1206.2.1, 1206.3.1).",
    "Blower door test of each unit (IECC R402.4.1.2) after the drywall is up: 5.0 ACH50 max.",
    "Third-party inspection of firestopping recommended (ASTM E2174); required if the building official asks.",
]
SL.notes_list(s, 26.55, 23.2, "TESTING", TEST, 5.25)
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="D-002", sheet_title="RATED ASSEMBLY\n+ FIRESTOP DETAILS"))
base = f"{OUT}/D-002_Model1_Rated_Assembly_Details"
s.to_pdf(base + ".pdf", title="D-002 Rated Assembly and Firestop Details - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
