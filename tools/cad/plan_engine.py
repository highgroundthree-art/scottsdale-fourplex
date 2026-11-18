"""Plan engine: rooms -> walls (by type) -> poché, outline, openings; annotation helpers."""
import math
import numpy as np
from cadkit import Sheet, fmt_ftin, text_w

G = 3          # label grid, inches
R = 4          # wall mask resolution, cells per inch
WALL_T = {"EXT": 7.5, "W2": 8.5, "W1": 9.5, "W3": 5.5, "P1": 4.5, "P2": 6.5}
WALL_GRAY = {"EXT": 0.62, "W2": 0.32, "W1": 0.32, "W3": 0.32, "P1": 0.70, "P2": 0.70}


class Plan:
    def __init__(self, sheet: Sheet, W_ft, D_ft):
        self.s = sheet
        self.W, self.D = int(W_ft * 12), int(D_ft * 12)
        self.spaces = []
        self.lab = None
        self.doors = []
        self.windows = []

    def space(self, sid, unit, group, rects_ft, name=None, number=None, tag_at=None, area=True, show=True, sub=None):
        self.spaces.append(dict(id=sid, unit=unit, group=group, rects=rects_ft, name=name, number=number,
                                tag_at=tag_at, area=area, show=show, sub=sub))

    # ---------- walls
    def build_walls(self, west_type="W2", overrides=None, pair_type=None):
        nx, ny = self.W // G, self.D // G
        lab = np.full((ny, nx), -1, int)
        for i, sp in enumerate(self.spaces):
            for (x, y, w, h) in sp["rects"]:
                lab[int(round(y * 12 / G)):int(round((y + h) * 12 / G)), int(round(x * 12 / G)):int(round((x + w) * 12 / G))] = i
        assert (lab >= 0).all(), "unassigned cells at %s" % (np.argwhere(lab < 0)[:5] * G / 12)
        self.lab = lab
        grp = lambda i: "OUT" if i < 0 else self.spaces[i]["group"]
        unit = lambda i: "OUT" if i < 0 else self.spaces[i]["unit"]
        segs = []  # (orient, fixed_in, a_in, b_in, type)

        def wtype(i, j, orient, fixed):
            if i < 0 or j < 0:
                if orient == "v" and fixed == 0:
                    return west_type
                return "EXT"
            if unit(i) != unit(j):
                if pair_type:
                    pt = pair_type(unit(i), unit(j))
                    if pt:
                        return pt
                return "W1"
            return "P1"
        # horizontal boundaries (between rows)
        for r in range(ny + 1):
            run = None
            for c in range(nx + 1):
                t = None
                if c < nx:
                    a = lab[r - 1, c] if r > 0 else -1
                    b = lab[r, c] if r < ny else -1
                    if grp(a) != grp(b):
                        t = wtype(a, b, "h", r * G)
                if run and (t != run[1]):
                    segs.append(("h", r * G, run[0] * G, c * G, run[1])); run = None
                if t and not run:
                    run = [c, t]
        for c in range(nx + 1):
            run = None
            for r in range(ny + 1):
                t = None
                if r < ny:
                    a = lab[r, c - 1] if c > 0 else -1
                    b = lab[r, c] if c < nx else -1
                    if grp(a) != grp(b):
                        t = wtype(a, b, "v", c * G)
                if run and (t != run[1]):
                    segs.append(("v", c * G, run[0] * G, r * G, run[1])); run = None
                if t and not run:
                    run = [r, t]
        if overrides:
            segs = [overrides(sg) or sg for sg in segs]
        self.segs = segs
        # masks
        H, Wc = self.D * R, self.W * R
        self.masks = {t: np.zeros((H, Wc), bool) for t in WALL_T}
        for (o, f, a, b, t) in segs:
            th = WALL_T[t]
            ext = t in ("EXT", "W2")
            if o == "h":
                if ext:
                    y0, y1 = (f, f + th) if f == 0 else (f - th, f)
                else:
                    y0, y1 = f - th / 2, f + th / 2
                x0, x1 = a - (0 if ext else th / 2), b + (0 if ext else th / 2)
            else:
                if ext:
                    x0, x1 = (f, f + th) if f == 0 else (f - th, f)
                else:
                    x0, x1 = f - th / 2, f + th / 2
                y0, y1 = a - (0 if ext else th / 2), b + (0 if ext else th / 2)
            self._paint(self.masks[t], x0, y0, x1, y1)
        # priority: rated > ext > partition
        pri = ["W1", "W3", "W2", "EXT", "P2", "P1"]
        taken = np.zeros((H, Wc), bool)
        for t in pri:
            self.masks[t] &= ~taken
            taken |= self.masks[t]
        self.union = taken

    def _paint(self, m, x0, y0, x1, y1, val=True):
        H, Wc = m.shape
        i0, i1 = max(0, int(round(y0 * R))), min(H, int(round(y1 * R)))
        j0, j1 = max(0, int(round(x0 * R))), min(Wc, int(round(x1 * R)))
        if i1 > i0 and j1 > j0:
            m[i0:i1, j0:j1] = val

    def wall_at(self, o, f, a, b):
        """find segment covering position"""
        for sg in self.segs:
            if sg[0] == o and abs(sg[1] - f) < 0.1 and sg[2] <= a + 0.1 and sg[3] >= b - 0.1:
                return sg
        raise KeyError((o, f, a, b))

    def carve(self, x0, y0, x1, y1):
        for m in self.masks.values():
            self._paint(m, x0, y0, x1, y1, False)
        self._paint(self.union, x0, y0, x1, y1, False)

    def wall_faces(self, sg):
        o, f, a, b, t = sg
        th = WALL_T[t]
        if t in ("EXT", "W2"):
            return (f, f + th) if f == 0 else (f - th, f)
        return (f - th / 2, f + th / 2)

    # ---------- openings
    def door(self, hinge_ft, strike_ft, swing_dir, tag=None, kind="swing", tag_side=None):
        """hinge/strike on wall boundary line (ft); swing_dir: +1/-1 along the wall-normal axis."""
        hx, hy = hinge_ft[0] * 12, hinge_ft[1] * 12
        sx, sy = strike_ft[0] * 12, strike_ft[1] * 12
        o = "h" if abs(hy - sy) < 0.01 else "v"
        if o == "h":
            sg = self.wall_at("h", hy, min(hx, sx), max(hx, sx))
        else:
            sg = self.wall_at("v", hx, min(hy, sy), max(hy, sy))
        f0, f1 = self.wall_faces(sg)
        Wd = abs(sx - hx) + abs(sy - hy)
        if o == "h":
            self.carve(min(hx, sx), f0 - 0.5, max(hx, sx), f1 + 0.5)
        else:
            self.carve(f0 - 0.5, min(hy, sy), f1 + 0.5, max(hy, sy))
        self.doors.append(dict(o=o, h=(hx, hy), st=(sx, sy), d=swing_dir, faces=(f0, f1), W=Wd, tag=tag, kind=kind, tag_side=tag_side))

    def window(self, side, a_ft, b_ft, tag):
        a, b = a_ft * 12, b_ft * 12
        if side in ("N", "S"):
            f = 0 if side == "N" else self.D
            sg = self.wall_at("h", f, a, b)
            f0, f1 = self.wall_faces(sg)
            self.carve(a, f0 - 0.5, b, f1 + 0.5)
        else:
            f = 0 if side == "W" else self.W
            sg = self.wall_at("v", f, a, b)
            f0, f1 = self.wall_faces(sg)
            self.carve(f0 - 0.5, a, f1 + 0.5, b)
        self.windows.append(dict(side=side, a=a, b=b, faces=(f0, f1), tag=tag))

    # ---------- drawing
    def draw_walls(self):
        s = self.s
        for t, m in self.masks.items():
            for (x0, y0, x1, y1) in mask_rects(m):
                s.fillrect(x0 / R, y0 / R, (x1 - x0) / R, (y1 - y0) / R, WALL_GRAY[t],
                           layer="A-WALL-RATE" if t in ("W1", "W2", "W3") else "A-WALL-PATT")
        for (a, b) in mask_outline(self.union):
            s.line((a[0] / R, a[1] / R), (b[0] / R, b[1] / R), layer="A-WALL", lw="h", space="m")

    def draw_openings(self):
        s = self.s
        for w in self.windows:
            f0, f1 = w["faces"]; a, b = w["a"], w["b"]
            mid = (f0 + f1) / 2
            if w["side"] in ("N", "S"):
                for yy, lw in ((f0, "f"), (f1, "f"), (mid - 0.75, "xf"), (mid + 0.75, "xf")):
                    s.line((a, yy), (b, yy), layer="A-GLAZ", lw=lw, space="m")
                # sill line inside
                si = f1 + 1.5 if f0 == 0 else f0 - 1.5
                s.line((a - 1.5, si), (b + 1.5, si), layer="A-GLAZ", lw="xf", space="m")
            else:
                for xx, lw in ((f0, "f"), (f1, "f"), (mid - 0.75, "xf"), (mid + 0.75, "xf")):
                    s.line((xx, a), (xx, b), layer="A-GLAZ", lw=lw, space="m")
                si = f1 + 1.5 if f0 == 0 else f0 - 1.5
                s.line((si, a - 1.5), (si, b + 1.5), layer="A-GLAZ", lw="xf", space="m")
        for d in self.doors:
            f0, f1 = d["faces"]; (hx, hy) = d["h"]; (sx, sy) = d["st"]; W = d["W"]; sd = d["d"]
            if d["kind"] == "overhead":
                mid = (f0 + f1) / 2
                if d["o"] == "h":
                    x0, x1 = min(hx, sx), max(hx, sx)
                    s.line((x0, mid), (x1, mid), layer="A-DOOR", lw="l", space="m")
                    s.rect(x0, f1, x1 - x0, 7 * 12, layer="A-FLOR-OVHD", lw="f", space="m", dash="HIDDEN") if f0 == 0 else s.rect(x0, f0 - 84, x1 - x0, 84, layer="A-FLOR-OVHD", lw="f", space="m", dash="HIDDEN")
                continue
            if d["kind"] == "bifold":
                face = f1 if sd > 0 else f0
                if d["o"] == "h":
                    x0, x1 = min(hx, sx), max(hx, sx); q = (x1 - x0) / 4
                    for j0, dirn in ((x0, 1), (x1, -1)):
                        s.pline([(j0, face), (j0 + dirn * q, face + sd * q * 0.9), (j0 + dirn * 2 * q, face)], layer="A-DOOR", lw="l", space="m")
                else:
                    y0, y1 = min(hy, sy), max(hy, sy); q = (y1 - y0) / 4
                    for j0, dirn in ((y0, 1), (y1, -1)):
                        s.pline([(face, j0), (face + sd * q * 0.9, j0 + dirn * q), (face, j0 + dirn * 2 * q)], layer="A-DOOR", lw="l", space="m")
                continue
            if d["kind"] == "bypass":
                mid = (f0 + f1) / 2
                if d["o"] == "h":
                    x0, x1 = min(hx, sx), max(hx, sx); half = (x1 - x0) / 2 + 2
                    s.rect(x0, mid - 2.0, half, 1.25, layer="A-DOOR", lw="f", space="m")
                    s.rect(x1 - half, mid + 0.75, half, 1.25, layer="A-DOOR", lw="f", space="m")
                else:
                    y0, y1 = min(hy, sy), max(hy, sy); half = (y1 - y0) / 2 + 2
                    s.rect(mid - 2.0, y0, 1.25, half, layer="A-DOOR", lw="f", space="m")
                    s.rect(mid + 0.75, y1 - half, 1.25, half, layer="A-DOOR", lw="f", space="m")
                continue
            face = f1 if sd > 0 else f0
            if d["o"] == "h":
                along = 1 if sx > hx else -1
                hp = (hx, face)
                leaf_end = (hx, face + sd * W)
                s.pline([(hx, face), (hx + along * 1.75, face), (hx + along * 1.75, face + sd * W), (hx, face + sd * W)], closed=True, layer="A-DOOR", lw="l", space="m")
                a_leaf = 90 if sd < 0 else -90       # paper angles (model y flipped)
                a_strike = 0 if along > 0 else 180
                st = (sx, face)
            else:
                along = 1 if sy > hy else -1
                hp = (face, hy)
                s.pline([(face, hy), (face, hy + along * 1.75), (face + sd * W, hy + along * 1.75), (face + sd * W, hy)], closed=True, layer="A-DOOR", lw="l", space="m")
                a_leaf = 0 if sd > 0 else 180
                a_strike = -90 if along > 0 else 90
                st = (face, sy)
            a0, a1 = sorted([a_leaf, a_strike])
            if a1 - a0 > 180:
                a0, a1 = a1, a0 + 360
            s.arc(hp, W, a0, a1, layer="A-DOOR", lw="xf", space="m")


