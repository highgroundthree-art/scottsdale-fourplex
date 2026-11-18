"""A-701 reflected ceiling plans, S-201 shear wall plans, G-004 accessibility plan (Model 1, both floors at 3/16")."""
from sheetkit import *
from mep_fix import *
from mep_b import unit_rooms, light


# ------------------------------------------------------------------ A-701
def rcp(lvl):
    def fn(d, p):
        d.layer = "A-CLNG"
        for sp in p.spaces:
            if not sp["name"]:
                continue
            (x, y, w, h) = sp["rects"][0]
            cx, cy = x + w / 2, y + h / 2
            light(d, cx, cy)
            d.box(cx, cy + 1.6, "9'-0\"" if sp["name"].replace("\n", " ") not in ("HALL",) else "8'-0\" SOFFIT" if lvl == 1 else "9'-0\"", 0.045)
        for u in UNITS[lvl]:
            for (cx, cy, n, cfm) in unit_rooms(u):
                d.R(cx + 1.2, cy - 0.5, 1.0, 1.0, "f"); d.L((cx + 1.2, cy - 0.5), (cx + 2.2, cy + 0.5), "xf"); d.L((cx + 1.2, cy + 0.5), (cx + 2.2, cy - 0.5), "xf")
            if lvl == 1:
                ax, ay = AHU[u]
                d.R(ax - 5.5, 13.6, 15.0 if u == "A" else 15.0, 3.8, "f", [4, 2]) if False else None
            else:
                d.R(7.0 if u == "C" else 51.0, 14.2, 2.0, 2.5, "m", fill=0.85)
                d.T(8.0 if u == "C" else 52.0, 17.5, "ATTIC ACCESS 22x30", 0.045)
        if lvl == 1:
            d.R(28.75, 16.0, 2.5, 2.5, "m", fill=0.85); d.T(30, 19.4, "HATCH TO LOFT 202", 0.045)
        d.color = RED
        d.T(12.5, -1.0 if lvl == 1 else -1.0, ("F1 RATED CEILING (D-002/3) — ALL UNIT CEILINGS ON THIS LEVEL" if lvl == 1 else "5/8\" TYPE X GWB ON TRUSSES, R-38 ABOVE"), 0.05)
        d.color = None
    return fn


s = new()
two_level(s, rcp(1), rcp(2), "A-701", "REFLECTED CEILING PLAN")
y = tbl(s, 15.3, TOPY, "CEILING SCHEDULE", [("TYPE", 0.6, "c"), ("CONSTRUCTION", 3.0, "l"), ("HT.", 0.7, "c"), ("FINISH", 1.2, "l")], [
    ("C1", "F1: 2 layers 5/8\" X on RC, ind. joists", "9'-0\"", "Smooth, flat paint"), ("C2", "5/8\" X GWB on roof trusses", "9'-0\"", "Smooth, flat paint"),
    ("C3", "Hall soffit at AHU, 5/8\" X", "8'-0\"", "Access panel 24x36"), ("C4", "Bath: 5/8\" X MR GWB", "9'-0\"", "Semi-gloss")])
notes(s, 15.3, y, "RCP NOTES", [
    "Ground-floor unit ceilings are the 1-hour F1 assembly: only listed penetrations (sprinklers with listed escutcheons, CRD-protected grilles, boxes listed for rated ceilings).",
    "Light fixtures are surface LED, centered in the room unless noted. Square with X: supply register (see M-101/M-102).",
    "Ceiling height 9'-0\" throughout except the hall soffit over AHU-A and AHU-B (8'-0\").",
    "Attic access 22x30 in the Unit C and D halls with weatherstripped, insulated R-38 hatch (IECC R402.2.4).",
], 5.6)
save(s, "A-701", "Model1_Reflected_Ceiling_Plans", "REFLECTED\nCEILING PLANS")


