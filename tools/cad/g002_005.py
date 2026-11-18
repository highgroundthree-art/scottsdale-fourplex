"""G-002 code analysis and G-005 rated assemblies + life safety plans, Model 1."""
import math, sys
from cadkit import Sheet
from plan_engine import table, para, hex_tag
import sheetlib as SL

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
F = 12
common = dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE)


def save(s, cfg):
    sc = s.scale
    s.scale = 48
    SL.border_and_titleblock(s, cfg)
    s.scale = sc
    base = f"{OUT}/{cfg['sheet_no']}_{cfg['file']}"
    s.to_pdf(base + ".pdf", title=f"{cfg['sheet_no']} {cfg['sheet_title']}", author="Scottsdale Fourplex")
    s.to_dxf(base + ".dxf")
    print("wrote", base)


def kv_block(s, x, y, title, rows, w, kw=1.9, h=0.075):
    y = SL.head(s, x, y, title, w)
    for k, v in rows:
        s.text((x, y), k, h, font="Helvetica-Bold", align="l")
        y = min(para(s, x + kw, y, v, w - kw, h, lead=1.4), y - 0.2) - 0.03
    return y - 0.1


# =============================================================== G-002 CODE ANALYSIS
s = Sheet(origin=(0, 0))
s.text((1.0, 22.95), "CODE ANALYSIS — MODEL 1, STACKED BIG HOUSE", 0.3, font="Helvetica-Bold", align="l")
s.text((1.0, 22.6), "2021 International Building Code as amended by the City of Scottsdale. Section numbers are IBC unless noted. Every line marked VERIFY is to be confirmed with Scottsdale Planning and Development Services at the pre-application meeting.", 0.09, align="l")
s.line((1.0, 22.45), (31.8, 22.45), lw="h")

C1, C2, C3 = 1.0, 11.4, 21.8
W = 9.9
y = kv_block(s, C1, 22.1, "1. APPLICABLE CODES", [
    ("BUILDING", "2021 IBC with City of Scottsdale amendments (Scottsdale Revised Code Ch. 31)"),
    ("FIRE", "2021 IFC with Scottsdale amendments (Ch. 36), incl. local sprinkler requirements"),
    ("PLUMBING / MECH / GAS", "2021 IPC, IMC, IFGC with Scottsdale amendments"),
    ("ELECTRICAL", "2020 NEC (NFPA 70) with Scottsdale amendments"),
    ("ENERGY", "2021 IECC residential provisions, climate zone 2B; Scottsdale green building options (IgCC) not adopted for this project unless elected"),
    ("ACCESSIBILITY", "IBC Ch. 11, ICC A117.1-2009; federal Fair Housing Act design requirements (four or more dwelling units = covered multifamily dwellings)"),
    ("ZONING", "City of Scottsdale Zoning Ordinance — district, setbacks, height and parking VERIFY once a parcel is selected"),
], W)
y = kv_block(s, C1, y, "2. OCCUPANCY CLASSIFICATION (CH. 3)", [
    ("GROUP", "R-2 — more than two dwelling units (310.4)"),
    ("ACCESSORY", "House storage 102 and storage loft 202 (±250 SF total) are accessory to R-2, under 10% of the floor area (508.2); no separation required"),
    ("MIXED USE", "None"),
], W)
y = kv_block(s, C1, y, "3. CONSTRUCTION TYPE (CH. 6)", [
    ("TYPE", "V-B, combustible, unprotected (602.5)"),
    ("TABLE 601", "Structural frame, bearing walls, floors and roof: 0 hours required. Rated elements on this project come from Ch. 4, 7 and 10, not from the construction type."),
    ("SPRINKLERS", "Automatic sprinkler system throughout, NFPA 13R (903.2.8 and 903.3.1.2; required by Scottsdale amendments). Deferred submittal, FP-001."),
], W)
y = kv_block(s, C1, y, "4. ALLOWABLE HEIGHT AND AREA (CH. 5)", [
    ("HEIGHT", "Table 504.3, R-2, V-B, S13R: 60 ft allowed. Provided: ±29'-8\" to the ridge above grade (building height measured to the average roof height per IBC 202 is ±24'-10\"). Zoning height governs: VERIFY."),
    ("STORIES", "Table 504.4, R-2, V-B, S13R: 3 stories allowed. Provided: 2 stories."),
    ("AREA", "Table 506.2, R-2, V-B, S13R: 7,000 SF per story (NS value; no area increase for 13R). Provided: 3,000 SF per story, 6,000 SF total. Frontage increase not needed."),
    ("RESULT", "Complies. Provided area is 43% of the allowable per story."),
], W)

