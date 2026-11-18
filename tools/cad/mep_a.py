"""X-101 MEP coordination, P-101.1 waste and vent, P-102.1 water, FP-101 sprinkler layout (Model 1, both floors at 3/16")."""
import math
from sheetkit import *
from mep_fix import *


def fix_marks(d, lvl, which):
    for u in UNITS[lvl]:
        for (t, x, y, st, dfu, c, h) in FIX[lvl][u]:
            d.C(x, y, 0.28, "l", fill=1.0)


def stacks(d, label=True):
    for k, (x, y) in STACKS.items():
        d.C(x, y, 0.45, "m", fill=0.0)
        if label:
            d.T(x, y - 0.9, k, 0.06, font="Helvetica-Bold")


# ------------------------------------------------------------------ P-101.1 waste and vent
def ww(lvl):
    def fn(d, p):
        d.color = GREEN; d.layer = "P-SANR"
        below = lvl == 1
        for u in UNITS[lvl]:
            for (t, x, y, st, dfu, c, h) in FIX[lvl][u]:
                sx, sy = STACKS[st]
                pts = [(x, y), (x, sy if abs(y - sy) > 0.5 else y), (sx, sy)] if t != "DW" else [(x, y), (x - 0.0, y)]
                if t == "DW":
                    continue
                d.PL([(x, y), (x, sy), (sx, sy)] if abs(x - sx) > abs(y - sy) else [(x, y), (sx, y), (sx, sy)], "l", [4, 2] if below else None)
                d.C(x, y, 0.3, "l", fill=1.0)
                d.T(x, y + 0.95 if y < 45 else y - 0.6, f"{t} {3 if t == 'WC' else 2}\"", 0.045)
        stacks(d)
        if below:
            # building drain under slab
            d.PL([STACKS["S1"], (26.5, 44.0), (33.5, 44.0)], "m", [6, 2]); d.PL([STACKS["S2"], (33.5, 44.0)], "m", [6, 2])
            d.PL([(33.5, 44.0), (33.5, 51.5)], "m", [6, 2])
            for (x, y) in ((26.5, 6.0), (33.5, 6.0), (26.5, 23.2), (33.5, 23.2)):
                d.R(x - 0.35, y - 0.35, 0.7, 0.7, "l", fill=1.0); d.T(x + 1.2, y + 0.2, "CO", 0.05)
            d.R(33.15, 51.0, 0.7, 0.7, "l", fill=0.0)
            d.T(36.0, 53.0, "4\" BUILDING SEWER @ 1/4\":12\" TO STREET, 2-WAY CO AT WALL (C-103)", 0.055, align="l")
            d.T(29.6, 43.2, "4\" BUILDING DRAIN BELOW SLAB", 0.05)
            for (u, (x, y)) in (("A", WH["A"]), ("B", WH["B"])):
                d.T(x + (2.6 if x < 30 else -2.6), y + 1.6, "WH PAN + T&P TO EXTERIOR", 0.045)
        else:
            d.T(30, 12.5, "STACKS CONTINUE TO VTR (A-103.1)", 0.05)
            for (u, (x, y)) in (("C", WH["C"]), ("D", WH["D"])):
                d.T(x + (2.6 if x < 30 else -2.6), y + 1.6, "WH PAN + T&P TO EXTERIOR", 0.045)
    return fn


s = new()
two_level(s, ww(1), ww(2), "P-101.1", "WASTE AND VENT PLAN")
dfu = {}
for lvl in (1, 2):
    for u in UNITS[lvl]:
        dfu[u] = sum(f[4] for f in FIX[lvl][u])
