"""S-101 foundation plan, post-tensioned slab on ground, Model 1 (design intent for the structural engineer)."""
import sys
from cadkit import Sheet
from plan_engine import dim_chain, bubble
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
F = 12
s = Sheet(origin=(3.6, 20.1))


def R(x, y, w, h, layer="S-FNDN", lw="l", dash=None, fill=None):
    s.rect(x * F, y * F, w * F, h * F, layer=layer, lw=lw, space="m", dash=dash, fill=fill)


def L(a, b, layer="S-FNDN", lw="l", dash=None):
    s.line((a[0] * F, a[1] * F), (b[0] * F, b[1] * F), layer=layer, lw=lw, space="m", dash=dash)


def T(x, y, t, h=0.075, **k):
    s.text(s.m2p(x * F, y * F), t, h, **k)


# slab edge
R(0, 0, 60, 50, lw="h")
# perimeter beam (12" wide inside the edge)
R(1, 1, 58, 48, lw="f", dash="HIDDEN")
# interior beams under W1 (16" wide) full depth of the building
for x in (25, 35):
    L((x - 0.67, 1), (x - 0.67, 49), lw="f", dash="HIDDEN"); L((x + 0.67, 1), (x + 0.67, 49), lw="f", dash="HIDDEN")
    T(x, 30, "B3", 0.08, font="Helvetica-Bold", rot=90)
# ribs (12") — E-W at y 17.5 and 33; N-S at x 12.5 and 47.5
for y in (17.5, 33.0):
    for (a, b) in ((1, 24.33), (25.67, 34.33), (35.67, 59)):
        L((a, y - 0.5), (b, y - 0.5), lw="f", dash="HIDDEN"); L((a, y + 0.5), (b, y + 0.5), lw="f", dash="HIDDEN")
    T(6, y - 0.9, "RIB R1", 0.065)
for x in (12.5, 47.5):
    L((x - 0.5, 1), (x - 0.5, 49), lw="f", dash="HIDDEN"); L((x + 0.5, 1), (x + 0.5, 49), lw="f", dash="HIDDEN")
T(3, 2.6, "B1 PERIMETER", 0.065, align="l")
# tendons: representative lines + anchors
for x in [2.5 + 4 * k for k in range(15)]:
    L((x, 0.3), (x, 49.7), "S-TNDN", "xf", [2, 3])
for y in [2.5 + 4 * k for k in range(12)]:
    L((0.3, y), (59.7, y), "S-TNDN", "xf", [2, 3])
for y in [2.5 + 4 * k for k in range(12)]:
    R(-0.35, y - 0.2, 0.35, 0.4, "S-TNDN", "xf", fill=0.0)
    R(60, y - 0.2, 0.35, 0.4, "S-TNDN", "xf", fill=1.0)
for x in [2.5 + 4 * k for k in range(15)]:
    R(x - 0.2, -0.35, 0.4, 0.35, "S-TNDN", "xf", fill=0.0)
    R(x - 0.2, 50, 0.4, 0.35, "S-TNDN", "xf", fill=1.0)
# loggia slab
R(22.5, 50, 15, 7, lw="m"); T(30, 53.6, "LOGGIA SLAB (TE EDGE)", 0.065, font="Helvetica-Bold"); T(30, 55.2, "4\" ON GRADE, #4 @ 18\" E.W.", 0.055)
L((22.5, 50.6), (37.5, 50.6), lw="f", dash="HIDDEN")
# slab recesses at doors
for (x, y, w, h, t) in ((27.75, 49.0, 3.5, 1.0, "101"), (4, 0, 6, 1.0, "119"), (50, 0, 6, 1.0, "131")):
    R(x, y, w, h, lw="l", fill=0.75)
    T(x + w / 2, y + (2.2 if y < 1 else -0.6), f"1½\" RECESS @ {t}", 0.055)
# plumbing chases / sleeves
for (x, y, w, h, t) in ((25, 0, 3, 9, "CH1"), (32, 0, 3, 9, "CH2"), (25, 20, 3, 3.5, "CH3"), (32, 20, 3, 3.5, "CH4")):
    R(x, y, w, h, lw="f", dash=[3, 2])
    T(x + w / 2, y + h / 2 + 0.3, t, 0.055)
T(30, 21.8, "DWV SLEEVES THROUGH B3 — COORD. P-101.1", 0.05)
# hold-downs at shear wall ends (design intent)
for (x, y) in ((0.6, 0.6), (59.4, 0.6), (0.6, 49.4), (59.4, 49.4), (25, 0.6), (35, 0.6), (25, 49.4), (35, 49.4), (0.6, 25), (59.4, 25)):
    s.pline([((x - 0.45) * F, y * F), (x * F, (y - 0.45) * F), ((x + 0.45) * F, y * F), (x * F, (y + 0.45) * F)], layer="S-FNDN", lw="m", space="m", closed=True, fill=0.0)
# section marks
for (x, y, n, sh) in ((-4.0, 12, "1", "S-501"), (30, -4.0, "2", "S-501"), (64.0, 33, "3", "S-501")):
    p = s.m2p(x * F, y * F)
    s.circle(p, 0.2, lw="m", fill=1.0); s.line((p[0] - 0.2, p[1]), (p[0] + 0.2, p[1]), lw="f")
    s.text((p[0], p[1] + 0.04), n, 0.08, font="Helvetica-Bold"); s.text((p[0], p[1] - 0.13), sh, 0.05)
