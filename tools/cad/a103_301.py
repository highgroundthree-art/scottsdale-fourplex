"""A-103.1 roof plan and A-301.1 building sections, Model 1."""
import math, sys
from cadkit import Sheet, fmt_ftin
from elev import Elev, FFU, PLATE, EAVE, GRADE, PITCH
from plan_engine import dim_chain, bubble, para
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
F = 12
common = dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE)


def save(s, cfg):
    SL.border_and_titleblock(s, cfg)
    base = f"{OUT}/{cfg['sheet_no']}_{cfg['file']}"
    s.to_pdf(base + ".pdf", title=f"{cfg['sheet_no']} {cfg['sheet_title']}", author="Scottsdale Fourplex")
    s.to_dxf(base + ".dxf")
    print("wrote", base)


# =============================================================== A-103.1 ROOF PLAN
s = Sheet(origin=(3.6, 19.75))
L = lambda a, b, lw="l", layer="A-ROOF", dash=None: s.line((a[0] * F, a[1] * F), (b[0] * F, b[1] * F), layer=layer, lw=lw, space="m", dash=dash)
T = lambda x, y, t, h=0.08, **k: s.text(s.m2p(x * F, y * F), t, h, **k)
# walls below (dashed)
s.rect(0, 0, 60 * F, 50 * F, layer="A-ROOF", lw="f", space="m", dash="HIDDEN")
for x in (25, 35):
    L((x, 0), (x, 50), "f", dash="HIDDEN")
# eaves, gutter
E0, E1, N0, N1 = -2, 62, -2, 52
s.rect(E0 * F, N0 * F, (E1 - E0) * F, (N1 - N0) * F, layer="A-ROOF", lw="h", space="m")
s.rect((E0 + 0.45) * F, (N0 + 0.45) * F, (E1 - E0 - 0.9) * F, (N1 - N0 - 0.9) * F, layer="A-ROOF", lw="f", space="m")
# ridge + hips
r0, r1, ry = 25, 35, 25
L((r0, ry), (r1, ry), "h")
for c, r in (((E0, N0), (r0, ry)), ((E0, N1), (r0, ry)), ((E1, N0), (r1, ry)), ((E1, N1), (r1, ry))):
    L(c, r, "m")
# tile hatch (light courses parallel to each eave)
def courses(poly, axis, start, end, step=1.5):
    v = start
    while v < end:
        # intersect line axis=v with polygon
        xs = []
        n = len(poly)
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            a1, a2 = (y1, y2) if axis == "y" else (x1, x2)
            if (a1 - v) * (a2 - v) <= 0 and a1 != a2:
                t = (v - a1) / (a2 - a1)
                xs.append(x1 + t * (x2 - x1) if axis == "y" else y1 + t * (y2 - y1))
        if len(xs) >= 2:
            lo, hi = min(xs), max(xs)
            if axis == "y":
                L((lo + 0.3, v), (hi - 0.3, v), "xf")
            else:
                L((v, lo + 0.3), (v, hi - 0.3), "xf")
        v += step
courses([(E0, N0), (E1, N0), (r1, ry), (r0, ry)], "y", N0 + 1.5, ry)
courses([(E0, N1), (E1, N1), (r1, ry), (r0, ry)], "y", ry + 1.5, N1)
courses([(E0, N0), (r0, ry), (E0, N1)], "x", E0 + 1.5, r0)
courses([(E1, N0), (r1, ry), (E1, N1)], "x", r1 + 1.5, E1)
# loggia roof
lg = (22.5, 50, 37.5, 57.0)
s.rect(lg[0] * F, lg[1] * F, (lg[2] - lg[0]) * F, (lg[3] - lg[1]) * F, layer="A-ROOF", lw="m", space="m", fill=1.0)
L((lg[0], lg[3]), (lg[0] + 3.5, 53.5), "l"); L((lg[2], lg[3]), (lg[2] - 3.5, 53.5), "l"); L((lg[0] + 3.5, 53.5), (lg[2] - 3.5, 53.5), "l")
T(30, 55.6, "LOGGIA ROOF · 4:12 TILE", 0.065)
# slope arrows
def slope(x, y, ang, txt="4:12"):
    a = math.radians(ang); dx, dy = math.cos(a) * 3.0, math.sin(a) * 3.0
    L((x, y), (x + dx, y + dy), "f", layer="A-ANNO-SYMB")
    p = (x + dx, y + dy); b1 = math.radians(ang + 150); b2 = math.radians(ang - 150)
    s.pline([((p[0] + 0.7 * math.cos(b1)) * F, (p[1] + 0.7 * math.sin(b1)) * F), (p[0] * F, p[1] * F), ((p[0] + 0.7 * math.cos(b2)) * F, (p[1] + 0.7 * math.sin(b2)) * F)], layer="A-ANNO-SYMB", lw="f", space="m")
    T(x + dx / 2, y + dy / 2 - 0.6, txt, 0.065, font="Helvetica-Bold")