y = kv_block(s, C2, 22.1, "5. FIRE-RESISTANCE RATINGS (CH. 4 AND 7)", [
    ("UNIT SEPARATION WALLS (W1)", "Required 1 hour (420.2, 708.3); 1/2 hour is permitted for V-B with 13R (708.3 exc. 2). PROVIDED 1 HOUR, by choice, for fire safety and STC 50 sound isolation. Continuous from slab to roof deck (708.4)."),
    ("FLOOR / CEILING (F1)", "Required 1 hour (420.3, 711.2.4.3); 1/2 hour permitted with 13R. PROVIDED 1 HOUR, STC/IIC 50 (1206)."),
    ("CORRIDORS 100 / 200", "Table 1020.2, R, occupant load over 10, sprinklered: 1/2 hour. Provided by the 1-hour W1 walls. Unit entry doors 20-minute, self-closing, positive-latching (716.2.2.1)."),
    ("EXTERIOR WALLS", "Table 602, V-B, R: fire separation distance (FSD) under 10 ft = 1 hour. WEST WALL (W2), FSD 7'-0\": 1 HOUR from both sides. North, south and east walls: FSD 10 ft or more: 0 hour."),
    ("OPENINGS IN WEST WALL", "Table 705.8, FSD 5 to under 10 ft, unprotected, sprinklered: 25% max per story. Provided: ±42 SF of 500 SF per story = 8%. Complies."),
    ("PROJECTIONS", "West eave 2'-0\" leaves 5'-0\" (60\") to the lot line; 705.2 minimum 40\". Eave framing within FSD under 10 ft: 1-hour or fire-retardant-treated per 705.2.3: VERIFY detail D-002."),
    ("ATTIC", "Draftstopping by the W1 walls run to the roof deck (718.4.2). Attic area per draftstop compartment under 3,000 SF."),
    ("PENETRATIONS", "Through-penetration firestop systems in W1, W2 and F1 (714). Listed ceiling radiation dampers at F1 duct openings (717.6.2)."),
], W, kw=2.3)

y = kv_block(s, C2, y, "6. MEANS OF EGRESS (CH. 10)", [
    ("OCCUPANT LOAD", "Table 1004.5, residential 200 gross: 3,000 / 200 = 15 per story; 30 total."),
    ("EXITS PER STORY", "One exit permitted per story: Table 1006.3.4(1), R-2, max. 4 dwelling units per story and 125 ft exit access travel distance, building sprinklered with emergency escape openings. Provided: 2 units per story; travel distance see G-005."),
    ("COMMON STAIR", "Exit access stairway serving two stories only, unenclosed permitted (1019.3 exc. 1); built inside the 1-hour core anyway. Width 3'-8\" clear (36\" min., 1011.2). Risers 6¾\" (7\" max.), treads 11\" (1011.5.2). Handrails both sides (1014). Headroom 6'-8\" min. Space below enclosed, no storage (1011.7.3)."),
    ("EXIT", "Door 101 at shared entry 100 to the exterior, 3'-6\" x 8'-0\", 34\" clear min. Panic hardware not required (occupant load under 50). Exit discharge to the public way at the street walk."),
    ("UNIT EGRESS", "Each Unit A and B also exits directly to the rear patio through slider 119/131. Units C and D: all bedrooms have emergency escape openings (1031)."),
    ("ESCAPE OPENINGS", "Every sleeping room: 5.7 SF net clear (5.0 SF at grade floor), 24\" min. height, 20\" min. width, sill 44\" max. (1031.3)."),
    ("ILLUMINATION", "Means of egress lighting at the stair, landing and entry; emergency power not required for 2-exit-free R-2 under 1008.3 exceptions: VERIFY."),
], W, kw=2.3)

