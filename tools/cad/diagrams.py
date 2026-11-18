"""E-201 one-line, P-201 DWV + water risers, P-202 gas riser (alternate), Model 1. Paper-space diagrams."""
from sheetkit import *
import sheetlib as SL
from textsheets import Flow

T = lambda s, x, y, t, h=0.085, **k: s.text((x, y), t, h, **k)


def box(s, x, y, w, h, t, sub=None, fill=1.0, lw="m"):
    s.rect(x - w / 2, y - h / 2, w, h, lw=lw, fill=fill)
    T(s, x, y + (0.05 if sub else -0.04), t, 0.085, font="Helvetica-Bold")
    if sub:
        T(s, x, y - 0.17, sub, 0.065)


def brk(s, x, y, t=None):
    s.circle((x, y + 0.12), 0.05, lw="l", fill=1.0); s.circle((x, y - 0.12), 0.05, lw="l", fill=1.0)
    s.arc((x + 0.02, y), 0.14, 100, 260, layer="A-ANNO-SYMB", lw="l")
    if t:
        T(s, x + 0.25, y - 0.03, t, 0.07, align="l")


def meter(s, x, y, t=None):
    s.circle((x, y), 0.22, lw="m", fill=1.0); T(s, x, y - 0.04, "M", 0.1, font="Helvetica-Bold")
    if t:
        T(s, x + 0.35, y - 0.03, t, 0.07, align="l")


# ===================================================================== E-201
s = new()
L = lambda a, b, lw="m", dash=None: s.line(a, b, lw=lw, dash=dash)
box(s, 3.0, 21.2, 2.4, 0.8, "UTILITY TRANSFORMER", "APS / SRP PAD-MOUNT (BY UTILITY)")
L((3.0, 20.8), (3.0, 19.2)); T(s, 3.15, 20.0, "UTILITY SERVICE LATERAL (BY UTILITY)", 0.07, align="l")
s.rect(1.4, 6.0, 14.8, 13.2, lw="h")
T(s, 1.6, 18.9, "MC-1  METER CENTER, 400A, 120/240V 1Ø 3W, NEMA 3R, ON THE NORTH WALL", 0.1, font="Helvetica-Bold", align="l")
T(s, 1.6, 18.65, "22 kAIC (VERIFY AVAILABLE FAULT CURRENT WITH THE UTILITY), SERVICE ENTRANCE RATED", 0.07, align="l")
L((3.0, 19.2), (3.0, 17.6)); brk(s, 3.0, 17.3, "400A MAIN"); L((3.0, 17.0), (3.0, 16.4))
L((2.6, 16.4), (15.4, 16.4), "h")
cols = [(3.6, "A", "125A", "UNIT A"), (6.2, "B", "125A", "UNIT B"), (8.8, "C", "125A", "UNIT C"), (11.4, "D", "125A", "UNIT D"), (14.0, "H", "60A", "HOUSE")]
for (x, u, a, nm) in cols:
    L((x, 16.4), (x, 15.4)); meter(s, x, 15.1); L((x, 14.88), (x, 14.0)); brk(s, x, 13.7, a); L((x, 13.4), (x, 6.0))
    fe = "3 #1/0 AL + #6 CU EGC, 2\" C" if a == "125A" else "3 #6 CU + #10 CU EGC, 1\" C"
    T(s, x - 0.08, 10.2, fe, 0.06, rot=90)
    box(s, x, 4.9, 2.2, 1.2, f"PANEL {u if u != 'H' else 'HP'}", f"{a} MAIN, 42 SP" if u != "H" else "60A MAIN, 24 SP")
    L((x, 6.0), (x, 5.5))
    T(s, x, 3.95, nm + (" — HALL" if u != "H" else " — SHARED ENTRY"), 0.065)
    T(s, x, 3.75, "SURGE PROTECTION (230.67)" if u != "H" else "SITE, ENTRY, EV, BELL", 0.06)
# grounding
L((1.4, 17.0), (0.95, 17.0), "l"); L((0.95, 17.0), (0.95, 8.0), "l")
for k in range(3):
    L((0.75 + k * 0.07, 8.0 - k * 0.07), (1.15 - k * 0.07, 8.0 - k * 0.07), "l")
