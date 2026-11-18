"""A-201.1 (south + north) and A-202.1 (east + west) exterior elevations, Model 1."""
import math, sys
from cadkit import Sheet
from elev import Elev, WIN, FFU, PLATE, EAVE, GRADE
import sheetlib as SL
from plan_engine import para

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
W, D = 60.0, 50.0
UP = FFU

KEYNOTES = [
    "Smooth three-coat cement plaster (stucco), white sand finish, over WRB and lath; control joints per D-001.",
    "Two-piece clay barrel tile over double-layer underlayment, 4:12 hip roof. Class A roof assembly.",
    "Precast concrete band at the upper floor line; precast sills at every window.",
    "4\" foam window surround with stucco finish, typical all windows.",
    "Stained wood shutters, south face only (not on the rated west wall).",
    "Wrought-iron Juliet rail at the landing window.",
    "Arched loggia: 13'-0\" x 6'-0\", stucco piers, tile roof; shelters the shared zero-step entry, mailboxes and address numbers.",
    "5\" K-style gutter and 3x4 downspout to splash block and retention basin. Keep 3'-0\" from MC-1 and gas meters.",
    "Meter center MC-1 (four units + house meter), 3'-0\" working space in front (E-201).",
    "6'-0\" x 8'-0\" sliding glass door to the rear patio (doors 119 and 131).",
    "Wall light, full cutoff, dark-sky compliant, at every exterior door.",
    "Unit address numbers, 4\" min., contrasting, visible from the street (one address per unit).",
    "2x8 fascia, 2'-0\" stucco soffit; west side overhang 2'-0\" max. (7'-0\" to lot line).",
    "1-hour rated exterior wall W2: 5/8\" Type X exterior gypsum sheathing; unprotected openings 42 SF per story (45 SF allowed).",
    "Stucco weep screed at the slab edge, 4\" min. above grade; finish floor 8\" above finish grade.",
]
GEN = [
    "Elevations show design intent. Window and door sizes, sills and heads per A-601; tags refer to the A-101.1 / A-102.1 schedules.",
    "Window heads at 7'-0\" A.F.F. on both floors; doors 8'-0\" high. Bedroom egress sills 3'-0\" A.F.F. (44\" max.).",
    "Building height: ridge ±29'-0\" above finish floor, ±29'-8\" above finish grade. Confirm Scottsdale's height measurement method at pre-app; fallback is a 3½:12 tile roof.",
    "Exterior colors and materials subject to Scottsdale design review. Santa Barbara style shown (Elevation 2 of the style study).",
    "Attic and roof ventilation per IBC 1202; the W1 unit separation walls continue to the roof deck and divide the attic (G-005).",
]


def facade(e, x0, x1, ops_g, ops_u, roof, loggia=None, shutters=False, ds=(), extras=None, depth=None):
    e.wall(x0, x1)
    zr = e.hip_roof_long(x0, x1, depth) if roof == "long" else e.hip_roof_end(x0, x1)
    for o in ops_g:
        kind = o[0]
        if kind == "W":
            _, a, b, t = o; w, h, sill = WIN[t]
            e.window(a, b, sill, sill + h, t)
        else:
            _, a, b, tag, style = o
            e.door(a, b, 8.0, tag, slider=style == "slider", glass=style == "glass")
            e.light(a - 0.9, 7.2)
    for o in ops_u:
        _, a, b, t = o; w, h, sill = WIN[t]
        e.window(a, b, UP + sill, UP + sill + h, t, shutters=shutters and t != "F", arch=(t == "F"))
    for x in ds:
        e.downspout(x)
    if extras:
        extras(e)
    return zr


def loggia_front(e):
    # projecting loggia on the south face, x 23.5-36.5
    a, b = 23.5, 36.5
    e.rect(a, GRADE, b, 10.2, lw="m", fill=1.0)
    for (c0, c1) in ((24.25, 27.75), (28.25, 31.75), (32.25, 35.75)):
        r = (c1 - c0) / 2; cx = (c0 + c1) / 2; spring = 7.0
        pts = [(c0, 0), (c1, 0), (c1, spring)] + [(cx + r * math.cos(t), spring + r * math.sin(t)) for t in [i * math.pi / 16 for i in range(17)]] + [(c0, spring)]
        e.poly(pts, lw="l", fill=0.82)
    pts = [(a - 1.0, 10.2), (b + 1.0, 10.2), (b - 1.0, 12.0), (a + 1.0, 12.0)]
    e._tile(pts, a - 1, b + 1, 12.0) if False else None
    e.poly(pts, lw="m", fill=1.0)
    z = 10.6
    while z < 11.9:
        xs = e._clip(pts, z); e.line((xs[0], z), (xs[1], z), lw="xf"); z += 0.45
    e.rect(a - 1.0, 9.7, b + 1.0, 10.2, lw="l", fill=1.0)
    # door behind center arch
    e.rect(27.75, 0, 31.25, 6.5, lw="f")
    e.text(30.0, 3.4, "101", 0.06)
    e.text(26.0, 8.6, "1001 · 1003", 0.06, font="Helvetica-Bold")
    e.text(34.0, 8.6, "1005 · 1007", 0.06, font="Helvetica-Bold")
    # Juliet rail at landing window
    e.rect(28.0, UP + 2.0, 32.0, UP + 3.2, lw="f")
    x = 28.2
    while x < 32:
        e.line((x, UP + 2.0), (x, UP + 3.2), lw="xf"); x += 0.35


