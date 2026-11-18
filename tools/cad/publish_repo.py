"""Copy Model 1 sheets to the repo, rebuild the combined set, update sheets.json and the build-set gallery, commit and push.
usage: python3 publish_repo.py "commit message"
"""
import glob, json, os, re, subprocess, sys

CAD = "/home/claude/cad"
REPO = "/home/claude/scottsdale-fourplex"
CD = f"{REPO}/drawings/construction-documents"
ORDER = ["G-001", "G-002", "G-003", "G-004", "G-005", "C-101", "C-102", "C-103", "L-101", "A-101.1", "A-102.1", "A-103.1", "A-201.1", "A-202.1",
         "A-301.1", "A-302", "A-401", "A-402", "A-501", "A-601", "A-602", "A-701", "S-001", "S-101", "S-102", "S-103", "S-201", "S-501", "S-502", "S-503",
         "X-101", "M-001", "M-101", "M-102", "M-501", "P-001", "P-101.1", "P-102.1", "P-201", "P-202", "E-001", "E-101", "E-102", "E-201", "E-301", "E-401",
         "FP-001", "FP-101", "EN-001", "D-001", "D-002", "D-003"]
HAND = {"A-101.1", "A-102.1"}   # already in the gallery as concept pairs


def sh(cmd, cwd=None):
    print("+", cmd)
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def main(msg, model=1):
    global ORDER, HAND
    if model != 1:
        ORDER = [x.replace(".1", f".{model}") if x.endswith(".1") else x for x in ORDER]
        if model == 3:
            ORDER.insert(ORDER.index("A-102.3") + 1, "A-111.3")
        HAND = {f"A-101.{model}", f"A-102.{model}", "A-111.3"}
        return main_model(msg, model)
    # mark drawn sheets DD-1 on the cover index and regenerate G-001
    g = open(f"{CAD}/g001.py").read()
    for sid in ORDER:
        if glob.glob(f"{CAD}/out/{sid}_Model1*.pdf"):
            g = re.sub(r'\("%s", ("[^"]*"), "[^"]*"\)' % re.escape(sid), r'("%s", \1, "DD-1")' % sid, g)
    open(f"{CAD}/g001.py", "w").write(g)
    sh("python3 g001.py out", CAD)
    sh("git pull -q --no-rebase origin main", REPO)
    have = []
    for sid in ORDER:
        pdfs = [p for p in glob.glob(f"{CAD}/out/{sid}_*.pdf") if "Model1" in p]
        if not pdfs:
            continue
        pdf = sorted(pdfs)[0]
        base = pdf[:-4]
        if not os.path.exists(base + ".png") or os.path.getmtime(base + ".png") < os.path.getmtime(pdf):
            sh(f"pdftoppm -r 100 -png -singlefile '{pdf}' '{base}'")
        for ext in (".pdf", ".dxf", ".png"):
            sh(f"cp '{base}{ext}' '{CD}/'")
        have.append((sid, os.path.basename(base)))
    sh(f"cp {CAD}/*.py {REPO}/tools/cad/")
    files = " ".join(f"'{CD}/{b}.pdf'" for _, b in have)
    sh(f"pdfunite {files} '{CD}/set.tmp' && mv '{CD}/set.tmp' '{CD}/Scottsdale_Fourplex_Model1_DD_Set.pdf'")
    # sheets.json
    p = f"{REPO}/data/sheets.json"
    d = json.load(open(p))
    idx = {x["sheet"]: i for i, x in enumerate(d)}
    titles = {}
    g = open(f"{CAD}/g001.py").read()
    for m in re.finditer(r'\("([A-Z]{1,2}-\d{3}(?:\.\d)?)", "([^"]+)", "([^"]+)"\)', g):
        titles[m.group(1)] = m.group(2).encode().decode("unicode_escape") if "\\u" in m.group(2) else m.group(2)
    for sid, b in have:
        rec = dict(sheet=sid, title=f"Model 1, {titles.get(sid, sid)} (Design Development, CAD)", plan="1", revision="DD-1", date="2026-11-18",
                   status="Design Development", file=f"drawings/construction-documents/{b}.pdf")
        if sid in idx:
            d[idx[sid]] = rec
        else:
            d.append(rec)
    json.dump(d, open(p, "w"), indent=2)
    # gallery: rebuild the Model 1 "rest of the set" grid
    h = open(f"{REPO}/index.html").read()
    key = '<h3 class="model-h">Model 1 &middot; the full build set</h3>'
    if key not in h:
        key = '<h3 class="model-h">Model 1 &middot; the rest of the architectural set</h3>'
    start = h.index(key)
    gs = h.index('<div class="grid g2">', start)
    ge = h.index("\n    </div>", gs)
    figs = []
    for sid, b in have:
        if sid in HAND:
            continue
        t = titles.get(sid, sid)
        src = f"drawings/construction-documents/{b}"
        figs.append(f'<figure class="dwg"><img src="{src}.png" alt="{sid} {t}"><figcaption><b>{sid}</b> &middot; {t} &middot; DD-1 &middot; '
                    f'<a href="{src}.pdf">PDF</a> &middot; <a href="{src}.dxf">DXF (AutoCAD)</a></figcaption></figure>')
    h = h[:gs] + '<div class="grid g2">\n      ' + "\n      ".join(figs) + h[ge:]
    h = h.replace('Model 1 &middot; the rest of the architectural set', 'Model 1 &middot; the full build set')
    h = h.replace('<h3 class="model-h">Model 1 &middot; the full build set</h3>', '<h3 class="model-h">Model 1 &middot; the full build set</h3>', 1)
    h = re.sub(r'Download the Model 1 set so far \(PDF, \d+ sheets\)', f'Download the Model 1 set so far (PDF, {len(have)} sheets)', h)
    open(f"{REPO}/index.html", "w").write(h)
    sh("git add -A", REPO)
    r = subprocess.run("git diff --cached --quiet", shell=True, cwd=REPO)
    if r.returncode:
        cm = msg + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01NME2RbPyaSBYNEZmfVuK6o"
        open("/tmp/cm.txt", "w").write(cm)
        sh("git commit -q -F /tmp/cm.txt && git -c push.negotiate=true push -q origin main && git log --oneline -1", REPO)
    print("SHEETS", len(have))