T(s, 0.9, 12.0, "GEC #4 CU TO CONCRETE-ENCASED ELECTRODE (20 FT #4 REBAR IN PT SLAB EDGE BEAM, 250.52(A)(3)) + WATER PIPE BOND", 0.065, rot=90)
SL.drawing_title(s, 1.35, 2.3, "1", "E-201", "ELECTRICAL ONE-LINE DIAGRAM", "NOT TO SCALE   DESIGN INTENT — ELECTRICAL ENGINEER OF RECORD TO FINALIZE", w=15.0, scalebar=False)
f = Flow(s); f.col = 3
f.notes("ONE-LINE NOTES", [
    "Service: 400A, 120/240V, single-phase, underground. Load calculation on E-301 (NEC 220.84): 85.5 kVA = 356 A.",
    "Dwelling feeders sized per NEC 310.12 (83% rule): 125A → #1/0 AL or #2 CU. Final sizes by the engineer after voltage-drop check (2% feeders).",
    "Meter center by the utility's approved list; meter sockets labeled UNIT A–D and HOUSE, permanently engraved (NEC 230.72, 408.4).",
    "Each unit panel has a 125A main breaker in the unit (one-disconnect per unit for occupant access, NEC 240.24(B)).",
    "Available fault current label at MC-1 (110.24).",
    "EV-ready: four 40A 2P circuits (future) from panel HP or the unit panels; confirm with Scottsdale's EV ordinance at pre-app.",
])
save(s, "E-201", "Model1_One_Line_Diagram", "ONE-LINE\nDIAGRAM")


# ===================================================================== P-201
s = new()
L = lambda a, b, lw="m", dash=None, color=None: s.line(a, b, lw=lw, dash=dash, color=color)


def stack(x, name, fixtures_g, fixtures_u):
    y0, y1, y2, y3 = 6.0, 11.0, 16.0, 19.5     # below slab, ground fl, upper fl, roof
    L((x, y0), (x, y3 + 0.6), "h", color=GREEN)
    T(s, x, y3 + 0.75, f"{name}: 3\" VTR", 0.08, font="Helvetica-Bold")
    L((x - 1.4, y3), (x + 1.4, y3), "l"); T(s, x + 1.5, y3 - 0.03, "ROOF", 0.06, align="l")
    for (yy, t) in ((y1, "GROUND FLOOR"), (y2, "UPPER FLOOR")):
        L((x - 2.6, yy), (x + 2.6, yy), "xf", dash="CENTER"); T(s, x - 2.6, yy + 0.08, t, 0.06, align="l")
    for i, (t, sz) in enumerate(fixtures_g):
        xx = x - 2.2 + i * 1.1
        L((xx, y1 - 0.6), (xx, y0 + 0.6), "l", dash=[4, 2], color=GREEN); L((xx, y0 + 0.6), (x, y0 + 0.4), "l", dash=[4, 2], color=GREEN)
        T(s, xx, y1 - 0.45, t, 0.06, font="Helvetica-Bold"); T(s, xx + 0.05, y1 - 1.6, sz, 0.055, rot=90)
    for i, (t, sz) in enumerate(fixtures_u):
        xx = x - 2.2 + i * 1.1
        L((xx, y2 - 0.6), (xx, y1 + 1.1), "l", color=GREEN); L((xx, y1 + 1.1), (x, y1 + 0.9), "l", color=GREEN)
        L((xx, y2 - 0.6), (xx, y2 + 0.9), "xf", dash=[3, 2], color=GREEN); L((xx, y2 + 0.9), (x, y2 + 1.4), "xf", dash=[3, 2], color=GREEN)
        T(s, xx, y2 - 0.45, t, 0.06, font="Helvetica-Bold")
    s.rect(x - 0.18, y0 + 1.0, 0.36, 0.36, lw="l", fill=1.0); T(s, x + 0.3, y0 + 1.1, "CO", 0.06, align="l")
    L((x, y0), (x + 3.0, y0 - 0.5), "h", color=GREEN)
    T(s, x + 0.2, y0 - 0.55, "4\" TO BLDG DRAIN", 0.06, align="l")


stack(3.6, "S1 (A + C)", [("WC", "3\""), ("SH", "2\""), ("LAV", "1-1/2\""), ("CW", "2\"")], [("TUB", "2\""), ("WC", "3\""), ("LAV", "1-1/2\""), ("CW", "2\"")])
stack(10.2, "S3 (A + C)", [("TUB", "2\""), ("WC", "3\""), ("LAV", "1-1/2\""), ("KS", "2\"")], [("TUB", "2\""), ("WC", "3\""), ("LAV", "1-1/2\""), ("KS", "2\"")])
T(s, 7.0, 4.6, "S2 AND S4 (UNITS B + D) ARE THE SAME, MIRRORED", 0.08, font="Helvetica-Bold")
SL.drawing_title(s, 1.35, 3.3, "1", "P-201", "DWV RISER DIAGRAMS — STACKS S1 AND S3", "NOT TO SCALE   DASHED: BELOW SLAB / VENTS", w=13.0, scalebar=False)
# water riser
x0 = 15.0
L((x0, 7.0), (x0, 8.5), "h", color=BLUE); T(s, x0 + 0.15, 7.2, "1-1/2\" SERVICE FROM CITY METER", 0.065, align="l")
for (yy, t) in ((8.8, "BALL VALVE"), (9.3, "PRV (IF > 80 PSI) + GAUGE"), (9.8, "STRAINER"), (10.3, "HEADER IN ROOM 103")):
    s.rect(x0 - 0.15, yy - 0.12, 0.3, 0.24, lw="l", fill=1.0); T(s, x0 + 0.3, yy - 0.03, t, 0.065, align="l")
    L((x0, yy + 0.12), (x0, yy + 0.38), "h", color=BLUE)
