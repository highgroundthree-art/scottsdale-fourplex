"""Exterior elevation drawing (CAD style). Units: feet along facade (x) and height (z, up)."""
import math
from plan_engine import diamond_tag, circle_tag, bubble
from cadkit import fmt_ftin

PITCH = 4 / 12
FFU = 10 + 8 / 12      # upper finish floor
PLATE = 19 + 8 / 12
EAVE = 20.0            # top of fascia
GRADE = -8 / 12
WIN = {"A": (6, 4, 3.0), "B": (3, 5, 2.0), "C": (3, 4, 3.0), "D": (6, 5, 2.0), "F": (3, 5, 2.0)}  # w, h, sill


class Elev:
    def __init__(self, s, origin):
        self.s = s
        s.ox, s.oy = origin

    def P(self, x, z):
        return (x * 12, -z * 12)

    def line(self, a, b, layer="A-ELEV", lw="l", dash=None):
        self.s.line(self.P(*a), self.P(*b), layer=layer, lw=lw, space="m", dash=dash)

    def poly(self, pts, lw="l", fill=None, closed=True, dash=None, layer="A-ELEV"):
        self.s.pline([self.P(*p) for p in pts], layer=layer, lw=lw, space="m", fill=fill, closed=closed, dash=dash)

    def rect(self, x0, z0, x1, z1, **k):
        self.poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], **k)

    def text(self, x, z, t, h=0.07, **k):
        self.s.text(self.s.m2p(x * 12, -z * 12), t, h, space="p", **k)

    # ---------------------------------------------------------------
    def wall(self, x0, x1, top=PLATE + 0.35):
        self.rect(x0, 0, x1, top, lw="m")
        self.rect(x0, GRADE, x1, 0, lw="f", fill=0.92)                    # exposed slab edge / screed
        self.rect(x0, FFU - 0.42, x1, FFU + 0.25, lw="f", fill=0.94)      # precast band at floor line
        self.line((x0, 0.0), (x1, 0.0), lw="f")

    def hip_roof_long(self, x0, x1, depth, ov=2.0):
        """hip roof seen from the long side: eave x0-ov .. x1+ov, ridge length = (x1-x0) - depth."""
        a, b = x0 - ov, x1 + ov
        run = depth / 2 + ov
        zr = EAVE + run * PITCH
        r0, r1 = a + run, b - run
        pts = [(a, EAVE), (b, EAVE), (r1, zr), (r0, zr)]
        self._tile(pts, a, b, zr)
        self.poly(pts, lw="m")
        self.rect(a, EAVE - 0.6, b, EAVE, lw="l", fill=1.0)               # fascia + gutter
        self.line((r0, zr), (a + 0.0, EAVE), lw="f"); self.line((r1, zr), (b, EAVE), lw="f")
        return zr

    def hip_roof_end(self, x0, x1, ov=2.0):
        a, b = x0 - ov, x1 + ov
        run = (x1 - x0) / 2 + ov
        zr = EAVE + run * PITCH
        pts = [(a, EAVE), (b, EAVE), ((a + b) / 2, zr)]
        self._tile(pts, a, b, zr)
        self.poly(pts, lw="m")
        self.rect(a, EAVE - 0.6, b, EAVE, lw="l", fill=1.0)
        return zr

    def _tile(self, pts, a, b, zr):
        # horizontal courses clipped to the polygon, with barrel ticks
        z = EAVE + 0.55
        k = 0
        while z < zr - 0.2:
            xs = self._clip(pts, z)
            if xs:
                self.line((xs[0], z), (xs[1], z), lw="xf")
                x = xs[0] + (0.4 if k % 2 else 0.0)
                while x < xs[1] - 0.2:
                    self.line((x, z), (x, z + 0.42), lw="xf")
                    x += 0.8
            z += 0.55; k += 1

    @staticmethod
    def _clip(pts, z):
        xs = []
        n = len(pts)
        for i in range(n):
            (x1, z1), (x2, z2) = pts[i], pts[(i + 1) % n]
            if (z1 - z) * (z2 - z) <= 0 and z1 != z2:
                xs.append(x1 + (z - z1) * (x2 - x1) / (z2 - z1))
        xs = sorted(xs)
        return (xs[0], xs[-1]) if len(xs) >= 2 else None

    def window(self, x0, x1, sill, head, tag=None, shutters=False, arch=False):
        self.rect(x0 - 0.33, sill - 0.25, x1 + 0.33, head + 0.33, lw="f", fill=1.0)   # foam surround
        self.rect(x0 - 0.45, sill - 0.42, x1 + 0.45, sill - 0.2, lw="l", fill=0.9)    # precast sill
        if arch:
            r = (x1 - x0) / 2; cx = (x0 + x1) / 2; spring = head - r
            pts = [(x0, sill), (x1, sill), (x1, spring)] + [(cx + r * math.cos(t), spring + r * math.sin(t)) for t in [i * math.pi / 16 for i in range(17)]] + [(x0, spring)]
            self.poly(pts, lw="l")
            self.line((cx, sill), (cx, head), lw="xf")
        else:
            self.rect(x0, sill, x1, head, lw="l")
            self.rect(x0 + 0.15, sill + 0.15, x1 - 0.15, head - 0.15, lw="xf")
            if x1 - x0 > 4:
                self.line(((x0 + x1) / 2, sill + 0.15), ((x0 + x1) / 2, head - 0.15), lw="f")
            else:
                self.line((x0 + 0.15, (sill + head) / 2), (x1 - 0.15, (sill + head) / 2), lw="f")
        if shutters:
            w = (x1 - x0) / 2
            for sx in (x0 - 0.45 - w * 0.9, x1 + 0.45):
                self.rect(sx, sill, sx + w * 0.9 * (1 if sx > x0 else 1), head, lw="f")
                z = sill + 0.3
                while z < head - 0.2:
                    self.line((sx + 0.1, z), (sx + w * 0.9 - 0.1, z), lw="xf"); z += 0.35
        if tag:
            diamond_tag(self.s, self.s.m2p((x0 + x1) / 2 * 12, -(sill - 1.0) * 12), tag)

    def door(self, x0, x1, head, tag=None, glass=False, slider=False, z0=0.0):
        self.rect(x0 - 0.33, z0, x1 + 0.33, head + 0.33, lw="f", fill=1.0)
        self.rect(x0, z0, x1, head, lw="l")
        if slider:
            m = (x0 + x1) / 2
            self.line((m, z0), (m, head), lw="f")
            for a, b in ((x0, m), (m, x1)):
                self.rect(a + 0.2, z0 + 0.3, b - 0.2, head - 0.2, lw="xf")
        elif glass:
            self.rect(x0 + 0.4, z0 + 3.0, x1 - 0.4, head - 0.5, lw="xf")
        else:
            self.rect(x0 + 0.3, z0 + 0.5, x1 - 0.3, head - 0.5, lw="xf")
            self.rect(x0 + 0.3, z0 + 0.5, x1 - 0.3, (head + z0) / 2, lw="xf")
        if tag:
            circle_tag(self.s, self.s.m2p((x0 + x1) / 2 * 12, -(z0 - 1.0) * 12), tag)

    def light(self, x, z):
        self.rect(x - 0.25, z - 0.4, x + 0.25, z + 0.4, lw="f", fill=0.15)

    def downspout(self, x, z_top=EAVE - 0.6):
        self.rect(x - 0.17, GRADE + 0.3, x + 0.17, z_top, lw="f")
        self.rect(x - 0.6, GRADE, x + 0.6, GRADE + 0.3, lw="xf")

    def grade(self, x0, x1):
        self.line((x0, GRADE), (x1, GRADE), lw="xh")
        x = x0
        while x < x1:
            self.line((x, GRADE), (x - 0.6, GRADE - 0.6), lw="xf"); x += 1.2

    def levels(self, x_right, zr):
        rows = [(GRADE, "FIN. GRADE", "-0'-8\""), (0, "FIN. FLOOR", "0'-0\" (EL. 100'-0\")"),
                (FFU, "UPPER FIN. FLOOR", "10'-8\""), (PLATE, "TOP OF PLATE", "19'-8\""), (zr, "TOP OF RIDGE", fmt_ftin(zr * 12) + " ±")]
        for z, a, b in rows:
            self.line((x_right + 0.5, z), (x_right + 3.4, z), lw="xf", dash="CENTER")
            c = self.s.m2p((x_right + 4.0) * 12, -z * 12)
            if z == GRADE:
                c = (c[0], c[1] - 0.12)
            self.s.circle(c, 0.09, layer="A-ANNO-SYMB", lw="f")
            self.s.pline([(c[0] - 0.09, c[1]), (c[0], c[1] + 0.09), (c[0], c[1] - 0.09)], layer="A-ANNO-SYMB", lw="f", fill=0.1, closed=True)
            self.s.text((c[0] + 0.16, c[1] + 0.04), a, 0.072, align="l", font="Helvetica-Bold")
            self.s.text((c[0] + 0.16, c[1] - 0.11), b, 0.068, align="l")

    def keynote(self, x, z, n, dx, dz):
        a = self.s.m2p(x * 12, -z * 12)
        b = (a[0] + dx, a[1] + dz)
        self.s.line(a, b, layer="A-ANNO-SYMB", lw="xf")
        self.s.circle(a, 0.025, layer="A-ANNO-SYMB", lw="f", fill=0.0)
        self.s.rect(b[0] - 0.1, b[1] - 0.08, 0.2, 0.16, layer="A-ANNO-SYMB", lw="f", fill=1.0)
        self.s.text(b, str(n), 0.07, layer="A-ANNO-SYMB", font="Helvetica-Bold", valign="m")

    def grids(self, items, z=-3.2):
        for x, lab in items:
            self.line((x, GRADE - 0.4), (x, z + 0.8), lw="xf", dash="CENTER")
            bubble(self.s, self.s.m2p(x * 12, -z * 12), lab)

    def hdim(self, xs, z):
        from plan_engine import dim_chain
        dim_chain(self.s, [x * 12 for x in xs], -z * 12, "h", 0.0)


LAY = set()
