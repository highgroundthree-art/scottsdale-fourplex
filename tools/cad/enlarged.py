"""A-401 enlarged kitchens, A-402 enlarged baths, A-501 interior elevations (Model 1)."""
from sheetkit import *
from bgplan import enlarged
import sheetlib as SL
from plan_engine import dim_chain


def view(s, lvl, win, at, num, sheet, ttl, sub, notes_xy=None, notes_list=(), dims=None):
    enlarged(s, lvl, win, at, scale=24)
    s.scale = 24
    ox, oy = s.ox, s.oy
    if dims:
        for (vals, base, ori, off) in dims:
            dim_chain(s, [v * 12 for v in vals], base * 12, ori, off)
    s.scale = 48
    w = (win[2] - win[0]) * 0.5
    h = (win[3] - win[1]) * 0.5
    SL.drawing_title(s, at[0] - 0.2, at[1] - h - 0.75, num, sheet, ttl, sub, w=max(5.6, w + 0.4), scalebar=False)
    if notes_list:
        x, y = notes_xy
        for i, t in enumerate(notes_list):
            s.text((x, y - i * 0.19), t, 0.062, align="l")
    s.ox, s.oy = ox, oy


# ===================================================================== A-401
s = new()
view(s, 1, (14.5, 24.5, 25.5, 37.5), (1.6, 22.4), "1", "A-401", "KITCHEN — UNIT A (TYPE A)", "SCALE: 1/2\" = 1'-0\"",
     (1.4, 14.6), ["• 34\" high work surface section 30\" wide, knee space below", "• Sink: removable base cabinet, insulated pipes", "• 60\" turning circle in the kitchen (shown)",
                   "• Range: front controls; side-swing or wall oven option", "• 30x48 clear floor space at each appliance", "• Pull-out shelves, D-pulls; 15\"–48\" reach"],
     dims=[((15, 17.2, 22.6, 24.6, 25), 37.0, "h", -0.45)])
view(s, 1, (34.5, 24.5, 45.5, 37.5), (8.4, 22.4), "2", "A-401", "KITCHEN — UNIT B (TYPE B)", "SCALE: 1/2\" = 1'-0\"",
     (8.2, 14.6), ["• 40\" min. clearance between counters", "• 30x48 parallel approach at sink and range", "• Counters 36\" A.F.F.; uppers 54\" A.F.F.",
                   "• Range hood ducted to the exterior (M-101)", "• Dishwasher left of sink; ref. at the end"],
     dims=[((35, 35.4, 37.4, 42.8, 45), 37.0, "h", -0.45)])
view(s, 2, (14.5, 24.5, 25.5, 37.5), (15.2, 22.4), "3", "A-401", "KITCHEN — UNITS C + D (TYPICAL UPPER)", "SCALE: 1/2\" = 1'-0\"",
     (15.0, 14.6), ["• Same layout as Unit A without the Type A features", "• Blocking in walls for future grab bars and uppers", "• Unit D is the mirror (see A-102.1)"])
notes(s, NC2, TOPY, "KITCHEN NOTES", [
    "Cabinets: plywood box shaker, soft-close, full-extension drawers; quartz or solid-surface counters; 3x12 porcelain backsplash to 18\".",
    "Appliances (all ENERGY STAR where available): 30\" electric/induction range, ducted hood 150 CFM, 24\" dishwasher, 30\" refrigerator, over-range or counter microwave.",
    "Every kitchen has the same finishes and appliances; Unit A adds the accessible features.",
    "Receptacles every 4 ft of counter on two 20A GFCI/AFCI circuits (E-101).",
    "Kitchens sit against the W1 wall: no boxes, pipes or ducts in W1. Sink drains and vents go to chase CH3/CH4 through the floor or base cabinet.",
], 5.25)
save(s, "A-401", "Model1_Enlarged_Kitchen_Plans", "ENLARGED PLANS\nKITCHENS")


# ===================================================================== A-402
s = new()
view(s, 1, (13.5, -0.5, 25.5, 9.0), (1.6, 22.4), "1", "A-402", "ROLL-IN BATH — UNIT A", "SCALE: 1/2\" = 1'-0\"",
     (1.4, 16.4), ["• Roll-in shower 60x36 min., trench drain, no curb", "• Fold-down seat, handheld shower on slide bar", "• Grab bars per D-003; WC 16\"–18\" to CL",
                   "• Lav knee space, offset drain, insulated pipes", "• 60\" turning circle (shown)"])
