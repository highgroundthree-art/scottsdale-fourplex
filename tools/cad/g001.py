"""G-001 cover sheet: project data, code summary, sheet index, deferred submittals. Model 1."""
import sys
from cadkit import Sheet
from plan_engine import table, para
import sheetlib as SL
from elev import Elev
import a20x_1 as P

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATE = "2026-11-18"
s = Sheet(origin=(0, 0), scale=96)  # 1/8" = 1'-0" for the cover graphic

# ---- title block area big title
s.text((1.0, 22.6), "SCOTTSDALE FOURPLEX", 0.55, font="Helvetica-Bold", align="l")
s.text((1.0, 21.95), "MODEL 1 — STACKED BIG HOUSE  ·  FOUR DWELLING UNITS  ·  DESIGN DEVELOPMENT SET", 0.2, align="l")
s.line((1.0, 21.75), (31.8, 21.75), lw="h")

# ---- cover graphic: south elevation at 1/8"
e = Elev(s, (2.0, 15.6))
P.facade(e, 0, 60, P.south_g, P.south_u, "long", shutters=True, ds=(0.6, 59.4), extras=P.loggia_front, depth=50.0)
e.grade(-4, 64)
s.text((5.75, 14.85), "SOUTH (STREET) ELEVATION — SEE A-201.1", 0.1, font="Helvetica-Bold")

# ---- project data
y = SL.head(s, 1.0, 14.2, "PROJECT DATA", 8.6)
rows = [
    ("PROJECT", "Scottsdale Fourplex — Model 1, Stacked Big House"),
    ("ADDRESS / APN", "TBD (south Scottsdale, near Old Town)"),
    ("OWNER / DEVELOPER", "TBD"),
    ("ZONING", "TBD — confirm middle-housing district, setbacks and height at pre-app"),
    ("LOT", "80' x 125' typical, 10,000 SF (assumed until a parcel is selected)"),
    ("USE", "Four dwelling units, sold whole to one owner-occupant (1–4 unit residential financing)"),
    ("UNITS", "A 2 BR / 2 BA (Type A) · B, C, D 3 BR / 2 BA · 1,250 SF each"),
    ("GROSS FLOOR AREA", "6,000 SF (3,000 SF per floor) plus 78 SF covered loggia"),
    ("STORIES / HEIGHT", "2 stories · ridge ±29'-0\" above finish floor (±29'-8\" above grade)"),
    ("LOT COVERAGE", "±30% (C-101)"),
    ("PARKING", "7 stalls incl. 1 van-accessible, rear lot off the east side drive"),
]
for k, v in rows:
    s.text((1.0, y), k, 0.075, font="Helvetica-Bold", align="l"); s.text((3.3, y), v, 0.075, align="l"); y -= 0.21

y -= 0.1
y = SL.head(s, 1.0, y, "CODE SUMMARY (CONFIRM AT PRE-APPLICATION)", 8.6)
code = [
    ("CODES", "2021 IBC, IFC, IPC, IMC, IFGC, IECC, IEBC, IgCC with City of Scottsdale amendments; 2020 NEC; ICC A117.1-2009"),
    ("OCCUPANCY", "Group R-2 (four dwelling units)"),
    ("CONSTRUCTION", "Type V-B, fully sprinklered NFPA 13R (City Code Ch. 36)"),
    ("SEPARATIONS", "1-hour unit separation walls (W1) and floor/ceilings (F1); 1-hour west wall (W2), 7'-0\" to lot line"),
    ("ALLOWABLE", "3 stories, 60 ft, 7,000 SF per story (V-B, R-2, 13R) — provided 2 stories, 3,000 SF"),
    ("ACCESSIBILITY", "Unit A Type A (by choice), Unit B Type B; upper units not covered (no elevator)"),
    ("ENERGY", "IECC 2021 residential, climate zone 2B (EN-001)"),
]
for k, v in code:
    s.text((1.0, y), k, 0.075, font="Helvetica-Bold", align="l")
    y = min(para(s, 3.3, y, v, 6.3, 0.075, lead=1.4), y - 0.21) - 0.04

# ---- vicinity map placeholder + deferred submittals
s.rect(10.2, 9.4, 4.4, 4.6, lw="l")
s.text((12.4, 13.75), "VICINITY MAP", 0.1, font="Helvetica-Bold")
s.text((12.4, 11.75), "Parcel not yet selected.", 0.08)
s.text((12.4, 11.55), "South Scottsdale, inside the", 0.08)
s.text((12.4, 11.35), "middle-housing area near Old Town.", 0.08)
SL.north_arrow(s, 12.4, 10.2)
y2 = SL.head(s, 10.2, 9.0, "DEFERRED SUBMITTALS", 4.4)
for t in ("Post-tension slab shop drawings and calcs", "Engineered floor and roof truss layouts and calcs", "Fire sprinkler shop drawings and hydraulic calcs (NFPA 13R)", "Any items Scottsdale adds at pre-application"):
    y2 = para(s, 10.2, y2, "• " + t, 4.4, 0.075)
y2 -= 0.1
y2 = SL.head(s, 10.2, y2, "DESIGN TEAM", 4.4)
for t in ("ARCHITECT OF RECORD — TBD", "STRUCTURAL — TBD", "MEP / ENERGY — TBD", "CIVIL / LANDSCAPE — TBD", "FIRE SPRINKLER — deferred, licensed contractor"):
    s.text((10.2, y2), t, 0.075, align="l"); y2 -= 0.2

