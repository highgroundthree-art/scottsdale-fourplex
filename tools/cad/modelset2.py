"""Model 2 / Model 3 sheets, part 2: roof, elevations, sections, enlarged plans, schedules, structure, site, cover, code, MEP notes.
usage: python3 modelset2.py out 2|3 [sheet ...]"""
import math, sys
from modelset import *
from modelset import save as msave
from bgplan import clip_items
from textsheets import Flow
from elev import Elev, GRADE

FFU, PLT = 10 + 8 / 12, 9 + 8 / 12 + 10 / 12     # floor-to-floor; plate above each floor
PITCH = 4 / 12


def views_of(b):
    return [k for k in b["views"]]


def scratch_views(keys):
    s = Sheet(origin=(0, 0))
    out = []
    for k in keys:
        vc, lvl, ttl, ds = VIEWS[k]
        v = View(s, vc).build(); v.draw(lvl, ds); v.key = k
        out.append(v)
    return out


ALLV = scratch_views(list(VIEWS))
VBY = {v.key: v for v in ALLV}


# ============================================================== roof
def roof_outline(d, W, D, ov=2.0):
    a0, a1, b0, b1 = -ov, W + ov, -ov, D + ov
    d.R(a0, b0, a1 - a0, b1 - b0, "h")
    d.R(0, 0, W, D, "f", dash="HIDDEN")
    if W >= D:
        run = (D + 2 * ov) / 2
        r0, r1, rc = a0 + run, a1 - run, (b0 + b1) / 2
        d.L((r0, rc), (r1, rc), "h")
        for c, r in (((a0, b0), (r0, rc)), ((a0, b1), (r0, rc)), ((a1, b0), (r1, rc)), ((a1, b1), (r1, rc))):
            d.L(c, r, "m")
    else:
        run = (W + 2 * ov) / 2
        r0, r1, rc = b0 + run, b1 - run, (a0 + a1) / 2
        d.L((rc, r0), (rc, r1), "h")
        for c, r in (((a0, b0), (rc, r0)), ((a1, b0), (rc, r0)), ((a0, b1), (rc, r1)), ((a1, b1), (rc, r1))):
            d.L(c, r, "m")
    for (x, y) in ((0.3, -1.6), (W - 0.3, -1.6), (0.3, D + 1.6), (W - 0.3, D + 1.6)):
        d.R(x - 0.25, y - 0.17, 0.5, 0.34, "l", fill=0.2); d.T(x + (1.2 if x < W / 2 else -1.2), y + 0.2, "DS", 0.05, font="Helvetica-Bold")
    rise = min(W, D) / 2 * PITCH
    return rise


def sheet_A103():
    s = sheetkit.new()
    y = 22.6
    for b in BLDGS:
        sc = 64 if b["w"] > 50 else 64
        s.scale = sc; s.ox, s.oy = 1.8, y
        d = Draw(s, "A-ROOF")
        rise = roof_outline(d, b["w"], b["d"])
        d.T(b["w"] / 2, b["d"] / 2 + 1.2, f"RIDGE ±{(b['stories'] * FFU - 1 + rise + 0.6):.0f}'-0\" A.F.F.", 0.07, font="Helvetica-Bold")
        d.T(b["w"] / 2, b["d"] / 2 - 1.0, "4:12 CLAY TILE, HIP", 0.06)
        s.scale = 48
        h = (b["d"] + 4) * 12 / sc
        SL.drawing_title(s, 1.4, y - h - 0.8, str(BLDGS.index(b) + 1), "A-103" + SUF, f"ROOF PLAN — {b['name']}", "SCALE: 3/16\" = 1'-0\"", w=12.0, scalebar=False)
        y = y - h - 2.0
    notes(s, NC, TOPY, "ROOF PLAN NOTES", [
        "Two-piece clay tile on two layers of underlayment, 7/16\" OSB on engineered trusses @ 24\" o.c., 4:12 hip, eaves 2'-0\". Class A.",
        "Vented attic per IBC 1202, 1/150 net free area, balanced; R-38 at full height over the plates (raised-heel trusses).",
        "Attics divided at every W1 wall (draftstop to the deck, D-002/4).",
        "5\" gutters, 3x4 downspouts (DS) to splash blocks and the retention basins (C-102). No discharge within 3 ft of meters.",
        "One VTR per plumbing stack; flash with tile vent flashing. No roof-mounted equipment.",
        "Ridge height to be confirmed against the zoning height limit at pre-application" + (" — the carriage house with a loft is the critical case (OPEN ITEM)." if M == 3 else "."),
    ], 10.6)
    msave(s, "A-103" + SUF, "Roof_Plan", "ROOF PLAN")


# ============================================================== elevations
WSIZE = {"A": (6, 4, 3.0), "B": (3, 5, 2.0), "C": (3, 4, 3.0), "D": (6, 5, 2.0), "E": (4, 5, 2.0), "F": (3, 5, 2.0)}


def face_ops(b, face):
    """openings on a frame face for all levels of building b: list of (x0, x1, z0, z1, kind)."""
    ops = []
    for i, k in enumerate(b["views"]):
        v = VBY[k]
        W, D = v.W, v.D
        z0 = i * FFU
        for w in v.p.windows:
            if w["side"] != face:
                continue
            a, c = w["a"] / 12, w["b"] / 12
            if face == "N":
                a, c = W - c, W - a
            if face == "E":
                a, c = D - c, D - a
            ww = c - a
            sill = 3.0 if ww >= 5.5 else 2.0
            ops.append((a, c, z0 + sill, z0 + 7.0, "W"))
        for dr in v.p.doors:
            hx, hy, sx, sy = dr["h"][0] / 12, dr["h"][1] / 12, dr["st"][0] / 12, dr["st"][1] / 12
            on = {"N": abs(hy) < 0.6 and abs(sy) < 0.6, "S": abs(hy - D) < 0.6 and abs(sy - D) < 0.6, "W": abs(hx) < 0.6 and abs(sx) < 0.6, "E": abs(hx - W) < 0.6 and abs(sx - W) < 0.6}[face]
            if not on:
                continue
            if face in ("N", "S"):
                a, c = sorted((hx, sx))
                if face == "N":
                    a, c = W - c, W - a
            else:
                a, c = sorted((hy, sy))
                if face == "E":
                    a, c = D - c, D - a
            ops.append((a, c, z0, z0 + 8.0, "D"))
    return ops


