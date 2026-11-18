"""cadkit: minimal CAD sheet engine.
Paper space: inches, origin bottom-left of ARCH D (36 x 24), y up.
Model space: inches, origin at building NW corner, x east, y SOUTH (down).
Every primitive is stored in paper coordinates; PDF plots directly,
DXF writes model-space inches (paper elements scaled by 1/scale).
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase.pdfmetrics import stringWidth

MM = 72 / 25.4
LW = {"xh": 0.70 * MM, "h": 0.50 * MM, "m": 0.35 * MM, "l": 0.25 * MM, "f": 0.18 * MM, "xf": 0.13 * MM}
LAYERS = {  # name: (aci color, linetype)
    "A-WALL": (7, "CONTINUOUS"), "A-WALL-PATT": (8, "CONTINUOUS"), "A-WALL-RATE": (1, "CONTINUOUS"),
    "A-DOOR": (2, "CONTINUOUS"), "A-GLAZ": (4, "CONTINUOUS"), "A-FLOR-FIXT": (6, "CONTINUOUS"),
    "A-FLOR-CASE": (6, "CONTINUOUS"), "A-FLOR-OVHD": (9, "HIDDEN"), "A-FLOR-STRS": (3, "CONTINUOUS"),
    "A-ANNO-DIMS": (1, "CONTINUOUS"), "A-ANNO-TEXT": (7, "CONTINUOUS"), "A-ANNO-SYMB": (5, "CONTINUOUS"),
    "A-ANNO-IDEN": (5, "CONTINUOUS"), "A-GRID": (3, "CENTER"), "A-ANNO-TTLB": (7, "CONTINUOUS"),
    "A-AREA-IDEN": (7, "CONTINUOUS"), "A-ANNO-NPLT": (8, "CONTINUOUS"),
}
DASH = {"HIDDEN": [4, 2.5], "CENTER": [14, 3, 3, 3], "PHANTOM": [10, 2, 2, 2, 2, 2], "CONTINUOUS": None}


class Sheet:
    def __init__(self, w=36.0, h=24.0, scale=48.0, origin=(0, 0)):
        self.w, self.h, self.scale = w, h, scale
        self.ox, self.oy = origin  # paper location of model (0,0)
        self.items = []

    # ---- coordinate helpers
    def m2p(self, x, y):
        return (self.ox + x / self.scale, self.oy - y / self.scale)

    def P(self, pts, space):
        return [self.m2p(*p) for p in pts] if space == "m" else list(pts)

    # ---- primitives (stored in paper inches)
    def line(self, p1, p2, layer="A-ANNO-TEXT", lw="l", space="p", dash=None, color=None):
        a, b = self.P([p1, p2], space)
        self.items.append(("line", layer, lw, dash, color, a, b))

    def pline(self, pts, layer="A-ANNO-TEXT", lw="l", space="p", closed=False, dash=None, fill=None, color=None, stroke=True):
        self.items.append(("pline", layer, lw, dash, color, self.P(pts, space), closed, fill, stroke))

    def rect(self, x, y, w, h, **k):
        self.pline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], closed=True, **k)

    def fillrect(self, x, y, w, h, gray, layer="A-WALL-PATT", space="m"):
        pts = self.P([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], space)
        self.items.append(("solid", layer, gray, pts))

    def arc(self, c, r, a0, a1, layer="A-DOOR", lw="f", space="p", dash=None):
        """angles in degrees in PAPER orientation (ccw, y up)."""
        if space == "m":
            c = self.m2p(*c); r = r / self.scale
        self.items.append(("arc", layer, lw, dash, None, c, r, a0, a1))

    def circle(self, c, r, layer="A-ANNO-SYMB", lw="l", space="p", fill=None, dash=None):
        if space == "m":
            c = self.m2p(*c); r = r / self.scale
        self.items.append(("circle", layer, lw, dash, None, c, r, fill))

    def text(self, p, s, h=0.094, layer="A-ANNO-TEXT", align="c", font="Helvetica", rot=0, space="p", color=None, valign="b"):
        if space == "m":
            p = self.m2p(*p)
        self.items.append(("text", layer, p, s, h, align, font, rot, color, valign))

    # ---- PDF
    def to_pdf(self, path, title="", author=""):
        c = canvas.Canvas(path, pagesize=(self.w * 72, self.h * 72))
        c.setTitle(title); c.setAuthor(author); c.setCreator("cadkit")
        c.setLineCap(0); c.setLineJoin(0)
        order = {"solid": 0}
        for it in sorted(self.items, key=lambda i: order.get(i[0], 1)):
            kind = it[0]
            if kind == "solid":
                _, layer, gray, pts = it
                c.setFillColor(Color(gray, gray, gray)); c.setStrokeColor(Color(gray, gray, gray)); c.setLineWidth(0.15)
                p = c.beginPath(); p.moveTo(pts[0][0] * 72, pts[0][1] * 72)
                for q in pts[1:]:
                    p.lineTo(q[0] * 72, q[1] * 72)
                p.close(); c.drawPath(p, stroke=1, fill=1)
                continue
            if kind == "text":
                _, layer, p, s, h, align, font, rot, color, valign = it
                pt = h * 72 / 0.72  # cap height ~0.72 of font size
                c.saveState(); c.translate(p[0] * 72, p[1] * 72); c.rotate(rot)
                c.setFillColor(color or Color(0.07, 0.07, 0.07)); c.setFont(font, pt)
                dy = {"b": 0, "m": -h * 72 / 2, "t": -h * 72}[valign]
                if align == "c":
                    c.drawCentredString(0, dy, s)
                elif align == "r":
                    c.drawRightString(0, dy, s)
                else:
                    c.drawString(0, dy, s)
                c.restoreState(); continue
            _, layer, lw, dash, color = it[:5]
            c.setLineWidth(LW[lw]); c.setStrokeColor(color or Color(0.05, 0.05, 0.05))
            lt = dash or LAYERS[layer][1]
            d = DASH.get(lt) if isinstance(lt, str) else lt
            c.setDash(d if d else [])
            if kind == "line":
                a, b = it[5], it[6]
                c.line(a[0] * 72, a[1] * 72, b[0] * 72, b[1] * 72)
            elif kind == "pline":
                pts, closed, fill, stroke = it[5], it[6], it[7], it[8]
                p = c.beginPath(); p.moveTo(pts[0][0] * 72, pts[0][1] * 72)
                for q in pts[1:]:
                    p.lineTo(q[0] * 72, q[1] * 72)
                if closed:
                    p.close()
                if fill is not None:
                    c.setFillColor(Color(fill, fill, fill) if isinstance(fill, float) else fill)
                c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill is not None else 0)
            elif kind == "arc":
                cc, r, a0, a1 = it[5], it[6], it[7], it[8]
                p = c.beginPath(); p.arc((cc[0] - r) * 72, (cc[1] - r) * 72, (cc[0] + r) * 72, (cc[1] + r) * 72, a0, a1 - a0)
                c.drawPath(p, stroke=1, fill=0)
            elif kind == "circle":
                cc, r, fill = it[5], it[6], it[7]
                if fill is not None:
                    c.setFillColor(Color(fill, fill, fill))
                c.circle(cc[0] * 72, cc[1] * 72, r * 72, stroke=1, fill=1 if fill is not None else 0)
        c.setDash([])
        c.showPage(); c.save()

    # ---- DXF R12 (model-space inches)
    def to_dxf(self, path):
        S = self.scale
        X = lambda p: ((p[0] - self.ox) * S, (p[1] - self.oy) * S)
        out = []
        w = lambda code, val: out.extend([str(code), str(val)])
        w(0, "SECTION"); w(2, "HEADER"); w(9, "$ACADVER"); w(1, "AC1009"); w(9, "$MEASUREMENT"); w(70, 0); w(0, "ENDSEC")
        w(0, "SECTION"); w(2, "TABLES")
        w(0, "TABLE"); w(2, "LTYPE"); w(70, 4)
        for nm, pat in (("CONTINUOUS", []), ("HIDDEN", [0.25 * S, -0.125 * S]), ("CENTER", [0.5 * S, -0.125 * S, 0.125 * S, -0.125 * S])):
            w(0, "LTYPE"); w(2, nm); w(70, 0); w(3, nm); w(72, 65); w(73, len(pat)); w(40, sum(abs(v) for v in pat))
            for v in pat:
                w(49, v)
        w(0, "ENDTAB")
        w(0, "TABLE"); w(2, "LAYER"); w(70, len(LAYERS))
        for nm, (col, lt) in LAYERS.items():
            w(0, "LAYER"); w(2, nm); w(70, 0); w(62, col); w(6, lt)
        w(0, "ENDTAB"); w(0, "ENDSEC")
        w(0, "SECTION"); w(2, "ENTITIES")
        for it in self.items:
            k = it[0]
            if k == "solid":
                pts = [X(p) for p in it[3]]
                if len(pts) == 4:
                    a, b, c2, d = pts
                    w(0, "SOLID"); w(8, it[1])
                    for i, (pp) in enumerate((a, b, d, c2)):
                        w(10 + i, pp[0]); w(20 + i, pp[1]); w(30 + i, 0)
                continue
            if k == "line":
                a, b = X(it[5]), X(it[6])
                w(0, "LINE"); w(8, it[1]); w(10, a[0]); w(20, a[1]); w(30, 0); w(11, b[0]); w(21, b[1]); w(31, 0)
            elif k == "pline":
                pts = [X(p) for p in it[5]]
                w(0, "POLYLINE"); w(8, it[1]); w(66, 1); w(10, 0); w(20, 0); w(30, 0); w(70, 1 if it[6] else 0)
                for p in pts:
                    w(0, "VERTEX"); w(8, it[1]); w(10, p[0]); w(20, p[1]); w(30, 0)
                w(0, "SEQEND"); w(8, it[1])
            elif k == "arc":
                cc = X(it[5]); w(0, "ARC"); w(8, it[1]); w(10, cc[0]); w(20, cc[1]); w(30, 0); w(40, it[6] * S); w(50, it[7]); w(51, it[8])
            elif k == "circle":
                cc = X(it[5]); w(0, "CIRCLE"); w(8, it[1]); w(10, cc[0]); w(20, cc[1]); w(30, 0); w(40, it[6] * S)
            elif k == "text":
                _, layer, p, s, h, align, font, rot, color, valign = it
                pp = X(p); hh = h * S
                w(0, "TEXT"); w(8, layer); w(10, pp[0]); w(20, pp[1]); w(30, 0); w(40, hh); w(1, s.replace("·", "-").replace("×", "x")); w(50, rot)
                ha = {"l": 0, "c": 1, "r": 2}[align]; va = {"b": 0, "m": 2, "t": 3}[valign]
                if ha or va:
                    w(72, ha); w(73, va); w(11, pp[0]); w(21, pp[1]); w(31, 0)
        w(0, "ENDSEC"); w(0, "EOF")
        open(path, "w").write("\n".join(out) + "\n")


def fmt_ftin(inches):
    inches = round(inches * 2) / 2
    ft = int(inches // 12); i = inches - ft * 12
    if abs(i - round(i)) < 1e-6:
        istr = str(int(round(i)))
    else:
        istr = f"{int(i)} 1/2" if int(i) else "1/2"
    return f"{ft}'-{istr}\""


def text_w(s, h, font="Helvetica"):
    return stringWidth(s, font, h * 72 / 0.72) / 72