# ---- sheet index (two columns)
IDX = [
    ("G-001", "Cover Sheet, Project Data, Sheet Index", "DD-1"), ("G-002", "Code Analysis", "DD-1"), ("G-003", "General Construction Notes", "DD-1"),
    ("G-004", "Accessibility Plan and Notes", "DD-1"), ("G-005", "Rated Assemblies and Life Safety Plan", "DD-1"),
    ("C-101", "Site Plan", "DD-1"), ("C-102", "Grading and Drainage Plan", "DD-1"), ("C-103", "Utility Plan", "DD-1"), ("L-101", "Landscape Plan", "DD-1"),
    ("A-101.1", "Ground Floor Plan", "DD-1"), ("A-102.1", "Upper Floor Plan", "DD-1"), ("A-103.1", "Roof Plan", "DD-1"),
    ("A-201.1", "Exterior Elevations — South, North", "DD-1"), ("A-202.1", "Exterior Elevations — East, West", "DD-1"), ("A-301.1", "Building Sections", "DD-1"),
    ("A-302", "Wall Sections", "DD-1"), ("A-401", "Enlarged Plans — Kitchens", "DD-1"), ("A-402", "Enlarged Plans — Baths", "DD-1"),
    ("A-501", "Interior Elevations", "DD-1"), ("A-601", "Door and Window Schedules and Types", "DD-1"), ("A-602", "Finish Schedule", "DD-1"), ("A-701", "Reflected Ceiling Plans", "DD-1"),
    ("S-001", "Structural General Notes", "DD-1"), ("S-101", "Foundation Plan — PT Slab", "DD-1"), ("S-102", "Floor Framing Plan", "DD-1"), ("S-103", "Roof Framing Plan", "DD-1"),
    ("S-201", "Shear Wall Plan and Schedule", "DD-1"), ("S-501", "Foundation and PT Details", "DD-1"), ("S-502", "Framing Details", "DD-1"), ("S-503", "Truss Details", "DD-1"),
    ("X-101", "MEP Coordination, Chase and Penetration Plan", "DD-1"),
    ("M-001", "Mechanical Notes and Equipment Schedule", "DD-1"), ("M-101", "Ground Floor HVAC Plan", "DD-1"), ("M-102", "Upper Floor HVAC Plan", "DD-1"), ("M-501", "Mechanical Details", "DD-1"),
    ("P-001", "Plumbing Notes, Legend, Schedules", "DD-1"), ("P-101.1", "Waste and Vent Plan", "DD-1"), ("P-102.1", "Water and Gas Plan", "DD-1"),
    ("P-201", "DWV and Water Riser Diagrams", "DD-1"), ("P-202", "Gas Riser Diagram", "DD-1"),
    ("E-001", "Electrical Notes and Symbols", "DD-1"), ("E-101", "Ground Floor Electrical Plan", "DD-1"), ("E-102", "Upper Floor Electrical Plan", "DD-1"),
    ("E-201", "One-Line Diagram", "DD-1"), ("E-301", "Panel Schedules and Load Calculations", "DD-1"), ("E-401", "Site Electrical", "DD-1"),
    ("FP-001", "Fire Sprinkler Notes and Riser", "DD-1"), ("FP-101", "Fire Sprinkler Layout", "DD-1"), ("EN-001", "Energy Compliance", "DD-1"),
    ("D-001", "Envelope Details", "DD-1"), ("D-002", "Rated Assembly and Firestop Details", "DD-1"), ("D-003", "Accessibility Details", "DD-1"),
]
cols = [("SHEET", 0.75, "l"), ("TITLE", 3.35, "l"), ("STATUS", 0.85, "c")]
half = (len(IDX) + 1) // 2
y3 = SL.head(s, 15.2, 21.4, f"SHEET INDEX — MODEL 1 ({len(IDX)} SHEETS)", 10.9)
table(s, 15.2, y3 + 0.04, cols, IDX[:half], h=0.07, rowh=0.165)
table(s, 21.1, y3 + 0.04, cols, IDX[half:], h=0.07, rowh=0.165)
y4 = y3 - (half + 1) * 0.165 - 0.25
for t in ["STATUS: DD-1 = drawn to construction-document standard in this set. CONCEPT = concept sheet exists (Claude artifacts), to be redrawn on this title block. SE / MEP = prepared and sealed by the engineer of record; design intent to be drafted. DEFERRED = deferred submittal by the specialty contractor. — = not started.",
          "Models 2 and 3 follow the same sheet list with suffix .2 and .3 (floor plans already drawn: A-101.2, A-102.2, A-101.3, A-102.3, A-111.3)."]:
    y4 = para(s, 15.2, y4, t, 10.9, 0.075)

s.scale = 48  # title block text uses paper inches only
SL.border_and_titleblock(s, dict(model_line="MODEL 1 — STACKED BIG HOUSE", lot_line="LOT: 80' x 125' TYPICAL", projno="SF-M1", date=DATE,
                                 sheet_no="G-001", sheet_title="COVER SHEET\n+ SHEET INDEX"))
s.scale = 96
base = f"{OUT}/G-001_Model1_Cover_Sheet_and_Index"
s.to_pdf(base + ".pdf", title="G-001 Cover Sheet - Model 1", author="Scottsdale Fourplex")
s.to_dxf(base + ".dxf")
print("wrote", base)