# ------------------------------------------------------------------ S-201
SEGS = [  # (x0, y0, x1, y1, tag) exterior + W1 shear walls, feet
    (0, 0, 0, 13.5, "SW1"), (0, 28, 0, 37, "SW1"), (60, 0, 60, 13.5, "SW1"), (60, 28, 60, 37, "SW1"),
    (0, 0, 4, 0, "SW2"), (10, 0, 25, 0, "SW1"), (35, 0, 50, 0, "SW1"), (56, 0, 60, 0, "SW2"),
    (0, 50, 9.5, 50, "SW1"), (15.5, 50, 25, 50, "SW1"), (35, 50, 39.5, 50, "SW2"), (45.5, 50, 52, 50, "SW2"),
    (25, 0, 25, 50, "SW3"), (35, 0, 35, 50, "SW3"),
]


def shear(lvl):
    def fn(d, p):
        d.layer = "S-SHWL"; d.color = RED
        for (x0, y0, x1, y1, t) in SEGS:
            d.L((x0, y0), (x1, y1), "xh")
            d.box((x0 + x1) / 2 + (1.6 if x0 == x1 and x0 < 30 else -1.6 if x0 == x1 else 0), (y0 + y1) / 2 + (0 if x0 == x1 else (-1.0 if y0 == 0 else 1.0)), t, 0.05)
            for (hx, hy) in ((x0, y0), (x1, y1)):
                d.PL([(hx - 0.45, hy), (hx, hy - 0.45), (hx + 0.45, hy), (hx, hy + 0.45)], "m", closed=True, fill=0.0)
        d.color = None
    return fn


s = new()
two_level(s, shear(1), shear(2), "S-201", "SHEAR WALL PLAN (DESIGN INTENT)")
y = tbl(s, 15.3, TOPY, "SHEAR WALL SCHEDULE (PRELIMINARY)", [("MARK", 0.6, "c"), ("SHEATHING", 2.0, "l"), ("EDGE NAIL", 1.1, "c"), ("PLATE ATTACH.", 1.8, "l")], [
    ("SW1", "7/16\" OSB one side", "8d @ 6\"", "5/8\" AB @ 48\" / SDS"), ("SW2", "7/16\" OSB one side", "8d @ 4\"", "5/8\" AB @ 32\""),
    ("SW3", "W1: 7/16\" OSB each stud row, under GWB", "8d @ 4\"", "5/8\" AB @ 32\" each plate")], w=5.5)
notes(s, 15.3, y, "LATERAL SYSTEM", [
    "Light-frame wood shear walls with wood structural panel sheathing; roof and floor diaphragms 7/16\" and 3/4\" OSB. Design per ASCE 7-16/22 and AWC SDPWS by the structural engineer of record.",
    "Preliminary criteria: wind 115 mph Vult, exposure C; Seismic Design Category B (Phoenix area). Verify for the parcel with the ASCE Hazard Tool.",
    "Black diamonds: hold-downs at every shear wall end, both floors, continuous rod or strap to the PT slab (S-101, S-502).",
    "W1 walls (SW3): sheathing goes on the stud face toward the cavity of each stud row so the double-stud acoustic and fire design (D-002/1) is unchanged — confirm with the listing.",
    "Window and door openings in shear lines are designed as perforated or force-transfer shear walls by the engineer.",
], 5.6)
save(s, "S-201", "Model1_Shear_Wall_Plan", "SHEAR WALL\nPLAN")


