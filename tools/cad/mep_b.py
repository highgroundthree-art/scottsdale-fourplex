"""M-101, M-102 HVAC plans and E-101, E-102 power + lighting plans, Model 1 (1/4")."""
import math
from sheetkit import *
from mep_fix import *

ORIG = (3.6, 19.75)


def unit_rooms(u):
    """supply-register rooms per unit (cx, cy, name, cfm)."""
    west = u in "AC"
    base = [(7, 6.75, "PRIMARY BED", 160), (19.5, 4.25, "BATH", 50), (6, 21.75, "BED 2", 110), (21, 21.25, "HALL BATH", 40),
            (7.5, 32.5, "DINING", 110), (20, 31, "KITCHEN", 120)]
    if u == "A":
        base += [(12.5, 43.5, "LIVING", 240)]
    else:
        base += [(3.75, 43.5, "BED 3", 100), (17.5, 43.5, "LIVING", 190)]
    if not west:
        base = [(60 - x, y, n, c) for (x, y, n, c) in base]
    return base


def hvac(lvl):
    def fn(d, p):
        d.layer = "M-DUCT"
        for u in UNITS[lvl]:
            west = u in "AC"
            ax, ay = AHU[u]
            d.color = ORANGE
            d.R(ax - 2.5, ay - 1.3, 5.0, 2.6, "m", fill=1.0); d.T(ax, ay + 0.25, f"AHU-{u}", 0.07, font="Helvetica-Bold")
            tx = 22.5 if west else 37.5
            d.PL([(ax + (2.5 if west else -2.5), ay - 0.5), (tx, ay - 0.5)], "m"); d.PL([(ax + (2.5 if west else -2.5), ay + 0.5), (tx, ay + 0.5)], "m")
            d.T((ax + tx) / 2, ay - 0.9, "12x8 SUPPLY TRUNK", 0.055)
            for (cx, cy, n, cfm) in unit_rooms(u):
                bx = cx
                d.PL([(bx, ay + (0.5 if cy > ay else -0.5)), (bx, cy)], "l")
                d.R(cx - 0.6, cy - 0.6, 1.2, 1.2, "l", fill=1.0); d.L((cx - 0.6, cy - 0.6), (cx + 0.6, cy + 0.6), "xf"); d.L((cx - 0.6, cy + 0.6), (cx + 0.6, cy - 0.6), "xf")
                d.T(cx, cy + 1.45, f"{cfm} CFM", 0.05)
                if lvl == 1:
                    d.T(cx, cy + 2.05, "CRD", 0.045, color=RED)
            # return
            rx = ax + (-4.5 if west else 4.5)
            d.color = GREEN
            d.R(rx - 1.0, ay - 0.6, 2.0, 1.2, "m", fill=1.0); d.L((rx - 1.0, ay), (rx + 1.0, ay), "xf")
            d.T(rx, ay - 1.0, "RG 24x12", 0.05)
            # exhaust fans
            d.color = BLUE
            for (ex, ey, t, to) in ((22.0, 2.0, "EF-1 BATH 80", (22.0, -0.3)), (23.0, 23.0, "EF-1 HALL BATH 80", (23.0 - 0.0, 25.0) if False else (14.0, 23.0)),
                                    (22.0, 11.0, "DRYER 4\" RIGID", (22.0, 8.5)), (23.6, 31.3, "HOOD 150 CFM", (23.6, 31.3))):
                ex2 = ex if west else 60 - ex
                d.C(ex2, ey, 0.55, "l", fill=1.0); d.T(ex2, ey + 0.2, "E", 0.055, font="Helvetica-Bold")
                d.T(ex2 + (2.6 if west else -2.6), ey + 1.0, t, 0.045)
            # exhaust route arrows to exterior
            ext = (0.0 if west else 60.0)
            for ey in (23.0, 31.3):
                d.PL([(23.0 if west else 37.0, ey), (ext, ey)], "f", [3, 2])
                d.arrow((ext + (2 if west else -2), ey), (ext + (-0.8 if west else 0.8), ey), "l", 0.5)
            d.PL([(22.0 if west else 38.0, 2.0), (22.0 if west else 38.0, -0.8)], "f", [3, 2])
            d.PL([(22.0 if west else 38.0, 11.0), (22.0 if west else 38.0, -0.8)], "f", [3, 2])
            d.color = None
        if lvl == 1:
            for u, (x, y) in CU.items():
                d.R(x - 1.3, y - 1.3, 2.6, 2.6, "m"); d.T(x, y + 0.2, f"CU-{u}", 0.055, font="Helvetica-Bold")
            d.T(31.0, -5.2, "CONDENSERS ON PADS, LINE SETS UP THE EXTERIOR CHASE TO AHU-C / AHU-D IN THE ATTIC", 0.055)
        else:
            d.T(30, 12.8, "AHU-C / AHU-D: ATTIC ABOVE THE HALL, ON PLATFORM WITH 30\" SERVICE SPACE + LIGHT", 0.05)
    return fn