rows = [(u, "2 BR / 2 BA" if u == "A" else "3 BR / 2 BA", "9", str(dfu[u]), "S1 + S3" if u in "AC" else "S2 + S4") for u in "ABCD"]
rows.append(("TOTAL", "", "36", str(sum(dfu.values())), "4\" bldg drain"))
y = tbl(s, 15.3, TOPY, "DRAINAGE FIXTURE UNITS (IPC TABLE 709.1)", [("UNIT", 0.6, "c"), ("TYPE", 1.3, "l"), ("FIX.", 0.5, "c"), ("DFU", 0.6, "c"), ("STACKS", 2.5, "l")], rows)
y = tbl(s, 15.3, y, "STACK SCHEDULE", [("STACK", 0.6, "c"), ("SERVES", 2.2, "l"), ("SIZE", 0.9, "c"), ("VENT", 1.8, "l")], [
    ("S1", "A + C bath, laundry", "3\" / 4\" base", "3\" VTR, 12\" above roof"), ("S2", "B + D bath, laundry", "3\" / 4\" base", "3\" VTR"),
    ("S3", "A + C hall bath, kitchen", "3\" / 4\" base", "3\" VTR"), ("S4", "B + D hall bath, kitchen", "3\" / 4\" base", "3\" VTR")])
notes(s, 15.3, y, "LEGEND", ["Green dashed: waste below slab (ground floor). Green solid: waste in the floor-truss space (upper floor).",
                             "Black dot: stack in chase. Square: cleanout. Circle: fixture drain."], 5.5)
notes(s, NC, TOPY, "WASTE AND VENT NOTES", [
    "Design intent. The plumbing engineer or licensed plumbing contractor sizes and routes all piping per the 2021 IPC with Scottsdale amendments; this sheet sets the stack and chase strategy.",
    "PVC or ABS Schedule 40 DWV below slab and in chases; cast iron in chases is an approved alternate for quieter stacks (recommended: dignity / sound standard).",
    "Every stack runs in a chase (CH1–CH4) in the core, never inside a W1 wall. Branch penetrations through W1 into a chase use a listed firestop system plus acoustic isolation (D-002/5).",
    "Upper-floor branches run in the open-web floor trusses above the F1 rated ceiling; no piping attached to the independent ceiling joists.",
    "Wet rooms stack: upper baths, laundries and kitchens sit over the same rooms below, so each stack has short branches on both floors.",
    "Slopes: 1/4\" per foot for 3\" and smaller, 1/8\" per foot min. for 4\" building drain where needed. Cleanouts at the base of every stack, at each change of direction over 45°, and at the building exit.",
    "Vents: one 3\" vent through the roof per stack, 12\" min. above the roof, 10 ft from or 3 ft above any opening or air intake. No air admittance valves.",
    "Water heater relief and pan drains discharge to the exterior at 6\"–24\" above grade, visible, per IPC 504.6.",
    "Sleeves for all below-slab piping through the PT slab beams set before the pour (S-101). No cutting after stressing.",
], 5.1)
notes(s, NC2, TOPY, "ACCESSIBILITY (UNIT A)", [
    "Roll-in shower drain: trench or linear drain, slope 2% max.; no curb (A117.1 1003.11).",
    "Lavatories in Unit A: offset drains and insulated or covered pipes below (A117.1 606.5).",
    "Kitchen sink in Unit A: removable base cabinet for knee clearance; protect pipes.",
], 5.25)
save(s, "P-101.1", "Model1_Waste_and_Vent_Plan", "WASTE AND VENT\nPLAN")