# grids + dims
for x, lab in ((0, "1"), (25, "2"), (35, "3"), (60, "4")):
    px = s.m2p(x * F, 0)[0]; py = s.m2p(0, -6 * F)[1]
    s.line((px, py - 0.2), (px, py - 0.85), layer="A-GRID", lw="xf"); bubble(s, (px, py), lab)
for y, lab in ((0, "A"), (50, "B")):
    py = s.m2p(0, y * F)[1]; px = s.m2p(-6 * F, 0)[0]
    s.line((px + 0.2, py), (px + 0.85, py), layer="A-GRID", lw="xf"); bubble(s, (px, py), lab)
dim_chain(s, [0, 300, 420, 720], 59 * F, "h", -0.3)
dim_chain(s, [0, 720], 59 * F, "h", -0.6)
dim_chain(s, [0, 210, 396, 600], 61.5 * F, "v", 0.4)
dim_chain(s, [0, 600], 61.5 * F, "v", 0.7)
SL.drawing_title(s, 1.35, 3.15, "1", "S-101", "FOUNDATION PLAN — POST-TENSIONED SLAB ON GROUND", "SCALE: 1/4\" = 1'-0\"   DESIGN INTENT — FINAL DESIGN BY THE STRUCTURAL ENGINEER OF RECORD", w=16.0)
SL.north_arrow(s, 18.6, 3.6)

# beam schedule
from plan_engine import table
y = SL.head(s, 21.15, 23.2, "BEAM AND SLAB SCHEDULE (PRELIMINARY)", 10.6)
table(s, 21.15, y + 0.04, [("MARK", 0.7, "c"), ("WIDTH x DEPTH", 1.4, "c"), ("WHERE", 3.0, "l"), ("REINFORCING / TENDONS", 5.5, "l")], [
    ("SLAB", "4\" THICK", "All", "1/2\" ø 270 ksi unbonded tendons @ 4'-0\" o.c. max. each way, centered in the slab"),
    ("B1", "12\" x 24\"", "Perimeter", "(2) #4 bottom continuous; tendon at 3\" from bottom at the edge; 18\" min. below grade"),
    ("B3", "16\" x 20\"", "Under each W1 wall", "(2) #5 bottom continuous; (1) extra tendon in the beam"),
    ("R1", "12\" x 20\"", "Ribs, 2 each way", "(1) #4 bottom continuous"),
    ("TE", "12\" x 18\"", "Loggia edge", "(2) #4 continuous, dowel #4 @ 24\" to B1 with expansion joint"),
], h=0.066, rowh=0.17)
NOTES = [
    "Design intent only. Slab type, beam sizes, spacing and tendon forces are set by the Arizona-registered structural engineer from a geotechnical report for the selected parcel. PT shop drawings and calcs are a deferred submittal.",
    "Design basis: PTI DC10.5 (slabs on expansive and compressible soils), ACI 318-19, IBC 1808.6. Concrete f'c 3,000 psi at 28 days (2,000 psi before stressing). Tendons ASTM A416, 270 ksi, 1/2\" dia., encapsulated anchors.",
    "Footing depth 18\" min. below finish grade (City of Scottsdale amendment to IBC 1809.4). Bear on undisturbed soil or engineered fill compacted per the geotech.",
    "15-mil vapor retarder (ASTM E1745 Class A) over 4\" ABC; lap 6\" and tape; seal penetrations.",
    "Stressing: 3–10 days after the pour per the PT engineer; no saw cuts, drilling or coring in the slab after stressing without the engineer's approval. Mark the slab 'POST-TENSIONED SLAB — DO NOT CUT' at each unit entry.",
    "Sleeve all plumbing through beams before the pour (P-101.1); no plumbing runs inside beams lengthwise. Chases CH1–CH4 per X-101.",
    "Hold-downs (black diamonds) at shear-wall ends shown for coordination only; size and embed per S-201. Anchor bolts or straps at all bottom plates per S-201.",
    "Slab recesses 1½\" at doors 101, 119, 131 for accessible thresholds (D-001/6). Finish floor 100.00' = 8\" above adjacent grade.",
    "Termite treatment per Arizona OPM before the vapor retarder.",
]
SL.notes_list(s, 21.15, 21.55, "FOUNDATION NOTES", NOTES, 10.6)
y = SL.head(s, 21.15, 15.9, "LEGEND", 10.6)
for t in ("— — —  beam or rib edge below slab", "- - - - -  representative tendon (4'-0\" o.c.)", "filled / open box at slab edge  tendon dead end / live (stressing) end",
          "black diamond  hold-down location (S-201)", "shaded box  1½\" slab recess at accessible door"):
    s.text((21.2, y), t, 0.07, align="l"); y -= 0.21
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="S-101", sheet_title="FOUNDATION PLAN"))
base = f"{OUT}/S-101_Model1_Foundation_Plan"
s.to_pdf(base + ".pdf", title="S-101 Foundation Plan - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
