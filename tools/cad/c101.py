"""C-101 architectural site plan, Model 1 on the typical 80' x 125' lot."""
import math, sys
from cadkit import Sheet
from plan_engine import table, para, dim_chain
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
F = 12
s = Sheet(origin=(3.2, 21.9), scale=96)
M = lambda x, y: (x * F, y * F)


def R(x, y, w, h, layer="C-SITE", lw="l", dash=None, fill=None):
    s.rect(x * F, y * F, w * F, h * F, layer=layer, lw=lw, space="m", dash=dash, fill=fill)


def L(a, b, layer="C-SITE", lw="l", dash=None):
    s.line(M(*a), M(*b), layer=layer, lw=lw, space="m", dash=dash)


def T(x, y, t, h=0.075, **k):
    s.text(s.m2p(x * F, y * F), t, h, **k)


BX, BY = 7, 55          # building origin on the lot (plan 0,0 = NW corner)
# street + sidewalk
R(-8, 125, 96, 1.0, lw="l")                         # curb back of walk
R(-8, 125, 96, 5.0, lw="f")
L((-8, 131), (88, 131), lw="m"); L((-8, 131.5), (88, 131.5), lw="f")
T(40, 136, "PUBLIC STREET (NAME TBD) — EXISTING CURB, GUTTER AND 5'-0\" SIDEWALK", 0.09, font="Helvetica-Bold")
T(40, 128.4, "EX. SIDEWALK", 0.06)
# lot lines
s.rect(0, 0, 80 * F, 125 * F, layer="C-PROP", lw="h", space="m", dash="PHANTOM")
# setbacks (verify)
for (a, b) in (((0, 20), (80, 20)), ((7, 0), (7, 125)), ((0, 105), (80, 105)), ((73, 0), (73, 125))):
    L(a, b, "C-SETB", "f", [6, 3])
T(3.5, 62, "7'-0\" SIDE", 0.055, rot=90); T(76.5, 62, "SETBACK VERIFY", 0.055, rot=90)
# drive + motor court + parking
s.pline([M(68, 125), M(80, 125), M(80, 2), M(8, 2), M(8, 44), M(68, 44)], layer="C-PVMT", lw="m", space="m", closed=True, fill=0.92)
T(74, 90, "12'-0\" CONCRETE DRIVE", 0.075, font="Helvetica-Bold", rot=90)
T(38, 32, "MOTOR COURT / BACK-UP AISLE 24'-0\"", 0.075, font="Helvetica-Bold")
xs = [8, 19, 27] + [27 + 8.5 * k for k in range(1, 7)]
for x in xs:
    L((x, 2), (x, 20), "C-PVMT-STRP", "l")
L((8, 20), (78, 20), "C-PVMT", "f", [3, 2])
for c in range(0, 27, 2):   # 45-degree hatch clipped to x 19..27, y 2..20 : line y = x - 19 + 2 - 8 + c
    pts = []
    for (x, y) in ((19, 19 + c - 25), (27, 27 + c - 25)):
        pass
    x0, x1 = 19, 27
    ya, yb = 2 + c - 8, 2 + c
    # segment from (x0, ya) to (x1, yb), clip to 2..20
    t0 = max(0, (2 - ya) / 8); t1 = min(1, (20 - ya) / 8)
    if t1 > t0:
        L((x0 + 8 * t0, ya + 8 * t0), (x0 + 8 * t1, ya + 8 * t1), "C-PVMT-STRP", "xf")
T(23, 17.5, "8' AISLE", 0.055, font="Helvetica-Bold")
T(13.5, 9, "P1 VAN", 0.08, font="Helvetica-Bold"); T(13.5, 11.2, "ACCESSIBLE", 0.06); T(13.5, 13, "11'-0\"", 0.06)
for i in range(6):
    x = 27 + 8.5 * i + 4.25
    T(x, 11, f"P{i + 2}", 0.08, font="Helvetica-Bold")
for x in [13.5] + [27 + 8.5 * i + 4.25 for i in range(6)]:
    s.rect((x - 1.5) * F, 18.5 * F, 3 * F, 0.5 * F, layer="C-PVMT", lw="f", space="m", fill=0.6)