def draw_face(e, b, face, x0=0.0):
    long_face = face in ("N", "S")
    L = (b["w"] if long_face else b["d"])
    depth = (b["d"] if long_face else b["w"])
    top = b["stories"] * FFU - 1.0
    eave = top + 0.4
    e.rect(x0, 0, x0 + L, top, lw="m")
    e.rect(x0, GRADE, x0 + L, 0, lw="f", fill=0.92)
    for i in range(1, b["stories"]):
        e.rect(x0, i * FFU - 0.42, x0 + L, i * FFU + 0.25, lw="f", fill=0.94)
    ov = 2.0
    a, c = x0 - ov, x0 + L + ov
    if b["w"] >= b["d"]:
        is_long = long_face
    else:
        is_long = not long_face
    if is_long:
        run = depth / 2 + ov
        zr = eave + run * PITCH
        pts = [(a, eave), (c, eave), (c - run, zr), (a + run, zr)]
    else:
        run = (c - a) / 2
        zr = eave + run * PITCH
        pts = [(a, eave), (c, eave), ((a + c) / 2, zr)]
    e.poly(pts, lw="m", fill=0.85)
    for k in range(int(a) + 1, int(c), 1):
        pass
    e.rect(a, eave - 0.6, c, eave, lw="l", fill=1.0)
    for (p, q, z0, z1, kind) in face_ops(b, face):
        e.rect(x0 + p, z0, x0 + q, z1, lw="l", fill=1.0)
        if kind == "W":
            e.line((x0 + (p + q) / 2, z0), (x0 + (p + q) / 2, z1), lw="xf")
        else:
            e.rect(x0 + p + 0.25, z0, x0 + q - 0.25, z1 - 0.25, lw="xf")
    e.line((x0 - 4, GRADE), (x0 + L + 4, GRADE), lw="h")
    return zr


def sheet_elev(no, faces):
    s = sheetkit.new()
    y = 22.9
    k = 0
    for b in BLDGS:
        for face in faces:
            long_face = face in ("N", "S")
            L = b["w"] if long_face else b["d"]
            top = b["stories"] * FFU - 1.0
            zr = top + 0.4 + (min(b["w"], b["d"]) / 2 + 2.0) * PITCH
            h = (zr + 0.5) * 12 / 96
            oy = y - h
            e = Elev(s, (1.8, oy))
            s.scale = 96
            draw_face(e, b, face)
            k += 1
            s.scale = 48
            SL.drawing_title(s, 1.4, oy - 0.95, str(k), no, f"{FACE[face]} ELEVATION \u2014 {b['name']}", "SCALE: 1/8\" = 1'-0\"", w=max(5.6, L * 12 / 96 + 0.6), scalebar=False)
            y = oy - 1.55
    s.scale = 48
    notes(s, NC, TOPY, "ELEVATION NOTES", [
        "Same material palette as Model 1: 7/8\" three-coat stucco (warm sand), off-white trim bands at floor lines, two-tone clay tile hip roofs, deep-green doors and shutters.",
        "Window heads align at 7'-0\" above each floor; sills 3'-0\" at bedroom sliders (escape openings), 2'-0\" elsewhere.",
        "Elevations are generated from the A-101/A-102 plans; final trim, shutters and entry details to be developed with the owner as on Model 1 (A-201.1).",
        "Building height to the ridge to be confirmed against zoning at pre-application.",
    ], 10.6)
    msave(s, no, "Exterior_Elevations_" + ("Long_Faces" if faces[0] in "NS" else "End_Faces"), "EXTERIOR\nELEVATIONS")


# ============================================================== sections
def sheet_A301():
    s = sheetkit.new()
    s.scale = 96
    y = 22.9
    k = 0
    for b in BLDGS:
        for long in (True, False):
            L = b["w"] if long else b["d"]
            depth = b["d"] if long else b["w"]
            zr0 = b["stories"] * FFU - 1.0 + 0.4 + (min(b["w"], b["d"]) / 2 + 2.0) * PITCH
            y = y - (zr0 + 0.5) * 12 / 96
            e = Elev(s, (1.6, y))
            s.scale = 96
            n = b["stories"]
            top = n * FFU - 1.0
            e.rect(0, -0.33, L, 0, lw="m", fill=0.55)
            for (bx, bw, bd) in ((0.5, 1.0, 2.0), (L - 0.5, 1.0, 2.0)):
                e.rect(bx - bw / 2, -bd, bx + bw / 2, -0.33, lw="m", fill=0.55)
            for i in range(1, n):
                e.rect(0, i * FFU - 1.6, L, i * FFU, lw="f", fill=0.85)
            e.rect(0, 0, 0.5, top, lw="h", fill=0.5); e.rect(L - 0.5, 0, L, top, lw="h", fill=0.5)
            v = VBY[b["views"][0]]
            cut = (v.D / 2) if long else (v.W / 2)
            for sg in v.p.segs:
                o, f, a, c, t = sg
                if t != "W1":
                    continue
                if long and o == "v" and a / 12 <= cut <= c / 12:
                    e.rect(f / 12 - 0.4, 0, f / 12 + 0.4, top + 3, lw="h", fill=0.3)
                if not long and o == "h" and a / 12 <= cut <= c / 12:
                    e.rect(f / 12 - 0.4, 0, f / 12 + 0.4, top + 3, lw="h", fill=0.3)
            ov = 2.0
            run = depth / 2 + ov
            zr = top + 0.4 + (min(depth, L) / 2 + ov) * PITCH
            if long:
                r = min(b["w"], b["d"]) / 2 + ov
                e.poly([(-ov, top + 0.4), (L + ov, top + 0.4), (L + ov - r, top + 0.4 + r * PITCH), (-ov + r, top + 0.4 + r * PITCH)], lw="m")
            else:
                e.poly([(-ov, top + 0.4), (L + ov, top + 0.4), (L / 2, top + 0.4 + (L / 2 + ov) * PITCH)], lw="m")
            e.line((-4, GRADE), (L + 4, GRADE), lw="h")
            for i, kk in enumerate(b["views"]):
                vv = VBY[kk]
                for r in rooms(vv):
                    inside = (r["y"] <= cut <= r["y"] + r["h"]) if long else (r["x"] <= cut <= r["x"] + r["w"])
                    if inside and r["w"] * r["h"] > 40:
                        xc = r["cx"] if long else r["cy"]
                        e.text(xc, i * FFU + 4.0, r["name"][:16], 0.055, font="Helvetica-Bold")
            for i in range(n + 1):
                z = i * FFU if i < n else top
                e.line((L + 1, z), (L + 5, z), lw="xf", dash="CENTER")
                e.text(L + 5.3, z + 0.2, ("FIN. FLOOR" if i == 0 else f"LEVEL {i + 1}" if i < n else "TOP OF PLATE") + f" {z:.1f}'", 0.055, align="l")
            k += 1
            s.scale = 48
            SL.drawing_title(s, 1.4, y - 2.0 * 12 / 96 - 0.7, str(k), "A-301" + SUF, f"BUILDING SECTION {'LONG' if long else 'CROSS'} — {b['name']}", "SCALE: 1/8\" = 1'-0\"   SCHEMATIC", w=max(5.6, L * 12 / 96 + 2.0), scalebar=False)
            s.scale = 96
            y -= 2.0 * 12 / 96 + 1.3
    s.scale = 48
    notes(s, NC, TOPY, "SECTION NOTES", [
        "Assemblies as Model 1: F1 1-hour floor/ceiling with independent ceiling joists (D-002/3) wherever one unit sits over another; W1 1-hour walls slab to roof deck (dark) dividing the attics.",
        "PT slab on ground with thickened edges and beams under every W1 wall (S-101). Floor-to-floor 10'-8\"; ceilings 9'-0\".",
        "Roof: 4:12 hip, engineered trusses @ 24\" with raised heel, R-38 blown, vented attic.",
        "Room names along each cut are from the A-101/A-102 plans. Sections are schematic; wall sections and details on A-302, D-001, D-002.",
    ] + (["Carriage house: garage level with 5/8\" Type X ceiling and walls separating the casita above (IRC R302.6 / IBC 406.3); loft level within the roof volume — height and story count to verify (OPEN)."] if M == 3 else []), 10.6)
    msave(s, "A-301" + SUF, "Building_Sections", "BUILDING\nSECTIONS")


