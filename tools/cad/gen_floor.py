"""Concept floor (SVG) -> CAD plan view on a Sheet."""
import math, re
import numpy as np
from floorparse import parse_floor, UNITC
from concept_parse import parse
from plan_engine import (Plan, dim_chain, bubble, hex_tag, circle_tag, diamond_tag, room_tag, R as MR, G as LG)

F = 12.0
OPEN_NAMES = ("LIVING", "DINING", "KITCHEN", "HALL", "FOYER", "FAMILY", "GREAT ROOM", "NOOK", "LANDING", "SHARED", "STAIR", "U-STAIR", "ENTRY", "KITCHENETTE")
SMALL = ("CH", "WH", "CL", "LIN", "STOR", "FR", "WIC", "R")
RENAME = {
    "PRIMARY BED": "PRIMARY\nBEDROOM", "SUITE BED": "SUITE\nBEDROOM", "BED 2": "BEDROOM 2", "BED 3": "BEDROOM 3", "BED": "BEDROOM",
    "SITTING / BED 5": "SITTING /\nBEDROOM 5", "FLEX / OFFICE": "FLEX /\nOFFICE", "LIVING / DINING": "LIVING /\nDINING",
    "ENTRY / DINING": "ENTRY /\nDINING", "LAUNDRY + WH": "LAUNDRY\n+ WH", "LOFT / BED 4": "LOFT /\nBEDROOM 4",
    "PRIMARY BATH": "PRIMARY\nBATH", "SUITE BATH": "SUITE\nBATH", "ROLL-IN BATH": "ROLL-IN\nBATH", "HALL BATH 2": "HALL\nBATH 2",
    "SHARED ENTRY": "SHARED\nENTRY", "FAMILY ROOM": "FAMILY\nROOM", "GREAT ROOM": "GREAT\nROOM", "STAIR TO C": "STAIR\nTO C",
    "STAIR TO LOFT": "STAIR", "STAIR (OPEN BELOW)": "STAIR", "GARAGE 1": "GARAGE 1", "GARAGE 2": "GARAGE 2",
}
DIMRE = re.compile(r"\d+'")


def transform(d, W, D, rot):
    """rot: None or 'cw' (north -> page right). Returns new dict and new (W,D)."""
    if not rot:
        return d, W, D
    P = lambda x, y: (round(D - y, 3), x)
    out = dict(rooms=[], doors=[], wins=[], fx=[], texts=[], treads=[])
    for r in d["rooms"]:
        r2 = dict(r); r2.update(x=round(D - r["y"] - r["h"], 3), y=r["x"], w=r["h"], h=r["w"]); out["rooms"].append(r2)
    for x in d["doors"]:
        out["doors"].append(dict(a=P(*x["a"]), b=P(*x["b"]), leaf=P(*x["leaf"])))
    for w in d["wins"]:
        out["wins"].append(dict(x=round(D - w["y"] - w["h"], 3), y=w["x"], w=w["h"], h=w["w"]))
    for f in d["fx"]:
        g = dict(f)
        if f["k"] == "rect":
            g.update(x=round(D - f["y"] - f["h"], 3), y=f["x"], w=f["h"], h=f["w"])
        elif f["k"] == "ell":
            c = P(f["cx"], f["cy"]); g.update(cx=c[0], cy=c[1], rx=f["ry"], ry=f["rx"])
        else:
            c = P(f["cx"], f["cy"]); g.update(cx=c[0], cy=c[1])
        out["fx"].append(g)
    for t in d["texts"]:
        c = P(t["x"], t["y"]); g = dict(t); g.update(x=c[0], y=c[1]); out["texts"].append(g)
    for (a, b) in d.get("treads", []):
        out["treads"].append((P(*a), P(*b)))
    return out, D, W


def extra_parse(path, ppf, origin):
    """tread lines (#888) and red chase rects."""
    vb, els = parse(path)
    ox, oy = origin
    X = lambda v: round((float(v) - ox) / ppf, 3); Y = lambda v: round((float(v) - oy) / ppf, 3)
    treads, chases, turns = [], [], []
    for e in els:
        if e["_t"] == "line" and e.get("stroke") == "#888":
            treads.append(((X(e["x1"]), Y(e["y1"])), (X(e["x2"]), Y(e["y2"]))))
        if e["_t"] == "rect" and e.get("stroke") == "#c00" and e.get("stroke-width") == "2":
            chases.append(dict(x=X(e["x"]), y=Y(e["y"]), w=float(e["width"]) / ppf, h=float(e["height"]) / ppf))
        if e["_t"] == "circle" and e.get("stroke-dasharray"):
            turns.append((X(e["cx"]), Y(e["cy"]), float(e["r"]) / ppf))
    return treads, chases, turns