def main_model(msg, model):
    sh("git pull -q --no-rebase origin main", REPO)
    have = []
    for sid in ORDER:
        pdfs = [p for p in glob.glob(f"{CAD}/out/{sid}_*.pdf") if f"Model{model}" in p]
        if not pdfs:
            print("MISSING", sid); continue
        pdf = sorted(pdfs)[0]; base = pdf[:-4]
        if not os.path.exists(base + ".png") or os.path.getmtime(base + ".png") < os.path.getmtime(pdf):
            sh(f"pdftoppm -r 100 -png -singlefile '{pdf}' '{base}'")
        for ext in (".pdf", ".dxf", ".png"):
            sh(f"cp '{base}{ext}' '{CD}/'")
        have.append((sid, os.path.basename(base)))
    sh(f"cp {CAD}/*.py {REPO}/tools/cad/")
    files = " ".join(f"'{CD}/{b}.pdf'" for _, b in have)
    sh(f"pdfunite {files} '{CD}/set.tmp' && mv '{CD}/set.tmp' '{CD}/Scottsdale_Fourplex_Model{model}_DD_Set.pdf'")
    p = f"{REPO}/data/sheets.json"
    d = json.load(open(p))
    keyf = lambda x: (x["sheet"], x.get("plan"))
    idx = {keyf(x): i for i, x in enumerate(d)}
    for sid, b in have:
        t = b.split(f"_Model{model}_", 1)[1].replace("_", " ")
        rec = dict(sheet=sid, title=f"Model {model}, {t} (Design Development, CAD)", plan=str(model), revision="DD-1", date="2026-11-18",
                   status="Design Development", file=f"drawings/construction-documents/{b}.pdf")
        if (sid, str(model)) in idx:
            d[idx[(sid, str(model))]] = rec
        else:
            d.append(rec)
    json.dump(d, open(p, "w"), indent=2)
    h = open(f"{REPO}/index.html").read()
    figs = []
    for sid, b in have:
        if sid in HAND:
            continue
        t = b.split(f"_Model{model}_", 1)[1].replace("_", " ")
        src = f"drawings/construction-documents/{b}"
        figs.append(f'<figure class="dwg"><img src="{src}.png" alt="{sid} {t}"><figcaption><b>{sid}</b> &middot; {t} &middot; DD-1 &middot; '
                    f'<a href="{src}.pdf">PDF</a> &middot; <a href="{src}.dxf">DXF (AutoCAD)</a></figcaption></figure>')
    block = (f'    <h3 class="model-h" id="set-model{model}">Model {model} &middot; the full build set</h3>\n'
             f'    <p class="sub" style="margin-bottom:16px"><a class="btn" href="drawings/construction-documents/Scottsdale_Fourplex_Model{model}_DD_Set.pdf">Download the Model {model} set (PDF, {len(have)} sheets)</a></p>\n'
             '    <div class="grid g2">\n      ' + "\n      ".join(figs) + "\n    </div>\n")
    marker = f'<h3 class="model-h" id="set-model{model}">'
    if marker in h:
        a = h.index(marker); a = h.rindex("\n", 0, a) + 1
        b_ = h.index("\n    </div>\n", a) + len("\n    </div>\n")
        h = h[:a] + block + h[b_:]
    else:
        i = h.index('<section id="buildset">'); j = h.index("</section>", i)
        k = h.rindex("  </div>", i, j)
        h = h[:k] + block + h[k:]
    open(f"{REPO}/index.html", "w").write(h)
    sh("git add -A", REPO)
    r = subprocess.run("git diff --cached --quiet", shell=True, cwd=REPO)
    if r.returncode:
        cm = msg + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01NME2RbPyaSBYNEZmfVuK6o"
        open("/tmp/cm.txt", "w").write(cm)
        sh("git commit -q -F /tmp/cm.txt && git -c push.negotiate=true push -q origin main && git log --oneline -1", REPO)
    print("SHEETS", len(have))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1)