# ============================================================== enlarged plans
def enlarged_room(s, key, room, at, scale=24):
    vc, lvl, ttl, ds = VIEWS[key]
    win = (room["x"] - 0.6, room["y"] - 0.6, room["x"] + room["w"] + 0.6, room["y"] + room["h"] + 0.6)
    s.scale = scale
    ox, oy = at[0] - win[0] * 12 / scale, at[1] + win[1] * 12 / scale
    s.ox, s.oy = ox, oy
    n0 = len(s.items)
    v = View(s, vc).build(); v.draw(lvl, ds)
    s.items[n0:] = [it for it in s.items[n0:] if it[1] not in ("A-ANNO-DIMS", "A-GRID")]
    a = s.m2p(win[0] * 12, win[1] * 12); b = s.m2p(win[2] * 12, win[3] * 12)
    clip_items(s, n0, (a[0], b[1], b[0], a[1]))
    s.rect(a[0], b[1], b[0] - a[0], a[1] - b[1], layer="A-ANNO-SYMB", lw="xf", dash="CENTER")
    s.scale = 48
    return (b[0] - a[0], a[1] - b[1])


def sheet_enlarged(no, words, ttl, tb):
    s = sheetkit.new()
    picks, seen = [], set()
    for k in VIEWS:
        for r in rooms(VBY[k]):
            if any(w in r["name"] for w in words) and (r["unit"], r["name"]) not in seen and r["w"] * r["h"] < 260:
                seen.add((r["unit"], r["name"])); picks.append((k, r))
    picks = picks[:6]
    x, y, rowh = 1.4, 22.6, 0
    for i, (k, r) in enumerate(picks):
        w = (r["w"] + 1.2) * 0.5; h = (r["h"] + 1.2) * 0.5
        if x + w > 20.5:
            x, y = 1.4, y - rowh - 1.6; rowh = 0
        enlarged_room(s, k, r, (x, y))
        SL.drawing_title(s, x - 0.2, y - h - 0.75, str(i + 1), no, f"{r['name']} — UNIT {r['unit']}", "SCALE: 1/2\" = 1'-0\"", w=max(4.5, w + 0.3), scalebar=False)
        x += max(w, 4.7) + 0.9; rowh = max(rowh, h)
    nts = (["Cabinets, counters and appliances per Model 1 A-401 standards: plywood-box shaker cabinets, quartz/solid-surface counters, ENERGY STAR appliances, ducted hood.",
            f"Unit {TYPEA} (Type A): 34\" work surface with knee space, removable sink base, 40\" min. clearance, 60\" turning space.",
            "Every unit gets the same finishes; kitchenettes in suites are limited to a sink, under-counter refrigerator and microwave (no range) so they do not create a fifth dwelling (OPEN item for zoning)."]
           if "KITCHEN" in words else
           ["Baths per Model 1 A-402 standards: cement board and tile at wet walls, blocking for grab bars at every WC/tub/shower, WaterSense fixtures, pressure-balance valves.",
            f"Unit {TYPEA} (Type A): roll-in shower with trench drain, fold-down seat, handheld shower, 60\" turning space, lav knee space.",
            "Exhaust fans ducted to the exterior; primary bath fan continuous for ventilation."])
    notes(s, NC, TOPY, f"{ttl} NOTES", nts, 10.6)
    msave(s, no, "Enlarged_" + ("Kitchen" if "KITCHEN" in words else "Bath") + "_Plans", tb)


# ============================================================== door + window schedules
def sheet_A601():
    s = sheetkit.new()
    rows = []
    for v in ALLV:
        rows += v.door_rows
    half = (len(rows) + 1) // 2
    SL.door_schedule(s, 1.0, 23.2, rows[:half], 9.6)
    if rows[half:]:
        SL.door_schedule(s, 11.0, 23.2, rows[half:], 9.6)
    SL.window_schedule(s, NC, 23.2, window_rows(ALLV), 10.6)
    notes(s, NC, 14.0, "DOOR AND WINDOW NOTES", [
        "Door and window types, hardware sets and installation per Model 1 A-601 and D-001. Schedules generated from A-101/A-102 plans; quantities are for this model.",
        "Unit entry doors from shared areas: 20-minute, self-closing, positive latching. Exterior unit entries: insulated fiberglass, lever hardware, deadbolt.",
        f"Unit {TYPEA} (Type A): 32\" clear doors, 1/2\" max. thresholds, lever hardware, 18\" latch-side pull clearance.",
        "Windows U 0.30 / SHGC 0.25, NFRC labeled; safety glazing per IBC 2406; escape openings per IBC 1031 at every bedroom.",
    ], 10.6)
    msave(s, "A-601", "Door_and_Window_Schedules", "DOOR + WINDOW\nSCHEDULES")