s.rect(8.6 * F, 2.6 * F, 2.4 * F, 2.4 * F, layer="C-PVMT", lw="l", space="m", fill=0.85)
T(9.8, 4.4, "SIGN", 0.045)
# trash + recycle enclosure
R(0.5, 21, 6, 8, lw="m", fill=0.75); T(3.5, 25.6, "TRASH /", 0.055, font="Helvetica-Bold"); T(3.5, 27, "RECYCLE", 0.055, font="Helvetica-Bold")
# building footprint
R(BX, BY, 60, 50, "A-WALL", "h", fill=0.86)
s.rect((BX - 2) * F, (BY - 2) * F, 64 * F, 54 * F, layer="A-ROOF", lw="f", space="m", dash="HIDDEN")
for (a, b) in (((BX - 2, BY - 2), (BX + 25, BY + 25)), ((BX - 2, BY + 52), (BX + 25, BY + 25)), ((BX + 62, BY - 2), (BX + 35, BY + 25)), ((BX + 62, BY + 52), (BX + 35, BY + 25)), ((BX + 25, BY + 25), (BX + 35, BY + 25))):
    L(a, b, "A-ROOF", "xf")
L((BX + 25, BY), (BX + 25, BY + 50), "A-WALL", "f", "HIDDEN"); L((BX + 35, BY), (BX + 35, BY + 50), "A-WALL", "f", "HIDDEN")
T(BX + 12.5, BY + 34, "UNIT A", 0.09, font="Helvetica-Bold"); T(BX + 12.5, BY + 36.2, "(C ABOVE)", 0.065)
T(BX + 47.5, BY + 34, "UNIT B", 0.09, font="Helvetica-Bold"); T(BX + 47.5, BY + 36.2, "(D ABOVE)", 0.065)
T(BX + 30, BY + 9.5, "FOURPLEX", 0.1, font="Helvetica-Bold")
T(BX + 30, BY + 12, "2 STORIES · TYPE V-B · 13R", 0.065)
T(BX + 30, BY + 14, "FF 100.00'", 0.07, font="Helvetica-Bold")
# loggia + entry walk
R(BX + 22.5, BY + 50, 15, 6, "A-WALL", "m", fill=0.85); T(BX + 30, BY + 53.6, "LOGGIA", 0.065, font="Helvetica-Bold")
R(BX + 28, BY + 56, 4, 125 - (BY + 56), "C-WALK", "l", fill=0.95)
T(BX + 30, 118, "ENTRY WALK", 0.05, rot=90)
# west accessible walk from motor court to rear patios + side
R(1.5, 44, 4.5, 61, "C-WALK", "l", fill=0.95); T(3.7, 74, "5'-0\" WALK", 0.05, rot=90)
# rear patios
for x in (BX + 3, BX + 41):
    R(x, BY - 10, 16, 10, "C-WALK", "l", fill=0.97)
    T(x + 8, BY - 6, "PATIO", 0.065, font="Helvetica-Bold"); T(x + 8, BY - 4.4, "(SLIDER)", 0.05)
L((BX + 3, BY - 10), (BX + 19, BY - 10), "C-WALK", "f")
# accessible route
s.pline([M(13, 18.5), M(13, 44), M(13, 47), M(BX + 9, BY - 10)], layer="C-ADA", lw="m", space="m", dash=[4, 1.5, 1, 1.5])
s.pline([M(BX + 30, 125), M(BX + 30, BY + 50)], layer="C-ADA", lw="m", space="m", dash=[4, 1.5, 1, 1.5])
# retention basins
for (x, y, w, h) in ((9, 108, 18, 15), (48, 110, 18, 13)):
    s.rect(x * F, y * F, w * F, h * F, layer="C-TOPO", lw="m", space="m", dash=[6, 3])
    s.rect((x + 2) * F, (y + 2) * F, (w - 4) * F, (h - 4) * F, layer="C-TOPO", lw="f", space="m", dash=[6, 3])
    T(x + w / 2, y + h / 2, "RETENTION", 0.06, font="Helvetica-Bold"); T(x + w / 2, y + h / 2 + 1.5, "BASIN, 1' DEEP", 0.05)