def mask_rects(m):
    """run-length rects (x0,y0,x1,y1) in cells."""
    H, Wc = m.shape
    out = []
    prev = {}
    for i in range(H + 1):
        row = m[i] if i < H else np.zeros(Wc, bool)
        runs = {}
        if row.any():
            d = np.diff(np.concatenate([[0], row.astype(int), [0]]))
            st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
            runs = {(a, b): None for a, b in zip(st, en)}
        nxt = {}
        for k, i0 in prev.items():
            if k in runs:
                nxt[k] = i0
            else:
                out.append((k[0], i0, k[1], i))
        for k in runs:
            if k not in nxt:
                nxt[k] = i
        prev = nxt
    return out


def mask_outline(m):
    H, Wc = m.shape
    p = np.zeros((H + 2, Wc + 2), bool); p[1:-1, 1:-1] = m
    segs = []
    dh = p[1:, 1:-1] != p[:-1, 1:-1]   # (H+1, Wc) horizontal edges at y=i
    for i in range(dh.shape[0]):
        row = dh[i]
        if row.any():
            d = np.diff(np.concatenate([[0], row.astype(int), [0]]))
            for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
                segs.append(((a, i), (b, i)))
    dv = p[1:-1, 1:] != p[1:-1, :-1]   # (H, Wc+1)
    for j in range(dv.shape[1]):
        col = dv[:, j]
        if col.any():
            d = np.diff(np.concatenate([[0], col.astype(int), [0]]))
            for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
                segs.append(((j, a), (j, b)))
    return segs