# ============================================================== structure
def struct_plan(no, kind, ttl, tb):
    s = sheetkit.new()
    y = 22.4
    for bi, b in enumerate(BLDGS):
        s.scale = 64; s.ox, s.oy = 1.8, y
        d = Draw(s, "S-FNDN" if kind == "fdn" else "S-FRAM")
        W, D = b["w"], b["d"]
        v = VBY[b["views"][0]]
        w1 = [sg for sg in v.p.segs if sg[4] == "W1"]
        if kind == "fdn":
            d.R(0, 0, W, D, "h"); d.R(1, 1, W - 2, D - 2, "f", dash="HIDDEN")
            for sg in w1:
                (x0, y0), (x1, y1) = seg_pts(sg)
                d.L((x0 - (0.67 if x0 == x1 else 0), y0 - (0.67 if y0 == y1 else 0)), (x1 - (0.67 if x0 == x1 else 0), y1 - (0.67 if y0 == y1 else 0)), "f", "HIDDEN")
                d.L((x0 + (0.67 if x0 == x1 else 0), y0 + (0.67 if y0 == y1 else 0)), (x1 + (0.67 if x0 == x1 else 0), y1 + (0.67 if y0 == y1 else 0)), "f", "HIDDEN")
            for xx in [W * i / (math.ceil(W / 16)) for i in range(1, math.ceil(W / 16))]:
                d.L((xx, 1), (xx, D - 1), "xf", "HIDDEN")
            for yy in [D * i / (math.ceil(D / 16)) for i in range(1, math.ceil(D / 16))]:
                d.L((1, yy), (W - 1, yy), "xf", "HIDDEN")
            for xx in range(2, int(W), 4):
                d.L((xx + 0.5, 0.3), (xx + 0.5, D - 0.3), "xf", [2, 3])
            for yy in range(2, int(D), 4):
                d.L((0.3, yy + 0.5), (W - 0.3, yy + 0.5), "xf", [2, 3])
        else:
            d.R(0, 0, W, D, "h")
            for sg in w1:
                (x0, y0), (x1, y1) = seg_pts(sg)
                d.L((x0, y0), (x1, y1), "xh")
            short_y = D <= W
            n = int((W if short_y else D) / 2)
            for i in range(n):
                p = 1 + i * 2
                if short_y:
                    d.L((p, 0.3), (p, D - 0.3), "xf")
                else:
                    d.L((0.3, p), (W - 0.3, p), "xf")
            if kind == "floor" and (D if short_y else W) > 26:
                mid = (D if short_y else W) / 2
                if short_y:
                    d.L((0.5, mid), (W - 0.5, mid), "h", [10, 3]); d.T(W / 2, mid - 0.7, "FB1 BEARING LINE / FLUSH BEAM (ENGINEER TO CONFIRM)", 0.055)
                else:
                    d.L((mid, 0.5), (mid, D - 0.5), "h", [10, 3])
            lbl = {"floor": "FT1 11-7/8\" OPEN-WEB @ 24\"", "roof": "T1/T2 HIP TRUSS SYSTEM @ 24\", 4:12, 14\" HEEL"}[kind]
            d.box(W / 2, D / 3, lbl, 0.055)
        s.scale = 48
        h = D * 12 / 64
        SL.drawing_title(s, 1.4, y - h - 0.8, str(bi + 1), no, f"{ttl} — {b['name']}", "SCALE: 3/16\" = 1'-0\"   DESIGN INTENT", w=12.0, scalebar=False)
        y = y - h - 2.2
        if kind == "floor" and b["stories"] < 2:
            continue
    nts = {"fdn": ["Post-tensioned slab on ground per PTI DC10.5 (same system as Model 1, S-101/S-501): 12x24 perimeter beam, 16x20 beams under every W1 wall, 12x20 ribs at about 16 ft each way, 1/2\" tendons at 4'-0\" o.c. each way (representative lines shown).",
                   "Footings 18\" min. below grade (Scottsdale). Geotechnical report for the parcel governs. PT shop drawings are a deferred submittal.",
                   "Sleeve plumbing through beams before the pour; no cutting after stressing; 1-1/2\" recesses at accessible doors."],
           "floor": ["Open-web floor trusses @ 24\" spanning the short direction; intermediate bearing line where the span exceeds about 26 ft. Final design by the truss maker and engineer of record.",
                     "Floors between stacked units are the F1 1-hour, STC/IIC 50 assembly (D-002/3): nothing attached to the truss bottom chords.",
                     "Each unit's framing bears on its own stud row at W1 walls; nothing frames across W1."],
           "roof": ["Engineered hip truss system @ 24\", 4:12, 14\" raised heel; TCDL 27 psf (clay tile), TCLL 20 psf, BCDL 10 psf; wind 115 mph exposure C (verify).",
                    "Trusses split at each W1 wall (draftstop to the deck). Hurricane ties every truss; girder straps per S-201.",
                    "Truss design drawings are a deferred submittal (S-503)."]}[kind]
    notes(s, NC, TOPY, f"{ttl} NOTES", nts, 10.6)
    msave(s, no, {"fdn": "Foundation_Plan", "floor": "Floor_Framing_Plan", "roof": "Roof_Framing_Plan"}[kind], tb)


# ============================================================== site
if M == 2:
    SITE = dict(W=66, D=152, alley=False, bldgs=[(12, 30, 28, 102, "FOURPLEX (2 STORIES)")],
                pave=[(46, 0, 12, 152), (26, 2, 20, 27), (58, 36, 8, 88)], stalls=[(26, 2, 20, 9, "VAN + AISLE")] + [(26 + 0, 11 + i * 0, 0, 0, "") for i in range(0)],
                stall_rows=[(58, 36, 8, 22, 4, "v")], walks=[(40, 30, 6, 102), (24, 132, 4, 20)], patios=[(2, 36, 10, 10), (2, 58, 10, 10), (2, 80, 10, 10)],
                basins=[(2, 135, 20, 14), (30, 136, 15, 13)], trash=(1, 2, 6, 7), entry=(26, 132), street="S")
else:
    SITE = dict(W=80, D=125, alley=True, bldgs=[(10, 65, 60, 40, "MAIN HOUSE (2 STORIES)"), (14, 25, 48, 24, "CARRIAGE HOUSE (GARAGES + CASITA + LOFT)")],
                pave=[(17, 0, 45, 25), (1, 2, 16, 18)], stalls=[(1, 2, 11, 18, "VAN")], stall_rows=[(12, 2, 5, 18, 1, "h")],
                walks=[(3, 20, 5, 85), (3, 105, 31, 3.5), (38, 105, 4, 20)], patios=[(10, 49, 60, 16)], basins=[(9, 110, 21, 13), (50, 110, 20, 13)],
                trash=(68, 1, 8, 6), entry=(40, 105), street="S")


def site_draw(d):
    S = SITE
    d.R(0, 0, S["W"], S["D"], "h", dash="PHANTOM", layer="C-PROP")
    d.R(-8, S["D"], S["W"] + 16, 5, "f"); d.T(S["W"] / 2, S["D"] + 2.9, "PUBLIC STREET (SOUTH) — EXISTING CURB, GUTTER, 5' SIDEWALK", 0.08, font="Helvetica-Bold")
    if S["alley"]:
        d.R(-8, -16, S["W"] + 16, 16, "f", fill=0.92); d.T(S["W"] / 2, -8, "PUBLIC ALLEY (NORTH) — GARAGE ACCESS + TRASH PICKUP", 0.08, font="Helvetica-Bold")
    for (x, y, w, h) in S["pave"]:
        d.R(x, y, w, h, "m", fill=0.92, layer="C-PVMT")
    for (x, y, w, h, t) in S["stalls"]:
        d.R(x, y, w, h, "l", layer="C-PVMT-STRP"); d.T(x + w / 2, y + h / 2, t, 0.06, font="Helvetica-Bold")
    for (x, y, w, h, n, o) in S["stall_rows"]:
        for i in range(n):
            if o == "v":
                d.R(x, y + i * h, w, h, "l", layer="C-PVMT-STRP"); d.T(x + w / 2, y + i * h + h / 2, f"P{i + 2}", 0.055)
            else:
                d.R(x + i * w, y, w, h, "l", layer="C-PVMT-STRP"); d.T(x + i * w + w / 2, y + h / 2, f"P{i + 2}", 0.055)
    for (x, y, w, h) in S["walks"]:
        d.R(x, y, w, h, "l", fill=0.97, layer="C-WALK")
    for (x, y, w, h) in S["patios"]:
        d.R(x, y, w, h, "l", fill=0.97, layer="C-WALK"); d.T(x + w / 2, y + h / 2, "PATIO" if w < 30 else "COURTYARD / PATIOS", 0.055)
    for (x, y, w, h) in S["basins"]:
        d.R(x, y, w, h, "m", dash=[6, 3], layer="C-TOPO"); d.R(x + 2, y + 2, w - 4, h - 4, "f", dash=[6, 3], layer="C-TOPO")
        d.T(x + w / 2, y + h / 2, "RETENTION BASIN", 0.055, font="Helvetica-Bold")
    tx, ty, tw, th = S["trash"]; d.R(tx, ty, tw, th, "m", fill=0.75); d.T(tx + tw / 2, ty + th / 2, "TRASH", 0.05, font="Helvetica-Bold")
    for (x, y, w, h, t) in S["bldgs"]:
        d.R(x, y, w, h, "h", fill=0.86, layer="A-WALL"); d.R(x - 2, y - 2, w + 4, h + 4, "f", dash="HIDDEN", layer="A-ROOF")
        d.T(x + w / 2, y + h / 2, t, 0.075, font="Helvetica-Bold"); d.T(x + w / 2, y + h / 2 + 2.2, "FF 100.00'", 0.06)


