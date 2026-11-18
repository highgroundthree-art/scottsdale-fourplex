"""Detail sheets: S-501 foundation/PT, S-502 framing, S-503 truss, M-501 mechanical, D-003 accessibility (Model 1).
Six cells per sheet (3 columns x 2 rows). Each detail is drawn in model INCHES at its own scale, z up."""
import math
from sheetkit import *
import sheetlib as SL

COLX = [1.2, 7.9, 14.6]
ROWY = [13.9, 5.6]        # drawing-title baseline of each row; drawing sits above it
CELL_W, CELL_H = 6.3, 7.4


class Det:
    """Collects primitives in model inches (z up); title() fits them into the left part of the cell."""

    def __init__(self, s, c, r, k):
        self.s, self.k0 = s, k
        self.c, self.r = c, r
        self.ops, self.nts = [], []

    # ---- collection
    def R(self, x, z, w, h, lw="l", fill=None, dash=None):
        self.ops.append(("pl", [(x, z), (x + w, z), (x + w, z + h), (x, z + h)], lw, fill, True, dash))

    def L(self, a, b, lw="l", dash=None):
        self.ops.append(("pl", [a, b], lw, None, False, dash))

    def PL(self, pts, lw="l", fill=None, closed=False, dash=None):
        self.ops.append(("pl", list(pts), lw, fill, closed, dash))

    def X(self, x, z, w, h, fill=0.55):
        self.R(x, z, w, h, "l", fill); self.L((x, z), (x + w, z + h), "xf"); self.L((x, z + h), (x + w, z), "xf")

    def C(self, x, z, r, fill=None):
        self.ops.append(("c", (x, z), r, fill))

    def notes(self, items, dx=None, top=None):
        self.nts += items

    # ---- placement
    def title(self, num, sheet, t, sub):
        xs, zs = [], []
        for op in self.ops:
            if op[0] == "pl":
                xs += [p[0] for p in op[1]]; zs += [p[1] for p in op[1]]
            else:
                xs += [op[1][0] - op[2], op[1][0] + op[2]]; zs += [op[1][1] - op[2], op[1][1] + op[2]]
        for (pt, _) in self.nts:
            xs.append(pt[0]); zs.append(pt[1])
        x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
        aw, ah = 3.5, CELL_H - 1.7
        k = self.k0
        nts_scale = True
        kf = min(aw / max(1e-6, x1 - x0), ah / max(1e-6, z1 - z0))
        if abs(kf - k) / k > 0.02:
            k = min(kf, 3 * k); nts_scale = False
        ox = COLX[self.c] + 0.2 + (aw - (x1 - x0) * k) / 2 - x0 * k
        oz = ROWY[self.r] + 0.75 + (ah - (z1 - z0) * k) / 2 - z0 * k
        P = lambda p: (ox + p[0] * k, oz + p[1] * k)
        for op in self.ops:
            if op[0] == "pl":
                _, pts, lw, fill, closed, dash = op
                self.s.pline([P(p) for p in pts], layer="A-DETL", lw=lw, fill=fill, closed=closed, dash=dash)
            else:
                _, c, r, fill = op
                self.s.circle(P(c), r * k, layer="A-DETL", lw="l", fill=fill)
        tx = COLX[self.c] + 3.95
        n = len(self.nts)
        y = min(ROWY[self.r] + CELL_H - 1.0, oz + z1 * k)
        for (pt, txt) in sorted(self.nts, key=lambda a: -a[0][1]):
            a = P(pt)
            self.s.line(a, (tx - 0.05, y + 0.03), lw="xf")
            self.s.circle(a, 0.015, lw="xf", fill=0.0)
            self.s.text((tx, y), txt, 0.058, align="l")
            y -= 0.22
        SL.drawing_title(self.s, COLX[self.c] - 0.1, ROWY[self.r] - 0.25, num, sheet, t, sub if nts_scale else "NOT TO SCALE", w=6.0, scalebar=False)