# utilities
s.rect((BX + 25.2) * F, (BY - 1.1) * F, 5.0 * F, 1.1 * F, layer="E-SITE", lw="m", space="m", fill=0.2)
T(BX + 27.7, BY - 2.6, "MC-1", 0.06, font="Helvetica-Bold")
L((BX + 27.7, BY - 1.1), (BX + 27.7, 46.5), "E-SITE", "f", "HIDDEN"); L((BX + 27.7, 46.5), (78.5, 46.5), "E-SITE", "f", "HIDDEN"); L((78.5, 46.5), (78.5, 125.5), "E-SITE", "f", "HIDDEN")
T(70, 48, "E — UG ELECTRIC TO PAD-MOUNT / POLE (APS, VERIFY)", 0.05)
for (x, lab) in ((BX + 26, "W"), (BX + 34, "SS"), (BX + 40, "G")):
    L((x, BY + 50), (x, 131), "C-UTIL", "f", "HIDDEN")
    T(x + 1.0, 127.3, lab, 0.06, font="Helvetica-Bold")
s.circle(M(BX + 26, 126.5), 0.6 * F, layer="C-UTIL", lw="l", space="m"); T(BX + 22.5, 129.6, "WATER METER", 0.045)
s.circle(M(BX + 46, 106.5), 0.5 * F, layer="C-UTIL", lw="l", space="m", fill=0.0); T(BX + 48.8, 106.9, "FDC", 0.06, font="Helvetica-Bold")
T(-3.5, 128.4, "EX. FIRE HYDRANT — LOCATE", 0.05, align="l")
# spot elevations
for (x, y, e) in ((1, 124, "99.10"), (79, 124, "99.00"), (1, 1, "99.60"), (79, 1, "99.40"), (BX + 30, BY + 57.5, "99.83"), (40, 30, "99.45")):
    s.text(s.m2p(x * F, y * F), "+" + e, 0.055, align="l")
# drainage arrows
for (x, y, ang) in ((40, 36, 180), (56, 114, 90), (20, 114, 90), (74, 60, 90)):
    a = math.radians(ang); p = (x + 2.5 * math.cos(a), y + 2.5 * math.sin(a))
    L((x, y), p, "C-TOPO", "l"); L(p, (p[0] - 0.9 * math.cos(a + 0.5), p[1] - 0.9 * math.sin(a + 0.5)), "C-TOPO", "l"); L(p, (p[0] - 0.9 * math.cos(a - 0.5), p[1] - 0.9 * math.sin(a - 0.5)), "C-TOPO", "l")
# dimensions
dim_chain(s, [0, 80 * F], -4 * F, "h", -0.35)
dim_chain(s, [0, 7 * F, 67 * F, 80 * F], -1.0 * F, "h", -0.18)
dim_chain(s, [0, 20 * F, 44 * F, 55 * F, 105 * F, 125 * F], 83 * F, "v", 0.3)
dim_chain(s, [0, 125 * F], 86 * F, "v", 0.6)
SL.drawing_title(s, 1.0, 3.3, "1", "C-101", "ARCHITECTURAL SITE PLAN — MODEL 1", "SCALE: 1/8\" = 1'-0\"   TYPICAL 80' x 125' INTERIOR LOT, STREET TO THE SOUTH", w=13.6, scalebar=False)
SL.north_arrow(s, 14.6, 5.6)

# site data
y = SL.head(s, 15.6, 21.8, "SITE DATA (TYPICAL LOT — VERIFY WITH SURVEY)", 5.2)
rows = [("Lot area", "10,000 SF (0.23 AC)"), ("Building footprint", "3,000 SF + 90 SF loggia"), ("Lot coverage", "30.9%"),
        ("Paving (drive, court, stalls)", "±4,000 SF"), ("Walks + patios", "±950 SF"), ("Landscape / basins", "±1,960 SF (20%)"),
        ("Dwelling units", "4 (2 BR x1, 3 BR x3)"), ("Density", "17.4 du/ac"), ("Parking provided", "7 (incl. 1 van-accessible)"),
        ("Parking required", "VERIFY (Zoning Ord. Art. IX)"), ("Bicycle", "4 spaces at the loggia"), ("Setbacks", "Front 20' · sides 7' / 13' · rear 55' to bldg")]
