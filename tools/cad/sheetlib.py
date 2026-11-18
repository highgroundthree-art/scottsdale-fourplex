"""Shared sheet furniture: border, title block, headings, legends, schedules, drawing titles."""
import math
from cadkit import text_w
from plan_engine import hex_tag, circle_tag, diamond_tag, bubble, room_tag, para, table

TB = 32.15


def head(s, x, y, t, w=5.1):
    s.text((x, y), t, 0.1, font="Helvetica-Bold", align="l")
    s.line((x, y - 0.06), (x + w, y - 0.06), lw="l")
    return y - 0.24


def border_and_titleblock(s, cfg):
    s.rect(0.5, 0.375, 35.25, 23.25, layer="A-ANNO-TTLB", lw="xh")
    s.line((TB, 0.375), (TB, 23.625), layer="A-ANNO-TTLB", lw="h")
    tw = 35.75 - TB
    st = {"yy": 23.625}

    def box(hgt, lines, title=None):
        y0 = st["yy"] - hgt
        s.line((TB, y0), (35.75, y0), layer="A-ANNO-TTLB", lw="l")
        ty = st["yy"] - 0.18
        if title:
            s.text((TB + 0.12, ty), title, 0.062, font="Helvetica-Bold", align="l"); ty -= 0.18
        for (t, h, f) in lines:
            s.text((TB + 0.12, ty), t, h, font=f, align="l"); ty -= h * 1.6
        st["yy"] = y0
        return y0
    H, B = "Helvetica", "Helvetica-Bold"
    box(1.25, [("", 0.12, H), ("SCOTTSDALE", 0.2, B), ("FOURPLEX", 0.2, B), ("DIGNITY-BASED ATTAINABLE HOUSING", 0.068, H)])
    box(1.0, [(cfg["model_line"], 0.085, B), ("SOUTH SCOTTSDALE, ARIZONA", 0.075, H), ("PARCEL / ADDRESS: TBD", 0.075, H), (cfg["lot_line"], 0.075, H)], "PROJECT")
    box(0.95, [("________________________", 0.075, H), ("", 0.075, H), ("________________________", 0.075, H)], "OWNER / DEVELOPER")
    box(0.95, [("________________________", 0.075, H), ("", 0.075, H), ("________________________", 0.075, H)], "ARCHITECT OF RECORD")
    box(0.95, [("STRUCTURAL: TBD", 0.068, H), ("MEP / FIRE PROTECTION: TBD", 0.068, H), ("CIVIL: TBD", 0.068, H)], "CONSULTANTS")
    y0 = box(3.0, [], "SEAL")
    s.rect(TB + 0.5, y0 + 0.35, tw - 1.0, 2.2, layer="A-ANNO-TTLB", lw="f", dash="HIDDEN")
    for i, (t, h, f) in enumerate([("DESIGN DEVELOPMENT", 0.1, B), ("NOT FOR CONSTRUCTION", 0.1, B), ("Not for permit, bidding or", 0.068, H),
                                   ("construction until sealed by", 0.068, H), ("an Arizona-registered", 0.068, H), ("design professional.", 0.068, H)]):
        s.text((TB + tw / 2, y0 + 1.62 - [0, .22, .47, .60, .73, .86][i]), t, h, font=f)
    box(1.05, [("2021 IBC · GROUP R-2 · TYPE V-B", 0.068, H), ("NFPA 13R · 1-HR UNIT SEPARATIONS", 0.068, H),
               ("CITY OF SCOTTSDALE AMENDMENTS", 0.068, H), ("ICC A117.1-2009 (TYPE A + TYPE B)", 0.068, H)], "CODE BASIS")
    y0 = box(1.55, [], "ISSUES / REVISIONS")
    ry = y0 + 1.15
    for a, b, c_ in cfg.get("revs", [("1.4", "2026-11-14", "CONCEPT COORDINATION"), ("DD-1", cfg["date"], "DESIGN DEVELOPMENT")]):
        s.text((TB + 0.12, ry), a, 0.066, align="l", font=B); s.text((TB + 0.55, ry), b, 0.066, align="l"); s.text((TB + 1.35, ry), c_, 0.066, align="l")
        ry -= 0.17
    for _ in range(3):
        s.line((TB + 0.12, ry + 0.06), (35.6, ry + 0.06), layer="A-ANNO-TTLB", lw="xf"); ry -= 0.17
    box(1.25, [(f"PROJECT NO.   {cfg['projno']}", 0.068, H), (f"DATE            {cfg['date']}", 0.068, H),
               ("SCALE           1/4\" = 1'-0\"", 0.068, H), ("DRAWN / CHK   — / —", 0.068, H)], "")
    lines = [(t, 0.14, B) for t in cfg["sheet_title"].split("\n")]
    box(0.35 + 0.23 * len(lines), lines, "SHEET TITLE")
    s.text((TB + 0.12, st["yy"] - 0.2), "SHEET", 0.062, font=B, align="l")
    s.text((TB + tw / 2, 0.375 + 0.75), cfg["sheet_no"], 0.42 if len(cfg["sheet_no"]) <= 7 else 0.36, font=B)