def soil(d, x0, x1, z):
    d.L((x0, z), (x1, z), "m")
    for x in range(int(x0) + 2, int(x1), 6):
        d.L((x, z), (x - 3, z - 3), "xf")


# ===================================================================== S-501
s = new()
k = 1 / 8   # 1 1/2" = 1'-0"
d = Det(s, 0, 0, k)
soil(d, -10, 30, -4)
d.R(-10, -4, 30, 4, "m", 0.55); d.R(8, -24, 12, 20, "m", 0.55); d.R(-10, -8, 18, 4, "xf", 0.85)
d.L((-10, -4.3), (8, -4.3), "f", [3, 1.5])
d.C(14, -21, 0.3, 0.0); d.C(17, -21, 0.3, 0.0); d.PL([(-10, -2), (6, -2), (12, -20), (19, -20)], "m", dash=[6, 2])
d.R(19, -21.5, 1.2, 3, "l", 0.2)
d.notes([((0, -2), "4\" SLAB, TENDONS CENTERED"), ((-4, -4.3), "15-MIL VAPOR RETARDER ON 4\" ABC"), ((14, -21), "(2) #4 BOTTOM CONT."),
         ((12, -12), "B1 EDGE BEAM 12\" x 24\""), ((19.6, -20), "LIVE-END ANCHOR, ENCAPSULATED, GROUT POCKET"), ((25, -4), "FINISH GRADE, 18\" MIN. TO BOTTOM")], dx=3.6)
d.title("1", "S-501", "PERIMETER BEAM B1", "1½\" = 1'-0\"")
d = Det(s, 1, 0, k)
soil(d, -16, 22, -4)
d.R(-16, -4, 38, 4, "m", 0.55); d.R(-2, -20, 16, 16, "m", 0.55); d.R(-16, -8, 14, 4, "xf", 0.85); d.R(14, -8, 8, 4, "xf", 0.85)
for x in (1, 6, 11):
    d.C(x, -17, 0.32, 0.0)
d.PL([(-16, -2), (0, -2), (6, -16), (12, -2), (22, -2)], "m", dash=[6, 2])
d.R(-0.5, 0, 6.0, 1.5, "l", 0.6); d.R(6.5, 0, 6.0, 1.5, "l", 0.6)
d.notes([((2.5, 0.7), "W1: TWO 2x6 PLATES, 1\" GAP"), ((6, -10), "B3 BEAM 16\" x 20\" UNDER EVERY W1"), ((11, -17), "(2) #5 BOTTOM CONT."),
         ((6, -16), "EXTRA TENDON DRAPED IN BEAM"), ((-10, -2), "SLAB TENDONS @ 48\" O.C.")], dx=3.6)
d.title("2", "S-501", "INTERIOR BEAM B3 AT W1", "1½\" = 1'-0\"")
d = Det(s, 2, 0, k)
soil(d, -10, 30, -4)
d.R(-10, -4, 30, 4, "m", 0.55); d.R(4, -20, 12, 16, "m", 0.55)
d.C(10, -17, 0.3, 0.0)
d.R(-2, -12, 6, 8, "l", None, [3, 2]); d.C(1, -10, 2.0)
d.notes([((10, -12), "RIB R1 12\" x 20\""), ((1, -10), "DWV SLEEVE THROUGH BEAM, SET BEFORE POUR"), ((1, -4), "NO CORING AFTER STRESSING"),
         ((-6, -2), "SLAB")], dx=3.6)
d.title("3", "S-501", "RIB R1 + PIPE SLEEVE", "1½\" = 1'-0\"")
d = Det(s, 0, 1, k)
soil(d, -14, 36, -4)
d.R(-14, -4, 20, 4, "m", 0.55); d.R(-6, -24, 12, 20, "m", 0.55)
d.R(6.5, -4.5, 26, 4, "m", 0.85); d.R(20, -18, 12, 14, "m", 0.85)
d.L((6.2, -4.5), (6.2, 0), "m"); d.C(10, -2.5, 0.3, 0.0); d.L((0, -2.5), (18, -2.5), "l")
d.notes([((6.2, -1), "1/2\" EXPANSION JOINT + SEALANT"), ((12, -2.5), "#4 DOWEL @ 24\", GREASED ONE END"), ((26, -10), "LOGGIA THICKENED EDGE 12\" x 18\""),
         ((-2, -12), "B1")], dx=3.6)
