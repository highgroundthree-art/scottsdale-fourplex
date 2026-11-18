src=open('a101_1.py').read()
names=['spaces (feet)','openings','fixtures & casework','draw walls/openings','grids','dimensions (model inches)','tags','notes columns']
idx=[src.index('# ------------------------------------------------------------------ '+n) for n in names]
head=src[:idx[0]]
parts={n:src[idx[i]:(idx[i+1] if i+1<len(idx) else len(src))] for i,n in enumerate(names)}
def rl(text, prefix, new):
    lines=text.split('\n'); hit=0
    for i,l in enumerate(lines):
        if l.strip().startswith(prefix):
            lines[i]=new; hit+=1
    assert hit==1,(prefix,hit)
    return '\n'.join(lines)
spaces=open('a102_spaces.txt').read()
openings=open('a102_openings.txt').read()
fx=parts['fixtures & casework']
a=fx.index('# Unit A'); b=fx.index('# bed 2 closet rod')
fx=fx[:a]+open('a102_fx_units.txt').read()+fx[b:]
fx=fx.replace('# bed 2 closet rod\nL(0.6, 26.75, 5.4, 26.75, dash="HIDDEN")','# closet rods\nL(0.6, 26.75, 5.4, 26.75, dash="HIDDEN")\nL(8.75, 37.6, 8.75, 41.9, dash="HIDDEN")')
fx=fx.replace('turning(19.6, 31.2)\n','',1).replace('turning(40.4, 31.2)\n','')
a=fx.index('# Stair (west run up'); b=fx.index('# chases hatch')
fx=fx[:a]+open('a102_stair.txt').read()+fx[b:]
a=fx.index('# fire riser'); b=fx.index('# electric panels')
fx=fx[:a]+fx[b:]
dims=parts['dimensions (model inches)']
dims=dims.replace('(0, 7, 25, 30, 35, 53, 60)], 0, "h", 0.55)','(0, 7, 25, 35, 53, 60)], 0, "h", 0.55)')
dims=dims.replace('(0, 12.5, 25, 29.5, 35, 42.5, 55, 60)], 600, "h", -0.55)','(0, 5, 17.5, 25, 30, 35, 42.5, 55, 60)], 600, "h", -0.55)')
dims=dims.replace('idim_h([15, 25], 36.3)\n','idim_h([15, 25], 36.3)\nidim_h([35, 45], 36.3)\n')
tags=parts['tags']
tags=tags.replace('for (x, y, t) in [(3.0, 27.3, "CL"), (57.0, 27.3, "CL"), (51.25, 40.2, "CL")]:','for (x, y, t) in [(3.0, 27.3, "CL"), (57.0, 27.3, "CL"), (51.25, 40.2, "CL"), (8.75, 40.2, "CL")]:')
a=tags.index('    OVR = {'); b=tags.index('    if d["tag"] in ("101",):')
tags=tags[:a]+'''    OVR = {"213": (11.6, 11.0), "233": (48.4, 11.0), "212": (12.6, 4.0), "232": (47.4, 4.0),
           "214": (22.0, 15.9), "234": (38.0, 15.9), "215": (5.0, 15.5), "235": (55.0, 15.5),
           "217": (15.6, 21.5), "237": (44.4, 21.5), "219": (11.6, 44.0), "210": (23.4, 44.0), "230": (36.6, 44.0)}
    if d["tag"] in OVR:
        c = s.m2p(OVR[d["tag"]][0] * F, OVR[d["tag"]][1] * F)
'''+tags[b:]
a=tags.index('    if d["tag"] in ("101",):'); b=tags.index('    circle_tag(s, c, d["tag"])')
tags=tags[:a]+tags[b:]
tags=tags.replace('callout(14.25, 0.75, 10.4, 7.6, "3", "A-402", (24.65, 7.7, -0.3, 0.0))\n','')
tags=tags.replace('callout(15.2, 25.2, 9.55, 11.6, "1", "A-401"','callout(15.2, 25.2, 9.55, 11.6, "2", "A-401"')
tags=tags.replace('"A-101.1", 0.07)','"A-102.1", 0.07)').replace('GROUND FLOOR PLAN','UPPER FLOOR PLAN').replace('UNITS A + B','UNITS C + D')
tags=tags.replace('hex_tag(s, s.m2p(25 * F, 47.0 * F), "W1"); hex_tag(s, s.m2p(35 * F, 47.0 * F), "W1")','hex_tag(s, s.m2p(25 * F, 48.5 * F), "W1"); hex_tag(s, s.m2p(35 * F, 48.5 * F), "W1")')
n=parts['notes columns']
n=rl(n,'"Every bedroom has','    "Every bedroom has an emergency escape and rescue opening: 5.7 SF min. net clear, 24\\" min. clear height, 20\\" min. clear width, sill 44\\" max. A.F.F. (IBC 1031). Bedroom 3 (C211) egresses through window A on the south wall.",')
n=rl(n,'"Unit A is an ICC','    "Units C and D are upper-floor units in a building without an elevator, so Fair Housing Act Type B design applies to ground-floor units only. Lever hardware and 32\\" clear doors are still provided throughout.",')
n=n.replace('Unit entry doors 110 and 120','Unit entry doors 210 and 230')
n=n.replace('Unit A: install grab bars and a fold-down shower seat.','Upper-floor washers and water heaters sit in drain pans with automatic leak shutoff.')
n=n.replace('42 SF shown.','42 SF shown (3050 + 3050 + 3040).')
n=n.replace('42\\" guards at the well.','42\\" guards at the well and the landing edge.')
n=n.replace('Units A and B 1,250 SF each.','Units C and D 1,250 SF each. Floor/ceiling below is the F1 1-hour decoupled assembly (G-005).')
a=n.index('drows = ['); b=n.index(']\ny2 = table(s, X2, y2 + 0.04, DCOLS, drows')
D3="3'-0\\\" x 8'-0\\\""; BI="(2) 1'-6\\\" x 8'-0\\\""; BP="(2) 2'-6\\\" x 8'-0\\\""
M="\\u2014"
rows=[("210","UNIT C ENTRY",D3,"C","20 MIN S","ENTRY / CLOSER","5"),("211","C PRIMARY BEDROOM",D3,"D",M,"PRIVACY",""),("212","C PRIMARY BATH",D3,"D",M,"PRIVACY",""),
("213","C WIC",D3,"D",M,"PASSAGE",""),("214","C LAUNDRY",BI,"F",M,"PASSAGE",""),("215","C WATER HEATER",BI,"F",M,"PASSAGE","6"),("216","C BEDROOM 2",D3,"D",M,"PRIVACY",""),
("217","C HALL BATH",D3,"D",M,"PRIVACY",""),("218","C BED 2 CLOSET",BP,"E",M,"PULLS",""),("219","C BEDROOM 3",D3,"D",M,"PRIVACY",""),("220","C BED 3 CLOSET",BP,"E",M,"PULLS",""),
("230","UNIT D ENTRY",D3,"C","20 MIN S","ENTRY / CLOSER","5"),("231","D PRIMARY BEDROOM",D3,"D",M,"PRIVACY",""),("232","D PRIMARY BATH",D3,"D",M,"PRIVACY",""),("233","D WIC",D3,"D",M,"PASSAGE",""),
("234","D LAUNDRY",BI,"F",M,"PASSAGE",""),("235","D WATER HEATER",BI,"F",M,"PASSAGE","6"),("236","D BEDROOM 2",D3,"D",M,"PRIVACY",""),("237","D HALL BATH",D3,"D",M,"PRIVACY",""),
("238","D BED 2 CLOSET",BP,"E",M,"PULLS",""),("239","D BEDROOM 3",D3,"D",M,"PRIVACY",""),("240","D BED 3 CLOSET",BP,"E",M,"PULLS","")]
n=n[:a]+'drows = [\n'+"".join('    ('+", ".join(f'"{v}"' for v in r)+'),\n' for r in rows)+n[b:]
n=rl(n,'for t in ["TYPES:','for t in ["TYPES: C solid-core wood 1\\u00be\\", 20-min label; D solid-core wood flush, 1\\u00be\\"; E bypass, solid-core; F bi-fold, solid-core.",')
n=rl(n,'"NOTES: 1 Type A unit','          "NOTES: 5 Self-closing, positive latching, smoke gasketing (S-label). 6 Combustion and make-up air per IFGC if gas option."]:')
a=n.index('wrows = ['); b=n.index(']\ny2 = table(s, X2, y2 + 0.04, WCOLS, wrows')
n=n[:a]+'''wrows = [
    ("A", "6'-0\\" x 4'-0\\"", "HORIZ. SLIDER", "3'-0\\"", "YES", "8", "BEDROOMS"),
    ("B", "3'-0\\" x 5'-0\\"", "SINGLE HUNG", "2'-0\\"", "BED 2", "2", "WEST (W2)"),
    ("C", "3'-0\\" x 4'-0\\"", "SINGLE HUNG", "3'-0\\"", "\\u2014", "1", "WEST (W2) BED 3"),
    ("D", "6'-0\\" x 5'-0\\"", "HORIZ. SLIDER", "2'-0\\"", "\\u2014", "3", "LIVING / DINING"),
    ("F", "3'-0\\" x 5'-0\\"", "FIXED, ARCH TOP", "2'-0\\"", "\\u2014", "1", "LANDING (SOUTH)"),
'''+n[b:]
n=n.replace("Egress windows: verify net clear opening with the manufacturer.","Upper-floor egress windows need 5.7 SF net clear; verify with the manufacturer. Window C is not an egress window.")
a=n.index('dd = ['); b=n.index(']\nfor n, t in dd:')
n=n[:a]+'''dd = [
    ("a.", "Bedroom doors 211 and 231 swing into the bedrooms; hall bath doors 217 and 237 swing out to the hall (they hit the tubs swinging in). Matches A-101.1."),
    ("b.", "Fixtures are kept off W1 and stacked over the ground floor: primary baths over A108/B108, hall baths over A106/B106, kitchens over kitchens."),
    ("c.", "Stair: the mid landing is open to below from this level; 42\\" guards at the landing edge and the well."),
    ("d.", "OPEN \\u2014 The core space over house storage 102 has no access from this floor. Drawn as a storage loft reached by a ceiling hatch from 102. Confirm, or leave it as dead space."),
'''+n[b:]
n=rl(n,'y2 = head(X2, y2, "AREA SUMMARY','y2 = head(X2, y2, "AREA SUMMARY \\u2014 UPPER FLOOR", 5.25)')
n=rl(n,'arows = [("UNIT A','arows = [("UNIT C (UPPER FLAT, OWNER OR RENTAL)", "3 BR / 2 BA", "\\u2014", "1,250"),')
n=rl(n,'("UNIT B (FLAT, RENTAL)"','         ("UNIT D (UPPER FLAT, RENTAL)", "3 BR / 2 BA", "\\u2014", "1,250"),')
n=rl(n,'("COMMON CORE (ENTRY','         ("COMMON CORE (LANDING, STAIR, LOFT)", "\\u2014", "\\u2014", "500"),')
n=n.replace('("GROUND FLOOR", 0.14,','("UPPER FLOOR", 0.14,').replace('"A-101.1", 0.42,','"A-102.1", 0.42,')
n=n.replace('A-101.1_Model1_Ground_Floor_Plan','A-102.1_Model1_Upper_Floor_Plan').replace('"A-101.1 Ground Floor Plan - Model 1"','"A-102.1 Upper Floor Plan - Model 1"')
n=n.replace('"ROOM NAME", "A101"','"ROOM NAME", "C201"')
open('a102_1.py','w').write(head+spaces+openings+fx+parts['draw walls/openings']+parts['grids']+dims+tags+n)
