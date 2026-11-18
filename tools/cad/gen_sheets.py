"""Model 2 and Model 3 design-development floor plan sheets."""
import sys
from cadkit import Sheet
from gen_floor import View, window_rows, F
import sheetlib as SL
from plan_engine import para

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
which = sys.argv[2:] or ["A-101.2", "A-102.2", "A-101.3", "A-102.3", "A-111.3"]
FP = "/home/claude/scottsdale-fourplex/drawings/floor-plans/"
DATE = "2026-11-18"
M = "—"


def common_notes(model, level, extra=None):
    n = [
        "Do not scale drawings. Exterior dimensions are to outside face of exterior wall finish; interior dimensions are to centerline of partitions; grid lines are at outside face of exterior walls and centerline of rated walls, unless noted otherwise.",
        "Wall types per legend. Rated walls are 1-hour fire-resistance-rated assemblies (G-005). Run W1 continuous from top of slab to underside of roof deck; seal every penetration with a listed firestop system (D-002).",
        "Building is fully sprinklered per NFPA 13R. Provide interconnected smoke alarms in each sleeping room, outside each sleeping area and on each story; CO alarms per IFC 915.",
        ("Every bedroom has an emergency escape and rescue opening: " + ("5.0 SF min. net clear at grade floor" if level == 1 else "5.7 SF min. net clear") +
         ", 24\" min. clear height, 20\" min. clear width, sill 44\" max. A.F.F. (IBC 1031)."),
        "No plumbing, recessed boxes or ductwork in W1 walls. Wet rooms stack over wet rooms; do not cut or notch joists, trusses or beams (X-101).",
        "Kitchens: pull-out trash and recycling compartment with two 7-gallon bins per Scottsdale IBC 1211. Range hoods recirculating or ducted up; no duct through a rated wall.",
        "Provide 2x blocking for grab bars at every toilet, tub and shower. Upper-floor washers and water heaters sit in drain pans with automatic leak shutoff.",
        "Window sizes are nominal; verify rough openings with the manufacturer. Side yards are 10'-0\" min., so exterior wall openings are not limited by fire separation distance.",
        "Ceiling height 9'-0\" A.F.F. unless noted. Fixtures, casework and door swings follow the concept plans (rev 1.4) and are to be confirmed on the enlarged plans (A-401, A-402).",
    ]
    return n + (extra or [])


def notes_cols(s, cols, cfg, views, dd, area_rows, area_title, walls):
    """cols: list of (x, ytop, width) for 4 blocks: notes, walls+symbols, doors, windows+dd+area."""
    (x1, y1, w1), (x2, y2, w2), (x3, y3, w3), (x4, y4, w4) = cols
    y = SL.notes_list(s, x1, y1, "GENERAL NOTES — FLOOR PLANS", cfg["notes"], w1)
    if x2 == x1:
        y2 = y
    y = SL.wall_legend(s, x2, y2, walls, w2)
    y = SL.symbols(s, x2, y - 0.1, w2)
    rows = []
    for v in views:
        rows += v.door_rows
    yd = SL.door_schedule(s, x3, y3, rows, w3)
    if x4 == x3:
        y4 = yd
    y = SL.window_schedule(s, x4, y4, window_rows(views), w4)
    y = SL.notes_list(s, x4, y, "DESIGN-DEVELOPMENT COORDINATION", dd, w4, h=0.068, numbering="alpha")
    SL.area_summary(s, x4, y, area_title, area_rows, w4)


def save(s, cfg):
    SL.border_and_titleblock(s, cfg)
    base = f"{OUT}/{cfg['sheet_no']}_{cfg['file']}"
    s.to_pdf(base + ".pdf", title=f"{cfg['sheet_no']} {cfg['sheet_title'].replace(chr(10), ' ')}", author="Scottsdale Fourplex")
    s.to_dxf(base + ".dxf")
    print("wrote", base)