d.title("4", "S-501", "LOGGIA SLAB AT BUILDING", "1½\" = 1'-0\"")
d = Det(s, 1, 1, 1 / 8)
soil(d, -16, 22, -4)
d.R(-16, -4, 38, 4, "m", 0.55)
d.R(-14, -1.5, 18, 1.5, "l", 0.75)
d.PL([(4, -1.5), (6, -1.5), (6, 0)], "m")
d.R(6, 0, 16, 0.5, "l", 0.9)
d.notes([((-6, -1), "1-1/2\" SLAB RECESS AT DOOR"), ((5, -0.8), "TROWELED SLOPE, SILL PAN OVER"), ((14, 0.2), "INTERIOR FINISH FLUSH"),
         ((-8, -3), "PT SLAB: TENDONS DROP UNDER RECESS")], dx=3.6)
d.title("5", "S-501", "SLAB RECESS AT ACCESSIBLE DOOR", "1½\" = 1'-0\"")
d = Det(s, 2, 1, 1 / 8)
soil(d, -10, 30, -4)
d.R(-10, -4, 30, 4, "m", 0.55); d.R(0, -24, 12, 20, "m", 0.55)
d.R(4, 0, 4, 30, "l", 0.7); d.L((6, -18), (6, 32), "m"); d.R(4.5, 30, 3, 1, "l", 0.3)
d.notes([((6, 25), "HOLD-DOWN / CONT. ROD AT SHEAR WALL END (S-201)"), ((6, -10), "ANCHOR EMBED PER MFR. + ENGINEER"), ((6, 4), "POST / KING STUDS"),
         ((-4, -2), "SLAB EDGE")], dx=3.6)
d.title("6", "S-501", "HOLD-DOWN ANCHOR AT SLAB EDGE", "1½\" = 1'-0\"")
s.text((21.15, 23.2), "FOUNDATION DETAILS — DESIGN INTENT; FINAL BY THE STRUCTURAL / PT ENGINEER", 0.1, font="Helvetica-Bold", align="l")
save(s, "S-501", "Model1_Foundation_Details", "FOUNDATION\n+ PT DETAILS")


# ===================================================================== S-502
s = new()
d = Det(s, 0, 0, 1 / 8)
d.R(-6, 0, 6, 30, "f"); d.R(-6, 30, 6, 3, "l", 0.55)
d.PL([(-8, 31), (30, 43.5)], "m"); d.L((-6, 33), (24, 33), "l"); d.L((0, 33), (0, 35), "l")
d.R(-1.0, 28, 1.0, 9, "l", 0.25)
d.notes([((-0.5, 34), "HURRICANE TIE EVERY TRUSS (H2.5 OR EQ.)"), ((5, 37), "TRUSS, 14\" RAISED HEEL"), ((-3, 31.5), "DOUBLE TOP PLATE"),
         ((-3, 15), "2x6 STUDS @ 16\"")], dx=3.6)
d.title("1", "S-502", "TRUSS TO TOP PLATE", "1½\" = 1'-0\"")
d = Det(s, 1, 0, 1 / 8)
d.R(-6, 0, 6, 20, "f"); d.R(-6, 20, 6, 3, "l", 0.55)
d.R(-6, 23, 1.25, 12, "l", 0.7); d.R(-4.75, 23, 30, 12, "f")
for x in range(0, 24, 8):
    d.L((x - 4, 24.5), (x, 33.5), "xf"); d.L((x, 33.5), (x + 4, 24.5), "xf")