def mech_sheet(lvl, sheet, file):
    s = new()
    p = bg(s, lvl, ORIG)
    s.ox, s.oy = ORIG
    hvac(lvl)(Draw(s), p)
    s.ox, s.oy = ORIG
    plan_grids(s)
    lv = "GROUND" if lvl == 1 else "UPPER"
    title(s, "1", sheet, f"{lv} FLOOR HVAC PLAN", "SCALE: 1/4\" = 1'-0\"   DESIGN INTENT — MECHANICAL ENGINEER TO SIZE (MANUAL J / S / D)")
    north(s)
    units = UNITS[lvl]
    y = tbl(s, NC, TOPY, "EQUIPMENT (SEE M-001)", [("MARK", 0.9, "c"), ("DESCRIPTION", 3.4, "l"), ("SIZE", 1.0, "c"), ("ELEC.", 1.0, "c"), ("NOTE", 4.3, "l")], [
        (f"AHU-{units[0]}/{units[1]}", "Variable-speed air handler, heat pump", "2.5 TON", "240V/1", "Ground: hall soffit" if lvl == 1 else "Upper: attic platform"),
        (f"CU-{units[0]}/{units[1]}", "Inverter heat pump condenser, SEER2 16+, HSPF2 8+", "2.5 TON", "240V/1", "Pad on north yard"),
        ("EF-1", "Bath fan, continuous-rated, ENERGY STAR", "80 CFM", "120V", "Primary bath fan runs continuously at 45 CFM (whole-house ventilation)"),
        ("HOOD", "Range hood ducted to exterior", "150 CFM", "120V", "Make-up air not required under 400 CFM"),
        ("DRYER", "Electric dryer, 4\" rigid duct", "—", "240V/30A", "35 ft max. equivalent length; booster not needed"),
    ], w=10.6)
    nts = [
        "Design intent. Heating and cooling loads, equipment size and duct sizes by the mechanical engineer using ACCA Manual J, S and D for the Phoenix design conditions (cooling 108°F dry bulb).",
        "Each unit has its own system and thermostat; no shared equipment, no shared ducts.",
    ]
    if lvl == 1:
        nts += ["Ground units: ducts run in the open-web floor trusses above the F1 rated ceiling. Every supply and return opening in the F1 ceiling gets a listed ceiling radiation damper (CRD) per UL 555C. No ducts in W1 walls.",
                "AHU-A / AHU-B: horizontal air handler above a dropped soffit in the hall (8'-0\" A.F.F.), access panel 24x36, secondary drain pan with float switch; condensate to the laundry standpipe.",
                "Line sets from the condensers enter at the north wall in sealed sleeves and run in the soffit."]
    else:
        nts += ["Upper units: AHU and ducts in the vented attic. Ducts sealed with mastic, R-8 insulation, leakage tested to 4 CFM25 per 100 SF max. (IECC R403.3).",
                "Attic platform with 30\" clear service space, light and receptacle at the AHU (IMC 306.3). Secondary drain pan with float switch.",
                "No duct crosses the W1 draftstop between attics."]
    nts += ["Bath and dryer exhaust and range hood duct to the exterior through wall caps with dampers, never into the attic or soffit. No vents in the west W2 eave or within 3 ft of MC-1.",
            "Whole-dwelling ventilation per IMC 403.3.2 / ASHRAE 62.2: primary bath fan on continuous low speed (45 CFM for a 1,250 SF 3-bedroom unit).",
            "Transfer grilles or jump ducts above each bedroom door so bedrooms do not pressurize when the doors are closed. In F1 ceilings use wall-mounted transfer grilles (no ceiling openings)."]
    notes(s, NC, y, "HVAC NOTES", nts, 10.6)
    save(s, sheet, file, f"{lv} FLOOR\nHVAC PLAN")


mech_sheet(1, "M-101", "Model1_Ground_Floor_HVAC_Plan")
mech_sheet(2, "M-102", "Model1_Upper_Floor_HVAC_Plan")


# ============================================================ ELECTRICAL
def recept(d, x, y, kind=""):
    d.C(x, y, 0.32, "l", fill=1.0)
    d.L((x - 0.12, y - 0.32), (x - 0.12, y + 0.32), "xf"); d.L((x + 0.12, y - 0.32), (x + 0.12, y + 0.32), "xf")
    if kind:
        d.T(x + 0.75, y + 0.25, kind, 0.04)