# ------------------------------------------------------------------ MODEL 2
def model2(level):
    svg = FP + ("model2-ground.svg" if level == 1 else "model2-upper.svg")
    s = Sheet(origin=(3.575, 21.15))
    vc = dict(svg=svg, ppf=6.6, origin=(60, 40), W=28, D=102, rot="cw", west_type="EXT", type_a_unit="A",
              grids=([(0, "1"), (36, "2"), (58, "3"), (80, "4"), (102, "5")], [(0, "A"), (28, "B")]),
              wall_tags=[(36, 14.0, "W1"), (58, 14.0, "W1"), (80, 14.0, "W1"), (47, 0.3, "E1"), (91, 27.7, "E1")],
              group_rects=([((23, 16.5, 13, 3), "BS"), ((19, 0, 4, 28), "BS"), ((12, 8, 7, 4), "BS"), ((12, 12, 7, 16), "BS"), ((0, 12, 12, 16), "BS")] if level == 2 else []),
              door_edits=([lambda L: [d for d in L if not (d["o"] == "h" and abs(d["a"][1] - 19.5) < .01 and 37 < d["a"][0] < 41)]] if level == 2 else []))
    v = View(s, vc).build()
    v.draw(level, level * 100 + 1)
    title = ("GROUND" if level == 1 else "UPPER") + " FLOOR PLAN — MODEL 2 TOWNHOMES + OWNER SUITE"
    sub = "SCALE: 1/4\" = 1'-0\"   PLAN ROTATED: NORTH TO THE RIGHT, STREET TO THE LEFT"
    SL.drawing_title(s, 1.35, 11.35, "1", f"A-10{level}.2", title, sub, w=24.0)
    SL.north_arrow(s, 30.6, 11.5, angle=0)
    extra = ([
        "Unit A is an ICC A117.1-2009 Type A unit (zero-step entry from the side walk, roll-in shower, 5'-0\" turning circles). Townhomes B, C and D are multistory units in a building without an elevator and are not covered by Fair Housing Act Type B requirements.",
        "Townhome entry doors open to the exterior side walk and need no fire rating. Stairs inside a dwelling unit: 7¾\" max. risers, 10\" min. treads, handrail one side (IBC 1011.5.2 exc. 3, 1014.8).",
    ] if level == 1 else [
        "Unit B's suite over Unit A sits on the F1 1-hour floor/ceiling (G-005); the W1 walls between townhomes continue full height.",
        "Stairs inside a dwelling unit: 7¾\" max. risers, 10\" min. treads, handrail one side, 36\" min. clear width (IBC 1011.5.2 exc. 3).",
    ])
    cfg = dict(sheet_no=f"A-10{level}.2", file=f"Model2_{'Ground' if level == 1 else 'Upper'}_Floor_Plan",
               sheet_title=("GROUND" if level == 1 else "UPPER") + " FLOOR\nPLAN", model_line="MODEL 2 — TOWNHOMES + SUITE",
               lot_line="LOT: ±66' x 152' DEEP (ASSUMED)", projno="SF-M2", date=DATE, notes=common_notes(2, level, extra))
    dd = (["Plan is drawn from concept rev 1.4 as-is; the townhome entries are on the east side walk, the patios on the west.",
           "OPEN — Model 2 lot size is still an assumption (66' x 152'). Confirm before the civil and structural sheets are redrawn.",
           "OPEN — Fire riser closet and FDC location are not yet drawn for Model 2 (Scottsdale Fire to confirm)."] if level == 1 else
          ["Upper floors stack bedrooms over living spaces inside each townhome; Unit B's suite over Unit A is the only unit-over-unit floor.",
           "OPEN — Confirm Unit B suite kitchenette scope (cooking appliance or not) with zoning: a second full kitchen can read as a fifth dwelling."])
    area = ([("UNIT A (FLAT, TYPE A)", "2 BR / 2 BA", "TYPE A", "1,008"), ("UNIT B (OWNER) — GROUND", "—", "—", "616"),
             ("UNIT C — GROUND", "—", "—", "616"), ("UNIT D — GROUND", "—", "—", "616"), ("TOTAL THIS LEVEL", "", "", "2,856")]
            if level == 1 else
            [("UNIT B (OWNER) — UPPER + SUITE", "5 BR / 3.5 BA TOTAL", "—", "1,624"), ("UNIT C — UPPER", "3 BR / 2.5 BA TOTAL", "—", "616"),
             ("UNIT D — UPPER", "3 BR / 2.5 BA TOTAL", "—", "616"), ("TOTAL THIS LEVEL", "", "", "2,856")])
    cols = [(0.9, 10.75, 7.2), (8.6, 10.75, 7.2), (16.3, 10.75, 7.2), (24.0, 10.75, 7.6)]
    # wall tags
    notes_cols(s, cols, cfg, [v], dd, area, "AREA SUMMARY — " + ("GROUND" if level == 1 else "UPPER") + " FLOOR", ["W1", "E1", "P1"])
    save(s, cfg)