d.R(-6, 35, 31, 0.75, "l", 0.5); d.R(-6, 35.75, 6, 1.5, "l", 0.55); d.R(-6, 37.25, 6, 14, "f")
d.R(-4.75, 17.5, 30, 5.5, "xf")
d.notes([((-5.4, 28), "1-1/4\" LSL RIM BOARD"), ((8, 29), "OPEN-WEB FLOOR TRUSS"), ((8, 35.4), "3/4\" T&G OSB, GLUED + SCREWED"),
         ((8, 20), "INDEPENDENT CEILING JOISTS (F1)"), ((-3, 44), "UPPER WALL, STRAP TO LOWER WALL PER S-201")], dx=3.6)
d.title("2", "S-502", "FLOOR TRUSS AT EXTERIOR WALL", "1½\" = 1'-0\"")
d = Det(s, 2, 0, 1 / 8)
d.R(-14, 0, 6, 32, "f"); d.R(-2, 0, 6, 32, "f")
d.R(-14, 32, 6, 3, "l", 0.55); d.R(-2, 32, 6, 3, "l", 0.55)
d.R(-28, 35, 14, 12, "f"); d.R(4, 35, 14, 12, "f")
d.R(-14.5, 35, 0.5, 12, "l", 0.3); d.R(4, 35, 0.5, 12, "l", 0.3)
d.notes([((-11, 33), "UNIT A/C SIDE BEARS ON ITS OWN STUD ROW"), ((1, 33), "CORE / UNIT B SIDE ON ITS OWN ROW"), ((-5, 20), "1\" AIR GAP: NOTHING BRIDGES"),
         ((-20, 41), "FLOOR TRUSSES DO NOT CROSS W1")], dx=3.6)
d.title("3", "S-502", "FLOOR BEARING AT W1", "1½\" = 1'-0\"")
d = Det(s, 0, 1, 1 / 8)
d.R(-6, 0, 6, 40, "f"); d.R(-6, 40, 6, 3, "l", 0.55)
d.X(-6, 30, 6, 10)
d.R(-6, 0, 1.5, 30, "l", 0.7); d.R(-1.5, 0, 1.5, 30, "l", 0.7)
d.notes([((-3, 35), "HEADER (S-102 / A-601), 4x12 OR LVL"), ((-5.2, 15), "JACK + KING STUDS EACH SIDE"), ((-3, 41), "TOP PLATE")], dx=3.6)
d.title("4", "S-502", "TYPICAL HEADER", "1½\" = 1'-0\"")
d = Det(s, 1, 1, 1 / 8)
d.R(0, 0, 3.5, 40, "l", 0.55); d.R(-2, -1.5, 7.5, 1.5, "l", 0.3); d.R(-1, 40, 5.5, 1.5, "l", 0.3)
d.R(-10, 41.5, 24, 11.875, "f")
d.notes([((1.7, 20), "POST (6x6 OR 3-2x6) TO RIB R1"), ((1.7, -0.8), "POST BASE, STANDOFF"), ((1.7, 40.7), "POST CAP"), ((2, 47), "FB1 FLUSH LVL BEAM")], dx=3.6)
d.title("5", "S-502", "POST AT FLUSH BEAM FB1", "1½\" = 1'-0\"")
d = Det(s, 2, 1, 1 / 8)
d.R(0, 0, 40, 1.5, "l", 0.55)
d.L((0, 6), (40, 6), "l")
for x in (4, 12, 20, 28, 36):
    d.C(x, 0.75, 0.25, 0.0)
d.notes([((4, 0.75), "EDGE NAIL PER S-201 SCHEDULE"), ((20, 6), "OSB SHEATHING, BLOCKED AT ALL EDGES"), ((36, 0.75), "ANCHOR BOLT 5/8\" + 3x3 PLATE WASHER")], dx=3.6)
d.title("6", "S-502", "SHEAR WALL NAILING (TYP.)", "1½\" = 1'-0\"")
s.text((21.15, 23.2), "FRAMING DETAILS — DESIGN INTENT; FINAL BY THE STRUCTURAL ENGINEER", 0.1, font="Helvetica-Bold", align="l")
save(s, "S-502", "Model1_Framing_Details", "FRAMING\nDETAILS")