def drawing_title(s, x, y, num, sheet_no, title, sub, w=13.0, scalebar=True):
    s.circle((x + 0.35, y + 0.2), 0.32, layer="A-ANNO-TEXT", lw="m", fill=1.0)
    s.line((x + 0.03, y + 0.2), (x + 0.67, y + 0.2), layer="A-ANNO-TEXT", lw="f")
    s.text((x + 0.35, y + 0.28), num, 0.15, font="Helvetica-Bold")
    s.text((x + 0.35, y + 0.03), sheet_no, 0.07)
    s.text((x + 0.85, y + 0.27), title, 0.19, font="Helvetica-Bold", align="l")
    s.line((x + 0.85, y + 0.18), (x + w, y + 0.18), layer="A-ANNO-TEXT", lw="h")
    s.text((x + 0.85, y - 0.02), sub, 0.09, align="l")
    if scalebar:
        sbx, sby = x + w - 2.4, y - 0.08
        for i in range(4):
            s.rect(sbx + i * 0.25, sby, 0.25, 0.06, layer="A-ANNO-TEXT", lw="xf", fill=0.1 if i % 2 == 0 else 1.0)
        s.rect(sbx + 1.0, sby, 1.0, 0.06, layer="A-ANNO-TEXT", lw="xf", fill=1.0)
        for v, lab in ((0, "0"), (0.5, "2'"), (1.0, "4'"), (2.0, "8'")):
            s.text((sbx + v, sby + 0.1), lab, 0.06)


