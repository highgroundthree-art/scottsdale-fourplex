import re, html
from concept_parse import parse
UNITC = {"#111111": "A", "#1a8f3c": "B", "#c62828": "C", "#1e5bd8": "D", "#777777": "K"}

def num(v): return float(v)

def parse_floor(path, ppf, origin):
    vb, els = parse(path)
    ox, oy = origin
    X = lambda v: round((num(v) - ox) / ppf, 3)
    Y = lambda v: round((num(v) - oy) / ppf, 3)
    Ln = lambda v: round(num(v) / ppf, 3)
    rooms, doors, wins, fx, texts, treads = [], [], [], [], [], []
    i = 0
    while i < len(els):
        e = els[i]; t = e['_t']; sw = e.get('stroke-width')
        if t == 'rect' and sw == '1.3':
            r = dict(x=X(e['x']), y=Y(e['y']), w=Ln(e['width']), h=Ln(e['height']), fill=e['fill'], color=None, op=0)
            if i + 1 < len(els) and els[i + 1]['_t'] == 'rect' and els[i + 1].get('stroke') == 'none' and els[i + 1]['x'] == e['x'] and els[i + 1]['y'] == e['y']:
                r['color'] = els[i + 1]['fill']; r['op'] = float(els[i + 1].get('fill-opacity', 0)); i += 1
            rooms.append(r)
        elif t == 'line' and e.get('stroke') == '#fff' and sw == '5':
            leaf = els[i + 1]
            a = (X(e['x1']), Y(e['y1'])); b = (X(e['x2']), Y(e['y2']))
            le = (X(leaf['x2']), Y(leaf['y2']))
            doors.append(dict(a=a, b=b, leaf=le)); i += 2
        elif t == 'rect' and sw == '1' and e.get('fill') == '#fff' and (e['width'] == '6.0' or e['height'] == '6.0'):
            wins.append(dict(x=X(e['x']), y=Y(e['y']), w=Ln(e['width']), h=Ln(e['height'])))
        elif t in ('rect', 'ellipse', 'circle') and sw in ('0.8', '0.7', '0.5', '.8', '.6', '1', '0.6'):
            if t == 'rect':
                fx.append(dict(k='rect', sw=sw, x=X(e['x']), y=Y(e['y']), w=Ln(e['width']), h=Ln(e['height'])))
            elif t == 'ellipse':
                fx.append(dict(k='ell', sw=sw, cx=X(e['cx']), cy=Y(e['cy']), rx=Ln(e['rx']), ry=Ln(e['ry'])))
            else:
                if e.get('stroke-dasharray'):
                    pass
                else:
                    fx.append(dict(k='circ', sw=sw, cx=X(e['cx']), cy=Y(e['cy']), r=Ln(e['r'])))
        elif t == 'text':
            texts.append(dict(x=X(e['x']), y=Y(e['y']), fs=float(e.get('font-size', 0)), t=html.unescape(e['_txt'] or '')))
        i += 1
    return dict(rooms=rooms, doors=doors, wins=wins, fx=fx, texts=texts)

if __name__ == '__main__':
    import sys, json
    f, ppf, ox, oy = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    d = parse_floor(f, ppf, (ox, oy))
    for r in d['rooms']:
        lab = [t['t'] for t in d['texts'] if r['x'] <= t['x'] <= r['x'] + r['w'] and r['y'] <= t['y'] <= r['y'] + r['h'] and t['fs'] >= 7]
        print('R', r['x'], r['y'], r['w'], r['h'], r['fill'][:8], r['color'], r['op'], lab[:2])
    for x in d['doors']: print('D', x)
    for x in d['wins']: print('W', x)
    print('FX', len(d['fx']))