# ===================================================================== S-503
s = new()
for i, (nm, span, kind) in enumerate([("T1 COMMON", 600, "common"), ("T2 STEP-DOWN HIP", 600, "hip"), ("FT1 FLOOR TRUSS", 150, "floor")]):
    kk = 5.6 / span
    d = Det(s, i, 0, kk)
    if kind == "floor":
        d.R(0, 0, span, 11.875, "l"); d.L((0, 1.5), (span, 1.5), "f"); d.L((0, 10.375), (span, 10.375), "f")
        for x in range(0, span - 12, 12):
            d.L((x, 1.5), (x + 12, 10.375), "xf")
        d.notes([((span / 2, 11.875), "11-7/8\" OPEN-WEB @ 24\" O.C."), ((span / 2, 0), "BOTTOM CHORD: NOTHING ATTACHED"), ((5, 6), "STRONGBACK AT MID-SPAN")], dx=0.4, top=ROWY[0] + 3.8)
    else:
        rise = span / 2 * 4 / 12
        top = rise if kind == "common" else rise * 0.6
        pts = [(0, 14), (span / 2 - (0 if kind == "common" else 120), top + 14), (span / 2 + (0 if kind == "common" else 120), top + 14), (span, 14)]
        d.PL(pts, "m"); d.L((0, 0), (span, 0), "m"); d.L((0, 0), (0, 14), "m"); d.L((span, 0), (span, 14), "m")
        for x in range(60, span, 60):
            zt = 14 + min(top, rise * (1 - abs(x - span / 2) / (span / 2)) if kind == "common" else top)
            d.L((x, 0), (x, min(zt, 14 + rise * (1 - abs(x - span / 2) / (span / 2)))), "xf")
        d.notes([((span / 2, top + 14), "4:12, 14\" RAISED HEEL"), ((span / 2, 0), "50'-0\" SPAN, BEARING EXT. WALLS"), ((5, 7), "HEEL")], dx=0.4, top=ROWY[0] + 3.8)
    d.title(str(i + 1), "S-503", nm, "NOT TO SCALE")
y = tbl(s, 1.2, 8.6, "TRUSS DESIGN REQUIREMENTS (FOR THE TRUSS DESIGNER)", [("ITEM", 3.0, "l"), ("REQUIREMENT", 16.0, "l")], [
    ("Code / standard", "2021 IBC, ANSI/TPI 1, ASCE 7 loads as on S-001; sealed truss design drawings by an Arizona-registered engineer"),
    ("Roof loads", "TCDL 27 psf (clay tile), TCLL 20 psf, BCDL 10 psf; attic storage none; wind 115 mph exp. C uplift to each bearing"),
    ("Floor loads", "TCDL 15 psf + 10 psf topping/mat, TCLL 40 psf (100 psf at core landing), BCDL 0 (independent ceiling joists)"),
    ("Deflection", "Floor L/480 live, L/360 total; roof L/240 total; no camber reversal at tile"),
    ("Heel", "14\" min. at the outside face of wall for full R-38 + baffle"),
    ("W1", "No member crosses a W1 wall; trusses and girders split at each W1 (draftstop D-002/4)"),
    ("Ducts", "Floor trusses with duct chase panels aligned to X-101 duct routes before fabrication"),
    ("Bracing", "Permanent lateral and diagonal bracing on the truss drawings; BCSI-B1 / B3 for temporary and permanent bracing"),
], w=19.4, h=0.08, rowh=0.22)
save(s, "S-503", "Model1_Truss_Details", "TRUSS\nDETAILS")


# ===================================================================== M-501
s = new()
d = Det(s, 0, 0, 1 / 12)
d.R(0, 0, 60, 30, "m", 1.0); d.R(60, 8, 12, 14, "l"); d.R(-12, 8, 12, 14, "l")
d.R(0, -6, 60, 4, "l", 0.85); d.L((60, -4), (66, -4), "l"); d.R(64, -6, 4, 4, "l")
d.notes([((30, 15), "HORIZONTAL AHU, VARIABLE SPEED"), ((30, -4), "SECONDARY PAN + FLOAT SWITCH"), ((66, -4), "CONDENSATE TO STANDPIPE (TRAPPED)"),
         ((66, 15), "SUPPLY PLENUM, LINED"), ((-6, 15), "RETURN + MERV 8 FILTER")], dx=3.3)