def loggia_side(e, at_left, x_face):
    """loggia seen from the side, projecting 6' beyond the south face."""
    d = -1 if at_left else 1
    x_out = x_face + d * 6.0
    lo, hi = sorted((x_face, x_out))
    e.rect(lo, GRADE, hi, 10.2, lw="m", fill=1.0)
    c0, c1 = lo + 1.0, hi - 1.0
    r = (c1 - c0) / 2; cx = (c0 + c1) / 2
    pts = [(c0, 0), (c1, 0), (c1, 7.0)] + [(cx + r * math.cos(t), 7.0 + r * math.sin(t)) for t in [i * math.pi / 16 for i in range(17)]] + [(c0, 7.0)]
    e.poly(pts, lw="l", fill=0.82)
    edge = x_out + d * 1.0
    pts = [(edge, 10.2), (x_face, 12.0), (x_face, 10.2)]
    e.poly(pts, lw="m", fill=1.0)
    e.rect(min(edge, x_face), 9.7, max(edge, x_face), 10.2, lw="l", fill=1.0)


def mc1(e):
    # north face seen from the north: plan x maps to 60 - x
    a, b = 60 - 36.9, 60 - 31.9
    e.rect(a, 1.0, b, 6.5, lw="l", fill=0.85)
    for i in range(5):
        xx = a + 0.5 + i * 0.85
        e.s.circle(e.s.m2p((xx + 0.2) * 12, -4.8 * 12), 0.035, layer="A-ANNO-TEXT", lw="f")
    e.text((a + b) / 2, 2.2, "MC-1", 0.065, font="Helvetica-Bold")


def sheet(cfg, views):
    s = Sheet(origin=(0, 0))
    for v in views:
        e = Elev(s, v["origin"])
        zr = v["draw"](e)
        e.grade(v["x0"] - 4, v["x1"] + 4)
        e.levels(v["x1"] + 2.5, zr)
        e.grids(v["grids"])
        e.hdim(v["dims"], GRADE - 1.4)
        for (x, z, n, dx, dz) in v.get("keys", []):
            e.keynote(x, z, n, dx, dz)
        SL.drawing_title(s, 1.35, v["title_y"], v["num"], cfg["sheet_no"], v["title"], "SCALE: 1/4\" = 1'-0\"", w=17.0)
    y = SL.notes_list(s, 21.15, 23.2, "KEYNOTES — EXTERIOR ELEVATIONS", KEYNOTES, 5.1)
    y = SL.notes_list(s, 26.55, 23.2, "GENERAL NOTES — ELEVATIONS", GEN, 5.25)
    y = SL.head(s, 26.55, y, "WINDOW TYPES (SEE A-601)", 5.25)
    for t, txt in (("A", "6'-0\" x 4'-0\" horizontal slider, egress, sill 3'-0\""), ("B", "3'-0\" x 5'-0\" single hung, sill 2'-0\""),
                   ("C", "3'-0\" x 4'-0\" single hung, sill 3'-0\""), ("D", "6'-0\" x 5'-0\" horizontal slider, sill 2'-0\""), ("F", "3'-0\" x 5'-0\" fixed, arch top (landing)")):
        from plan_engine import diamond_tag
        diamond_tag(s, (26.7, y - 0.03), t)
        s.text((26.95, y - 0.06), txt, 0.068, align="l"); y -= 0.3
    for t in cfg.get("extra_notes", []):
        y = para(s, 26.55, y - 0.1, t, 5.25, 0.072)
    SL.border_and_titleblock(s, cfg)
    base = f"{OUT}/{cfg['sheet_no']}_{cfg['file']}"
    s.to_pdf(base + ".pdf", title=f"{cfg['sheet_no']} {cfg['sheet_title']}", author="Scottsdale Fourplex")
    s.to_dxf(base + ".dxf")
    print("wrote", base)


common = dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE)

# ---------------- A-201.1: south (front) and north (rear)
south_g = [("W", 9.5, 15.5, "D"), ("W", 39.5, 45.5, "D"), ("W", 52, 58, "A")]
south_u = [("W", 2, 8, "A"), ("W", 14.5, 20.5, "D"), ("W", 28.5, 31.5, "F"), ("W", 39.5, 45.5, "D"), ("W", 52, 58, "A")]
# north seen from the north: x_e = 60 - x
north_g = [("D", 60 - 10, 60 - 4, "119", "slider"), ("D", 60 - 31.5, 60 - 28.5, "103", "solid"), ("D", 60 - 56, 60 - 50, "131", "slider")]
north_u = [("W", 60 - 10, 60 - 4, "A"), ("W", 60 - 56, 60 - 50, "A")]