view(s, 1, (34.5, -0.5, 46.5, 9.0), (8.4, 22.4), "2", "A-402", "PRIMARY BATH — UNIT B (TYPE B)", "SCALE: 1/2\" = 1'-0\"",
     (8.2, 16.4), ["• Tub 60x30 with blocking for grab bars", "• 30x48 clear floor at lav, WC, tub", "• Option A Type B bathroom (A117.1 1004.11.3.1)"])
view(s, 2, (13.5, -0.5, 25.5, 9.0), (15.2, 22.4), "3", "A-402", "PRIMARY BATH — UNITS C + D", "SCALE: 1/2\" = 1'-0\"",
     (15.0, 16.4), ["• Tub stacks over the Unit A shower drain zone; stack S1", "• WC on the west wall, 3\" branch in floor trusses"])
view(s, 1, (16.5, 17.0, 25.5, 25.5), (1.6, 13.4), "4", "A-402", "HALL BATH — UNIT A (TYPICAL ALL UNITS)", "SCALE: 1/2\" = 1'-0\"",
     (1.4, 8.0), ["• Same layout on both floors, all units (mirrored in B, D)", "• Tub/shower with pressure-balance valve", "• Exhaust fan EF-2 with humidity control"])
notes(s, NC2, TOPY, "BATH NOTES", [
    "Wet walls: cement board behind tile at tubs and showers, full height in the roll-in shower; moisture-resistant GWB elsewhere.",
    "Waterproofing: sheet or liquid membrane under the roll-in shower floor and up the walls 6\" min. beyond the wet area; flood test 24 h before tile.",
    "Floor tile DCOF 0.42 wet min.; slope to drains 2% max. in the accessible shower.",
    "Blocking for grab bars at every WC, tub and shower in every unit (A117.1 1004.11.1).",
    "Fixtures per P-001: WaterSense WC 1.28 gpf, lavatories 1.2 gpm, showers 1.8 gpm, pressure-balance valves, anti-scald 120°F max.",
    "Medicine cabinets surface-mounted only on walls other than W1.",
], 5.25)
save(s, "A-402", "Model1_Enlarged_Bath_Plans", "ENLARGED PLANS\nBATHS")


# ===================================================================== A-501
s = new()
K = 0.5 / 12   # 1/2" = 1'-0", paper inches per model inch


def elev_frame(x0, y0, w_in, h_in=108):
    s.rect(x0, y0, w_in * K, h_in * K, lw="m")
    s.line((x0 - 0.2, y0), (x0 + w_in * K + 0.2, y0), lw="h")


def cab(x0, y0, x_in, w_in, h_in, z_in, doors=1, label=None, fill=None):
    s.rect(x0 + x_in * K, y0 + z_in * K, w_in * K, h_in * K, lw="l", fill=fill)
    for i in range(1, doors):
        s.line((x0 + (x_in + w_in * i / doors) * K, y0 + z_in * K), (x0 + (x_in + w_in * i / doors) * K, y0 + (z_in + h_in) * K), lw="xf")
    if label:
        s.text((x0 + (x_in + w_in / 2) * K, y0 + (z_in + h_in / 2) * K - 0.03), label, 0.055)


def kitchen_elev(x0, y0, accessible):
    W = 120
    elev_frame(x0, y0, W)
    ch = 34 if accessible else 36
    cab(x0, y0, 0, 30, 70, 0, 1, "REF")
    cab(x0, y0, 30, 33, ch - 1.5, 0, 2, "SINK" if not accessible else "KNEE SPACE")
    cab(x0, y0, 63, 24, ch - 1.5, 0, 1, "DW")
    cab(x0, y0, 87, 33, ch - 1.5, 0, 2)
    s.rect(x0 + 30 * K, y0 + (ch - 1.5) * K, 90 * K, 1.5 * K, lw="m", fill=0.6)
    s.rect(x0 + 30 * K, y0 + ch * K, 90 * K, 18 * K, lw="xf", fill=0.95)
    for xx in range(30, 120, 6):
        s.line((x0 + xx * K, y0 + ch * K), (x0 + xx * K, y0 + (ch + 18) * K), lw="xf")
    cab(x0, y0, 30, 33, 30, 54 if not accessible else 48, 2); cab(x0, y0, 87, 33, 30, 54 if not accessible else 48, 2)
    for (z, t) in ((ch, f"{ch}\" COUNTER"), (ch + 18, "BACKSPLASH 18\""), (54 if not accessible else 48, ("54\"" if not accessible else "48\"") + " UPPERS"), (108, "9'-0\" CLG")):
        s.text((x0 + W * K + 0.1, y0 + z * K - 0.03), t, 0.055, align="l")