slope(30, 15, -90); slope(30, 36, 90); slope(10, 25, 180); slope(50, 25, 0)
# downspouts
for (x, y) in ((0.3, -1.6), (59.7, -1.6), (0.3, 51.6), (59.7, 51.6), (22.9, 56.6), (37.1, 56.6)):
    s.rect((x - 0.25) * F, (y - 0.17) * F, 0.5 * F, 0.34 * F, layer="A-ROOF", lw="l", space="m", fill=0.2)
    T(x + (1.4 if x < 30 else -1.4), y + (-0.4 if y < 25 else 0.9), "DS", 0.06, font="Helvetica-Bold")
# VTRs and roof jacks
for (x, y) in ((21, 3), (21, 24), (20, 25.6), (39, 3), (39, 24), (40, 25.6)):
    s.circle((x * F, y * F), 0.25 * F, layer="A-ROOF", lw="l", space="m")
    T(x + 1.3, y + 0.2, "VTR", 0.055)
# attic access
for (x, y) in ((8, 15.5), (52, 15.5)):
    s.rect((x - 1.1) * F, (y - 1.25) * F, 2.2 * F, 2.5 * F, layer="A-ROOF", lw="f", space="m", dash="HIDDEN")
    T(x, y + 2.2, "ATTIC ACCESS BELOW", 0.05)
# MC-1 clearance note
s.rect(31.9 * F, -1.1 * F, 5.0 * F, 1.1 * F, layer="A-ROOF", lw="f", space="m", dash="HIDDEN")
T(34.4, -3.3, "MC-1 BELOW — NO DOWNSPOUT OR SCUPPER WITHIN 3'-0\"", 0.055)
T(30, 25.9, "RIDGE EL. ±29'-0\"", 0.07, font="Helvetica-Bold")
T(14, 9, "W1 BELOW: ATTIC SEPARATION TO DECK", 0.055)
# grids + dims
for x, lab in ((0, "1"), (25, "2"), (35, "3"), (60, "4")):
    px = s.m2p(x * F, 0)[0]
    s.line((px, s.m2p(0, -2 * F)[1] + 1.0), (px, s.m2p(0, -2 * F)[1] + 0.1), layer="A-GRID", lw="xf")
    bubble(s, (px, s.m2p(0, -2 * F)[1] + 1.2), lab)
for y, lab in ((0, "A"), (50, "B")):
    py = s.m2p(0, y * F)[1]
    s.line((s.m2p(-2 * F, 0)[0] - 1.0, py), (s.m2p(-2 * F, 0)[0] - 0.1, py), layer="A-GRID", lw="xf")
    bubble(s, (s.m2p(-2 * F, 0)[0] - 1.2, py), lab)
dim_chain(s, [-24, 0, 720, 744], 57 * F, "h", -0.45)
dim_chain(s, [-24, 744], 57 * F, "h", -0.8)
dim_chain(s, [-24, 0, 600, 624], 62 * F, "v", 0.55)
dim_chain(s, [-24, 624], 62 * F, "v", 0.9)
SL.drawing_title(s, 1.35, 4.05, "1", "A-103.1", "ROOF PLAN — MODEL 1 STACKED BIG HOUSE", "SCALE: 1/4\" = 1'-0\"   HIP ROOF, 4:12, TWO-PIECE CLAY TILE", w=15.8)
SL.north_arrow(s, 18.6, 4.3)
notes = [
    "Roof: two-piece clay barrel tile, battens as required, two layers of ASTM D226 Type II underlayment (or one layer self-adhered), 7/16\" OSB sheathing on engineered trusses @ 24\" o.c. (S-103). Class A assembly.",
    "Slope 4:12 all planes; eaves 2'-0\" (west side 2'-0\" max., 7'-0\" to lot line). Ridge ±29'-0\" above finish floor: confirm height method at pre-app.",
    "Vented attic per IBC 1202: continuous soffit intake plus low-profile tile vents near the ridge; net free area 1/150 of attic floor (±21 SF), balanced 50/50. Insulation R-38 blown at the ceiling (EN-001).",
    "The attic is divided at each W1 unit separation wall, which runs to the roof deck (draftstopping per IBC 718 and G-005). Provide an attic access per attic area: 22\" x 30\" min., in Units C and D hall ceilings; the core attic is reached from storage loft 202.",
    "Gutters: 5\" K-style aluminum all eaves; 3x4 downspouts to splash blocks and the retention basins (C-102). No downspout, scupper or roof discharge within 3'-0\" of meter center MC-1, unit panels or gas meters (Scottsdale IPC 1106.5.1).",
    "Plumbing vents (VTR) per P-101.1: one per stack, no air admittance valves. Flash with lead or tile-specific vent flashing; keep 10'-0\" from any air intake or 3'-0\" above it.",
    "No roof-mounted equipment. Condensers at grade on the east side yard (M-101). Bath and dryer exhaust routes per M-001; any roof jack uses tile-vent flashing.",
    "Solar-ready zone (IECC appendix) and EV readiness are open items for the pre-application meeting; the south roof plane is kept free of vents and penetrations so a solar zone can be added.",
]
y = SL.notes_list(s, 21.15, 23.2, "ROOF PLAN NOTES", notes, 5.1)
y = SL.head(s, 26.55, 23.2, "LEGEND", 5.25)
for t in ("DS  downspout to splash block", "VTR  plumbing vent through roof", "---  wall below / attic access below", "→ 4:12  slope direction (down)"):
    s.text((26.6, y), t, 0.072, align="l"); y -= 0.22