# ------------------------------------------------------------------ MODEL 3
def model3(level):
    svg = FP + ("model3-main-ground.svg" if level == 1 else "model3-upper-owner.svg")
    s = Sheet(origin=(3.6, 19.25))
    vc = dict(svg=svg, ppf=12, origin=(70, 60), W=60, D=40, west_type="EXT", type_a_unit="A",
              grids=([(0, "1"), (26, "2"), (34, "3"), (60, "4")], [(0, "A"), (40, "B")]),
              unit_rects=([((26, 0, 8, 40), "K"), ((30, 16.5, 4, 13.5), "C")] if level == 1 else []),
              wall_tags=([(26, 22, "W1"), (34, 22, "W1"), (8, 0.3, "E1"), (59.7, 26, "E1")] if level == 1 else [(8, 0.3, "E1"), (59.7, 26, "E1")]))
    v = View(s, vc).build()
    v.draw(level, level * 100 + 1)
    title = ("GROUND" if level == 1 else "UPPER") + " FLOOR PLAN — MODEL 3 BIG HOUSE (MAIN HOUSE)"
    SL.drawing_title(s, 1.35, 5.55, "1", f"A-10{level}.3", title, "SCALE: 1/4\" = 1'-0\"   CARRIAGE HOUSE AND CASITA: SEE A-111.3", w=15.8)
    SL.north_arrow(s, 18.6, 5.8, angle=90)
    extra = ([
        "Unit A is an ICC A117.1-2009 Type A unit; Unit B is a Type B unit. Maintain clear floor spaces and 5'-0\" turning circles shown dashed.",
        "Unit entry doors off the shared entry, and the door to owner stair STAIR TO C: 20-minute, self-closing, positive-latching, S-label (G-005).",
    ] if level == 1 else [
        "Unit C (owner) occupies the entire upper floor and is reached by its private stair from the shared entry. Floor/ceiling below is the F1 1-hour decoupled assembly (G-005).",
        "Unit C is an upper-floor unit in a building without an elevator and is not covered by Fair Housing Act Type B requirements.",
    ])
    cfg = dict(sheet_no=f"A-10{level}.3", file=f"Model3_Main_{'Ground' if level == 1 else 'Upper'}_Floor_Plan",
               sheet_title=("GROUND" if level == 1 else "UPPER") + " FLOOR\nPLAN — MAIN", model_line="MODEL 3 — BIG HOUSE + CASITA",
               lot_line="LOT: 80' x 125' + REAR ALLEY", projno="SF-M3", date=DATE, notes=common_notes(3, level, extra))
    dd = (["Plan is drawn from concept rev 1.4. Core: chases CH, house storage, private stair to Unit C and the fire riser FR off the shared entry.",
           "OPEN — Several bedroom and bath doors swing into the 4'-0\" halls as drawn in concept; confirm swings on A-401/A-402 (Model 1 swings them into the rooms)."] if level == 1 else
          ["Owner floor: suite (sitting/bed 5) on the west half for multigenerational living; primary suite, bedrooms 2 and 3 and the family room on the east half.",
           "OPEN — Two kitchens in one unit (suite kitchen + main): confirm the suite kitchen stays a kitchenette so the building reads as four dwellings."])
    area = ([("UNIT A (FLAT, TYPE A)", "2 BR / 2 BA", "TYPE A", "1,040"), ("UNIT B (FLAT)", "2 BR / 2 BA", "TYPE B", "1,040"),
             ("CORE + STAIR TO C", "—", "ACCESSIBLE ROUTE", "320"), ("TOTAL THIS LEVEL", "", "", "2,400")]
            if level == 1 else [("UNIT C (OWNER, ENTIRE FLOOR)", "4–5 BR / 3 BA", "—", "±2,300"), ("CHASES", "—", "—", "100"),
                                ("TOTAL THIS LEVEL", "", "", "2,400")])
    cols = [(21.15, 23.2, 5.1), (21.15, None, 5.1), (26.55, 23.2, 5.25), (26.55, None, 5.25)]
    notes_cols(s, cols, cfg, [v], dd, area, "AREA SUMMARY — " + ("GROUND" if level == 1 else "UPPER") + " FLOOR", ["W1", "E1", "P1"] if level == 1 else ["E1", "P1"])
    save(s, cfg)