# ------------------------------------------------------------------ P-102.1 water
def wat(lvl):
    def fn(d, p):
        d.layer = "P-DOMW"
        for u in UNITS[lvl]:
            west = u in "AC"
            whx, why = WH[u]
            sgn = 1 if west else -1
            # unit service from the core to the WH closet, along the hall
            d.color = BLUE
            d.PL([(25 if west else 35, 15.0), (whx, 15.0)], "m")
            d.T((25 + whx) / 2 if west else (35 + whx) / 2, 14.4, "1\" CW TO UNIT " + u, 0.05)
            # cold + hot trunks
            for (t, x, y, st, dfu, c, h) in FIX[lvl][u]:
                if c:
                    d.color = BLUE; d.PL([(whx + 0.6 * sgn, 15.3), (x - 0.15, 15.3), (x - 0.15, y)], "xf")
                if h:
                    d.color = RED; d.PL([(whx + 0.6 * sgn, 15.7), (x + 0.15, 15.7), (x + 0.15, y)], "xf", [4, 2])
                d.color = None; d.C(x, y, 0.25, "l", fill=1.0)
            d.color = None
            d.R(whx - 1.0, why - 1.0, 2.0, 2.0, "m", fill=0.9); d.T(whx, why + 0.2, "WH-" + u, 0.05, font="Helvetica-Bold")
            d.T(whx + 3.2 * sgn, why + 2.6, "PEX MANIFOLD + SHUTOFF", 0.045)
        d.color = BLUE
        d.PL([(33.4, 48.0), (33.4, 46.5), (30.0, 46.5), (30.0, 15.0), (25, 15.0)], "m")
        d.PL([(30.0, 15.0), (35, 15.0)], "m")
        d.color = None
        if lvl == 1:
            d.R(RISER_RM[0], RISER_RM[1], RISER_RM[2], RISER_RM[3], "m", fill=0.85)
            d.T(33.4, 49.2, "RISER 103", 0.05, font="Helvetica-Bold")
            d.T(30.4, 39.0, "1-1/2\" CW MAIN IN CORE CEILING", 0.05, rot=90)
            d.T(36.5, 53.0, "1-1/2\" WATER SERVICE FROM METER AT STREET (C-103); PRV + 4 UNIT SUBMETERS IN 103", 0.055, align="l")
        else:
            d.T(30.4, 39.0, "1\" CW UP IN CORE TO UNITS C + D", 0.05, rot=90)
    return fn


s = new()
two_level(s, wat(1), wat(2), "P-102.1", "DOMESTIC WATER PLAN")
y = tbl(s, 15.3, TOPY, "WATER SUPPLY FIXTURE UNITS (IPC E103.3)", [("UNIT", 0.6, "c"), ("WSFU", 0.8, "c"), ("GPM", 0.8, "c"), ("BRANCH", 1.2, "c"), ("WH", 2.1, "l")], [
    ("A", "12.0", "11", "1\"", "WH-A 50 GAL HPWH"), ("B", "12.0", "11", "1\"", "WH-B 50 GAL HPWH"), ("C", "12.0", "11", "1\"", "WH-C 50 GAL HPWH"),
    ("D", "12.0", "11", "1\"", "WH-D 50 GAL HPWH"), ("BLDG", "48.0", "26", "1-1/2\"", "Service + PRV at 103")])
y = tbl(s, 15.3, y, "WATER HEATER SCHEDULE", [("MARK", 0.6, "c"), ("TYPE", 2.3, "l"), ("CAP.", 0.7, "c"), ("ELEC.", 0.9, "c"), ("UEF", 0.6, "c")], [
    ("WH-A–D", "Heat pump water heater, 240 V", "50 GAL", "30 A / 2P", "3.3+")])
notes(s, 15.3, y, "LEGEND", ["Blue: cold water. Red dashed: hot water. Square: water heater with drain pan."], 5.5)
notes(s, NC, TOPY, "DOMESTIC WATER NOTES", [
    "Design intent. Final sizing by the plumbing engineer or licensed contractor per the 2021 IPC and Scottsdale amendments.",
    "One City of Scottsdale water meter at the street (size per the utility, 1-1/2\" assumed). Pressure-reducing valve in riser room 103 if street pressure exceeds 80 psi; expansion tank at each water heater.",
    "Four unit submeters with isolation valves in room 103 so each owner or tenant pays for their own water (Arizona submetering rules, confirm).",
    "PEX-A home-run manifold in each water-heater closet with a labeled shutoff for every fixture. Quarter-turn main shutoff inside each unit.",
    "Heat pump water heaters in the closets: louvered bi-fold doors (type F) provide the air volume; condensate to a floor drain or the exterior.",
    "Hot water to every fixture within 50 ft of pipe (IECC R403.5.1); insulate hot lines R-3.",
    "Hose bibs: one frost-free bib at each rear patio and one at the front, on the house panel water line (common area).",
    "Gas: the base design is all-electric. A gas option is shown on P-202 only as an alternate.",
], 5.1)
save(s, "P-102.1", "Model1_Domestic_Water_Plan", "DOMESTIC WATER\nPLAN")