def site_sheet(no, ttl, tb, overlay, nts, file):
    s = sheetkit.new((3.2, 21.9), 96)
    d = Draw(s)
    site_draw(d)
    if overlay:
        overlay(d)
    s.scale = 96; s.ox, s.oy = 3.2, 21.9
    dim_chain(s, [0, SITE["W"] * 12], -(19 if SITE["alley"] else 3) * 12, "h", -0.3)
    dim_chain(s, [0, SITE["D"] * 12], (SITE["W"] + 3) * 12, "v", 0.4)
    s.scale = 48
    SL.drawing_title(s, 1.0, 1.35 if M == 2 else 1.6, "1", no, ttl, "SCALE: 1/8\" = 1'-0\"   TYPICAL LOT — REPLACE WITH SURVEY", w=13.6, scalebar=False)
    SL.north_arrow(s, 14.6 if M == 3 else 13.6, 4.0)
    notes(s, NC, TOPY, f"{ttl.split(' — ')[0]} NOTES", nts, 10.6)
    msave(s, no, file, tb)


def ov_grading(d):
    for (x, y, w, h, t) in SITE["bldgs"]:
        for (px, py, ang) in ((x - 3, y + h / 2, 180), (x + w + 3, y + h / 2, 0), (x + w / 2, y + h + 3, 90), (x + w / 2, y - 3, 270)):
            a = math.radians(ang); d.color = BLUE
            d.arrow((px, py), (px + 3.5 * math.cos(a), py + 3.5 * math.sin(a)), "m", 0.8)
            d.color = None
    d.T(SITE["W"] / 2, SITE["D"] - 4, "SWALES TO RETENTION BASINS; 5% AWAY FROM BUILDINGS FOR 10'", 0.06)


def ov_util(d):
    ex, ey = SITE["entry"]
    b = SITE["bldgs"][0]
    d.color = BLUE; d.PL([(ex + 2, SITE["D"] + 5), (ex + 2, b[1] + b[3])], "h"); d.T(ex + 3.5, SITE["D"] - 6, "1-1/2\" WATER", 0.055, rot=90, align="l")
    d.PL([(ex - 2, SITE["D"] + 5), (ex - 2, b[1] + b[3])], "m", [8, 2]); d.T(ex - 3.5, SITE["D"] - 6, "2\" FIRE SERVICE", 0.055, rot=90, align="l")
    d.color = GREEN; d.PL([(ex + 6, b[1] + b[3]), (ex + 6, SITE["D"] + 5)], "h"); d.T(ex + 7.5, SITE["D"] - 6, "4\" SEWER", 0.055, rot=90, align="l")
    d.color = ORANGE; d.PL([(SITE["W"] - 1.5, SITE["D"] + 5), (SITE["W"] - 1.5, b[1] + 2), (b[0] + b[2], b[1] + 2)], "h", [10, 3])
    d.T(SITE["W"] - 3.0, SITE["D"] / 2, "UG ELECTRIC TO METER CENTER", 0.055, rot=90)
    d.color = None
    if M == 3:
        c = SITE["bldgs"][1]
        d.color = ORANGE; d.PL([(b[0] + b[2], b[1] + 2), (c[0] + c[2] + 2, b[1] + 2), (c[0] + c[2] + 2, c[1] + c[3] / 2), (c[0] + c[2], c[1] + c[3] / 2)], "m", [6, 2])
        d.color = BLUE; d.PL([(ex + 2, b[1]), (ex + 2, c[1] + c[3])], "m"); d.color = GREEN; d.PL([(ex + 6, b[1]), (ex + 6, c[1] + c[3])], "m", [6, 2]); d.color = None
        d.T(ex + 9, (b[1] + c[1] + c[3]) / 2, "SERVICES TO CARRIAGE HOUSE", 0.05, align="l")


def ov_land(d):
    d.color = GREEN
    for (x, y, w, h) in SITE["basins"]:
        d.C(x + w / 2, y + h / 2, 4.5, "l"); d.T(x + w / 2, y + h / 2 - 5.2, "T1", 0.055, font="Helvetica-Bold")
    for (x, y, w, h, t) in SITE["bldgs"]:
        for k in range(int(x) + 2, int(x + w) - 1, 4):
            d.C(k, y + h + 1.5, 0.9, "l", fill=0.9)
    d.color = None
    d.T(SITE["W"] / 2, SITE["D"] - 1.5, "DG 2\" ALL PLANTING AREAS; LOW-WATER ADWR PLANTS; DRIP IRRIGATION", 0.055)


def ov_selec(d):
    d.color = ORANGE
    for (x, y, w, h) in SITE["pave"]:
        for (px, py) in ((x + 1, y + 1), (x + w - 1, y + h - 1)):
            d.C(px, py, 0.8, "m", fill=1.0); d.T(px + 2.2, py + 0.2, "SL-1", 0.05)
    d.color = None


