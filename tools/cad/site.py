"""C-102 grading + drainage, C-103 utilities, L-101 landscape, E-401 site electrical (Model 1, typical lot, 1/8")."""
import math
from reportlab.lib.colors import Color
from sheetkit import *

GRAY = Color(0.62, 0.62, 0.62)
TGRAY = Color(0.45, 0.45, 0.45)
ORIG = (3.2, 21.9)
BX, BY = 7, 55


def site_bg(s):
    src = open("c101.py").read()
    cut = src.index("SL.drawing_title(s, 1.0, 3.3")
    code = src[:cut].replace("s = Sheet(origin=(3.2, 21.9), scale=96)", "s = __S__")
    n0 = len(s.items)
    s.scale = 96; s.ox, s.oy = ORIG
    import sys as _sys
    argv = _sys.argv; _sys.argv = ["bg", "/tmp"]
    try:
        exec(compile(code, "c101.py", "exec"), {"__name__": "bg", "__S__": s})
    finally:
        _sys.argv = argv
    out = []
    for it in s.items[n0:]:
        k = it[0]
        if k == "solid":
            out.append(("solid", "A-BKGD", 0.88, it[3]))
        elif k == "text":
            l = list(it); l[1] = "A-BKGD"; l[8] = TGRAY; out.append(tuple(l))
        else:
            l = list(it); l[1] = "A-BKGD"; l[4] = GRAY
            l[2] = "xf" if l[2] in ("l", "f", "xf") else "f"
            if k == "pline" and isinstance(l[7], float):
                l[7] = min(0.96, 0.6 + l[7] * 0.4)
            out.append(tuple(l))
    s.items[n0:] = out
    s.scale = 96; s.ox, s.oy = ORIG


def sheet(no, file, ttl, draw, sub, notes_title, nts, extra=None):
    s = new(ORIG, 96)
    site_bg(s)
    d = Draw(s)
    draw(d, s)
    s.scale = 96; s.ox, s.oy = ORIG
    title(s, "1", no, ttl, sub, x=1.0, y=3.3, w=13.6, scalebar=False)
    north(s, 14.6, 5.6)
    y = TOPY
    if extra:
        y = extra(s)
    notes(s, NC, y, notes_title, nts, 10.6)
    save(s, no, file, ttl.split(" — ")[0].replace(" PLAN", "\nPLAN") if len(ttl) > 18 else ttl)


# ---------------------------------------------------------------- C-102
def grading(d, s):
    d.color = GREEN
    # contours (1 ft intervals implied by spot elevations)
    for (pts, lab) in (([(-2, 6), (82, 4)], "99.5"), ([(-2, 118), (6, 112), (74, 112), (82, 118)], "99.2")):
        d.PL(pts, "l", [8, 3]); d.T(pts[0][0] + 6, pts[0][1] - 0.6, lab, 0.06)
    d.color = BLUE
    for (x, y, ang) in ((BX - 3, 70, 180), (BX + 63, 70, 0), (BX + 10, BY + 54, 90), (BX + 50, BY + 54, 90), (40, 30, 0), (74, 80, 90), (BX + 30, BY - 7, 270)):
        a = math.radians(ang)
        d.arrow((x, y), (x + 3.5 * math.cos(a), y + 3.5 * math.sin(a)), "m", 0.8)
        d.T(x + 1.8 * math.cos(a) + (0.8 if ang in (90, 270) else 0), y + 1.8 * math.sin(a) - 0.6, "2% MIN" if ang in (0, 180) else "5% / 10'", 0.05)
    for (x, y) in ((BX - 1, BY - 1), (BX + 61, BY - 1), (BX - 1, BY + 51), (BX + 61, BY + 51)):
        d.R(x - 0.6, y - 0.6, 1.2, 1.2, "m", fill=0.0); d.T(x + 2.6, y + 0.3, "DS → SPLASH", 0.045)
    d.color = None
    for (x, y, e) in ((BX + 30, BY + 25, "FF 100.00"), (BX - 2, BY + 25, "TG 99.33"), (BX + 62, BY + 25, "TG 99.33"), (BX + 30, BY + 57.2, "99.83"), (13, 10, "99.55"), (60, 10, "99.50"),
                      (74, 120, "99.05"), (18, 115, "98.20 BOTTOM"), (57, 116, "98.25 BOTTOM")):
        d.T(x, y, "+" + e, 0.06, font="Helvetica-Bold")