save(s, dict(common, sheet_no="A-103.1", file="Model1_Roof_Plan", sheet_title="ROOF PLAN"))

# =============================================================== A-301.1 BUILDING SECTIONS
s = Sheet(origin=(0, 0))
JST = 9.0
FLR0, FLR1 = 9.0, FFU          # lower ceiling .. upper floor


def section(e, x0, x1, roof_fn, walls, rooms, slab_beams, extra=None):
    """walls: list of (x, type, thick_ft, full_height?)"""
    # grade + slab
    e.grade(x0 - 4, x1 + 4)
    e.rect(x0, -0.33, x1, 0, lw="m", fill=0.55)
    for (bx, bw, bd) in slab_beams:
        e.rect(bx - bw / 2, -bd, bx + bw / 2, -0.33, lw="m", fill=0.55)
    # floor/ceiling assembly band
    e.rect(x0, FLR0, x1, FLR0 + 0.1, lw="f", fill=0.3)                       # 2 layers 5/8 Type X
    e.rect(x0, FLR0 + 0.1, x1, FLR0 + 0.56, lw="f")                          # independent ceiling joists
    xx = x0
    while xx < x1:
        e.rect(xx, FLR0 + 0.1, min(xx + 0.13, x1), FLR0 + 0.56, lw="xf", fill=0.6); xx += 1.33
    e.rect(x0, FLR0 + 0.66, x1, FLR1 - 0.08, lw="f")                          # open-web floor trusses
    xx = x0
    while xx < x1 - 1:
        e.line((xx, FLR0 + 0.7), (xx + 0.5, FLR1 - 0.12), lw="xf"); e.line((xx + 0.5, FLR1 - 0.12), (xx + 1.0, FLR0 + 0.7), lw="xf"); xx += 1.0
    e.rect(x0, FLR1 - 0.08, x1, FLR1, lw="l", fill=0.4)                      # subfloor + mat + finish
    # upper ceiling
    e.rect(x0, PLATE - 0.05, x1, PLATE, lw="l", fill=0.3)
    # insulation cloud
    xx = x0 + 0.2
    while xx < x1 - 0.6:
        pts = [(xx + 0.3 * (1 - math.cos(t)), PLATE + 0.05 + 0.5 * math.sin(t)) for t in [i * math.pi / 8 for i in range(9)]]
        e.poly(pts, lw="xf", closed=False); xx += 0.6
    roof_fn(e)
    # walls (cut)
    for (x, typ, th, full) in walls:
        top = e.roof_z(x) - 0.4 if full else PLATE
        g = 0.32 if typ in ("W1", "W2") else 0.62
        if typ == "P1":
            # partitions only between floors and ceilings
            e.rect(x - th / 2, 0, x + th / 2, FLR0, lw="l", fill=0.7)
            e.rect(x - th / 2, FLR1, x + th / 2, PLATE, lw="l", fill=0.7)
        else:
            a, b = (x, x + th) if typ in ("EXT", "W2") and x == x0 else ((x - th, x) if typ in ("EXT", "W2") else (x - th / 2, x + th / 2))
            e.rect(a, 0, b, top, lw="h", fill=g)
    for (x, z, t) in rooms:
        e.text(x, z, t, 0.08, font="Helvetica-Bold")
    if extra:
        extra(e)