def bath_elev(x0, y0, rollin):
    W = 132
    elev_frame(x0, y0, W)
    if rollin:
        s.rect(x0 + 72 * K, y0, 60 * K, 84 * K, lw="l", fill=0.95)
        for zz in range(0, 84, 6):
            s.line((x0 + 72 * K, y0 + zz * K), (x0 + 132 * K, y0 + zz * K), lw="xf")
        s.line((x0 + 76 * K, y0 + 34 * K), (x0 + 128 * K, y0 + 34 * K), lw="h")
        s.rect(x0 + 110 * K, y0 + 17 * K, 18 * K, 2 * K, lw="m", fill=0.3)
        s.line((x0 + 100 * K, y0 + 40 * K), (x0 + 100 * K, y0 + 64 * K), lw="m")
        s.text((x0 + 102 * K, y0 + 66 * K), "HANDHELD ON SLIDE BAR", 0.05, align="l")
        s.text((x0 + 100 * K, y0 + 30 * K), "GRAB BAR 33\"–36\"", 0.05)
        s.text((x0 + 119 * K, y0 + 13 * K), "SEAT 17\"–19\"", 0.05)
        cab(x0, y0, 10, 30, 6, 28, 1); s.text((x0 + 25 * K, y0 + 20 * K), "LAV 34\" MAX. RIM, KNEE SPACE", 0.05)
        s.rect(x0 + 12 * K, y0 + 40 * K, 26 * K, 30 * K, lw="l")
        s.text((x0 + 25 * K, y0 + 72 * K), "MIRROR, BOTTOM 40\" MAX.", 0.05)
    else:
        s.rect(x0 + 72 * K, y0, 60 * K, 20 * K, lw="m", fill=0.95)
        s.rect(x0 + 72 * K, y0 + 20 * K, 60 * K, 64 * K, lw="l", fill=0.97)
        for zz in range(20, 84, 6):
            s.line((x0 + 72 * K, y0 + zz * K), (x0 + 132 * K, y0 + zz * K), lw="xf")
        s.text((x0 + 102 * K, y0 + 10 * K), "TUB", 0.06)
        s.text((x0 + 102 * K, y0 + 50 * K), "TILE TO 84\"; BLOCKING FOR GRAB BARS", 0.05)
        cab(x0, y0, 6, 36, 32, 0, 2, "VANITY")
        s.rect(x0 + 10 * K, y0 + 42 * K, 28 * K, 30 * K, lw="l")
    for (z, t) in ((84, "TILE 84\""), (108, "9'-0\" CLG")):
        s.text((x0 + W * K + 0.1, y0 + z * K - 0.03), t, 0.055, align="l")


kitchen_elev(1.6, 17.2, True)
SL.drawing_title(s, 1.4, 16.2, "1", "A-501", "KITCHEN ELEVATION — UNIT A (TYPE A)", "SCALE: 1/2\" = 1'-0\"   SINK WALL", w=6.0, scalebar=False)
kitchen_elev(9.2, 17.2, False)
SL.drawing_title(s, 9.0, 16.2, "2", "A-501", "KITCHEN ELEVATION — UNITS B, C, D", "SCALE: 1/2\" = 1'-0\"   SINK WALL", w=6.0, scalebar=False)
bath_elev(1.6, 8.6, True)
SL.drawing_title(s, 1.4, 7.6, "3", "A-501", "ROLL-IN BATH ELEVATION — UNIT A", "SCALE: 1/2\" = 1'-0\"", w=6.0, scalebar=False)
bath_elev(9.2, 8.6, False)
SL.drawing_title(s, 9.0, 7.6, "4", "A-501", "BATH ELEVATION — TYPICAL", "SCALE: 1/2\" = 1'-0\"", w=6.0, scalebar=False)
notes(s, NC, TOPY, "INTERIOR ELEVATION NOTES", [
    "Mounting heights shown are to the top of the counter or the centerline of the item unless noted.",
    "Unit A (Type A): 34\" work surface and sink, uppers lowered to 48\", knee spaces with removable base and finished floor and walls behind.",
    "Units B, C, D: 36\" counters, 54\" upper cabinets, blocking for future lowered work surface not required (Type B / not covered).",
    "Tile per A-602. Grab-bar blocking 2x10 at 33\"–36\" A.F.F. at every WC, tub and shower in every unit.",
    "Mirrors: bottom edge 40\" max. A.F.F. at accessible lavatories.",
    "Coordinate receptacle and switch heights with E-101/E-102; accessible controls 15\"–48\".",
], 10.6)
save(s, "A-501", "Model1_Interior_Elevations", "INTERIOR\nELEVATIONS")