v_south = dict(origin=(2.7, 15.05), x0=0, x1=60, num="1", title="SOUTH (STREET) ELEVATION", title_y=13.25,
               draw=lambda e: facade(e, 0, 60, south_g, south_u, "long", shutters=True, ds=(0.6, 59.4), extras=loggia_front, depth=D),
               grids=[(0, "1"), (25, "2"), (35, "3"), (60, "4")], dims=[0, 25, 35, 60],
               keys=[(5, 5, 1, -0.35, 0.3), (46, 25.0, 2, 0.3, 0.3), (50, FFU, 3, 0.2, 0.25), (15.8, 4, 4, 0.3, 0.2), (1.4, UP + 4, 5, -0.4, 0.25),
                     (31.8, UP + 2.6, 6, 0.4, 0.25), (26, 5.0, 7, -0.6, -0.1), (59.4, 12, 8, 0.4, 0.0), (26.0, 8.6, 12, -0.9, 0.2), (40, EAVE - 0.3, 13, 0.3, 0.25), (8, -0.3, 15, 0.3, -0.25)])
v_north = dict(origin=(2.7, 4.25), x0=0, x1=60, num="2", title="NORTH (REAR) ELEVATION", title_y=2.45,
               draw=lambda e: facade(e, 0, 60, north_g, north_u, "long", ds=(0.6, 59.4), extras=mc1, depth=D),
               grids=[(0, "4"), (25, "3"), (35, "2"), (60, "1")], dims=[0, 25, 35, 60],
               keys=[(25.6, 5.5, 9, 0.5, 0.35), (53, 4, 10, 0.4, 0.3), (6.0, 7.2, 11, -0.4, 0.3), (0.6, 12, 8, -0.4, 0.0), (30, 25.0, 2, 0.3, 0.3), (20, 8, 1, 0.3, 0.3)])
sheet(dict(common, sheet_no="A-201.1", file="Model1_Exterior_Elevations_South_North", sheet_title="EXTERIOR\nELEVATIONS"), [v_south, v_north])

# ---------------- A-202.1: east and west
# east seen from the east: x_e = 50 - y (south at left); west seen from the west: x_e = y (north at left)
ew = [(3.75, 9.75, "A"), (19.75, 25.75, "A"), (29.5, 35.5, "D"), (40.5, 46.5, "A")]
east_g = [("W", 50 - b, 50 - a, t) for a, b, t in ew]
east_u = list(east_g)
wwin = [(21.25, 24.25, "B"), (31, 34, "B"), (42, 45, "C")]
west_g = [("W", a, b, t) for a, b, t in wwin]
west_u = list(west_g)


def east_extra(e):
    loggia_side(e, True, 0.0)


def west_extra(e):
    loggia_side(e, False, 50.0)
    e.text(25, 8.7, "1-HR RATED WALL W2 · OPENINGS 42 SF / STORY (45 SF ALLOWED) · 7'-0\" TO LOT LINE", 0.065, font="Helvetica-Bold")


v_east = dict(origin=(4.2, 15.05), x0=-6, x1=50, num="1", title="EAST ELEVATION (DRIVEWAY SIDE)", title_y=13.25,
              draw=lambda e: facade(e, 0, 50, east_g, east_u, "end", ds=(0.6, 49.4), extras=east_extra),
              grids=[(0, "B"), (50, "A")], dims=[-6, 0, 50],
              keys=[(30, 4, 4, 0.3, 0.3), (25, 24.5, 2, 0.3, 0.3), (-3, 5, 7, -0.4, 0.3), (20, FFU, 3, 0.3, 0.25), (8, -0.3, 15, 0.3, -0.25)])
v_west = dict(origin=(4.2, 4.25), x0=0, x1=56, num="2", title="WEST ELEVATION (7'-0\" SIDE YARD, RATED WALL)", title_y=2.45,
              draw=lambda e: facade(e, 0, 50, west_g, west_u, "end", ds=(0.6, 49.4), extras=west_extra),
              grids=[(0, "A"), (50, "B")], dims=[0, 50, 56],
              keys=[(22.75, 4, 14, -0.3, 0.35), (10, EAVE - 0.3, 13, 0.3, 0.25), (25, 24.5, 2, 0.3, 0.3)])
sheet(dict(common, sheet_no="A-202.1", file="Model1_Exterior_Elevations_East_West", sheet_title="EXTERIOR\nELEVATIONS",
           extra_notes=["West wall (W2): no wood shutters, vents or combustible trim; roof overhang 2'-0\" max.; any dryer or bath exhaust terminal counts against the 3 SF left in the opening budget (M-001)."]),
      [v_east, v_west])