def grading_tbl(s):
    return tbl(s, NC, TOPY, "RETENTION CALCULATION (FIRST FLUSH / 100-YR 2-HR — VERIFY WITH CITY)", [("ITEM", 4.0, "l"), ("VALUE", 2.2, "c"), ("NOTE", 4.4, "l")], [
        ("Lot area", "10,000 SF", "Typical lot"), ("Weighted runoff coefficient C", "0.70", "Roof, paving, landscape"),
        ("Rainfall depth P (100-yr, 2-hr)", "2.2 in (verify NOAA Atlas 14)", "Scottsdale DS&PM Ch. 4"), ("Required volume V = C·P/12·A", "1,283 CF", ""),
        ("Basin 1 (front west) 18x15, 1 ft deep, 4:1 sides", "±170 CF", "Increase depth or size"), ("Basin 2 (front east) 18x13, 1 ft deep", "±145 CF", ""),
        ("Shortfall", "±970 CF", "Underground storage or rear basin; civil to resolve")], w=10.6, h=0.07, rowh=0.19)


sheet("C-102", "Model1_Grading_and_Drainage_Plan", "GRADING AND DRAINAGE PLAN — MODEL 1", grading,
      "SCALE: 1/8\" = 1'-0\"   SCHEMATIC — CIVIL ENGINEER TO PREPARE FROM SURVEY",
      "GRADING NOTES", [
          "Schematic. A civil engineer registered in Arizona prepares the grading, drainage and retention plan from a boundary and topographic survey of the selected parcel, per the City of Scottsdale Design Standards & Policies Manual (DS&PM).",
          "Finish floor 100.00' = 8\" above the highest adjacent finish grade; grade falls 5% away from the building for 10 ft (IBC 1804.4) or to a swale.",
          "Stormwater retention: Scottsdale generally requires on-site retention of the 100-year, 2-hour storm; the two front basins shown do not hold the full volume. The civil engineer must add capacity (deeper basins, a rear basin, or underground storage chambers under the motor court). OPEN ITEM.",
          "Basins drain dry within 36 hours (percolation test or bleed-off drywell per City standards).",
          "Downspouts to splash blocks directed to swales and the basins; no discharge onto the neighbor's lot or the sidewalk.",
          "Paving: motor court and drive slope 1%–2% to valley gutters leading to the basins; accessible route 2% max. cross slope, 5% max. running slope.",
          "Dust control and storm water pollution prevention during construction per Maricopa County Rule 310 and City requirements.",
      ], extra=grading_tbl)


# ---------------------------------------------------------------- C-103
def utilities(d, s):
    d.color = BLUE
    d.PL([(BX + 26, 131), (BX + 26, 126.5), (BX + 26, BY + 50), (BX + 33.4, BY + 50)], "h"); d.T(BX + 21.5, 121, "1-1/2\" CU WATER SERVICE", 0.055, rot=90)
    d.PL([(BX + 22, 131), (BX + 22, BY + 50)], "m", [8, 2]); d.T(BX + 20.6, 121, "2\" FIRE SERVICE + DCVA", 0.055, rot=90)
    d.R(BX + 21.0, 124.0, 2.0, 1.5, "m", fill=0.85); d.T(BX + 17.0, 124.9, "BACKFLOW", 0.045)
    d.color = GREEN
    d.PL([(BX + 33.5, BY + 50), (BX + 33.5, 131)], "h"); d.T(BX + 35.0, 121, "4\" PVC SEWER @ 1/4\":12\" MIN.", 0.055, rot=90)
    d.R(BX + 33.0, BY + 51.5, 1.0, 1.0, "m", fill=0.0); d.T(BX + 36.5, BY + 52.0, "2-WAY CO", 0.05)
    d.color = ORANGE
    d.PL([(78.5, 131), (78.5, 46.5), (BX + 34.4, 46.5), (BX + 34.4, BY - 1.1)], "h", [10, 3]); d.T(79.8, 90, "UG ELECTRIC SERVICE (UTILITY DESIGN)", 0.055, rot=90)
    d.R(76.0, 126.0, 3.5, 3.5, "m", fill=0.85); d.T(77.75, 128.2, "XFMR?", 0.045)
    d.color = Color(0.4, 0.3, 0.1)
    d.PL([(BX + 40, 131), (BX + 40, BY + 50)], "l", [3, 3]); d.T(BX + 41.3, 121, "GAS (ALTERNATE ONLY)", 0.05, rot=90)
    d.color = None
    d.T(40, 133.6, "EXISTING MAINS IN STREET: WATER, SEWER, GAS, ELECTRIC — LOCATE, SIZE AND DEPTH BY SURVEY / BLUE STAKE", 0.065, font="Helvetica-Bold")