d.title("1", "M-501", "AHU IN HALL SOFFIT (A, B)", "1\" = 1'-0\"")
d = Det(s, 1, 0, 1 / 6)
d.R(0, 0, 28, 1.25, "l", 0.82); d.R(10, 1.25, 8, 10, "l"); d.R(9, -0.5, 10, 0.5, "l", 0.3)
d.L((10, 6), (18, 6), "f", [3, 2])
d.notes([((14, -0.25), "REGISTER"), ((14, 6), "LISTED CEILING RADIATION DAMPER (UL 555C)"), ((2, 0.6), "F1 RATED CEILING, 2 LAYERS 5/8\" X"),
         ((14, 10), "DUCT IN FLOOR-TRUSS SPACE")], dx=3.3)
d.title("2", "M-501", "REGISTER IN F1 RATED CEILING", "2\" = 1'-0\"")
d = Det(s, 2, 0, 1 / 6)
d.R(0, 0, 7.25, 30, "f"); d.C(14, 15, 3.0); d.L((-6, 15), (11, 15), "m"); d.L((-6, 17), (11, 17), "m")
d.R(11, 12, 4, 6, "l", 0.8)
d.notes([((13, 15), "WALL CAP WITH BACKDRAFT DAMPER + SCREEN (NOT DRYER)"), ((3, 16), "SEAL DUCT TO WRB / STUCCO"), ((-3, 16), "RIGID DUCT, SEALED")], dx=3.3)
d.title("3", "M-501", "EXHAUST WALL CAP", "2\" = 1'-0\"")
d = Det(s, 0, 1, 1 / 12)
d.R(0, 0, 36, 4, "m", 0.7); d.R(4, 4, 30, 30, "l"); d.C(19, 19, 11)
d.notes([((19, 2), "4\" CONCRETE PAD, 3\" ABOVE GRADE"), ((19, 19), "CONDENSER, 12\" CLEAR SIDES, 60\" TOP"), ((34, 30), "DISCONNECT WITHIN SIGHT")], dx=3.3)
d.title("4", "M-501", "CONDENSER PAD", "1\" = 1'-0\"")
d = Det(s, 1, 1, 1 / 12)
d.R(0, 0, 60, 3, "l", 0.6); d.R(10, 3, 40, 24, "l"); d.R(0, 30, 60, 0.75, "l", 0.4)
d.notes([((30, 15), "AHU-C/D ON 3/4\" PLYWOOD PLATFORM"), ((5, 1.5), "30\" SERVICE SPACE, LIGHT + RECEPT. (IMC 306.3)"), ((30, 30.4), "TRUSS BOTTOM CHORDS")], dx=3.3)
d.title("5", "M-501", "ATTIC AHU PLATFORM (C, D)", "1\" = 1'-0\"")
d = Det(s, 2, 1, 1 / 6)
d.R(0, 0, 30, 1.25, "l", 0.82); d.R(0, 1.25, 2, 12, "l"); d.R(28, 1.25, 2, 12, "l"); d.R(12, -0.4, 6, 0.4, "l", 0.2)
d.notes([((15, -0.2), "BATH FAN, CONTINUOUS 45 / BOOST 80 CFM"), ((1, 6), "SEALED HOUSING, GASKETED")], dx=3.3)
d.title("6", "M-501", "BATH FAN (VENTILATION)", "2\" = 1'-0\"")
save(s, "M-501", "Model1_Mechanical_Details", "MECHANICAL\nDETAILS")