# ---------------- annotation helpers (paper inches) ----------------
TXT = 0.094  # 3/32"


def dim_chain(s, pts_in, fixed_in, orient, offset_p, label_overall=False, ext_from=None, lw="xf", min_text=True):
    """dimension string. pts_in: model inches along axis; fixed_in: model coordinate of the measured edge;
    offset_p: paper offset of dim line from that edge (+ away from building). orient 'h' (along x) or 'v'."""
    pts = sorted(set(round(p, 2) for p in pts_in))
    if orient == "h":
        yline = s.m2p(0, fixed_in)[1] + offset_p
        ys = s.m2p(0, fixed_in)[1] + (0.06 if offset_p > 0 else -0.06)
        P = [s.m2p(p, fixed_in)[0] for p in pts]
        s.line((P[0] - 0.08, yline), (P[-1] + 0.08, yline), layer="A-ANNO-DIMS", lw=lw)
        for x in P:
            s.line((x, ys if ext_from is None else ext_from), (x, yline + (0.06 if offset_p > 0 else -0.06)), layer="A-ANNO-DIMS", lw="xf")
            s.line((x - 0.045, yline - 0.045), (x + 0.045, yline + 0.045), layer="A-ANNO-DIMS", lw="l")
        for a, b, pa, pb in zip(P, P[1:], pts, pts[1:]):
            t = fmt_ftin(pb - pa)
            w = text_w(t, TXT)
            if w + 0.06 < (b - a):
                s.text(((a + b) / 2, yline + 0.035), t, TXT, layer="A-ANNO-DIMS")
            else:
                s.text(((a + b) / 2, yline + 0.035 + 0.13), t, TXT * 0.9, layer="A-ANNO-DIMS")
    else:
        xline = s.m2p(fixed_in, 0)[0] + offset_p
        xs = s.m2p(fixed_in, 0)[0] + (0.06 if offset_p > 0 else -0.06)
        P = [s.m2p(fixed_in, p)[1] for p in pts]
        s.line((xline, P[0] + 0.08), (xline, P[-1] - 0.08), layer="A-ANNO-DIMS", lw=lw)
        for y in P:
            s.line((xs if ext_from is None else ext_from, y), (xline + (0.06 if offset_p > 0 else -0.06), y), layer="A-ANNO-DIMS", lw="xf")
            s.line((xline - 0.045, y - 0.045), (xline + 0.045, y + 0.045), layer="A-ANNO-DIMS", lw="l")
        for a, b, pa, pb in zip(P, P[1:], pts, pts[1:]):
            t = fmt_ftin(pb - pa)
            w = text_w(t, TXT)
            if w + 0.06 < abs(a - b):
                s.text((xline - 0.035, (a + b) / 2), t, TXT, layer="A-ANNO-DIMS", rot=90, valign="b")
            else:
                s.text((xline - 0.035 - 0.13, (a + b) / 2), t, TXT * 0.9, layer="A-ANNO-DIMS", rot=90)