def light(d, x, y, kind="surface"):
    d.C(x, y, 0.45, "l", fill=1.0)
    d.L((x - 0.32, y - 0.32), (x + 0.32, y + 0.32), "xf"); d.L((x - 0.32, y + 0.32), (x + 0.32, y - 0.32), "xf")


def switch(d, x, y):
    d.T(x, y + 0.2, "S", 0.06, font="Helvetica-Bold")


def smoke(d, x, y, co=False):
    d.C(x, y, 0.42, "l", fill=1.0); d.T(x, y + 0.18, "SC" if co else "SD", 0.04, font="Helvetica-Bold")


def elec(lvl):
    def fn(d, p):
        d.layer = "E-POWR"
        # lights + receptacles room by room from the plan spaces
        for sp in p.spaces:
            if not sp["name"] or sp["group"] in ("C", "K"):
                continue
            nm = sp["name"].replace("\n", " ")
            for (x, y, w, h) in sp["rects"][:1]:
                d.color = None
                cx, cy = x + w / 2, y + h / 2
                light(d, cx, cy)
                if nm in ("LIVING", "DINING", "KITCHEN") and w * h > 100:
                    light(d, cx, cy - 2.5) if h > 9 else None
                # receptacles: perimeter every ~10 ft
                per = [((x + 0.45, y + h * k / 3), "") for k in (1, 2)] + [((x + w - 0.45, y + h * k / 3), "") for k in (1, 2)] + \
                      [((x + w * k / 3, y + 0.45), "") for k in (1, 2)] + [((x + w * k / 3, y + h - 0.45), "") for k in (1, 2)]
                if nm in ("WIC", "HALL BATH", "BATH", "ROLL-IN BATH", "PRIMARY BATH", "LAUNDRY"):
                    per = per[:1]
                tag = "GFCI" if any(k in nm for k in ("BATH", "KITCHEN", "LAUNDRY")) else ""
                for (pt, _) in per:
                    recept(d, pt[0], pt[1], tag)
                if "BED" in nm or nm in ("HALL", "LIVING"):
                    smoke(d, cx + 1.6, cy, co=(nm == "HALL"))
        # switches at doors
        for dr in p.doors:
            if dr["kind"] not in ("swing",):
                continue
            hx, hy = dr["h"][0] / 12, dr["h"][1] / 12
            sx, sy = dr["st"][0] / 12, dr["st"][1] / 12
            if abs(hy - sy) < 0.01:
                ux = 1 if sx > hx else -1
                switch(d, sx + 0.55 * ux, sy + 0.55 * dr["d"])
            else:
                uy = 1 if sy > hy else -1
                switch(d, sx + 0.55 * dr["d"], sy + 0.55 * uy)
        # panels, equipment
        for u in UNITS[lvl]:
            px, py = PANEL[u]
            d.color = BLUE
            d.R(px - 0.9, py - 0.35, 1.8, 0.35, "m", fill=0.0); d.T(px, py + 1.0, f"PANEL {u} 125A", 0.06, font="Helvetica-Bold")
            wx, wy = WH[u]; d.T(wx, wy - 1.4, "WH 30A/2P", 0.045)
            ax, ay = AHU[u]; d.T(ax, ay - 1.6, f"AHU-{u} 40A/2P, DISC.", 0.045)
            d.color = None
        if lvl == 1:
            x, y, w, h = MC1
            d.color = BLUE
            d.R(x, y, w, h, "m", fill=0.3); d.T(x + w / 2, y - 0.7, "MC-1 400A METER CENTER (E-201)", 0.06, font="Helvetica-Bold")
            d.PL([(33.5, 0), (33.5, 9.0), (30, 9.0), (30, 15.5), (PANEL["A"][0] + 0.9, 15.5)], "m", [6, 2])
            d.PL([(30, 15.5), (PANEL["B"][0] - 0.9, 15.5)], "m", [6, 2])
            d.T(29.6, 12.0, "FEEDERS IN CH2 / CORE CEILING", 0.05, rot=90)
            for u, (x2, y2) in CU.items():
                d.R(x2 - 1.3, y2 - 1.3, 2.6, 2.6, "l"); d.T(x2, y2 + 0.2, f"CU-{u}", 0.045)
                d.T(x2, y2 - 1.7, "DISC.", 0.04)
            d.T(30, 30.0, "HOUSE PANEL HP", 0.055, font="Helvetica-Bold"); d.R(28.6, 30.4, 2.8, 0.35, "m", fill=0.0)
            for (x2, y2) in ((30, 27), (30, 38), (30, 47.5)):
                light(d, x2, y2)
            d.color = None
        else:
            for (x2, y2) in ((30, 40), (30, 47)):
                light(d, x2, y2)
            d.PL([(30, 17.5), (30, 38)], "m", [6, 2]); d.T(30.6, 30, "FEEDERS C + D FROM MC-1 VIA CH2", 0.05, rot=90)
    return fn