# ------------------------------------------------------------------ X-101 coordination
def xco(lvl):
    def fn(d, p):
        # W1 no-fly bands
        for x in (25, 35):
            d.R(x - 0.5, 0, 1.0, 50, "f", fill=None, color=RED, dash=[3, 2])
        d.color = RED
        d.T(25, -0.8, "W1: NO PIPES / DUCTS / BOXES", 0.045); d.T(35, -0.8, "W1", 0.045)
        d.color = None
        for k, (x, y, w, h) in CHASES.items():
            d.R(x, y, w, h, "m", fill=0.8)
            d.T(x + w / 2, y + h / 2 + 0.2, k, 0.05, font="Helvetica-Bold")
        stacks(d, False)
        for u in UNITS[lvl]:
            ax, ay = AHU[u]
            d.color = ORANGE
            d.R(ax - 2.5, ay - 1.4, 5.0, 2.8, "m", fill=1.0); d.T(ax, ay + 0.2, "AHU-" + u, 0.05, font="Helvetica-Bold")
            west = u in "AC"
            # supply trunk
            d.PL([(ax + (2.5 if west else -2.5), ay), (22.5 if west else 37.5, ay)], "h")
            d.PL([(ax, ay + 1.4), (ax, 40.0)], "h")
            d.color = BLUE
            px, py = PANEL[u]
            d.R(px - 0.8, py - 0.3, 1.6, 0.4, "m", fill=0.0); d.T(px, py + 0.9, "PNL " + u, 0.05, font="Helvetica-Bold")
            d.color = None
            wx, wy = WH[u]
            d.R(wx - 1, wy - 1, 2, 2, "l", fill=0.9); d.T(wx, wy + 0.2, "WH", 0.045)
        if lvl == 1:
            x, y, w, h = MC1
            d.color = BLUE; d.R(x, y, w, h, "m", fill=0.3); d.T(x + w / 2, y - 0.6, "MC-1", 0.05, font="Helvetica-Bold")
            d.PL([(33.5, 0), (33.5, 8.5)], "m", [5, 2]); d.T(36.2, 7.0, "FEEDERS IN CH2", 0.045, align="l")
            d.color = None
            for u, (x, y) in CU.items():
                d.R(x - 1.3, y - 1.3, 2.6, 2.6, "l"); d.T(x, y + 0.2, "CU-" + u, 0.045)
            d.R(RISER_RM[0], RISER_RM[1], RISER_RM[2], RISER_RM[3], "m", fill=0.85); d.T(33.4, 49.2, "FP RISER", 0.045)
    return fn


s = new()
two_level(s, xco(1), xco(2), "X-101", "MEP COORDINATION PLAN")
notes(s, 15.3, TOPY, "COORDINATION RULES", [
    "W1 unit separation walls (red bands) carry NO pipes, ducts, boxes or recessed items. Systems cross the core only inside chases CH1–CH4.",
    "Plumbing stacks: CH1–CH4 only. Electrical feeders from MC-1: CH2, then above the core ceiling to each panel.",
    "Ground units (A, B): ducts and pipes run in the open-web floor-truss space above the F1 rated ceiling. Every ceiling register and grille gets a listed ceiling radiation damper. No recessed cans.",
    "Upper units (C, D): AHUs and ducts in the attic over each unit, ducts R-8, sealed and tested. No ducts cross the W1 draftstop.",
    "Floor-truss order: the truss maker gets this plan so duct chases (14\" x 8\" max.) align with the open webs before fabrication.",
    "Condensers at grade on the north yard; line sets in the exterior wall chase beside each pad, sealed at the envelope.",
    "Sprinkler mains run in the core ceiling from riser room 103; branch lines into each unit through W1 with listed firestop (FP-101).",
], 5.6)
notes(s, NC, TOPY, "CLASH CHECKS DONE ON THIS SET", [
    "Kitchens back up to W1: sinks and ranges vent and drain to CH3/CH4, not into W1. Range hoods exhaust to the exterior east or west wall (M-101).",
    "Primary bath stacks S1/S2 serve the bath and laundry above and below; WC in Unit C moved to the west bath wall, branch 3\" in the floor trusses.",
    "Stair: no plumbing or ducts under the stair or in the enclosed space below the landing (IBC 1011.7.3).",
    "MC-1 working space 3'-0\" deep x 30\" wide x 6'-6\" high kept clear of condensers and downspouts.",
    "Open item: confirm the mid-unit bearing line on S-102 does not cross the AHU and duct trunk in the hall; trunk shown parallel to it.",
], 5.1)
save(s, "X-101", "Model1_MEP_Coordination_Plan", "MEP COORDINATION\nPLAN")