def bubble(s, c, label, r=0.19, layer="A-GRID"):
    s.circle(c, r, layer=layer, lw="l", fill=1.0)
    s.text((c[0], c[1]), label, 0.14, layer=layer, font="Helvetica-Bold", valign="m")


def hex_tag(s, c, label, r=0.11, layer="A-ANNO-IDEN"):
    pts = [(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    s.pline(pts, closed=True, layer=layer, lw="f", fill=1.0)
    s.text(c, label, 0.075, layer=layer, font="Helvetica-Bold", valign="m")


def circle_tag(s, c, label, r=0.115, layer="A-ANNO-IDEN"):
    s.circle(c, r, layer=layer, lw="f", fill=1.0)
    s.text(c, label, 0.068, layer=layer, font="Helvetica-Bold", valign="m")


def diamond_tag(s, c, label, r=0.13, layer="A-ANNO-IDEN"):
    pts = [(c[0], c[1] + r), (c[0] + r, c[1]), (c[0], c[1] - r), (c[0] - r, c[1])]
    s.pline(pts, closed=True, layer=layer, lw="f", fill=1.0)
    s.text(c, label, 0.072, layer=layer, font="Helvetica-Bold", valign="m")


def room_tag(s, c, name, number, area=None, sub=None, h=0.1):
    lines = name.split("\n")
    y = c[1] + 0.03 + (len(lines) - 1) * h * 0.65
    for ln in lines:
        s.text((c[0], y), ln, h, layer="A-AREA-IDEN", font="Helvetica-Bold")
        y -= h * 1.35
    bw = max(text_w(number, 0.075, "Helvetica-Bold") + 0.1, 0.36)
    s.rect(c[0] - bw / 2, y - 0.07, bw, 0.15, layer="A-AREA-IDEN", lw="f", fill=1.0)
    s.text((c[0], y), number, 0.075, layer="A-AREA-IDEN", font="Helvetica-Bold", valign="m")
    y -= 0.2
    if area:
        s.text((c[0], y), area, 0.068, layer="A-AREA-IDEN")
        y -= 0.13
    if sub:
        s.text((c[0], y), sub, 0.062, layer="A-AREA-IDEN")


def wrap(text, width, h, font="Helvetica"):
    words = text.split(); lines = []; cur = ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_w(t, h, font) <= width:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(s, x, y, text, width, h=0.078, lead=1.45, font="Helvetica", num=None, layer="A-ANNO-TEXT"):
    indent = 0.2 if num else 0
    lines = wrap(text, width - indent, h, font)
    if num:
        s.text((x, y), num, h, font="Helvetica-Bold", align="l", layer=layer)
    for ln in lines:
        s.text((x + indent, y), ln, h, font=font, align="l", layer=layer)
        y -= h * lead
    return y - h * 0.5


def table(s, x, y, cols, rows, h=0.072, rowh=0.17, head_h=0.078, layer="A-ANNO-TEXT"):
    """cols: [(title, width, align)] ; returns bottom y"""
    W = sum(c[1] for c in cols)
    s.rect(x, y - rowh, W, rowh, layer=layer, lw="f", fill=0.88)
    cx = x
    for (t, w, al) in cols:
        s.text((cx + 0.05 if al == "l" else cx + w / 2, y - rowh / 2), t, head_h * 0.9, font="Helvetica-Bold", align="l" if al == "l" else "c", valign="m", layer=layer)
        cx += w
    yy = y - rowh
    for r in rows:
        cx = x
        for (t, w, al), v in zip(cols, r):
            s.text((cx + 0.05 if al == "l" else cx + w / 2, yy - rowh / 2), str(v), h, align="l" if al == "l" else "c", valign="m", layer=layer)
            cx += w
        yy -= rowh
        s.line((x, yy), (x + W, yy), layer=layer, lw="xf")
    s.rect(x, yy, W, y - yy, layer=layer, lw="f")
    cx = x
    for (t, w, al) in cols[:-1]:
        cx += w
        s.line((cx, y), (cx, yy), layer=layer, lw="xf")
    return yy