y = table(s, 15.6, y + 0.04, [("ITEM", 2.6, "l"), ("VALUE", 2.6, "l")], rows, h=0.07, rowh=0.17) - 0.25
y = SL.head(s, 15.6, y, "LEGEND", 5.2)
leg = [("PHANTOM", "PROPERTY LINE"), ("SETB", "SETBACK LINE (VERIFY ZONING)"), ("ADA", "ACCESSIBLE ROUTE, 1:20 MAX., 2% CROSS SLOPE"), ("HID", "EAVE / UTILITY LINE"), ("PAVE", "CONCRETE PAVING")]
for k, t in leg:
    if k == "PHANTOM":
        s.line((15.6, y + 0.04), (16.3, y + 0.04), lw="h", dash="PHANTOM")
    elif k == "SETB":
        s.line((15.6, y + 0.04), (16.3, y + 0.04), lw="f", dash=[6, 3])
    elif k == "ADA":
        s.line((15.6, y + 0.04), (16.3, y + 0.04), lw="m", dash=[4, 1.5, 1, 1.5])
    elif k == "HID":
        s.line((15.6, y + 0.04), (16.3, y + 0.04), lw="f", dash="HIDDEN")
    else:
        s.rect(15.6, y - 0.03, 0.7, 0.14, lw="f", fill=0.92)
    s.text((16.45, y), t, 0.068, align="l"); y -= 0.22

NOTES = [
    "Site plan is drawn on the typical lot assumed for the prototype. When a parcel is selected, replace with a boundary and topographic survey by an Arizona registered land surveyor and redraw C-101 through C-103.",
    "Zoning district, setbacks, height, parking count and lot coverage are VERIFY items for the Scottsdale pre-application meeting.",
    "Fire access: building is within 150 ft hose-lay of the street on the west and east sides (IFC 503.1.1), sprinklered 13R. No fire apparatus road on site. Confirm with the fire marshal, with the FDC and hydrant locations.",
    "Accessible route: van stall P1 to the motor court, west walk, rear patio of Unit A, and from the public sidewalk up the entry walk to door 101 and units A and B. Slopes 1:20 max. walks, 2% cross slope max., no steps (IBC 1104, A117.1 402).",
    "Grading and drainage: finish floor 100.00' = 8\" above adjacent grade; slope away 5% for 10 ft (IRC/IBC 1804.4). Roof downspouts to splash blocks and the front retention basins; first-flush retention sized per Scottsdale DS&PM (C-102).",
    "Utilities: water, sewer and gas from the street; meters by the utilities (City of Scottsdale water/sewer, Southwest Gas). Electric service underground to meter center MC-1 on the north wall (APS); route along the east drive (C-103, E-401).",
    "Trash and recycling: roll-out containers in the screened enclosure by the drive; confirm City of Scottsdale residential pickup for four units versus a shared bin.",
    "Landscape: low-water desert plantings from the ADWR Phoenix AMA list, drip irrigation, 2 shade trees in the front yard; basins planted (L-101).",
    "Site lighting: full-cutoff fixtures at the drive, parking and walks, 1 fc min. on the accessible route, no light trespass at lot lines (Scottsdale dark sky ordinance) (E-401).",
]
SL.notes_list(s, 21.15, 23.2, "SITE PLAN NOTES", NOTES, 5.1)
KEY = [
    "Four homes under one roof, set back 20 ft behind a planted front yard with two retention basins, so the street sees one large house, not a complex.",
    "Cars are kept behind the building: one side drive to a rear motor court with 7 stalls. The front door and the loggia face the street.",
    "Each ground-floor home has its own rear patio through a 6 ft slider.",
]
SL.notes_list(s, 26.55, 23.2, "DESIGN INTENT", KEY, 5.25)

s.scale = 48
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE, sheet_no="C-101", sheet_title="SITE PLAN"))
s.scale = 96
base = f"{OUT}/C-101_Model1_Site_Plan"
s.to_pdf(base + ".pdf", title="C-101 Site Plan - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