L((x0 - 0.2, 10.6), (x0 + 4.6, 10.6), "h", color=BLUE)
for i, u in enumerate("ABCD"):
    xx = x0 + 0.4 + i * 1.2
    L((xx, 10.6), (xx, 14.6), "m", color=BLUE)
    s.circle((xx, 11.3), 0.16, lw="l", fill=1.0); T(s, xx, 11.26, "SM", 0.05)
    T(s, xx + 0.1, 12.6, f"1\" TO UNIT {u}", 0.06, rot=90)
    box(s, xx, 15.1, 1.0, 0.7, f"WH-{u}", "50 GAL HP")
SL.drawing_title(s, 14.6, 3.3, "2", "P-201", "DOMESTIC WATER RISER", "NOT TO SCALE   SM = UNIT SUBMETER", w=6.2, scalebar=False)
f = Flow(s); f.col = 3
f.notes("RISER NOTES", [
    "Fixture branch sizes: WC 3\", tub/shower 2\", lavatory 1-1/2\", kitchen sink 2\", clothes washer 2\" standpipe with 2\" trap.",
    "Each stack 3\" above the ground floor, 4\" at the base and below slab. Individual or common vents tie into the stack above the highest fixture (IPC Ch. 9).",
    "Upper-floor branches in the open-web floor trusses; isolate pipe from structure with resilient clips (sound).",
    "Unit submeters and isolation valves in room 103; each unit has its own main shutoff at the water heater closet.",
    "Test DWV at 10 ft head of water for 15 minutes; water at 100 psi for 15 minutes.",
])
save(s, "P-201", "Model1_DWV_and_Water_Riser_Diagrams", "DWV + WATER\nRISER DIAGRAMS")


# ===================================================================== P-202
s = new()
L = lambda a, b, lw="m", dash=None, color=None: s.line(a, b, lw=lw, dash=dash, color=color)
T(s, 1.2, 22.4, "GAS ALTERNATE — NOT IN THE BASE DESIGN", 0.18, font="Helvetica-Bold", align="l", color=RED)
T(s, 1.2, 22.0, "Use this sheet only if the owner elects natural gas for ranges, dryers or water heaters. The base design is all-electric (P-102.1, E-301).", 0.09, align="l")
x0 = 3.0
L((x0, 8.0), (x0, 10.0), "h", color=ORANGE); T(s, x0 + 0.15, 8.3, "SERVICE BY SOUTHWEST GAS", 0.065, align="l")
box(s, x0, 10.6, 2.0, 0.8, "METER MANIFOLD", "4 METERS, EAST WALL, 3 FT FROM MC-1")
L((x0 - 0.8, 11.0), (x0 + 6.0, 11.0), "h", color=ORANGE)
for i, u in enumerate("ABCD"):
    xx = x0 + 0.8 + i * 1.4
    L((xx, 11.0), (xx, 17.0), "m", color=ORANGE)
    T(s, xx + 0.1, 13.5, f"3/4\" CSST / BLACK STEEL TO UNIT {u}", 0.06, rot=90)
    box(s, xx, 17.5, 1.2, 0.7, f"UNIT {u}", "RANGE 65 MBH")
SL.drawing_title(s, 1.35, 3.3, "1", "P-202", "GAS RISER DIAGRAM (ALTERNATE)", "NOT TO SCALE", w=13.0, scalebar=False)
f = Flow(s); f.col = 3
f.notes("GAS ALTERNATE NOTES", [
    "Sizing per IFGC Ch. 4 (longest length method) after appliance selection. Pressure 7\" w.c. assumed.",
    "CSST bonded per the manufacturer and NEC 250.104(B); protect where within 3 in. of strike hazards.",
    "Gas water heaters would need combustion air and venting (IFGC Ch. 3 and 5); the closets would need redesign. Recommendation: keep electric heat pump water heaters even if gas ranges are chosen.",
    "Gas appliances require CO alarms in the units (already provided).",
    "Meters 3 ft min. from MC-1 and from any opening; not under the west eave.",
])
save(s, "P-202", "Model1_Gas_Riser_Alternate", "GAS RISER\n(ALTERNATE)")