class SE(Elev):
    def __init__(self, s, origin, profile):
        super().__init__(s, origin)
        self.profile = profile

    def roof_z(self, x):
        pts = self.profile
        for (x1, z1), (x2, z2) in zip(pts, pts[1:]):
            if min(x1, x2) <= x <= max(x1, x2) and x1 != x2:
                return z1 + (x - x1) * (z2 - z1) / (x2 - x1)
        return EAVE


def roof_profile_fn(prof):
    def fn(e):
        # top chord + sheathing + tile
        e.poly(prof, lw="m", closed=False)
        e.poly([(x, z + 0.35) for x, z in prof], lw="l", closed=False)
        # bottom chord
        e.line((prof[0][0] + 2.0, PLATE), (prof[-1][0] - 2.0, PLATE), lw="l")
        # webs
        x = prof[0][0] + 2.0; k = 0
        while x < prof[-1][0] - 2.0:
            zt = e.roof_z(x)
            if zt > PLATE + 0.3:
                e.line((x, PLATE), (x + 2.0, e.roof_z(x + 2.0)) if k % 2 == 0 else (x, zt), lw="xf")
            x += 2.0; k += 1
        # fascia
        for (x, z) in (prof[0], prof[-1]):
            e.rect(x - 0.1, z - 0.6, x + 0.1, z, lw="l", fill=1.0)
    return fn


# Section 1: E-W at y = 22.5, looking north. x along plan x.
zside = EAVE + 24.5 * PITCH
prof1 = [(-2, EAVE), (22.5, zside), (37.5, zside), (62, EAVE)]
e1 = SE(s, (2.7, 15.25), prof1)
section(e1, 0, 60, roof_profile_fn(prof1),
        walls=[(0, "W2", 0.71, False), (60, "EXT", 0.625, False), (25, "W1", 0.79, True), (35, "W1", 0.79, True), (12, "P1", 0.375, False), (17, "P1", 0.375, False), (43, "P1", 0.375, False), (48, "P1", 0.375, False), (28, "P1", 0.375, False), (32, "P1", 0.375, False)],
        rooms=[(6, 4.5, "BEDROOM 2  A105"), (14.5, 4.5, "HALL"), (21, 4.5, "HALL BATH"), (30, 4.5, "ENCL."), (39, 4.5, "HALL BATH"), (45.5, 4.5, "HALL"), (54, 4.5, "BEDROOM 2  B105"),
               (6, 15.2, "BEDROOM 2  C206"), (21, 15.2, "HALL BATH"), (30, 15.2, "LOFT 202"), (39, 15.2, "HALL BATH"), (54, 15.2, "BEDROOM 2  D206"), (30, 23.3, "ATTIC (DIVIDED AT W1)")],
        slab_beams=[(0.5, 1.0, 2.0), (59.5, 1.0, 2.0), (25, 1.33, 1.67), (35, 1.33, 1.67), (12.5, 1.0, 1.67), (47.5, 1.0, 1.67)])
e1.levels(62 + 2.5, zside)
e1.grids([(0, "1"), (25, "2"), (35, "3"), (60, "4")])
for (x, z, n, dx, dz) in [(3, 9.3, 1, -0.5, 0.0), (8, PLATE + 0.3, 2, 0.0, 0.5), (10, 24.0, 3, 0.0, 0.45), (25, 22, 4, -0.5, 0.2), (8, -0.2, 5, 0.0, -0.4), (0.3, 6, 6, -0.5, 0.0), (35, 6, 4, 0.5, 0.2)]:
    e1.keynote(x, z, n, dx, dz)
SL.drawing_title(s, 1.35, 13.35, "1", "A-301.1", "BUILDING SECTION 1 — EAST-WEST, LOOKING NORTH", "SCALE: 1/4\" = 1'-0\"   CUT AT 22'-6\" FROM THE NORTH FACE (SEE A-101.1)", w=17.0)

# Section 2: N-S at x = 27.5, looking west. horizontal axis = plan y (north at left).
zr = EAVE + 27 * PITCH
prof2 = [(-2, EAVE), (25, zr), (52, EAVE)]
e2 = SE(s, (3.2, 4.45), prof2)