y3 = kv_block(s, C3, 22.1, "7. FIRE PROTECTION SYSTEMS (CH. 9)", [
    ("SPRINKLERS", "NFPA 13R throughout, including attics where required by Scottsdale amendments: VERIFY. Riser in room 103 (door 102), FDC location per fire marshal."),
    ("FIRE ALARM", "Not required (907.2.9.1: under 3 stories above the lowest level of exit discharge and under 16 units). Sprinkler waterflow alarm bell on the exterior."),
    ("SMOKE ALARMS", "Hard-wired, interconnected within each unit, battery backup: each sleeping room, outside each sleeping area, each story (907.2.11.2)."),
    ("CO ALARMS", "Each unit with gas appliances: outside each sleeping area and in any bedroom with a fuel-burning appliance (IFC 915)."),
    ("EXTINGUISHERS", "Per IFC 906 and the fire marshal."),
    ("ADDRESS", "Building address and unit letters visible from the street, 4\" min. contrasting (IFC 505)."),
], W, kw=1.6)
y3 = kv_block(s, C3, y3, "8. ACCESSIBILITY (CH. 11, FAIR HOUSING ACT)", [
    ("REQUIREMENT", "Four or more dwelling units: ground-floor units in a building without an elevator are Type B (1107.6.2.2.1, 1107.7.2). Upper units exempt."),
    ("PROVIDED", "Unit A: Type A (exceeds requirement, by choice: roll-in shower, 60\" turning spaces, accessible kitchen). Unit B: Type B. Units C, D: not required."),
    ("SITE", "Accessible route from the public walk and the van-accessible stall to door 101 and to units A and B (1104). Slope 1:20 max. walks, 1:12 ramps with handrails. Details D-003, plan G-004."),
    ("PARKING", "1 van-accessible stall with 8 ft access aisle (1106)."),
], W, kw=1.6)
y3 = kv_block(s, C3, y3, "9. PLUMBING FIXTURES (IPC CH. 4)", [
    ("REQUIRED", "Table 2902.1, R-2 apartment: per dwelling unit 1 WC, 1 lav, 1 bathtub/shower, 1 kitchen sink, 1 clothes washer connection."),
    ("PROVIDED", "Unit A: 2 WC, 2 lav, roll-in shower + tub/shower. Units B, C, D: 2 WC, 3 lav, shower + tub/shower. Each: kitchen sink, dishwasher, washer box, 50-gal water heater."),
], W, kw=1.6)
y3 = kv_block(s, C3, y3, "10. ENERGY (IECC 2021, CZ 2B)", [
    ("ENVELOPE", "Ceiling R-38; walls R-13 cavity or R-0+10ci per R402.1.3; slab edge none required; fenestration U-0.40, SHGC 0.25. Air leakage 5 ACH50 max., tested."),
    ("SYSTEMS", "Heat pumps, ducts inside conditioned space or R-8 in the attic, duct leakage tested. 90% high-efficacy lighting. Compliance path on EN-001."),
], W, kw=1.6)

tbl_y = SL.head(s, C3, y3 - 0.05, "11. SUMMARY", W)
table(s, C3, tbl_y + 0.04, [("ITEM", 2.7, "l"), ("ALLOWED / REQUIRED", 3.0, "c"), ("PROVIDED", 3.0, "c"), ("OK", 0.5, "c")], [
    ("Height (IBC)", "60 ft / 3 stories", "±29'-8\" / 2 stories", "YES"),
    ("Area per story", "7,000 SF", "3,000 SF", "YES"),
    ("Unit separations", "1/2 hr (13R)", "1 hr", "YES"),
    ("West wall, FSD 7'", "1 hr", "1 hr both sides", "YES"),
    ("West wall openings", "25% max.", "8%", "YES"),
    ("Exit access travel", "125 ft (single exit)", "see G-005", "YES"),
    ("Accessibility", "B, B (ground)", "A, B", "YES"),
], h=0.07, rowh=0.17)
save(s, dict(common, sheet_no="G-002", file="Model1_Code_Analysis", sheet_title="CODE ANALYSIS"))

# =============================================================== G-005 RATED ASSEMBLIES + LIFE SAFETY
s = Sheet(origin=(1.4, 21.4), scale=96)


def setorg(x, y):
    s.ox, s.oy = x, y


def M(x, y):
    return (x * F, y * F)