# ============================================================== cover + code
def sheet_G001():
    s = sheetkit.new()
    s.text((1.0, 22.6), "SCOTTSDALE FOURPLEX", 0.55, font="Helvetica-Bold", align="l")
    s.text((1.0, 21.95), f"{NAME}  ·  FOUR DWELLING UNITS  ·  DESIGN DEVELOPMENT SET", 0.2, align="l")
    s.line((1.0, 21.75), (31.8, 21.75), lw="h")
    # street elevation graphic
    s.scale = 96
    b = BLDGS[0]
    face = "W" if M == 2 else "S"
    e = Elev(s, (1.6, 17.8))
    s.scale = 96
    draw_face(e, b, face)
    s.scale = 48
    s.text((5.0, 14.75), f"{FACE[face]} ELEVATION — SEE A-201{SUF}/A-202{SUF}", 0.1, font="Helvetica-Bold")
    y = SL.head(s, 1.0, 14.2, "PROJECT DATA", 8.6)
    rows = [("PROJECT", f"Scottsdale Fourplex — {NAME.title()}"), ("ADDRESS / APN", "TBD (south Scottsdale)"), ("LOT", f"{LOT[0]}' x {LOT[1]}' typical (assumed until a parcel is selected)"),
            ("USE", "Four dwelling units sold whole to one owner-occupant (1–4 unit financing)"), ("GROSS FLOOR AREA", f"±{GFA:,} SF"),
            ("BUILDINGS", " + ".join(f"{b['name'].title()} ({b['w']}' x {b['d']}', {b['stories']} levels)" for b in BLDGS))]
    for u, info in UNITS.items():
        rows.append((f"UNIT {u}", f"{info['t']} · ±{info['sf']:,} SF"))
    for k, v in rows:
        s.text((1.0, y), k, 0.075, font="Helvetica-Bold", align="l"); y = min(para(s, 3.3, y, v, 6.3, 0.075, lead=1.4), y - 0.21) - 0.03
    import re as _re
    _g = open("g001.py").read()
    IDX = [(m.group(1), (m.group(2).encode().decode("unicode_escape") if "\\u" in m.group(2) else m.group(2)), m.group(3)) for m in _re.finditer(r'\("([A-Z]{1,2}-\d{3}(?:\.\d)?)", "([^"]+)", "([^"]+)"\)', _g)]
    sfx = {"A-101.1": f"A-101{SUF}", "A-102.1": f"A-102{SUF}", "A-103.1": f"A-103{SUF}", "A-201.1": f"A-201{SUF}", "A-202.1": f"A-202{SUF}", "A-301.1": f"A-301{SUF}",
           "P-101.1": f"P-101{SUF}", "P-102.1": f"P-102{SUF}"}
    idx = [(sfx.get(a, a), b, "DD-1") for (a, b, c) in IDX]
    if M == 3:
        idx.insert(idx.index((f"A-102{SUF}", "Upper Floor Plan", "DD-1")) + 1, ("A-111.3", "Carriage House Plans", "DD-1"))
    cols = [("SHEET", 0.75, "l"), ("TITLE", 3.35, "l"), ("STATUS", 0.85, "c")]
    half = (len(idx) + 1) // 2
    y3 = SL.head(s, 15.2, 21.4, f"SHEET INDEX — MODEL {M} ({len(idx)} SHEETS)", 10.9)
    table(s, 15.2, y3 + 0.04, cols, idx[:half], h=0.07, rowh=0.165)
    table(s, 21.1, y3 + 0.04, cols, idx[half:], h=0.07, rowh=0.165)
    para(s, 15.2, y3 - (half + 1) * 0.165 - 0.3, f"All Model {M} sheets at DD-1. Typical sheets (notes, details) are shared with the Model 1 prototype and reissued with a Model {M} note. S/M/P/E/FP/C sheets show design intent for the Arizona-registered engineers of record.", 10.9, 0.075)
    msave(s, "G-001", "Cover_Sheet_and_Index", "COVER SHEET\n+ SHEET INDEX")


def sheet_G002():
    s = sheetkit.new()
    f = Flow(s)
    if M == 2:
        occ = ["R-2: four dwelling units in one building; Unit B's suite sits over Unit A, so the building is not a townhouse under the IRC (units are stacked).",
               "Construction type V-B, NFPA 13R sprinklers throughout (Scottsdale amendments).",
               "Allowable (Tables 504.3, 504.4, 506.2, R-2 V-B S13R): 60 ft, 3 stories, 7,000 SF per story. Provided: 2 stories, 2,856 SF per story. Complies.",
               "Separations: 1-hour W1 walls between units, slab to roof deck; F1 1-hour floor/ceiling between Unit B's suite and Unit A (1/2 hour permitted with 13R; 1 hour provided).",
               "Exterior walls: side yards 10'-0\" min. → fire separation distance 10 ft or more → 0-hour exterior walls, unprotected openings unlimited (Table 705.8, sprinklered, FSD 10 to <15 ft: verify 45%/75% limits with final openings).",
               "Means of egress: every unit has its own exterior door at grade; upper levels are within the same unit and reach the exit by the unit's own stair (IBC 1006.3.4, exit access within a dwelling unit). Common path within units under 125 ft.",
               "Stairs inside dwelling units: 7-3/4\" risers max., 10\" treads min., handrail one side, 36\" width (IBC 1011.5.2 exc. 3).",
               "Accessibility: Unit A (single-level ground flat) is Type A. Units B, C, D are multistory units in a building without an elevator and are not covered (IBC 1107.7.2, FHA).",
               "Escape openings at every bedroom (IBC 1031). Smoke/CO alarms per IFC 907.2.11 / 915. No fire alarm system required."]
    else:
        occ = ["MAIN HOUSE: R-2 — three dwelling units (A and B ground flats, owner Unit C on the entire upper floor). Type V-B, NFPA 13R.",
               "Main house allowable (R-2 V-B S13R): 60 ft, 3 stories, 7,000 SF/story. Provided 2 stories, 2,400 SF/story. Complies.",
               "Main house separations: W1 1-hour walls between A, B and the core; F1 1-hour floor/ceiling between the flats and Unit C (1/2 hour permitted with 13R).",
               "Main house egress: shared entry with exits to the exterior; Unit C reaches the exit by its private stair to the shared entry. Single exit per story allowed by Table 1006.3.4(1) for up to 4 units per story and 125 ft travel (sprinklered).",
               "CARRIAGE HOUSE: one dwelling unit (casita D) over two private garages. Design under the IRC as a detached dwelling (verify with Scottsdale) or IBC R-3/U. Garage separation: 5/8\" Type X ceiling under the casita and 1/2\" GWB walls (IRC R302.6); garage-to-garage wall W3 if the garages serve different units.",
               "Carriage house height: three levels (garages, casita, loft). The loft must qualify as a habitable attic or mezzanine (1/3 of the floor below, IRC R202 / IBC 505) or it counts as a story — OPEN ITEM with zoning height limits.",
               "Separation between buildings: 16 ft courtyard. Imaginary line placed 10 ft from the main house → 0-hour main-house wall; carriage house wall at 6 ft is unrated under the IRC with sprinklers (verify).",
               "Exterior stair to Unit D (IBC 1027.6 exception / IRC R311.7) with handrails, 7-3/4\" risers max.",
               "Accessibility: Unit A Type A, Unit B Type B (ground flats in a building without an elevator). Unit C (upper) and casita D are not covered.",
               "Escape openings at every bedroom; smoke/CO alarms; alley access for garages and trash."]
    f.notes(f"CODE ANALYSIS — {NAME}", ["2021 IBC, IFC, IPC, IMC, IECC with City of Scottsdale amendments; 2020 NEC; ICC A117.1-2009; federal Fair Housing Act. VERIFY items at pre-application."] + occ, h=0.09)
    f.table("SUMMARY", [("ITEM", 2.6, "l"), ("REQUIRED / ALLOWED", 2.0, "c"), ("PROVIDED", 2.0, "c")], [
        ("Occupancy", "R-2" if M == 2 else "R-2 + IRC/R-3", "Four dwelling units"), ("Construction", "V-B", "V-B, 13R"),
        ("Stories / height", "3 / 60 ft", "2" if M == 2 else "2 (main), 3 levels (carriage, VERIFY)"),
        ("Area per story", "7,000 SF", "2,856 SF" if M == 2 else "2,400 SF"), ("Unit separations", "1/2 hr (13R)", "1 hr"),
        ("Exterior walls", "0 hr at FSD ≥ 10 ft", "0 hr"), ("Accessibility", "Ground flats covered", f"{TYPEA} Type A" + (f", {TYPEB} Type B" if TYPEB else ""))])
    msave(s, "G-002", "Code_Analysis", "CODE ANALYSIS")