def elec_sheet(lvl, sheet, file):
    s = new()
    p = bg(s, lvl, ORIG)
    s.ox, s.oy = ORIG
    elec(lvl)(Draw(s), p)
    s.ox, s.oy = ORIG
    plan_grids(s)
    lv = "GROUND" if lvl == 1 else "UPPER"
    title(s, "1", sheet, f"{lv} FLOOR POWER AND LIGHTING PLAN", "SCALE: 1/4\" = 1'-0\"   DESIGN INTENT — ELECTRICAL ENGINEER / CONTRACTOR TO COMPLETE CIRCUITING")
    north(s)
    leg = [
        (lambda x, y: (s.circle((x + 0.3, y), 0.08, lw="l", fill=1.0), s.line((x + 0.27, y - 0.08), (x + 0.27, y + 0.08), lw="xf"), s.line((x + 0.33, y - 0.08), (x + 0.33, y + 0.08), lw="xf")), "Duplex receptacle, tamper-resistant, 15/20A, 18\" A.F.F. (GFCI where noted)"),
        (lambda x, y: (s.circle((x + 0.3, y), 0.11, lw="l", fill=1.0), s.line((x + 0.22, y - 0.08), (x + 0.38, y + 0.08), lw="xf"), s.line((x + 0.22, y + 0.08), (x + 0.38, y - 0.08), lw="xf")), "LED ceiling fixture, surface mount (no recessed cans in F1 ceilings)"),
        (lambda x, y: s.text((x + 0.3, y - 0.03), "S", 0.08, font="Helvetica-Bold"), "Switch, 44\" A.F.F. max. (48\" accessible)"),
        (lambda x, y: (s.circle((x + 0.3, y), 0.11, lw="l", fill=1.0), s.text((x + 0.3, y - 0.03), "SD", 0.045)), "Smoke alarm, hard-wired, interconnected, battery backup"),
        (lambda x, y: (s.circle((x + 0.3, y), 0.11, lw="l", fill=1.0), s.text((x + 0.3, y - 0.03), "SC", 0.045)), "Combination smoke / CO alarm"),
    ]
    y = legend(s, NC, TOPY, "LEGEND", leg, 10.6)
    nts = [
        "Design intent. Circuiting, conductor sizes and panel schedules by the electrical engineer or licensed contractor per the 2020 NEC with Scottsdale amendments.",
        "Receptacles: no point along a wall more than 6 ft from a receptacle (NEC 210.52); kitchen counters every 4 ft, two 20A small-appliance circuits; bath, laundry, kitchen and exterior on GFCI; all 120V 15/20A branch circuits in dwelling areas AFCI protected (210.12).",
        "Tamper-resistant receptacles throughout (406.12). Exterior receptacle at each patio and the front, in-use covers.",
        "Ground units (F1 ceilings): surface-mounted LED fixtures on listed boxes for rated ceilings, or fire-rated box covers. No recessed cans. Wiring in the floor-truss space, not on the independent ceiling joists.",
        "Smoke alarms in every bedroom, outside each sleeping area and on each level, interconnected within the unit; CO alarms outside sleeping areas (IFC 915). Hard-wired with battery backup.",
        "Unit A (Type A): switches and controls 15\"–48\" A.F.F.; receptacles 15\" min. A.F.F.; doorbell and visual alarm prewire at the entry and bedrooms (A117.1 1002.12).",
        "Each unit panel 125A, 42 spaces, in the hall; whole-unit surge protection (230.67). Panel working clearance 30\" wide x 36\" deep x 6'-6\" high kept clear.",
        "EV-ready: one 40A 240V circuit roughed to each of 4 parking stalls from the house panel or unit panels (E-401) — confirm Scottsdale requirement.",
    ]
    notes(s, NC, y, "POWER AND LIGHTING NOTES", nts, 10.6)
    save(s, sheet, file, f"{lv} FLOOR\nELECTRICAL PLAN")


elec_sheet(1, "E-101", "Model1_Ground_Floor_Electrical_Plan")
elec_sheet(2, "E-102", "Model1_Upper_Floor_Electrical_Plan")