def wall(a, b, kind):
    style = {"W1": ("xh", None), "W2": ("xh", [8, 2, 2, 2]), "EXT": ("m", None), "CORR": ("l", [3, 2])}[kind]
    s.line(M(*a), M(*b), layer="A-ANNO-SYMB" if kind != "EXT" else "A-WALL", lw=style[0], space="m", dash=style[1])
    if kind in ("W1", "W2"):  # rating ticks
        L = math.dist(a, b); n = int(L // 4)
        for i in range(1, n):
            t = i / n; px = a[0] + (b[0] - a[0]) * t; py = a[1] + (b[1] - a[1]) * t
            dx, dy = (0.7, 0) if a[0] == b[0] else (0, 0.7)
            s.line(M(px - dx, py - dy), M(px + dx, py + dy), layer="A-ANNO-SYMB", lw="l", space="m")


def path(pts, label, lab_at):
    s.pline([M(*p) for p in pts], layer="A-ANNO-SYMB", lw="m", space="m", dash=[5, 2])
    a, b = pts[-2], pts[-1]
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for d in (2.6, -2.6):
        s.line(M(*b), M(b[0] - 1.6 * math.cos(ang + d / 6), b[1] - 1.6 * math.sin(ang + d / 6)), layer="A-ANNO-SYMB", lw="m", space="m")
    s.circle(M(*pts[0]), 0.5 * F, layer="A-ANNO-SYMB", lw="m", space="m", fill=0.0)
    L = sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))
    s.text(s.m2p(*M(*lab_at)), f"{label} = {L:.0f}'-0\" (125' MAX.)", 0.075, font="Helvetica-Bold", align="l")
    return L


def keyplan(level):
    s.rect(0, 0, 60 * F, 50 * F, layer="A-WALL", lw="m", space="m")
    wall((0, 0), (0, 50), "W2")
    wall((25, 0), (25, 50), "W1"); wall((35, 0), (35, 50), "W1")
    if level == 1:
        names = [(18.5, 30, "UNIT A\nTYPE A · 1,250 SF\nOL 7"), (41.5, 30, "UNIT B\nTYPE B · 1,250 SF\nOL 7")]
        s.rect(25 * F, 23.5 * F, 10 * F, 26.5 * F, layer="A-ANNO-SYMB", lw="f", space="m", fill=0.9)
        s.text(s.m2p(30 * F, 40 * F), "SHARED", 0.07, font="Helvetica-Bold"); s.text(s.m2p(30 * F, 41.6 * F), "ENTRY 100", 0.07, font="Helvetica-Bold")
        s.text(s.m2p(30 * F, 12 * F), "STORAGE", 0.065); s.text(s.m2p(30 * F, 13.6 * F), "102", 0.065)
        s.rect(31.75 * F, 46 * F, 3.25 * F, 4 * F, layer="A-ANNO-SYMB", lw="l", space="m", fill=0.6)
        s.text(s.m2p(39.5 * F, 52.6 * F), "FIRE RISER 103", 0.06, align="l")
        s.line(M(33.4, 48), M(39, 51.8), layer="A-ANNO-SYMB", lw="f", space="m")
        # exits
        for (x, y, t) in ((29.5, 50, "EXIT 101"), (7, 0, "SLIDER 119"), (53, 0, "SLIDER 131")):
            s.text(s.m2p(x * F, (y + (3.6 if y else 2.2)) * F), t, 0.065, font="Helvetica-Bold")
        La = path([(2, 2), (12, 15), (12, 24), (12, 44), (24, 44), (27.5, 44), (29.5, 50)], "TRAVEL A", (0, -5.5))
        Lb = path([(58, 2), (48, 15), (48, 24), (48, 44), (36, 44), (31.5, 44), (29.5, 50)], "TRAVEL B", (36, -5.5))
    else:
        names = [(18.5, 30, "UNIT C\n3 BR · 1,250 SF\nOL 7"), (41.5, 30, "UNIT D\n3 BR · 1,250 SF\nOL 7")]
        s.rect(25 * F, 23.5 * F, 10 * F, 26.5 * F, layer="A-ANNO-SYMB", lw="f", space="m", fill=0.9)
        s.text(s.m2p(30 * F, 46.5 * F), "LANDING 200", 0.065, font="Helvetica-Bold")
        s.text(s.m2p(30 * F, 12 * F), "LOFT", 0.065); s.text(s.m2p(30 * F, 13.6 * F), "202", 0.065)
        for x0 in (25.4, 30.6):
            for i in range(10):
                yy = 27.5 + i * 11 / 12
                s.line(M(x0, yy), M(x0 + 4, yy), layer="A-FLOR-STRS", lw="xf", space="m")
        # travel: unit C farthest point to the exit door 101 (via stair, measured on the nosings)
        Lc = path([(2, 2), (12, 15), (12, 44), (24, 44), (32.6, 36), (32.6, 27.5), (30, 25.5), (27.4, 27.5), (27.4, 36), (27.4, 44), (29.5, 50)], "TRAVEL C (VIA STAIR TO 101)", (0, -5.5))
        s.text(s.m2p(40 * F, -5.5 * F), "UNIT D SAME, MIRRORED", 0.075, font="Helvetica-Bold", align="l")
        s.text(s.m2p(2 * F, -2.2 * F), "ALL BEDROOMS: EMERGENCY ESCAPE OPENINGS (1031)", 0.06, align="l")
    for (x, y, t) in names:
        for i, ln in enumerate(t.split("\n")):
            s.text(s.m2p(x * F, (y + i * 1.9) * F), ln, 0.085 if i == 0 else 0.065, font="Helvetica-Bold" if i == 0 else "Helvetica")