# ------------------------------------------------------------------ FP-101 sprinkler layout
def heads_for(rooms, mirror_east):
    pts = []
    for (x, y, w, h, n) in rooms:
        if w * h < 24:
            continue
        nx, ny = max(1, math.ceil(w / 14)), max(1, math.ceil(h / 14))
        for i in range(nx):
            for j in range(ny):
                px, py = x + w * (i + 0.5) / nx, y + h * (j + 0.5) / ny
                pts.append((px, py))
                if mirror_east:
                    pts.append((60 - px, py))
    return pts


def fp(lvl):
    def fn(d, p):
        d.layer = "F-SPRN"
        hs = heads_for(ROOMS_W, True)
        hs += [(30, 30), (30, 42), (30, 15)] if lvl == 1 else [(30, 30), (30, 42)]
        for (x, y) in hs:
            d.C(x, y, 0.35, "l", fill=1.0); d.L((x - 0.35, y), (x + 0.35, y), "xf"); d.L((x, y - 0.35), (x, y + 0.35), "xf")
        d.color = RED
        d.PL([(33.4, 48.0), (30.0, 46.0), (30.0, 3.0)], "h")
        for yy in (6.75, 15.5, 22.0, 31.5, 43.0):
            d.PL([(30.0, yy), (8.0, yy)], "m"); d.PL([(30.0, yy), (52.0, yy)], "m")
        d.color = None
        if lvl == 1:
            d.R(RISER_RM[0], RISER_RM[1], RISER_RM[2], RISER_RM[3], "m", fill=0.85)
            d.T(33.4, 49.3, "RISER", 0.05, font="Helvetica-Bold")
            d.T(36.5, 53.2, "2\" FIRE SERVICE + BACKFLOW (DCVA) TO RISER 103; FDC AT FRONT PER FIRE MARSHAL", 0.055, align="l")
        d.T(30.6, 10.0, "MAIN IN CORE CEILING", 0.05, rot=90)
    return fn


s = new()
two_level(s, fp(1), fp(2), "FP-101", "FIRE SPRINKLER LAYOUT (DESIGN INTENT)")
notes(s, 15.3, TOPY, "SPRINKLER NOTES", [
    "NFPA 13R system, design and hydraulic calculations by a licensed fire sprinkler contractor (deferred submittal). This sheet sets the intent and the riser location only.",
    "Residential pendant or concealed sprinklers, listed coverage up to 16 x 16 ft; quick response. Heads in every room and closet over 24 SF; baths over 55 SF. Attic protection only if Scottsdale requires it under its amendments (VERIFY).",
    "Mains and branch lines in the core ceiling and the floor-truss space; CPVC listed for the application where allowed, steel in the riser room. No piping inside W1 except listed firestopped crossings.",
    "Riser room 103 with exterior door 102: control valve, waterflow switch, drain, gauges; exterior waterflow bell. Monitoring per Scottsdale.",
    "Ceiling radiation dampers and the F1 rated ceiling must not be compromised: sprinkler heads in F1 ceilings use listed escutcheons.",
], 5.6)
save(s, "FP-101", "Model1_Fire_Sprinkler_Layout", "FIRE SPRINKLER\nLAYOUT")
