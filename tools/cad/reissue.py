"""Reissue Model 1 typical sheets for Model 2 or 3: python3 reissue.py out 2
Runs the Model 1 scripts with the title block, file names and model references switched,
and stamps a model note on each sheet."""
import os, runpy, sys
import cadkit
import sheetlib as SL

OUT, M = sys.argv[1], int(sys.argv[2])
INFO = {2: dict(model_line="MODEL 2 — TOWNHOMES + SUITE", lot_line="LOT: ±66' x 152' DEEP (ASSUMED)", projno="SF-M2"),
        3: dict(model_line="MODEL 3 — BIG HOUSE + CASITA", lot_line="LOT: 80' x 125' + REAR ALLEY", projno="SF-M3")}[M]
NOTE = (f"MODEL {M} REISSUE: typical sheet shared with the Model\u00a01 prototype. Where a note or detail names a Model\u00a01 room, door or "
        f"grid, apply it to the equivalent condition on the Model {M} plans (A-101.{M}, A-102.{M}). The rated exterior wall W2 is not used on Model {M}: "
        f"side yards are 10'-0\" min. (G-002).")

_text = cadkit.Sheet.text


def text(self, p, s, *a, **k):
    if isinstance(s, str):
        s = s.replace("MODEL 1 — STACKED BIG HOUSE", INFO["model_line"]).replace("Model 1", f"Model {M}").replace("MODEL 1", f"MODEL {M}")
    return _text(self, p, s, *a, **k)


cadkit.Sheet.text = text
_tb = SL.border_and_titleblock


def tb(s, cfg):
    cfg = dict(cfg, **INFO)
    _tb(s, cfg)
    sc, ox, oy = s.scale, s.ox, s.oy
    # model note box above the title block, bottom right of the drawing area
    s.rect(21.15, 0.75, 10.6, 0.62, lw="m", fill=1.0)
    from plan_engine import para
    para(s, 21.25, 1.2, NOTE, 10.4, 0.07)
    s.scale, s.ox, s.oy = sc, ox, oy


SL.border_and_titleblock = tb
_pdf, _dxf = cadkit.Sheet.to_pdf, cadkit.Sheet.to_dxf
cadkit.Sheet.to_pdf = lambda self, path, title="", author="": _pdf(self, path.replace("Model1", f"Model{M}"), title.replace("Model 1", f"Model {M}"), author)
cadkit.Sheet.to_dxf = lambda self, path: _dxf(self, path.replace("Model1", f"Model{M}"))

import sheetkit
sheetkit.COMMON.update(INFO)
_save = sheetkit.save
SKIP = set(sys.argv[3:])

JOBS = [("textsheets.py", None), ("details2.py", None), ("a302.py", None), ("d001.py", None), ("d002.py", None)]
sys.argv = [sys.argv[0], OUT]
import textsheets as TS
for (no, file, ttl, fn) in [("G-003", "Model1_General_Notes", "GENERAL\nCONSTRUCTION NOTES", TS.g003), ("S-001", "Model1_Structural_General_Notes", "STRUCTURAL\nGENERAL NOTES", TS.s001),
                            ("P-001", "Model1_Plumbing_Notes_Schedules", "PLUMBING NOTES\n+ SCHEDULES", TS.p001), ("FP-001", "Model1_Fire_Sprinkler_Notes", "FIRE SPRINKLER\nNOTES", TS.fp001),
                            ("EN-001", "Model1_Energy_Compliance", "ENERGY\nCOMPLIANCE", TS.en001), ("A-602", "Model1_Finish_Schedule", "FINISH\nSCHEDULE", TS.a602)]:
    TS.make(no, file, ttl, fn)
for script in ("details2.py", "a302.py", "d001.py", "d002.py"):
    runpy.run_path(script, run_name="__main__")
# P-202 gas alternate only
src = open("diagrams.py").read()
i = src.index("# ===================================================================== P-202")
ns = {"__name__": "__main__"}
exec(compile(src[:src.index("# ===================================================================== E-201")] + src[i:], "diagrams.py", "exec"), ns)

# A-501 interior elevations (typical)
src = open("enlarged.py").read()
i = src.index("# ===================================================================== A-501")
exec(compile(src[:src.index("# ===================================================================== A-401")] + src[i:], "enlarged.py", "exec"), {"__name__": "__main__"})