setorg(1.4, 21.4); keyplan(1)
SL.drawing_title(s, 1.0, 13.8, "1", "G-005", "LIFE SAFETY PLAN — GROUND FLOOR", "SCALE: 1/8\" = 1'-0\"   OCCUPANT LOAD 15 · ONE EXIT PERMITTED (TABLE 1006.3.4(1))", w=8.6, scalebar=False)
setorg(11.0, 21.4); keyplan(2)
SL.drawing_title(s, 10.6, 13.8, "2", "G-005", "LIFE SAFETY PLAN — UPPER FLOOR", "SCALE: 1/8\" = 1'-0\"   OCCUPANT LOAD 15 · EXIT ACCESS STAIR TO EXIT 101", w=8.6, scalebar=False)

# legend
ly = SL.head(s, 1.0, 13.1, "LIFE SAFETY LEGEND", 18.2)
items = [("W1", "1-HOUR UNIT SEPARATION WALL, SLAB TO ROOF DECK"), ("W2", "1-HOUR EXTERIOR WALL, RATED BOTH SIDES (FSD 7'-0\")"),
         ("PATH", "EXIT ACCESS TRAVEL PATH, MEASURED FROM THE MOST REMOTE POINT"), ("CORE", "SHARED ENTRY / LANDING: CORRIDOR, 1/2-HR REQUIRED, 1-HR PROVIDED")]