# ============================================================== MEP schedules / one-line / loads
def loads():
    rows = []
    for u, info in UNITS.items():
        sf = info["sf"]
        gen = 3 * sf + 4500 + 12000 + 5000 + 4500 + 1200 + 2400
        dem = 10000 + 0.4 * (gen - 10000)
        hv = 7500 if sf < 1800 else 10500
        tot = dem + hv
        amps = tot / 240
        panel = 125 if amps <= 120 else 150 if amps <= 145 else 200
        rows.append((u, sf, gen + hv, tot, amps, panel))
    return rows


def sheet_E301():
    s = sheetkit.new(); f = Flow(s)
    L = loads()
    f.table("UNIT LOAD CALCULATIONS — NEC 220.82 OPTIONAL METHOD", [("UNIT", 0.6, "c"), ("SF", 0.8, "c"), ("CONNECTED VA", 1.4, "c"), ("DEMAND VA", 1.3, "c"), ("AMPS @240", 1.0, "c"), ("PANEL", 0.9, "c")],
            [(u, f"{sf:,}", f"{c:,.0f}", f"{t:,.0f}", f"{a:.0f}", f"{p}A") for (u, sf, c, t, a, p) in L])
    conn = sum(r[2] for r in L)
    svc = conn * 0.45 + 12000
    f.table("SERVICE — NEC 220.84 (3–5 UNITS, 45%)", [("ITEM", 3.0, "l"), ("VA", 1.4, "c"), ("NOTE", 1.6, "l")], [
        ("Units connected (incl. HVAC)", f"{conn:,.0f}", ""), ("x 45% demand", f"{conn * 0.45:,.0f}", "Table 220.84(B)"), ("House panel", "12,000", "at 100%"),
        ("SERVICE TOTAL", f"{svc:,.0f}", f"= {svc / 240:.0f} A → {400 if svc / 240 <= 400 else 600} A")])
    f.notes("LOAD NOTES", ["Loads use the same all-electric appliance package as Model 1 (range 12 kW, dryer 5 kW, HPWH 4.5 kW, heat pump with strip heat). Larger units carry 10.5 kVA HVAC.",
                           "Panel schedules per Model 1 E-301 typical, sized per this table. Final by the electrical engineer of record."])
    msave(s, "E-301", "Panel_Schedules_Load_Calcs", "PANEL SCHEDULES\n+ LOAD CALCS")
    return svc


def sheet_E201(svc):
    s = sheetkit.new()
    amps = 400 if svc / 240 <= 400 else 600
    s.text((1.6, 21.6), f"MC-1 METER CENTER, {amps}A, 120/240V 1Ø 3W, NEMA 3R", 0.12, font="Helvetica-Bold", align="l")
    s.rect(1.4, 6.0, 15.0, 15.2, lw="h")
    s.line((3.0, 23.0), (3.0, 19.6), lw="m"); s.text((3.2, 22.4), "UTILITY UNDERGROUND SERVICE", 0.07, align="l")
    s.text((3.25, 19.25), f"{amps}A MAIN", 0.08, align="l")
    s.line((2.6, 18.4), (15.4, 18.4), lw="h")
    L = loads()
    cols = [(3.6 + i * 2.6, u, f"{p}A", f"UNIT {u}") for i, (u, sf, c, t, a, p) in enumerate(L)] + [(3.6 + len(L) * 2.6, "HP", "60A", "HOUSE")]
    for (x, u, a, nm) in cols:
        s.line((x, 18.4), (x, 6.0), lw="m")
        s.circle((x, 17.0), 0.22, lw="m", fill=1.0); s.text((x, 16.96), "M", 0.1, font="Helvetica-Bold")
        s.text((x + 0.25, 15.6), a, 0.08, align="l")
        s.rect(x - 1.1, 4.3, 2.2, 1.2, lw="m", fill=1.0); s.line((x, 6.0), (x, 5.5), lw="m")
        s.text((x, 4.95), f"PANEL {u}", 0.085, font="Helvetica-Bold"); s.text((x, 4.7), nm, 0.065)
    SL.drawing_title(s, 1.35, 2.3, "1", "E-201", "ELECTRICAL ONE-LINE DIAGRAM", "NOT TO SCALE   DESIGN INTENT", w=15.0, scalebar=False)
    notes(s, NC, TOPY, "ONE-LINE NOTES", [f"Service {amps}A per the NEC 220.84 calculation on E-301 ({svc:,.0f} VA).",
                                          "Dwelling feeders per NEC 310.12; meters engraved UNIT A–D and HOUSE; main breaker in each unit panel.",
                                          "Grounding: concrete-encased electrode in the PT slab beam plus water pipe bond." + (" Carriage house fed from MC-1 by a separate feeder to Panel D; garages on the house panel or Panel D (VERIFY)." if M == 3 else ""),
                                          "EV-ready circuits per E-401."], 10.6)
    msave(s, "E-201", "One_Line_Diagram", "ONE-LINE\nDIAGRAM")


def sheet_M001():
    s = sheetkit.new(); f = Flow(s)
    rows = []
    for u, info in UNITS.items():
        t = 2.0 if info["sf"] < 1300 else 3.0 if info["sf"] < 2000 else 4.0
        rows.append((u, f"{info['sf']:,}", f"{t:.1f} T", "Ground soffit" if UNITS[u]["lv"] == "g" and u in ("A",) or (M == 3 and u in "AB") else "Attic platform", "SEER2 16 / HSPF2 8.1"))
    f.table("HEAT PUMP SYSTEMS — ONE PER UNIT (PLACEHOLDER SIZES, MANUAL J TO CONFIRM)", [("UNIT", 0.6, "c"), ("SF", 0.8, "c"), ("SIZE", 0.8, "c"), ("AHU LOCATION", 1.6, "l"), ("EFFICIENCY", 1.8, "c")], rows)
    f.notes("MECHANICAL NOTES", ["Same standards as Model 1 M-001: independent systems per unit, Manual J/S/D, sealed ducts, CRDs in rated ceilings, R-8 attic ducts, continuous bath-fan ventilation (IMC 403.3.2), exhausts to the exterior.",
                                 "Townhome systems (Model 2) serve both floors of the unit with the AHU in the attic and a return at each level." if M == 2 else "Casita D system: AHU in the loft knee wall or attic, condenser by the alley pad (Model 3).",
                                 "Condensers on pads at grade, 12\" side clearance, disconnect in sight."])
    msave(s, "M-001", "Mechanical_Notes_Schedules", "MECHANICAL NOTES\n+ SCHEDULES")