def stair(e):
    rz = FFU / 19
    y, z = 35.75, 0.0
    pts = [(y, z)]
    for i in range(10):
        z += rz; pts.append((y, z)); y -= 11 / 12 if i < 9 else 0; pts.append((y, z))
    e.poly(pts, lw="l", closed=False)
    e.rect(23.6, 5.0, 27.5, z, lw="l", fill=0.75)
    e.text(30.5, 2.6, "RUN 1 UP", 0.065)
    pts = [(27.5, z)]
    y = 27.5
    for i in range(9):
        z += rz; pts.append((y, z)); y += 11 / 12; pts.append((y, z))
    e.poly(pts, lw="f", closed=False, dash="HIDDEN")
    e.text(31.5, 8.2, "RUN 2 BEYOND", 0.06)
    # loggia
    e.rect(50, 0, 56, 10.2, lw="l")
    e.poly([(50, 12.0), (57, 10.2), (56, 10.2), (50, 11.6)], lw="m", fill=0.7)
    e.rect(55.4, GRADE, 56, 9.7, lw="m", fill=0.62)
    e.text(53, 4.5, "LOGGIA", 0.07, font="Helvetica-Bold")


section(e2, 0, 50, roof_profile_fn(prof2),
        walls=[(0, "EXT", 0.625, False), (50, "EXT", 0.625, False), (9, "P1", 0.375, False), (20, "P1", 0.375, False), (23.5, "P1", 0.375, False)],
        rooms=[(4.5, 4.5, "CH1"), (14.5, 4.5, "HOUSE STORAGE 102"), (21.8, 4.5, "ENCL."), (43, 4.5, "SHARED ENTRY 100"), (14.5, 15.2, "STORAGE LOFT 202"), (43, 15.2, "LANDING 200"), (25, 23.3, "ATTIC")],
        slab_beams=[(0.5, 1.0, 2.0), (49.5, 1.0, 2.0), (25, 1.0, 1.67)], extra=stair)
e2.levels(56 + 2.0, zr)
e2.grids([(0, "A"), (50, "B")])
for (x, z, n, dx, dz) in [(12, 9.4, 1, -0.4, 0.3), (6, PLATE + 0.3, 2, 0.0, 0.5), (36, 23.5, 3, 0.3, 0.4), (34, 3, 7, 0.4, 0.3), (45, -0.2, 5, 0.0, -0.4)]:
    e2.keynote(x, z, n, dx, dz)
SL.drawing_title(s, 1.35, 2.5, "2", "A-301.1", "BUILDING SECTION 2 — NORTH-SOUTH THROUGH THE STAIR, LOOKING WEST", "SCALE: 1/4\" = 1'-0\"   CUT AT 27'-6\" FROM THE WEST FACE (SEE A-101.1)", w=17.0)

KEYS = [
    "F1 FLOOR/CEILING — 1 HR, STC/IIC 50 (field 45): finish floor over acoustic mat, 3/4\" T&G subfloor glued and screwed, 11⅞\" open-web floor trusses @ 24\" o.c. (nothing attached below), 1\" air gap / MEP zone, independent 2x6 ceiling joists @ 16\" o.c. with R-19 batts, two layers 5/8\" Type X GWB on resilient channel (UL L521 or L528, verify). Floor to floor 10'-8\" ±.",
    "Upper ceiling: 5/8\" Type X GWB on truss bottom chords; R-38 blown insulation; vented attic above (A-103.1).",
    "Roof: clay tile, two layers of underlayment, 7/16\" OSB on engineered trusses @ 24\" o.c., 4:12 (S-103). Heel height to suit R-38 at the plate.",
    "W1 unit separation wall continuous from top of slab to the underside of the roof deck; divides the attic. Firestop every penetration (D-002).",
    "4\" post-tension slab on 15-mil vapor retarder over 4\" ABC; perimeter beams 12\" x 24\", B3 16\" x 20\" under every W1 wall, ribs 12\" x 20\" (S-101). Footings 18\" deep min. (Scottsdale IBC 1809.4).",
    "W2 west wall, 1-hour rated both sides (A-202.1).",
    "Common stair: 19 risers @ ±6¾\", 11\" treads, 4'-0\" mid landing; handrails both sides; enclosed space below the landing has no storage (IBC 1011.7.3).",
]
y = SL.notes_list(s, 21.15, 23.2, "KEYNOTES — BUILDING SECTIONS", KEYS, 5.1)
GENS = [
    "Sections show design intent; structural members are sized by the engineer of record on the S-sheets. Truss and PT slab shop drawings are deferred submittals.",
    "Ceiling heights 9'-0\" both floors. Mechanical ducts run in dropped soffits below the rated ceiling or through the F1 MEP zone with listed ceiling radiation dampers (G-005, M-101). No recessed can lights in F1 ceilings.",
    "Finish floor 8\" above finish grade; weep screed at the slab edge.",
]
y = SL.notes_list(s, 26.55, 23.2, "GENERAL NOTES — SECTIONS", GENS, 5.25)
save(s, dict(common, sheet_no="A-301.1", file="Model1_Building_Sections", sheet_title="BUILDING\nSECTIONS"))