for i, (k, t) in enumerate(items):
    x = 1.0 + (i % 2) * 9.2; yy = ly - (i // 2) * 0.3
    if k == "W1":
        s.line((x, yy + 0.04), (x + 0.8, yy + 0.04), lw="xh")
    elif k == "W2":
        s.line((x, yy + 0.04), (x + 0.8, yy + 0.04), lw="xh", dash=[8, 2, 2, 2])
    elif k == "PATH":
        s.line((x, yy + 0.04), (x + 0.8, yy + 0.04), lw="m", dash=[5, 2]); s.circle((x, yy + 0.04), 0.04, lw="m", fill=0.0)
    else:
        s.rect(x, yy - 0.04, 0.8, 0.16, lw="f", fill=0.9)
    s.text((x + 1.0, yy), t, 0.072, align="l")

# rated assemblies table
ty = SL.head(s, 1.0, ly - 0.8, "RATED ASSEMBLY SCHEDULE", 18.2)
cols = [("TAG", 0.55, "c"), ("ASSEMBLY", 2.6, "l"), ("RATING", 0.7, "c"), ("LISTED DESIGN (OR EQUAL)", 1.65, "c"), ("CONSTRUCTION", 9.1, "l"), ("STC / IIC", 0.9, "c"), ("DETAIL", 0.7, "c")]
rows = [
    ("W1", "Unit separation wall", "1 HR", "UL U341 / GA WP 3820", "Staggered 2x4 studs @ 16\" on 2x6 plates, 3½\" batts woven, 5/8\" Type X GWB each side, resilient channel one side", "STC 55", "D-002/1"),
    ("W2", "Exterior wall, west (FSD 7')", "1 HR", "UL U356 / GA WP 8105", "2x6 studs @ 16\", R-21 batts, 5/8\" Type X GWB inside, 5/8\" Type X sheathing + 7/8\" 3-coat stucco outside", "—", "D-002/2"),
    ("EXT", "Exterior wall, typical", "0 HR", "—", "2x6 studs @ 16\", R-21 batts, 1/2\" GWB inside, 7/16\" OSB + WRB + 7/8\" 3-coat stucco outside", "—", "D-001/1"),
    ("F1", "Floor / ceiling between units", "1 HR", "UL L528 / GA FC 5512", "Finish over acoustic mat, 3/4\" T&G subfloor, 11-7/8\" open-web trusses @ 24\", independent 2x6 ceiling joists @ 16\" with R-19, RC, 2 layers 5/8\" Type X GWB", "50 / 50", "D-002/3"),
    ("R1", "Roof / ceiling", "0 HR", "—", "Clay tile on 2 layers underlayment, 7/16\" OSB, trusses @ 24\", R-38 blown, 5/8\" Type X GWB ceiling", "—", "A-301.1"),
    ("P1", "Interior partition", "0 HR", "—", "2x4 studs @ 16\", 1/2\" GWB each side; 5/8\" moisture-resistant at wet walls", "—", "—"),
    ("DS", "Attic draftstop", "—", "IBC 718.4", "W1 wall continued to the roof deck; 5/8\" Type X GWB both sides above the ceiling, joints taped", "—", "D-002/4"),
    ("DR-C", "Unit entry doors 110, 120, 210, 230", "20 MIN", "NFPA 252 / UL 10C", "1¾\" solid-core wood, labeled frame, self-closing, positive latching, smoke gasket (716.2.2.1)", "—", "A-601"),
]
ty = table(s, 1.0, ty + 0.04, cols, rows, h=0.068, rowh=0.19)

NOTES = [
    "Listed designs are the basis of design. A substitute must be a tested assembly of equal or greater rating with the listing submitted to the building official.",
    "Rated walls are continuous from the top of slab to the underside of the roof deck or the rated floor above. Seal top and bottom tracks with listed joint systems (715).",
    "Every penetration of a rated wall or floor uses a listed through-penetration firestop system (714.4, 714.5) matched to the item and the assembly. Membrane penetrations: outlet boxes max. 16 sq in., 24\" apart horizontally on opposite faces, or putty pads (714.4.2). No boxes in W1 walls on this project.",
    "Ducts through F1: listed ceiling radiation dampers (717.6.2). No ducts through W1 walls.",
    "Mark rated walls above the ceiling every 30 ft max. and within 15 ft of each end: 'FIRE AND/OR SMOKE BARRIER — PROTECT ALL OPENINGS', 3\" letters (703.5).",
    "Open-web floor trusses: no notching, drilling or attachment to the bottom chord inside F1 (nothing hangs from the trusses).",
    "Fire separation distance on the west is measured to the interior lot line. Any change to the lot or the building footprint requires a new check of W2 and the west openings (G-002).",
]
y = SL.notes_list(s, 21.15, 23.2, "RATED ASSEMBLY NOTES", NOTES, 5.1)
LS = [
    "Building sprinklered throughout per NFPA 13R; riser room 103 at the shared entry; FDC location per the Scottsdale fire marshal.",
    "Each story has one exit, permitted by Table 1006.3.4(1): 2 units per story (4 max.) and travel distances under 125 ft, shown on plans 1 and 2.",
    "Exit 101 has no lock requiring a key or special knowledge from the inside (1010.2.4). The shared entry is lit at all times the building is occupied (1008.2).",
    "Ground units also exit directly to the rear patios through sliders 119/131; these are not counted as required exits.",
    "Emergency escape and rescue openings at every bedroom (1031); sliders 119/131 serve the ground-floor primary bedrooms.",
    "Smoke alarms interconnected within each unit; CO alarms per IFC 915; exterior waterflow bell. No building fire alarm required (907.2.9.1).",
]
y = SL.notes_list(s, 26.55, 23.2, "LIFE SAFETY NOTES", LS, 5.25)
save(s, dict(common, sheet_no="G-005", file="Model1_Rated_Assemblies_Life_Safety", sheet_title="RATED ASSEMBLIES\n+ LIFE SAFETY"))
