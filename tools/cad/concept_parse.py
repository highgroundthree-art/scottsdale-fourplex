import re
def parse(path):
    s=open(path).read()
    vb=[float(v) for v in re.search(r'viewBox="([^"]+)"',s).group(1).split()]
    els=[]
    for m in re.finditer(r'<(rect|circle|ellipse|line|text|path|polygon)\b([^>]*?)/?>(?:([^<]*)</text>)?',s):
        tag,attrs,txt=m.groups()
        a=dict(re.findall(r'([\w-]+)="([^"]*)"',attrs)); a['_t']=tag; a['_txt']=txt
        els.append(a)
    return vb,els
if __name__=='__main__':
    import sys,collections
    for f in sys.argv[1:]:
        vb,els=parse(f)
        rooms=[e for e in els if e['_t']=='rect' and e.get('stroke-width')=='1.3']
        xs=[float(e['x']) for e in rooms]+[float(e['x'])+float(e['width']) for e in rooms]
        ys=[float(e['y']) for e in rooms]+[float(e['y'])+float(e['height']) for e in rooms]
        c=collections.Counter((e['_t'],e.get('stroke-width'),e.get('stroke')) for e in els)
        print(f.split('/')[-1],vb,'bbox',min(xs),max(xs),min(ys),max(ys),'rooms',len(rooms))
        print('  ',c.most_common(14))
        print('  texts:',[ (e['_txt'],e.get('font-size')) for e in els if e['_t']=='text'][:80])