def label_of(r, texts):
    ins = [t for t in texts if r["x"] - 0.01 <= t["x"] <= r["x"] + r["w"] + 0.01 and r["y"] - 0.01 <= t["y"] <= r["y"] + r["h"] + 0.01 and t["fs"] >= 6.5]
    names = [t for t in ins if not DIMRE.search(t["t"]) and t["t"] not in ("R",) and "PULL-OUT" not in t["t"] and t["t"].strip()]
    return names


class View:
    def __init__(self, s, cfg):
        self.s, self.cfg = s, cfg
        c = cfg
        d = parse_floor(c["svg"], c["ppf"], c["origin"])
        tr, ch, tu = extra_parse(c["svg"], c["ppf"], c["origin"])
        d["treads"] = tr
        W, D = c["W"], c["D"]
        shift = c.get("shift", (0, 0))
        if shift != (0, 0):
            for r in d["rooms"]:
                r["x"] -= shift[0]; r["y"] -= shift[1]
            for k in ("a", "b", "leaf"):
                for x in d["doors"]:
                    x[k] = (x[k][0] - shift[0], x[k][1] - shift[1])
            for w in d["wins"]:
                w["x"] -= shift[0]; w["y"] -= shift[1]
            for f in d["fx"]:
                if f["k"] == "rect":
                    f["x"] -= shift[0]; f["y"] -= shift[1]
                else:
                    f["cx"] -= shift[0]; f["cy"] -= shift[1]
            for t in d["texts"]:
                t["x"] -= shift[0]; t["y"] -= shift[1]
            d["treads"] = [((a[0] - shift[0], a[1] - shift[1]), (b[0] - shift[0], b[1] - shift[1])) for a, b in d["treads"]]
            ch = [dict(x=q["x"] - shift[0], y=q["y"] - shift[1], w=q["w"], h=q["h"]) for q in ch]
            tu = [(a - shift[0], b - shift[1], r) for a, b, r in tu]
        self.chases_red = ch; self.turns = tu
        d, W, D = transform(d, W, D, c.get("rot"))
        if c.get("rot"):
            self.chases_red = [dict(x=round(c["D"] - q["y"] - q["h"], 3), y=q["x"], w=q["h"], h=q["w"]) for q in ch]
            self.turns = [(round(c["D"] - b, 3), a, r) for a, b, r in tu]
        self.W, self.D, self.d = W, D, d
        # rooms edits
        rooms = [r for r in d["rooms"] if r["x"] >= -0.01 and r["y"] >= -0.01 and r["x"] + r["w"] <= W + 0.01 and r["y"] + r["h"] <= D + 0.01]
        self.outside = [r for r in d["rooms"] if r not in rooms]
        for fn in c.get("room_edits", []):
            rooms = fn(rooms)
        self.rooms = rooms

    # ------------------------------------------------------------------
    def build(self):
        s, c = self.s, self.cfg
        W, D = self.W, self.D
        p = self.p = Plan(s, W, D)
        texts = self.d["texts"]
        # unit assignment
        for r in self.rooms:
            r["unit"] = UNITC.get(r.get("color")) if r.get("color") else None
            r["names"] = []
        for t in texts:
            if t["fs"] < 6.5 or DIMRE.search(t["t"]) or t["t"] in ("R",) or "PULL-OUT" in t["t"] or not t["t"].strip():
                continue
            cand = [r for r in self.rooms if r["x"] - 0.01 <= t["x"] <= r["x"] + r["w"] + 0.01 and r["y"] - 0.01 <= t["y"] <= r["y"] + r["h"] + 0.01]
            if cand:
                min(cand, key=lambda r: r["w"] * r["h"])["names"].append(t)
        for r in self.rooms:
            if len(r["names"]) > 1:
                big = [t for t in r["names"] if t["t"] not in SMALL]
                if big:
                    r["names"] = big
            if r.get("force_name") is not None:
                nm = r["force_name"]
                r["names"] = [dict(x=r["x"] + r["w"] / 2, y=r["y"] + r["h"] / 2, t=nm, fs=8.5)] if nm else []
        for (rect, u) in c.get("unit_rects", []):
            for r in self.rooms:
                if r["x"] >= rect[0] - 0.01 and r["y"] >= rect[1] - 0.01 and r["x"] + r["w"] <= rect[0] + rect[2] + 0.01 and r["y"] + r["h"] <= rect[1] + rect[3] + 0.01:
                    r["unit"] = u
        # untinted: majority neighbor unit
        nx, ny = int(W * 12 / LG), int(D * 12 / LG)
        idx = np.full((ny, nx), -1, int)
        for i, r in enumerate(self.rooms):
            idx[int(round(r["y"] * 4)):int(round((r["y"] + r["h"]) * 4)), int(round(r["x"] * 4)):int(round((r["x"] + r["w"]) * 4))] = i
        for _ in range(3):
            for i, r in enumerate(self.rooms):
                if r["unit"]:
                    continue
                m = (idx == i)
                nb = np.zeros_like(m)
                nb[1:, :] |= m[:-1, :]; nb[:-1, :] |= m[1:, :]; nb[:, 1:] |= m[:, :-1]; nb[:, :-1] |= m[:, 1:]
                nb &= ~m
                cnt = {}
                for j in np.unique(idx[nb]):
                    if j >= 0 and self.rooms[j]["unit"]:
                        cnt[self.rooms[j]["unit"]] = cnt.get(self.rooms[j]["unit"], 0) + int((idx[nb] == j).sum())
                if cnt:
                    r["unit"] = max(cnt, key=cnt.get)
        # groups
        for i, r in enumerate(self.rooms):
            nm = " ".join(t["t"] for t in r["names"]).upper()
            is_open = (r.get("op") == 0.03) or nm == "HALL" or any(nm.startswith(k) for k in OPEN_NAMES if k != "HALL")
            if "BATH" in nm or "POWDER" in nm:
                is_open = False
            if r["fill"].startswith("url") or nm in ("CH",):
                is_open = False
            if "STAIR" in nm or (r["fill"] == "#fff" and not r.get("color") and r["w"] <= 1.01) or (r["fill"] == "#f1f1f1" and r["w"] <= 1.01):
                is_open = True
            custom = None
            for (rect, g) in c.get("group_rects", []):
                if abs(r["x"] - rect[0]) < .01 and abs(r["y"] - rect[1]) < .01 and abs(r["w"] - rect[2]) < .01 and abs(r["h"] - rect[3]) < .01:
                    if g in ("open", "closed"):
                        is_open = g == "open"
                    else:
                        is_open, custom = True, g
            r["open"] = is_open
            r["group"] = custom or ((r["unit"] or "X") + "O" if is_open else f"S{i}")
        # spaces to plan (draw order = overlap order)
        for i, r in enumerate(self.rooms):
            p.space(f"S{i}", r["unit"] or "X", r["group"], [(r["x"], r["y"], r["w"], r["h"])])
        p.build_walls(west_type=c.get("west_type", "EXT"), pair_type=c.get("pair_type"))
        # openings
        self.door_list = []
        for k, dd in enumerate(self.d["doors"]):
            a, b, lf = dd["a"], dd["b"], dd["leaf"]
            if abs(a[1] - b[1]) < 0.01:
                o = "h"; sd = 0 if abs(lf[1] - a[1]) < 0.01 else (1 if lf[1] > a[1] else -1)
            else:
                o = "v"; sd = 0 if abs(lf[0] - a[0]) < 0.01 else (1 if lf[0] > a[0] else -1)
            # snap opening to 3'-0" centered when ~2.8'
            L = abs(b[0] - a[0]) + abs(b[1] - a[1])
            if 2.6 < L < 3.0:
                mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                if o == "h":
                    sgn = 1 if b[0] > a[0] else -1
                    a, b = (mid[0] - 1.5 * sgn, a[1]), (mid[0] + 1.5 * sgn, b[1])
                else:
                    sgn = 1 if b[1] > a[1] else -1
                    a, b = (a[0], mid[1] - 1.5 * sgn), (b[0], mid[1] + 1.5 * sgn)
            kind = "overhead" if sd == 0 else "swing"
            self.door_list.append(dict(i=k, a=a, b=b, sd=sd if sd else 1, kind=kind, o=o))
        for fn in c.get("door_edits", []):
            self.door_list = fn(self.door_list)
        # auto: laundry / WH / linen -> bifold; closets without doors -> bypass
        self._auto_closets()
        for dd in self.door_list:
            try:
                p.door(dd["a"], dd["b"], dd["sd"], tag=dd.get("tag"), kind=dd["kind"])
                dd["ok"] = True
            except KeyError as e:
                dd["ok"] = False
                print("door skipped", dd, e)
        self.win_list = []
        for w in self.d["wins"]:
            cx, cy = w["x"] + w["w"] / 2, w["y"] + w["h"] / 2
            if w["w"] < w["h"]:
                side = "W" if cx < W / 2 else "E"; a, b = w["y"], w["y"] + w["h"]
            else:
                side = "N" if cy < D / 2 else "S"; a, b = w["x"], w["x"] + w["w"]
            self.win_list.append(dict(side=side, a=a, b=b))
        for fn in c.get("win_edits", []):
            self.win_list = fn(self.win_list)
        for w in self.win_list:
            w["room"] = self._room_at_window(w)
            w["type"] = self._win_type(w)
            p.window(w["side"], w["a"], w["b"], w["type"])
        return self

    # ------------------------------------------------------------------
    def _room_name(self, r):
        if r is None:
            return ""
        if r.get("force_name") is not None:
            return r["force_name"]
        nm = " ".join(t["t"] for t in r["names"]).strip().upper()
        return nm

    def _room_at(self, x, y):
        best = None
        for r in self.rooms:
            if r["x"] - 1e-6 <= x <= r["x"] + r["w"] + 1e-6 and r["y"] - 1e-6 <= y <= r["y"] + r["h"] + 1e-6:
                best = r  # later rects win (overlap order)
        return best

    def _room_at_window(self, w):
        m = (w["a"] + w["b"]) / 2
        pt = {"N": (m, 1.0), "S": (m, self.D - 1.0), "W": (1.0, m), "E": (self.W - 1.0, m)}[w["side"]]
        return self._room_at(*pt)

    def _win_type(self, w):
        L = round((w["b"] - w["a"]) * 2) / 2
        nm = self._room_name(w["room"])
        bed = "BED" in nm or "LOFT" in nm or "SITTING" in nm
        w["egress"] = bed
        if L >= 5.75:
            return "A" if bed else "D"
        if L >= 4.75:
            return "E"
        if "LIVING" in nm or nm.startswith("BED 3"):
            return "C"
        return "B"

    def _auto_closets(self):
        p = self.p
        have = set()
        for dd in self.door_list:
            mid = ((dd["a"][0] + dd["b"][0]) / 2, (dd["a"][1] + dd["b"][1]) / 2)
            for off in (0.4, -0.4):
                q = (mid[0], mid[1] + off) if dd["o"] == "h" else (mid[0] + off, mid[1])
                r = self._room_at(*q)
                if r is not None:
                    have.add(id(r))
            # bifold for laundry / WH / LIN closets the door opens into
            q = (mid[0], mid[1] + 0.4 * dd["sd"]) if dd["o"] == "h" else (mid[0] + 0.4 * dd["sd"], mid[1])
            r_in = self._room_at(*q)
            nm = self._room_name(r_in)
            if dd["kind"] == "swing" and r_in is not None and (nm in ("WH", "LIN", "LAUNDRY") or nm.startswith("LAUNDRY")) and r_in["w"] * r_in["h"] <= 32:
                dd["kind"] = "bifold"; dd["sd"] = -dd["sd"]
        # bypass for closets with no door
        for r in self.rooms:
            nm = self._room_name(r)
            if nm in ("CL",) and id(r) not in have:
                best = None
                for (o, f, a0, b0) in self._edges(r):
                    q = (((a0 + b0) / 2, f + 0.3) if o == "h" else (f + 0.3, (a0 + b0) / 2))
                    q2 = (((a0 + b0) / 2, f - 0.3) if o == "h" else (f - 0.3, (a0 + b0) / 2))
                    other = [x for x in (self._room_at(*q), self._room_at(*q2)) if x is not None and x is not r]
                    if not other:
                        continue
                    on = self._room_name(other[0])
                    if "BED" in on or "LOFT" in on or "SITTING" in on or other[0].get("open"):
                        L = b0 - a0
                        if best is None or L > best[3] - best[2]:
                            best = (o, f, a0, b0)
                if best:
                    o, f, a0, b0 = best
                    m = (a0 + b0) / 2; half = min((b0 - a0) / 2 - 0.5, 3.0)
                    if o == "h":
                        self.door_list.append(dict(a=(m - half, f), b=(m + half, f), sd=1, kind="bypass", o="h"))
                    else:
                        self.door_list.append(dict(a=(f, m - half), b=(f, m + half), sd=1, kind="bypass", o="v"))

    def _edges(self, r):
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        return [("h", y, x, x + w), ("h", y + h, x, x + w), ("v", x, y, y + h), ("v", x + w, y, y + h)]

    # ------------------------------------------------------------------
    def draw(self, level, door_start, room_prefix=None):
        s, c, p = self.s, self.cfg, self.p
        W, D = self.W, self.D
        self._fixtures()
        self._stairs()
        p.draw_walls(); p.draw_openings()
        self._grids()
        self._dims()
        rows = self._tags(level, door_start, room_prefix)
        return rows

    def _fixtures(self):
        s = self.s
        fx = self.d["fx"]
        texts = self.d["texts"]
        for f in fx:
            if f["k"] == "rect":
                if f["w"] < 0.05 or f["h"] < 0.05:
                    continue
                lw = "f" if f["sw"] in ("0.5",) else "l" if f["sw"] in ("0.8", "0.7") else "f"
                if f["sw"] == "1":
                    continue
                s.rect(f["x"] * F, f["y"] * F, f["w"] * F, f["h"] * F, layer="A-FLOR-FIXT", lw=lw, space="m")
                cx, cy = f["x"] + f["w"] / 2, f["y"] + f["h"] / 2
                if any(t["t"] == "R" and f["x"] <= t["x"] <= f["x"] + f["w"] and f["y"] - 0.3 <= t["y"] <= f["y"] + f["h"] + 0.3 for t in texts):
                    s.text((cx * F, cy * F), "REF", 0.05, layer="A-FLOR-FIXT", space="m", valign="m")
                if abs(f["w"] - f["h"]) < 0.05 and 2.2 < f["w"] < 2.6 and f["sw"] == "0.8":
                    pass
            elif f["k"] == "ell":
                pts = [((f["cx"] + f["rx"] * math.cos(a)) * F, (f["cy"] + f["ry"] * math.sin(a)) * F) for a in [i * math.pi / 18 for i in range(36)]]
                s.pline(pts, closed=True, layer="A-FLOR-FIXT", lw="f", space="m")
            elif f["k"] == "circ":
                if f["sw"] == "1":
                    s.circle((f["cx"] * F, f["cy"] * F), f["r"] * F, layer="A-FLOR-FIXT", lw="l", space="m")
                    s.text((f["cx"] * F, f["cy"] * F), "WH", 0.055, layer="A-FLOR-FIXT", space="m", valign="m")
                else:
                    s.circle((f["cx"] * F, f["cy"] * F), f["r"] * F, layer="A-FLOR-FIXT", lw="f", space="m")
        for t in texts:
            if t["t"] in ("ROLL-IN", "TROUGH DRAIN", "TD"):
                s.text((t["x"] * F, t["y"] * F), {"TD": "TRENCH DRAIN"}.get(t["t"], t["t"]), 0.045, layer="A-FLOR-FIXT", space="m", valign="m")
        for (x, y, r) in self.turns:
            s.circle((x * F, y * F), r * F, layer="A-ANNO-NPLT", lw="f", space="m", dash="HIDDEN")
        for q in self.chases_red:
            s.rect(q["x"] * F, q["y"] * F, q["w"] * F, q["h"] * F, layer="A-WALL-RATE", lw="l", space="m")
            s.line((q["x"] * F, q["y"] * F), ((q["x"] + q["w"]) * F, (q["y"] + q["h"]) * F), layer="A-WALL-PATT", lw="xf", space="m")
            s.line(((q["x"] + q["w"]) * F, q["y"] * F), (q["x"] * F, (q["y"] + q["h"]) * F), layer="A-WALL-PATT", lw="xf", space="m")
        for fn in self.cfg.get("extra_draw", []):
            fn(self)

    def _stairs(self):
        s = self.s
        for (a, b) in self.d["treads"]:
            s.line((a[0] * F, a[1] * F), (b[0] * F, b[1] * F), layer="A-FLOR-STRS", lw="f", space="m")
        for r in self.rooms:
            if r["fill"].startswith("url"):
                x0, y0, x1, y1 = r["x"] + 0.45, r["y"] + 0.45, r["x"] + r["w"] - 0.3, r["y"] + r["h"] - 0.3
                k = 0.0
                while k < (x1 - x0) + (y1 - y0):
                    ax, ay, bx, by = x0 + k, y0, x0, y0 + k
                    if ax > x1:
                        ay += ax - x1; ax = x1
                    if by > y1:
                        bx += by - y1; by = y1
                    s.line((ax * F, ay * F), (bx * F, by * F), layer="A-WALL-PATT", lw="xf", space="m")
                    k += 0.5
        for (pos, txt) in self.cfg.get("stair_labels", []):
            s.text((pos[0] * F, pos[1] * F), txt, 0.07, layer="A-ANNO-TEXT", space="m", valign="m", font="Helvetica-Bold")

    def _grids(self):
        s, c = self.s, self.cfg
        W, D = self.W, self.D
        gx, gy = c["grids"]
        off = c.get("grid_off", 1.75)
        top = s.m2p(0, 0)[1]; bot = s.m2p(0, D * F)[1]; lft = s.m2p(0, 0)[0]; rgt = s.m2p(W * F, 0)[0]
        for x, lab in gx:
            px = s.m2p(x * F, 0)[0]
            s.line((px, top + off - 0.2), (px, top + 0.08), layer="A-GRID", lw="xf")
            s.line((px, bot - 0.08), (px, bot - off + 0.2), layer="A-GRID", lw="xf")
            bubble(s, (px, top + off), lab); bubble(s, (px, bot - off), lab)
        for y, lab in gy:
            py = s.m2p(0, y * F)[1]
            s.line((lft - off + 0.2, py), (lft - 0.08, py), layer="A-GRID", lw="xf")
            s.line((rgt + 0.08, py), (rgt + off - 0.2, py), layer="A-GRID", lw="xf")
            bubble(s, (lft - off, py), lab); bubble(s, (rgt + off, py), lab)

    def _dims(self):
        s, c = self.s, self.cfg
        W, D = self.W, self.D
        gx = [g[0] for g in c["grids"][0]]; gy = [g[0] for g in c["grids"][1]]
        t1, t2, t3 = c.get("tiers", (0.55, 0.9, 1.25))
        side = {"N": [0, W], "S": [0, W], "W": [0, D], "E": [0, D]}
        for w in self.win_list:
            side[w["side"]].append((w["a"] + w["b"]) / 2)
        for dd in self.door_list:
            if not dd.get("ok"):
                continue
            (ax, ay), (bx, by) = dd["a"], dd["b"]
            if dd["o"] == "h" and (abs(ay) < .01 or abs(ay - D) < .01):
                side["N" if abs(ay) < .01 else "S"].append((ax + bx) / 2)
            if dd["o"] == "v" and (abs(ax) < .01 or abs(ax - W) < .01):
                side["W" if abs(ax) < .01 else "E"].append((ay + by) / 2)
        fi = lambda L: [v * F for v in L]
        dim_chain(s, fi(side["N"]), 0, "h", t1); dim_chain(s, fi(side["S"]), D * F, "h", -t1)
        dim_chain(s, fi(side["W"]), 0, "v", -t1); dim_chain(s, fi(side["E"]), W * F, "v", t1)
        if t2:
            if len(gx) > 2:
                dim_chain(s, fi(gx), 0, "h", t2); dim_chain(s, fi(gx), D * F, "h", -t2)
            if len(gy) > 2:
                dim_chain(s, fi(gy), 0, "v", -t2); dim_chain(s, fi(gy), W * F, "v", t2)
        ov = t3 if t3 else t2
        dim_chain(s, fi([0, W]), 0, "h", ov if len(gx) > 2 else t2); dim_chain(s, fi([0, W]), D * F, "h", -(ov if len(gx) > 2 else t2))
        dim_chain(s, fi([0, D]), 0, "v", -(ov if len(gy) > 2 else t2)); dim_chain(s, fi([0, D]), W * F, "v", (ov if len(gy) > 2 else t2))

    def _tags(self, level, door_start, room_prefix):
        s, c, p = self.s, self.cfg, self.p
        # rooms
        seq = {}
        self.placed = []
        self.room_rows = []
        cell_area = {}
        lab = p.lab
        for i, r in enumerate(self.rooms):
            cell_area[i] = int((lab == p.spaces.index(next(sp for sp in p.spaces if sp["id"] == f"S{i}"))).sum()) * (LG / 12) ** 2
        ordered = sorted(range(len(self.rooms)), key=lambda i: (self.rooms[i]["unit"] or "Z", self.rooms[i]["y"], self.rooms[i]["x"]))
        for i in ordered:
            r = self.rooms[i]
            nm = self._room_name(r)
            if not nm:
                continue
            u = r["unit"] or "X"
            if nm in SMALL or r["fill"].startswith("url") or (cell_area[i] < 22 and "BATH" not in nm and "POWDER" not in nm):
                t = r["names"][0]
                cx_, cy_ = (t["x"], t["y"]) if nm in SMALL else (r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
                s.text(s.m2p(cx_ * F, cy_ * F), nm if nm != "FR" else "FIRE RISER", 0.058, layer="A-AREA-IDEN", font="Helvetica-Bold", valign="m")
                continue
            seq[u] = seq.get(u, 0) + 1
            pre = (room_prefix or {}).get(u, u if u not in ("K", "X") else "")
            num = f"{pre}{level}{seq[u]:02d}"
            disp = RENAME.get(nm, nm)
            cx = sum(t["x"] for t in r["names"]) / len(r["names"]); cy = sum(t["y"] for t in r["names"]) / len(r["names"])
            cx, cy = c.get("tag_moves", {}).get(nm + "@" + u, (cx, cy)) if (nm + "@" + u) in c.get("tag_moves", {}) else (cx, cy)
            area = None if any(k in nm for k in ("HALL", "STAIR", "LAUNDRY", "LANDING", "SHARED", "ENTRY", "POWDER")) and "BATH" not in nm or "GARAGE" in nm else f"{int(round(cell_area[i]))} SF"
            if "GARAGE" in nm:
                area = f"{int(round(cell_area[i]))} SF"
            room_tag(s, s.m2p(cx * F, cy * F), disp, num, area)
            pc = s.m2p(cx * F, cy * F)
            self.placed.append((pc[0], pc[1] - 0.12, 0.33))
        # doors
        rows = []
        n = door_start
        OVR = c.get("door_tag_moves", {})
        for dd in self.door_list:
            if not dd.get("ok"):
                continue
            (ax, ay), (bx, by) = dd["a"], dd["b"]
            mx, my = (ax + bx) / 2, (ay + by) / 2
            W_ = abs(bx - ax) + abs(by - ay)
            sd = dd["sd"]
            q_in = (mx, my + 0.5 * sd) if dd["o"] == "h" else (mx + 0.5 * sd, my)
            q_out = (mx, my - 0.5 * sd) if dd["o"] == "h" else (mx - 0.5 * sd, my)
            r_in, r_out = self._room_at(*q_in), self._room_at(*q_out)
            ext = r_in is None or r_out is None
            tag = str(n); n += 1
            dd["tag"] = tag
            # place tag on the non-swing side unless overridden
            off = 1.55
            if dd["kind"] in ("bypass", "bifold"):
                kk = 1.45 if dd["kind"] == "bifold" else 1.1
                tp = (mx, my + kk * sd) if dd["o"] == "h" else (mx + kk * sd, my)
            elif dd["kind"] == "overhead":
                tp = (mx, my - 1.4) if abs(my) < 0.01 else (mx, my + 1.4)
            else:
                tp = (mx, my - off * sd) if dd["o"] == "h" else (mx - off * sd, my)
            if ext and dd["kind"] == "swing":
                tp = (mx, my + (-1.4 if abs(my) < 0.01 else 1.4)) if dd["o"] == "h" else (mx + (-1.4 if abs(mx) < 0.01 else 1.4), my)
            key = f"{round(mx, 1)},{round(my, 1)}"
            if key in OVR:
                tp = OVR[key]
            if key not in OVR:
                along = (1, 0) if dd["o"] == "h" else (0, 1)
                cands = [tp] + [(tp[0] + along[0] * k, tp[1] + along[1] * k) for k in (1.0, -1.0, 2.0, -2.0, 3.0, -3.0)]
                for cnd in cands:
                    pc = s.m2p(cnd[0] * F, cnd[1] * F)
                    if all(((pc[0] - q[0]) ** 2 + (pc[1] - q[1]) ** 2) ** 0.5 > q[2] + 0.13 for q in self.placed):
                        tp = cnd
                        break
            pc = s.m2p(tp[0] * F, tp[1] * F)
            self.placed.append((pc[0], pc[1], 0.12))
            circle_tag(s, pc, tag)
            # schedule row
            served = r_in if (r_in is not None and not r_in.get("open")) else (r_out if r_out is not None and not r_out.get("open") else r_in or r_out)
            nm = self._room_name(served) or "ROOM"
            u_in = r_in["unit"] if r_in else None; u_out = r_out["unit"] if r_out else None
            unit = (u_in if u_in not in (None, "K") else u_out) or ""
            if dd["kind"] == "overhead":
                rows.append((tag, f"{nm}", "9'-0\" x 8'-0\"", "G", "—", "OPENER", "")); continue
            size = f"{int(W_)}'-{int(round((W_ - int(W_)) * 12))}\" x 8'-0\""
            if dd["kind"] == "bypass":
                hw = W_ / 2 + 0.17
                size = f"(2) {fmt_w(hw)} x 8'-0\""; rows.append((tag, f"{unit} {nm} CLOSET".strip(), size, "E", "—", "PULLS", "")); continue
            if dd["kind"] == "bifold":
                size = f"(2) {fmt_w(W_ / 2)} x 8'-0\""; rows.append((tag, f"{unit} {nm}".strip(), size, "F", "—", "PASSAGE", "")); continue
            garage = "GARAGE" in self._room_name(r_in) or "GARAGE" in self._room_name(r_out)
            if ext:
                inner = r_in or r_out
                rows.append((tag, f"{self._room_name(inner) or 'EXTERIOR'} (EXT.)", size, "A", "—", "ENTRY / CLOSER" if not garage else "PASSAGE", "")); continue
            if u_in != u_out:
                label = "GARAGE" if garage else f"UNIT {unit} ENTRY"
                rows.append((tag, label, size, "C", "20 MIN S", "ENTRY / CLOSER", "5" if not garage else "7")); continue
            hw = "PRIVACY" if any(k in nm for k in ("BED", "BATH", "POWDER", "LOFT", "SITTING")) else "PASSAGE"
            rows.append((tag, f"{unit} {nm}".strip(), size, "D", "—", hw, "1" if unit == c.get("type_a_unit") else ""))
        self.door_rows = rows
        # windows
        for w in self.win_list:
            m = (w["a"] + w["b"]) / 2
            pt = {"N": (m, -1.35), "S": (m, self.D + 1.35), "W": (-1.35, m), "E": (self.W + 1.35, m)}[w["side"]]
            diamond_tag(s, s.m2p(pt[0] * F, pt[1] * F), w["type"])
        # wall type tags
        for (x, y, t) in c.get("wall_tags", []):
            hex_tag(s, s.m2p(x * F, y * F), t)
        return rows


def fmt_w(ft):
    inch = int(round(ft * 12 / 2) * 2)
    return f"{inch // 12}'-{inch % 12}\""


WIN_SIZES = {"A": ("6'-0\" x 4'-0\"", "HORIZ. SLIDER", "2'-6\""), "B": ("3'-0\" x 5'-0\"", "SINGLE HUNG", "2'-0\""),
             "C": ("3'-0\" x 4'-0\"", "SINGLE HUNG", "3'-0\""), "D": ("6'-0\" x 5'-0\"", "HORIZ. SLIDER", "2'-0\""),
             "E": ("5'-0\" x 4'-0\"", "HORIZ. SLIDER", "3'-6\"")}


def window_rows(views):
    agg = {}
    for v in views:
        for w in v.win_list:
            t = w["type"]
            a = agg.setdefault(t, dict(q=0, egress=False, rooms=set()))
            a["q"] += 1; a["egress"] |= w["egress"]
            nm = v._room_name(w["room"])
            a["rooms"].add("BEDROOMS" if ("BED" in nm or "LOFT" in nm or "SITTING" in nm) else ("KITCHEN" if "KITCHEN" in nm else "LIVING / DINING" if any(k in nm for k in ("LIVING", "DINING", "FAMILY", "GREAT", "FLEX")) else "BATH" if "BATH" in nm else nm or "—"))
    rows = []
    for t in sorted(agg):
        sz, op, sill = WIN_SIZES[t]
        rows.append((t, sz, op, sill, "YES" if agg[t]["egress"] else "—", str(agg[t]["q"]), " / ".join(sorted(agg[t]["rooms"]))[:22]))
    return rows