# ===================================================================== D-003 accessibility details
s = new()
d = Det(s, 0, 0, 1 / 16)
d.R(0, 0, 60, 36, "m"); d.R(0, 0, 60, 2, "l", 0.85)
d.L((4, 33), (56, 33), "m"); d.L((2, 0), (2, 36), "f", [3, 2])
d.R(48, 4, 10, 28, "l"); d.C(53, 18, 1.5)
d.notes([((30, 33), "GRAB BAR 33\"–36\" A.F.F."), ((53, 18), "HANDHELD ON 24\" SLIDE BAR"), ((30, 1), "TRENCH DRAIN, NO CURB"), ((48, 25), "FOLDING SEAT 17\"–19\"")], dx=3.3)
d.title("1", "D-003", "ROLL-IN SHOWER (UNIT A)", "3/4\" = 1'-0\"")
d = Det(s, 1, 0, 1 / 16)
d.R(0, 0, 18, 30, "l"); d.L((-14, 33), (40, 33), "m"); d.L((24, 33), (24, 60), "m")
d.C(9, 17, 6)
d.notes([((9, 17), "WC, SEAT 17\"–19\""), ((10, 33), "REAR BAR 36\" MIN., 33\"–36\" A.F.F."), ((24, 50), "SIDE BAR 42\" MIN."), ((2, 2), "16\"–18\" TO CL OF WC")], dx=3.3)
d.title("2", "D-003", "WATER CLOSET (UNIT A)", "3/4\" = 1'-0\"")
d = Det(s, 2, 0, 1 / 16)
d.R(0, 0, 36, 34, "l"); d.R(0, 27, 36, 7, "l", 0.8); d.R(4, 9, 28, 18, "f", dash=[3, 2])
d.notes([((18, 30), "LAV / SINK RIM 34\" MAX."), ((18, 15), "KNEE CLEARANCE 27\" H x 30\" W x 17\" D"), ((10, 22), "INSULATED PIPES BELOW")], dx=3.3)
d.title("3", "D-003", "LAV + SINK KNEE SPACE", "3/4\" = 1'-0\"")
d = Det(s, 0, 1, 1 / 16)
d.R(0, 0, 4, 80, "m"); d.R(4, 0, 36, 80, "l", 0.9); d.L((4, 0), (40, 0), "m")
d.L((40, 0), (58, 0), "m"); d.PL([(-18, 0), (0, 0)], "m")
d.notes([((22, 40), "32\" MIN. CLEAR OPENING"), ((48, 0), "18\" MIN. LATCH-SIDE PULL CLEARANCE"), ((-8, 0), "LEVEL LANDING 60\" MIN."), ((40, 36), "LEVER 34\"–48\" A.F.F.")], dx=3.3)
d.title("4", "D-003", "ACCESSIBLE DOOR", "1/2\" = 1'-0\"")
d = Det(s, 1, 1, 1 / 16)
d.R(0, 0, 70, 0.5, "l"); d.PL([(0, 0.5), (34, 0.5), (36, 2.0), (70, 2.0)], "m")
d.notes([((35, 1.2), "1/2\" MAX., BEVEL 1:2 ABOVE 1/4\""), ((10, 0.5), "EXTERIOR SLAB 2% AWAY"), ((60, 2), "INTERIOR FINISH")], dx=3.3)
d.title("5", "D-003", "THRESHOLD / LEVEL CHANGE", "3/4\" = 1'-0\"")
d = Det(s, 2, 1, 1 / 16)
d.R(0, 0, 4, 72, "m")
for (z, t) in ((15, "15\" MIN. OUTLETS"), (34, "34\" COUNTER (UNIT A)"), (44, "44\" TYP. SWITCH"), (48, "48\" MAX. CONTROLS / THERMOSTAT")):
    d.L((4, z), (30, z), "f", [3, 2]); d.notes([((20, z), t)])
d.title("6", "D-003", "REACH RANGES + MOUNTING HEIGHTS", "1/2\" = 1'-0\"")
s.text((21.15, 23.2), "ACCESSIBILITY DETAILS — ICC A117.1-2009, UNIT A (TYPE A) + COMMON AREAS", 0.1, font="Helvetica-Bold", align="l")
save(s, "D-003", "Model1_Accessibility_Details", "ACCESSIBILITY\nDETAILS")