sheet("C-103", "Model1_Utility_Plan", "UTILITY PLAN — MODEL 1", utilities, "SCALE: 1/8\" = 1'-0\"   SCHEMATIC — CIVIL / UTILITY DESIGN BY OTHERS",
      "UTILITY NOTES", [
          "Schematic. Connections, sizes and locations by the civil engineer and the utilities after the parcel is surveyed.",
          "Water: City of Scottsdale meter in the right-of-way; 1-1/2\" service to riser room 103 (P-201). Fire service 2\" with backflow assembly per the water purveyor and Fire Marshal.",
          "Sewer: one 4\" building sewer to the City main with a two-way cleanout at the building and a cleanout at the property line; slope 1/4\" per foot min.",
          "Electric: underground service per the utility (APS or SRP) from a pad-mount transformer or pole to meter center MC-1 on the north wall (E-201). Conduit and trench by the contractor per utility specs.",
          "Gas: not in the base design. If the alternate is elected, Southwest Gas service to a meter manifold 3 ft min. from MC-1 (P-202).",
          "Telecom: two 1\" conduits from the street to the house panel area for fiber/cable.",
          "Separation: water and sewer 10 ft horizontal or per IPC 603.2 when in a common trench with the water above.",
          "Call Arizona 811 (Blue Stake) before digging.",
      ])


# ---------------------------------------------------------------- L-101
def tree(d, x, y, r, lab):
    d.C(x, y, r, "l")
    for a in range(0, 360, 45):
        d.L((x, y), (x + r * 0.8 * math.cos(math.radians(a)), y + r * 0.8 * math.sin(math.radians(a))), "xf")
    d.T(x, y + r + 0.9, lab, 0.05, font="Helvetica-Bold")


def shrub(d, x, y, lab=None):
    d.C(x, y, 1.0, "l", fill=0.9)
    if lab:
        d.T(x, y + 0.35, lab, 0.04, font="Helvetica-Bold")


def landscape(d, s):
    d.color = GREEN
    for (x, y, l) in ((18, 115, "T1"), (58, 116, "T1"), (3.5, 37, "T2"), (44.0, 120.0, "T2")):
        tree(d, x, y, 5.0, l)
    for x in range(BX + 2, BX + 21, 3):
        shrub(d, x, BY + 52.5, "S1")
    for x in range(BX + 40, BY + 4, 3):
        shrub(d, x, BY + 52.5, "S1")
    for (x, y) in ((BX + 1.5, BY - 2.0), (BX + 19.5, BY - 9.0), (BX + 42.0, BY - 9.0), (BX + 58.5, BY - 2.0), (BX + 1.5, BY - 8.0), (BX + 58.5, BY - 8.0), (BX + 30, BY - 7.0), (BX + 27, BY - 7.0), (BX + 33, BY - 7.0)):
        shrub(d, x, y, "S2")
    for (x, y) in ((22, 108.5), (52, 109), (12, 122), (62, 122)):
        shrub(d, x, y, "S3")
    for y in range(4, 20, 2):
        shrub(d, 3.6, y, "G1")
    d.color = None
    d.T(30, 103.4 + 17, "DECOMPOSED GRANITE 1/2\" MINUS, 2\" DEEP, ALL PLANTING AREAS", 0.05)


def plant_tbl(s):
    return tbl(s, NC, TOPY, "PLANT SCHEDULE (LOW-WATER, ADWR PHOENIX AMA LIST)", [("KEY", 0.6, "c"), ("BOTANICAL / COMMON", 4.6, "l"), ("SIZE", 1.2, "c"), ("QTY", 0.7, "c"), ("NOTE", 3.5, "l")], [
        ("T1", "Parkinsonia x 'Desert Museum' / Desert Museum palo verde", "24\" box", "2", "Front yard shade, in basins"),
        ("T2", "Chilopsis linearis / desert willow", "15 gal", "2", "Side yards, patio shade"),
        ("S1", "Leucophyllum frutescens / Texas sage", "5 gal", "12", "Front foundation"),
        ("S2", "Tecoma stans 'Orange Jubilee'", "5 gal", "9", "Rear patios + core"),
        ("S3", "Muhlenbergia rigens / deer grass", "5 gal", "4", "Basin bottoms"),
        ("G1", "Lantana montevidensis / trailing lantana", "1 gal", "8", "West strip at parking"),
        ("DG", "Decomposed granite, 'Express Gold' or eq., 2\" deep", "—", "±2,000 SF", "Over weed barrier")], w=10.6, h=0.068, rowh=0.19)