def ext_stair(v):
    s = v.s
    x0, y0, w, h = 48.833, 4.0, 3.667, 16.0
    s.rect(x0 * F, y0 * F, w * F, h * F, layer="A-FLOR-STRS", lw="l", space="m")
    yy = y0 + 0.4
    while yy < y0 + h - 0.3:
        s.line((x0 * F, yy * F), ((x0 + w) * F, yy * F), layer="A-FLOR-STRS", lw="f", space="m"); yy += 11 / 12
    s.text(((x0 + w / 2) * F, (y0 + h / 2) * F), "EXT. STAIR TO UNIT D", 0.055, layer="A-ANNO-TEXT", space="m", rot=90, valign="m")


def chase_labels(v):
    for q, lab in zip(v.chases_red, ("D1", "D2")):
        v.s.text(((q["x"] + q["w"] / 2) * F, (q["y"] + q["h"] + 0.9) * F), lab, 0.06, layer="A-ANNO-TEXT", space="m", font="Helvetica-Bold", valign="m")


def model3_carriage():
    s = Sheet(origin=(3.4, 22.0))
    tiers = (0.5, 0.85, None)
    g = ([(0, "1"), (24, "2"), (48, "3")], [(0, "A"), (24, "B")])
    v1 = View(s, dict(svg=FP + "model3-carriage-ground.svg", ppf=12, origin=(70, 60), W=48, D=24, west_type="EXT", grids=g, tiers=tiers, grid_off=1.25,
                      unit_rects=[((0, 0, 24, 24), "G1"), ((24, 0, 24, 24), "G2")], pair_type=lambda a, b: "W3" if {a, b} == {"G1", "G2"} else None,
                      extra_draw=[ext_stair, chase_labels])).build()
    v1.draw(1, 151, room_prefix={"G1": "GA", "G2": "GB"})
    SL.drawing_title(s, 1.35, 12.95, "1", "A-111.3", "LEVEL 1 — PRIVATE GARAGES", "SCALE: 1/4\" = 1'-0\"   ALLEY (NORTH) AT TOP", w=13.5)
    s.ox, s.oy = 3.4, 11.15
    v2 = View(s, dict(svg=FP + "model3-casita-l2.svg", ppf=12, origin=(70, 60), W=48, D=24, west_type="EXT", grids=g, tiers=tiers, grid_off=1.25,
                      extra_draw=[ext_stair])).build()
    v2.draw(2, 251)
    SL.drawing_title(s, 1.35, 2.95, "2", "A-111.3", "LEVEL 2 — CASITA, UNIT D", "SCALE: 1/4\" = 1'-0\"", w=13.5)
    s.ox, s.oy = 19.3, 22.0
    v3 = View(s, dict(svg=FP + "model3-casita-loft.svg", ppf=12, origin=(70, 60), shift=(12, 0), W=24, D=24, west_type="EXT",
                      room_edits=[lambda rs: rs + [dict(x=22, y=0, w=2, h=8, fill="#fff", color="#1e5bd8", op=0.03)]],
                      group_rects=[((0, 8, 24, 16), "open")],
                      grids=([], []), tiers=(0.5, 0.85, None))).build()
    v3.draw(3, 351)
    SL.drawing_title(s, 17.8, 14.75, "3", "A-111.3", "LEVEL 3 — LOFT", "SCALE: 1/4\" = 1'-0\"", w=8.0, scalebar=False)
    SL.north_arrow(s, 17.8, 19.5, angle=90)
    cfg = dict(sheet_no="A-111.3", file="Model3_Carriage_House_Plans", sheet_title="CARRIAGE HOUSE\nPLANS", model_line="MODEL 3 — BIG HOUSE + CASITA",
               lot_line="LOT: 80' x 125' + REAR ALLEY", projno="SF-M3", date=DATE,
               notes=[
                   "Do not scale drawings. Exterior dimensions to outside face of exterior wall finish; interior to centerline of partitions, U.N.O.",
                   "Level 1: two private garages (Group U), 576 SF each, separated by W3, a 1-hour fire barrier full height to the rated floor/ceiling above (G-005). Each garage is under 1,000 SF (IBC 406.3).",
                   "Floor/ceiling between the garages and casita D is the F2 1-hour assembly. Drop chases D1 and D2 are 1-hour shafts on the garage door piers; nothing passes through the W3 wall above the slab.",
                   "Doors between a garage and any dwelling space: self-closing, gasketed, solid-core 1¾\" or 20-minute (IBC 406.3.2). No garage opening into a sleeping room.",
                   "Garage doors 9'-0\" x 8'-0\" insulated steel sectional with openers, facing the alley. Confirm 3'-0\" piers carry chases D1/D2 with the door supplier (fallback 3'-6\" piers with 8'-6\" doors).",
                   "Unit D casita (levels 2 and 3, 4 BR / 3 BA, 1,728 SF) is reached by the exterior stair on the east side. Sprinklered per NFPA 13R; smoke and CO alarms per IFC.",
                   "Bedroom egress: 5.7 SF min. net clear, sill 44\" max. Loft bedroom 4 egresses through the gable-end windows east and west.",
                   "Casita height and story count are a zoning risk (A-3.2): confirm before permit.",
               ])
    # notes: column at right, schedules under the loft
    y = SL.notes_list(s, 26.55, 23.2, "GENERAL NOTES — CARRIAGE HOUSE", cfg["notes"], 5.25)
    y = SL.wall_legend(s, 26.55, y, ["W3", "E1", "P1"], 5.25)
    y = SL.symbols(s, 26.55, y - 0.05, 5.25)
    rows = v1.door_rows + v2.door_rows + v3.door_rows
    yd = SL.door_schedule(s, 17.3, 13.9, rows, 5.25)
    y = SL.window_schedule(s, 17.3, yd, window_rows([v1, v2, v3]), 5.25)
    y = SL.notes_list(s, 26.55, min(y, 6.0) if False else 5.4, "DESIGN-DEVELOPMENT COORDINATION", [
        "Plans drawn from concept rev 1.4 (garage split into two 2-car garages, LOCKED 2026-11-14).",
        "OPEN — Casita story count / height vs. zoning (open mezzanine loft, drop the loft, or a written interpretation).",
        "OPEN — Exterior stair to Unit D: confirm IBC 1027.6 exception for no rated wall behind it.",
    ], 5.25, h=0.068, numbering="alpha")
    save(s, cfg)


for w in which:
    {"A-101.2": lambda: model2(1), "A-102.2": lambda: model2(2), "A-101.3": lambda: model3(1), "A-102.3": lambda: model3(2), "A-111.3": model3_carriage}[w]()