# ------------------------------------------------------------------ G-004
def acc(lvl):
    def fn(d, p):
        d.layer = "A-ANNO-SYMB"
        if lvl == 1:
            d.color = BLUE
            d.PL([(29.5, 57.0), (29.5, 46.0), (29.5, 44.0), (25.5, 44.0)], "h", [6, 2]); d.PL([(29.5, 44.0), (34.5, 44.0)], "h", [6, 2])
            d.arrow((26.5, 44.0), (25.3, 44.0), "h"); d.arrow((33.5, 44.0), (34.7, 44.0), "h")
            for (x, y) in ((19.6, 5.4), (19.6, 31.2), (12.0, 21.5), (8.0, 7.0), (12.5, 43.0)):
                d.C(x, y, 2.5, "l"); d.T(x, y + 0.2, "60\" TURN", 0.045)
            d.T(12.5, 47.5, "UNIT A — TYPE A", 0.09, font="Helvetica-Bold")
            d.T(47.5, 47.5, "UNIT B — TYPE B", 0.09, font="Helvetica-Bold")
            for (x, y) in ((40.4, 5.4), (40.4, 31.2), (48.0, 21.5), (52.0, 7.0)):
                d.C(x, y, 2.5, "l", ); d.T(x, y + 0.2, "60\" TURN", 0.045)
            d.T(29.5, 55.5, "ACCESSIBLE ROUTE FROM PUBLIC WALK + VAN STALL (C-101)", 0.05)
            for (x, y, t) in ((7, 0.0, "SLIDER 119: 1/2\" MAX. THRESHOLD"), (29.5, 50.6, "DOOR 101: 34\" CLR, 1/2\" THRESHOLD"), (25.5, 41.5, "110"), (34.5, 41.5, "120")):
                d.T(x, y + (-0.6 if y < 1 else 1.0), t, 0.05)
            d.color = None
        else:
            d.T(30, 30, "UPPER UNITS C AND D: NOT COVERED (NO ELEVATOR) — IBC 1107.7.2", 0.08, font="Helvetica-Bold", color=BLUE)
            d.T(30, 32, "Visitable features provided anyway: 32\" doors, lever hardware, blocking for grab bars, switches 48\" max.", 0.055, color=BLUE)
    return fn


s = new()
two_level(s, acc(1), acc(2), "G-004", "ACCESSIBILITY PLAN")
y = tbl(s, 15.3, TOPY, "UNIT A (TYPE A) FEATURES — ICC A117.1-2009 SEC. 1003", [("ITEM", 1.4, "l"), ("PROVIDED", 4.1, "l")], [
    ("Entry", "Door 110: 32\" clear, lever, 18\" latch-side pull clearance, 1/2\" max. threshold"),
    ("Route", "36\" min. within the unit; turning spaces in each room shown (60\" circle)"),
    ("Kitchen", "40\" clearance (U-shape 60\"); sink knee space w/ removable base; 34\" work surface"),
    ("Bath", "Roll-in shower 60x30 min., grab bars, fold seat; WC 16\"–18\" to CL; lav knee space"),
    ("Laundry", "Front-load W/D, side clear floor space 30x48"),
    ("Controls", "Switches, outlets, thermostat 15\"–48\" A.F.F.; panel within reach"),
    ("Alarms", "Visual smoke alarm prewire in bedrooms + doorbell signal"),
    ("Patio", "Slider 119: 1/2\" max. threshold, level patio 2% max."),
], w=5.5)
y = tbl(s, 15.3, y, "UNIT B (TYPE B) — SEC. 1004", [("ITEM", 1.4, "l"), ("PROVIDED", 4.1, "l")], [
    ("Doors", "31-3/4\" nominal clear at user passage doors"), ("Route", "36\" min.; changes in level 1/4\" max."),
    ("Kitchen", "30x48 parallel approach at sink, range, ref."), ("Baths", "Option A clearances; blocking for future grab bars"),
    ("Controls", "15\"–48\" A.F.F."),
], w=5.5)
notes(s, NC, TOPY, "ACCESSIBILITY NOTES", [
    "Building contains four dwelling units: covered multifamily dwelling under the federal Fair Housing Act and IBC 1107. Without an elevator, only ground-floor units are covered: Unit A is built to Type A (exceeding the requirement), Unit B to Type B.",
    "Accessible route (blue) from the public sidewalk and the van-accessible stall P1 to door 101, and from the shared entry 100 to doors 110 and 120. Walk slopes 1:20 max., cross slope 2% max.",
    "Thresholds 1/2\" max., beveled 1:2 above 1/4\" (D-001/6). Slab recessed at doors 101, 119, 131 (S-101).",
    "Common-use areas (shared entry, mailboxes, trash enclosure) meet A117.1 Ch. 4 and 7: mailboxes 15\"–48\" A.F.F., trash enclosure gate 32\" clear.",
    "Details and mounting heights on D-003 and the enlarged plans A-401 / A-402.",
], 5.1)
save(s, "G-004", "Model1_Accessibility_Plan", "ACCESSIBILITY\nPLAN")