sheet("L-101", "Model1_Landscape_Plan", "LANDSCAPE PLAN — MODEL 1", landscape, "SCALE: 1/8\" = 1'-0\"   CONCEPT PLANTING — LANDSCAPE ARCHITECT TO FINALIZE",
      "LANDSCAPE NOTES", [
          "Low-water desert planting from the ADWR Phoenix AMA low-water-use plant list; no turf.",
          "Drip irrigation with pressure regulation and filter, smart weather-based controller on the house panel; separate valves for trees and shrubs.",
          "Trees placed for afternoon shade on the west and south faces and the front yard; keep trees 10 ft from the building foundation and out of the fire access and utility easements.",
          "Basins planted with deer grass and boulders; maintain 1 ft retention depth.",
          "Scottsdale requirements for street frontage landscaping and sight visibility triangles at the drive to be confirmed (Zoning Ordinance Art. X).",
          "Maintenance: owner-occupant responsibility under the sale; provide a one-page care guide at close-out.",
      ], extra=plant_tbl)


# ---------------------------------------------------------------- E-401
def site_elec(d, s):
    d.color = ORANGE
    for (x, y) in ((8, 3), (78, 3), (8, 40), (78, 40), (74, 70), (74, 100)):
        d.C(x, y, 0.8, "m", fill=1.0); d.L((x - 0.55, y - 0.55), (x + 0.55, y + 0.55), "f"); d.L((x - 0.55, y + 0.55), (x + 0.55, y - 0.55), "f")
        d.T(x + 2.5, y + 0.2, "SL-1", 0.05)
    for (x, y) in ((BX + 26, BY + 56.5), (BX + 34, BY + 56.5), (BX + 30, 110), (BX + 30, 118)):
        d.C(x, y, 0.55, "l", fill=1.0); d.T(x + 2.0, y + 0.2, "SL-2", 0.045)
    for (i, x) in enumerate((31.25, 39.75, 48.25, 56.75)):
        d.R(x - 0.6, 3.0, 1.2, 1.2, "m", fill=0.0); d.T(x, 2.4, "EV", 0.05, font="Helvetica-Bold")
    d.PL([(BX + 34.4, BY - 1.1), (BX + 34.4, 46.5), (31.25, 46.5), (31.25, 4.2)], "m", [6, 2])
    d.PL([(31.25, 4.6), (56.75, 4.6)], "m", [6, 2])
    d.color = None
    d.T(44, 6.4, "EV-READY: 4 x 40A 240V CIRCUITS IN CONDUIT, CAPPED AT J-BOXES (FUTURE CHARGERS)", 0.055)


def lum_tbl(s):
    return tbl(s, NC, TOPY, "SITE LUMINAIRE SCHEDULE", [("MARK", 0.7, "c"), ("DESCRIPTION", 5.0, "l"), ("LAMP", 1.4, "c"), ("MOUNT", 1.6, "c"), ("CTRL", 1.9, "l")], [
        ("SL-1", "Full-cutoff area light, 3000K, BUG U0, dark-sky approved", "LED 30W", "12 ft pole", "Photocell + timer"),
        ("SL-2", "Bollard / wall step light, full-cutoff, 3000K", "LED 12W", "42\" bollard", "Photocell"),
        ("WL", "Wall sconce at each door and the loggia, full-cutoff", "LED 10W", "Wall 6'-6\"", "Photocell/motion")], w=10.6, h=0.068, rowh=0.19)


sheet("E-401", "Model1_Site_Electrical_Plan", "SITE ELECTRICAL PLAN — MODEL 1", site_elec, "SCALE: 1/8\" = 1'-0\"   DESIGN INTENT",
      "SITE ELECTRICAL NOTES", [
          "Site and common lighting on the house panel HP; 1 footcandle min. average on the accessible route and parking, 0.1 fc max. at the property line.",
          "All exterior fixtures full-cutoff, 3000K or warmer, per the City of Scottsdale outdoor lighting ordinance; no uplighting.",
          "EV-ready: conduit and 40A 240V circuits to four stalls, capped in weatherproof boxes; confirm Scottsdale EV requirements at pre-app.",
          "Service lateral and transformer per the utility (C-103, E-201).",
          "Underground conduits Schedule 40 PVC, 24\" min. cover under paving; warning tape 12\" above.",
      ], extra=lum_tbl)