def sheet_E001():
    s = sheetkit.new(); f = Flow(s)
    f.notes("ELECTRICAL GENERAL NOTES", ["Same standards as Model 1 E-001: 2020 NEC with Scottsdale amendments; AFCI/GFCI; tamper-resistant receptacles; surge protection; 100% LED; hard-wired interconnected smoke/CO alarms; no boxes in W1 walls; surface fixtures in rated ceilings.",
                                         "Service and panel sizes per E-201 / E-301 for this model.",
                                         f"Unit {TYPEA} (Type A): controls 15\"–48\" A.F.F.; doorbell and visual alarm prewire.",
                                         "Exterior lighting full-cutoff, 3000K (Scottsdale dark sky)."], h=0.09)
    msave(s, "E-001", "Electrical_Notes_Symbols", "ELECTRICAL NOTES\n+ SYMBOLS")


def sheet_P201():
    s = sheetkit.new()
    x0 = 3.0
    s.line((x0, 7.0), (x0, 10.6), lw="h", color=BLUE); s.text((x0 + 0.15, 7.2), "1-1/2\" SERVICE FROM CITY METER", 0.07, align="l")
    for (yy, t) in ((8.2, "BALL VALVE"), (8.9, "PRV + GAUGE"), (9.6, "STRAINER")):
        s.rect(x0 - 0.15, yy - 0.12, 0.3, 0.24, lw="l", fill=1.0); s.text((x0 + 0.3, yy - 0.03), t, 0.07, align="l")
    s.line((x0 - 0.2, 10.6), (x0 + 1.4 * len(UNITS), 10.6), lw="h", color=BLUE)
    for i, u in enumerate(UNITS):
        xx = x0 + 0.5 + i * 1.4
        s.line((xx, 10.6), (xx, 14.4), lw="m", color=BLUE)
        s.circle((xx, 11.3), 0.16, lw="l", fill=1.0); s.text((xx, 11.26), "SM", 0.05)
        s.rect(xx - 0.55, 14.4, 1.1, 0.7, lw="m", fill=1.0); s.text((xx, 14.8), f"WH-{u}", 0.08, font="Helvetica-Bold"); s.text((xx, 14.55), "50 GAL HP", 0.06)
    SL.drawing_title(s, 1.35, 5.6, "1", "P-201", "DOMESTIC WATER RISER (SCHEMATIC)", "NOT TO SCALE   SM = UNIT SUBMETER", w=8.0, scalebar=False)
    notes(s, NC, TOPY, "RISER NOTES", ["DWV stacks per P-101" + SUF + ": one stack per wet-room cluster, 3\" above the lowest floor, 4\" at the base, vented through the roof; same branch sizes as Model 1 (WC 3\", tub/shower 2\", lav 1-1/2\", sink 2\").",
                                       "Water: one City meter, PRV if over 80 psi, unit submeters and shutoffs, heat pump water heater per unit with PEX manifold.",
                                       "Typical DWV riser diagram: see Model 1 P-201 (same stack arrangement per wet-room cluster)."], 10.6)
    msave(s, "P-201", "DWV_and_Water_Riser_Diagrams", "DWV + WATER\nRISER DIAGRAMS")


# ============================================================== dispatcher
JOBS = {
    "A-103": sheet_A103, "A-201": lambda: sheet_elev("A-201" + SUF, ("S", "N")), "A-202": lambda: sheet_elev("A-202" + SUF, ("W", "E")),
    "A-301": sheet_A301, "A-401": lambda: sheet_enlarged("A-401", ("KITCHEN",), "KITCHEN", "ENLARGED PLANS\nKITCHENS"),
    "A-402": lambda: sheet_enlarged("A-402", ("BATH",), "BATH", "ENLARGED PLANS\nBATHS"), "A-601": sheet_A601,
    "S-101": lambda: struct_plan("S-101", "fdn", "FOUNDATION PLAN", "FOUNDATION PLAN"), "S-102": lambda: struct_plan("S-102", "floor", "FLOOR FRAMING PLAN", "FLOOR FRAMING\nPLAN"),
    "S-103": lambda: struct_plan("S-103", "roof", "ROOF FRAMING PLAN", "ROOF FRAMING\nPLAN"),
    "C-101": lambda: site_sheet("C-101", f"ARCHITECTURAL SITE PLAN — MODEL {M}", "SITE PLAN", None, [
        "Typical lot drawn from the concept site plan; replace with a boundary and topographic survey when a parcel is selected.",
        "Zoning district, setbacks, height, lot coverage and parking count are VERIFY items for pre-application.",
        "Fire access within 150 ft hose lay of the street (IFC 503.1.1), sprinklered 13R; confirm with the Fire Marshal" + (" — the deep Model 2 lot uses the 12 ft drive as fire access (OPEN)." if M == 2 else " — alley access for the carriage house."),
        "Accessible route from the public walk and the van stall to each covered unit entry, 1:20 max., 2% cross slope."], "Site_Plan"),
    "C-102": lambda: site_sheet("C-102", f"GRADING AND DRAINAGE PLAN — MODEL {M}", "GRADING +\nDRAINAGE PLAN", ov_grading, [
        "Schematic; civil engineer to prepare from survey per the Scottsdale DS&PM.",
        "Finish floor 8\" above adjacent grade; 5% away from buildings for 10 ft.",
        "Retention: 100-yr, 2-hr storm on site (verify). The front basins shown are likely too small, as on Model 1 — add capacity (OPEN).",
        "Basins drain within 36 hours; downspouts to splash blocks and swales."], "Grading_and_Drainage_Plan"),
    "C-103": lambda: site_sheet("C-103", f"UTILITY PLAN — MODEL {M}", "UTILITY PLAN", ov_util, [
        "Schematic; civil engineer and utilities to design. One City water meter, separate fire service with backflow, 4\" sewer, underground electric to the meter center.",
        "Gas not in the base design (all-electric). Call Arizona 811 before digging."], "Utility_Plan"),
    "L-101": lambda: site_sheet("L-101", f"LANDSCAPE PLAN — MODEL {M}", "LANDSCAPE PLAN", ov_land, [
        "Low-water ADWR Phoenix AMA plants, no turf, drip irrigation, smart controller (plant list per Model 1 L-101).",
        "Shade trees in the front basins and courtyards; keep trees 10 ft from foundations and out of fire access."], "Landscape_Plan"),
    "E-401": lambda: site_sheet("E-401", f"SITE ELECTRICAL PLAN — MODEL {M}", "SITE\nELECTRICAL PLAN", ov_selec, [
        "Full-cutoff 3000K site lights on the house panel; 1 fc on the accessible route, 0.1 fc at the property line.",
        "EV-ready 40A circuits to four stalls or garages (confirm Scottsdale requirement)."], "Site_Electrical_Plan"),
    "G-001": sheet_G001, "G-002": sheet_G002, "M-001": sheet_M001, "E-001": sheet_E001, "P-201": sheet_P201,
}

if __name__ == "__main__":
    for k, fn in JOBS.items():
        if want(k) or want(k + SUF):
            fn()
    if want("E-301") or want("E-201"):
        svc = sheet_E301()
        sheet_E201(svc)