def north_arrow(s, nx, ny, angle=90):
    """angle: paper direction north points, degrees (90 = up)."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a); px_, py_ = -uy, ux
    P = lambda f, g: (nx + ux * f + px_ * g, ny + uy * f + py_ * g)
    s.circle((nx, ny), 0.38, layer="A-ANNO-SYMB", lw="l")
    s.pline([P(0.55, 0), P(-0.25, 0.17), P(-0.08, 0), P(-0.25, -0.17)], closed=True, layer="A-ANNO-SYMB", lw="l", fill=0.08)
    tp = P(0.72, 0)
    s.text((tp[0], tp[1] - 0.06), "N", 0.13, layer="A-ANNO-SYMB", font="Helvetica-Bold")


WALL_DESC = {
    "W1": (0.32, "UNIT SEPARATION — 1 HR. Double 2x4 @ 16\" o.c. with 1\" air space, 3½\" batts each stud row, 5/8\" Type X GWB each face (UL U341, verify). ±9½\". To roof deck."),
    "W2": (0.32, "EXTERIOR — 1 HR, RATED BOTH SIDES (7'-0\" to lot line). 2x6 @ 16\", 5/8\" Type X exterior gypsum sheathing, WRB, 7/8\" three-coat stucco, R-21 batts, 5/8\" Type X GWB."),
    "W3": (0.32, "GARAGE FIRE BARRIER — 1 HR. 2x6 @ 16\", 5/8\" Type X GWB each face, R-21 batts (UL U305, verify). Full height to the rated floor/ceiling above."),
    "E1": (0.62, "EXTERIOR. 2x6 @ 16\", 7/16\" OSB, WRB, 7/8\" three-coat stucco, R-21 batts, 1/2\" GWB."),
    "P1": (0.70, "INTERIOR PARTITION. 2x4 @ 16\", 1/2\" GWB each face; moisture-resistant board at wet walls, cement board at tub and shower surrounds."),
}


def wall_legend(s, x, y, types, w=5.1, H=0.075):
    y = head(s, x, y, "WALL TYPES", w)
    for tag in types:
        g, txt = WALL_DESC[tag]
        s.rect(x, y - 0.12, 0.42, 0.18, layer="A-ANNO-TEXT", lw="l", fill=g)
        hex_tag(s, (x + 0.7, y - 0.03), tag)
        y = para(s, x + 0.95, y, txt, w - 0.95, H)
    return y


def symbols(s, x, y, w=5.1):
    y = head(s, x, y, "SYMBOLS", w)
    sym = [
        (lambda c: circle_tag(s, c, "201"), "DOOR TAG"),
        (lambda c: diamond_tag(s, c, "A"), "WINDOW TAG"),
        (lambda c: hex_tag(s, c, "W1"), "WALL TYPE TAG"),
        (lambda c: bubble(s, c, "2", r=0.13), "GRID LINE"),
        (lambda c: s.circle(c, 0.13, layer="A-ANNO-NPLT", lw="f", dash="HIDDEN"), "5'-0\" TURNING SPACE"),
        (lambda c: s.line((c[0] - 0.2, c[1]), (c[0] + 0.2, c[1]), layer="A-FLOR-OVHD", lw="f", dash="HIDDEN"), "OVERHEAD / ABOVE"),
    ]
    colw = w / 2
    for i, (fn, label) in enumerate(sym):
        cx = x + 0.2 + (i % 2) * colw
        cy = y - (i // 2) * 0.34
        fn((cx, cy - 0.02))
        s.text((cx + 0.28, cy - 0.05), label, 0.062, align="l")
    return y - ((len(sym) + 1) // 2) * 0.34 - 0.1


DCOLS = [("NO.", 0.38, "c"), ("LOCATION", 1.42, "l"), ("SIZE", 0.95, "c"), ("TYPE", 0.38, "c"), ("RATING", 0.6, "c"), ("HARDWARE", 0.82, "l"), ("NOTE", 0.7, "l")]
WCOLS = [("TYPE", 0.42, "c"), ("SIZE (W x H)", 0.98, "c"), ("OPERATION", 1.02, "l"), ("SILL A.F.F.", 0.72, "c"), ("EGRESS", 0.58, "c"), ("QTY", 0.38, "c"), ("LOCATION", 1.15, "l")]
DOOR_TYPES = ("TYPES: A insulated fiberglass, exterior, 1¾\"; C solid-core wood 1¾\", 20-min label; D solid-core wood flush, 1¾\"; "
              "E bypass, solid-core; F bi-fold, solid-core; G insulated steel overhead sectional, opener.")
DOOR_NOTES = ("NOTES: 1 Type A unit or accessible route: lever hardware, 32\" clear, 5 lbf max. opening force, ½\" max. threshold. "
              "5 Self-closing, positive latching, smoke gasketing (S-label). 6 Combustion and make-up air per IFGC if gas option. 7 Self-closing, gasketed, between garage and dwelling (IRC/IBC 406).")
WIN_NOTE = ("Dual-pane low-E vinyl or fiberglass, U-factor 0.40 max., SHGC 0.25 max. (IECC 2021, climate zone 2B). Safety glazing where required by IBC 2406. "
            "Egress windows: 5.7 SF min. net clear (5.0 SF at grade floor), 24\" min. clear height, 20\" min. clear width, sill 44\" max.; verify with the manufacturer.")


def door_schedule(s, x, y, rows, w=5.25):
    y = head(s, x, y, "DOOR SCHEDULE", w)
    y = table(s, x, y + 0.04, DCOLS, rows, h=0.066, rowh=0.15)
    y -= 0.12
    for t in (DOOR_TYPES, DOOR_NOTES):
        y = para(s, x, y, t, w, 0.068)
    return y - 0.06


def window_schedule(s, x, y, rows, w=5.25):
    y = head(s, x, y, "WINDOW SCHEDULE", w)
    y = table(s, x, y + 0.04, WCOLS, rows, h=0.066, rowh=0.15)
    y -= 0.12
    return para(s, x, y, WIN_NOTE, w, 0.068) - 0.06


def notes_list(s, x, y, title, items, w=5.1, h=0.075, numbering="num"):
    y = head(s, x, y, title, w)
    for i, n in enumerate(items, 1):
        lab = f"{i}." if numbering == "num" else f"{chr(96 + i)}."
        y = para(s, x, y, n, w, h, num=lab)
    return y - 0.08


def area_summary(s, x, y, title, rows, w=5.25):
    y = head(s, x, y, title, w)
    cols = [("SPACE", 2.45, "l"), ("BEDS / BATHS", 0.9, "c"), ("ACCESSIBILITY", 1.2, "c"), ("GROSS SF", 0.7, "c")]
    return table(s, x, y + 0.04, cols, rows, h=0.066, rowh=0.15) - 0.12
