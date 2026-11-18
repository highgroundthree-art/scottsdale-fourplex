"""Notes / schedule sheets for Model 1: G-003, S-001, M-001, P-001, E-001, FP-001, EN-001, A-602, E-301."""
from sheetkit import *
from plan_engine import wrap, table
import sheetlib as SL

COLW, GAP, X0, YTOP, YMIN = 6.05, 0.35, 1.0, 23.1, 0.9


class Flow:
    def __init__(self, s, ncols=5):
        self.s, self.col, self.y = s, 0, YTOP
        self.ncols = ncols

    @property
    def x(self):
        return X0 + self.col * (COLW + GAP)

    def need(self, hgt):
        if self.y - hgt < YMIN:
            self.col += 1; self.y = YTOP

    def notes(self, title, items, h=0.098):
        est = 0.28 + sum((len(wrap(t, COLW - 0.2, h, "Helvetica")) * h * 1.45 + h * 0.5) for t in items)
        if est > YTOP - YMIN:   # split long sections
            half = len(items) // 2
            self.notes(title, items[:half], h); self.notes(title + " (CONT.)", items[half:], h); return
        self.need(est)
        self.y = SL.notes_list(self.s, self.x, self.y, title, items, COLW, h) - 0.12

    def table(self, title, cols, rows, h=0.085, rowh=0.21):
        scale = COLW / sum(c[1] for c in cols)
        cols = [(a, b * scale, c) for a, b, c in cols]
        est = 0.3 + (len(rows) + 1) * rowh
        self.need(est)
        y = SL.head(self.s, self.x, self.y, title, COLW)
        self.y = table(self.s, self.x, y + 0.04, cols, rows, h=h, rowh=rowh) - 0.3


def make(sheet, file, ttl, build):
    s = new()
    f = Flow(s)
    build(f)
    save(s, sheet, file, ttl)


# ===================================================================== G-003
def g003(f):
    f.notes("GENERAL CONDITIONS", [
        "These drawings are design development documents for the Model 1 prototype. They are not for construction until completed, coordinated and sealed by an Arizona-registered architect and engineers of record and approved by the City of Scottsdale.",
        "Work shall comply with the 2021 IBC, IRC (where referenced), IFC, IPC, IMC, IFGC, IECC, 2020 NEC, ICC A117.1-2009, the federal Fair Housing Act, and all City of Scottsdale amendments and ordinances in force at permit.",
        "Contractor shall verify all dimensions and conditions at the site before starting work and report discrepancies to the architect in writing. Do not scale drawings. Written dimensions govern; large-scale details govern over small-scale plans.",
        "Dimensions on plans are to the face of stud or face of concrete unless noted; at rated walls dimensions are to the centerline of the assembly.",
        "Where a detail or note applies to one location it applies to all similar locations unless noted otherwise.",
        "Contractor is responsible for means, methods, sequencing, and jobsite safety, including OSHA 1926 fall protection and excavation requirements.",
        "Deferred submittals (PT slab, trusses, fire sprinklers) shall be submitted to the architect and engineer for review before submittal to the City; do not install before City approval.",
        "Substitutions: products listed as basis of design may be substituted only with written approval and, for rated assemblies, only with a tested and listed equal.",
    ])
    f.notes("QUALITY + DIGNITY STANDARD", [
        "This building is affordable, not cheap. Where these documents exceed code (1-hour separations, STC/IIC 50, U-0.30 windows, a Type A unit) the higher standard is part of the contract and is not value-engineered without the owner's written approval.",
        "Every unit gets the same finishes, fixtures and daylight. No unit is the 'lesser' unit.",
        "Mock-up: build one complete bathroom and one window/stucco wall panel for owner review before production.",
        "Sound: field-test one W1 wall and one F1 floor before move-in (FSTC/FIIC 45 min.). Failures are corrected at the contractor's cost.",
        "Air: blower-door test every unit (5 ACH50 max.); duct leakage test every system.",
    ])
    f.notes("SITE + EARTHWORK", [
        "Obtain a geotechnical report for the selected parcel; follow its recommendations for subgrade, fill, compaction and PT slab design values.",
        "Call Arizona 811 (Blue Stake) at least two working days before excavation.",
        "Dust control per Maricopa County Rule 310: obtain a dust control permit when disturbing 0.1 acre or more; water trucks, stabilized construction entrance, track-out control.",
        "Storm water: best management practices per the City of Scottsdale; protect inlets and the street gutter; no washout into the gutter.",
        "Termite treatment per Arizona Office of Pest Management before vapor retarder placement.",
    ])
    f.notes("CONCRETE + MASONRY", [
        "Concrete per ACI 318 and S-001. Slab finish: steel trowel in units; broom finish at exterior walks and patios.",
        "Exterior flatwork: 4\" concrete on compacted subgrade, control joints at 8 ft max., slopes per C-102 and accessibility limits.",
        "Trash enclosure: 6 ft CMU walls with stucco finish to match the building, steel gates with 32\" clear pedestrian gate.",
    ])
    f.notes("WOOD FRAMING", [
        "Framing lumber Douglas-fir or Hem-fir No. 2 or better; studs stud grade; KD-19. Pressure-treated plates on concrete.",
        "Engineered trusses, LVL and LSL per manufacturer's design and S-sheets. Do not cut, notch or drill engineered members without the engineer's written approval.",
        "Blocking: provide 2x blocking for grab bars in all bathrooms (Type B units and all upper units), cabinets, towel bars, TV mounts, handrails and door stops.",
        "Fireblocking at concealed spaces per IBC 718.2: at ceiling and floor levels, soffits, stair stringers, and penetrations.",
    ])
    f.notes("THERMAL + MOISTURE", [
        "Stucco system per D-001 and ASTM C926/C1063 with two layers of WRB. Control joints at 144 SF max. panels.",
        "Roofing: two-piece clay tile per the Tile Roofing Industry Alliance installation manual for the wind zone; two layers of underlayment.",
        "Sealants: polyurethane or silicone at exterior joints; acoustic sealant at all W1 and F1 perimeters; fire-rated sealant only where listed.",
        "Insulation: R-21 walls, R-38 ceilings, R-19 in F1 joists (acoustic). Install to RESNET Grade I.",
    ])
    f.notes("OPENINGS", [
        "Doors and hardware per A-601. Windows per A-601: vinyl or fiberglass, NFRC-labeled, U 0.30 / SHGC 0.25 max.",
        "Every window and door installed with sill pan, jamb and head flashing integrated with the WRB (D-001).",
        "Safety glazing per IBC 2406; escape openings per IBC 1031.",
    ])
    f.notes("FINISHES", [
        "Finishes per A-602. GWB: 1/2\" typical walls, 5/8\" Type X where rated or noted; moisture-resistant board at wet walls; cement board behind tile at tubs and showers.",
        "Level 4 finish on walls and ceilings; level 5 at the shared entry and stair.",
        "Paint: low-VOC (under 50 g/L flat, 150 g/L non-flat), two finish coats over primer.",
        "Flooring: luxury vinyl plank on acoustic mat throughout units (upper units: mat required as part of F1); porcelain tile at baths and the shared entry.",
    ])
    f.notes("SPECIALTIES + EQUIPMENT", [
        "Mailboxes: USPS-approved cluster box unit at the shared entry, accessible heights.",
        "Kitchen appliances per unit: refrigerator, electric/induction range with ducted hood, dishwasher, microwave. ENERGY STAR where available.",
        "Washer and dryer connections in every unit; front-load units in Unit A.",
        "Window coverings: 2\" faux-wood blinds at every window.",
        "Address numerals 6\" min. on the street face, illuminated; unit letters at each unit door.",
    ])
    f.notes("CLOSE-OUT", [
        "Provide owner's manuals, warranties, as-built drawings, test reports (sound, blower door, duct leakage, sprinkler acceptance), and a 30-minute walk-through for the owner of each unit.",
        "One-year contractor warranty; manufacturer warranties for roof (30 yr), windows, water heaters and HVAC.",
    ])
    f.table("ABBREVIATIONS", [("ABBR", 0.8, "l"), ("MEANING", 2.4, "l"), ("ABBR", 0.8, "l"), ("MEANING", 2.4, "l")], [
        ("A.F.F.", "Above finished floor", "GWB", "Gypsum wallboard"), ("AHU", "Air handling unit", "HPWH", "Heat pump water heater"),
        ("CH", "Plumbing chase", "MC", "Meter center"), ("CRD", "Ceiling radiation damper", "O.C.", "On center"),
        ("CU", "Condensing unit", "PT", "Post-tensioned"), ("DS", "Downspout", "RC", "Resilient channel"),
        ("FDC", "Fire department connection", "STC/IIC", "Sound / impact class"), ("FSD", "Fire separation distance", "VTR", "Vent through roof"),
        ("FT", "Floor truss", "W1/W2", "Rated wall types (G-005)")])


# ===================================================================== S-001
def s001(f):
    f.notes("DESIGN CRITERIA (PRELIMINARY — ENGINEER OF RECORD TO CONFIRM)", [
        "Code: 2021 IBC with City of Scottsdale amendments; ASCE 7-16 (or as adopted); ACI 318-19; AWC NDS 2018 and SDPWS 2021; PTI DC10.5.",
        "Risk Category II.",
        "Roof dead load 27 psf (clay tile 12 psf + framing/sheathing 15 psf); roof live 20 psf; ceiling dead 10 psf.",
        "Floor dead load 25 psf (incl. F1 assembly, acoustic mat, independent ceiling); live 40 psf in units, 100 psf at the stair and landing.",
        "Wind: Vult 115 mph, exposure C, Kzt = 1.0 (verify for parcel).",
        "Seismic: Site Class D (default, verify with geotech), SDS and SD1 per ASCE Hazard Tool; Seismic Design Category B anticipated; R = 6.5 light-frame wood shear walls with wood structural panels.",
        "Soil: allowable bearing and PT slab design parameters (em, ym) per the geotechnical report for the parcel.",
    ])
    f.notes("FOUNDATIONS", [
        "Post-tensioned slab on ground per PTI DC10.5; see S-101. Footing depth 18\" min. below finish grade (Scottsdale amendment).",
        "Concrete f'c 3,000 psi at 28 days; 2,000 psi before stressing; max. w/c 0.50; Type II cement.",
        "Tendons ASTM A416 Grade 270, 1/2\" diameter, unbonded, encapsulated; stressing by a PTI-certified crew; elongation records submitted.",
        "Reinforcing ASTM A615 Grade 60.",
    ])
    f.notes("WOOD", [
        "Sawn lumber Douglas-fir-larch No. 2 or better. Studs: 2x6 @ 16\" exterior, 2x4 staggered on 2x6 plates at W1.",
        "Engineered wood: LVL Fb 2,600 psi, E 2.0e6; LSL rim 1-1/4\".",
        "Sheathing: 7/16\" OSB exposure 1 walls and roof; 3/4\" T&G OSB floors, glued and screwed.",
        "Fasteners per IBC Table 2304.10.2 unless a heavier schedule is shown. Hot-dip galvanized or stainless fasteners in treated wood.",
        "Connectors: Simpson Strong-Tie or equal, installed per the manufacturer with all specified fasteners.",
    ])
    f.notes("SPECIAL INSPECTIONS (IBC CH. 17) — AS REQUIRED BY THE BUILDING OFFICIAL", [
        "Post-tensioning: tendon placement and stressing (periodic / continuous per IBC Table 1705.3).",
        "Soils: verification of subgrade and fill compaction (Table 1705.6).",
        "Wood shear walls and diaphragms: nailing where edge spacing is 4\" o.c. or less (1705.12.2), if required for the seismic design.",
        "Firestop systems in rated walls and floors (1705.17) where required.",
    ])
    f.notes("DEFERRED SUBMITTALS", [
        "Post-tension slab shop drawings and calculations.",
        "Floor and roof truss design drawings and layouts, sealed by the truss designer, reviewed by the engineer of record.",
    ])


# ===================================================================== M-001
def m001(f):
    f.table("EQUIPMENT SCHEDULE — PER UNIT (A, B, C, D)", [("MARK", 0.7, "c"), ("DESCRIPTION", 2.4, "l"), ("CAP.", 0.8, "c"), ("EFF.", 1.0, "c"), ("ELEC.", 0.9, "c")], [
        ("CU", "Inverter heat pump condenser", "2.5 T", "SEER2 16 / HSPF2 8.1", "240/1, 25A MOCP"),
        ("AHU", "Variable-speed AHU, 5 kW strip", "1,000 CFM", "ECM blower", "240/1, 40A"),
        ("EF-1", "Bath fan, continuous rated", "80/45 CFM", "ENERGY STAR", "120/1"),
        ("EF-2", "Hall bath fan, humidity control", "80 CFM", "ENERGY STAR", "120/1"),
        ("HOOD", "Range hood, ducted", "150 CFM", "—", "120/1"),
        ("T-STAT", "Programmable, Wi-Fi, Unit A at 48\" max.", "—", "—", "24V")])
    f.notes("DESIGN CONDITIONS", [
        "Phoenix-area outdoor design: cooling 108°F DB / 70°F WB (ACCA Manual J, 1%); heating 37°F (99%).",
        "Indoor: 75°F cooling, 70°F heating.",
        "Loads by ACCA Manual J; equipment by Manual S; ducts by Manual D. Expected load about 1.8–2.2 tons per unit; 2.5-ton equipment shown as a placeholder.",
    ])
    f.notes("MECHANICAL GENERAL NOTES", [
        "Comply with 2021 IMC, IECC, and Scottsdale amendments. Installer licensed in Arizona (ROC).",
        "Each dwelling has independent systems; no shared ducts, returns or exhausts between units.",
        "Ducts: sheet metal trunks, flex runouts 5 ft max., all joints mastic-sealed; supply registers with dampers; returns sized for 400 FPM max. face velocity.",
        "Ground units: ducts in the F1 floor-truss space; ceiling radiation dampers at every ceiling opening per the F1 listing.",
        "Upper units: ducts in the attic, R-8, buried where practical; AHU on a platform with service light and receptacle.",
        "Condensate: primary to an indirect receptor; secondary pan with float switch shutting down the AHU.",
        "Refrigerant line sets insulated 3/4\" with UV jacket outdoors; seal envelope penetrations.",
        "Exhausts terminate 3 ft min. from openings and property lines (IMC 501.3.1); none in the W2 west eave.",
        "Whole-house ventilation per IMC 403.3.2.1 / ASHRAE 62.2: continuous bath fan at 45 CFM per unit, with a labeled switch.",
        "Test and balance each system; submit duct leakage results (IECC R403.3.5).",
    ])


# ===================================================================== P-001
def p001(f):
    f.table("PLUMBING FIXTURE SCHEDULE — PER UNIT", [("MARK", 0.6, "c"), ("FIXTURE", 2.6, "l"), ("FLOW", 1.0, "c"), ("NOTE", 1.8, "l")], [
        ("WC-1", "Floor-mount, elongated, WaterSense", "1.28 gpf", "Unit A: 17\"–19\" seat"),
        ("LAV-1", "Undermount or drop-in, single-lever", "1.2 gpm", "Unit A: knee space"),
        ("TUB-1", "60\" alcove tub/shower, pressure-balance valve", "1.8 gpm SH", "Grab bar blocking"),
        ("SH-1", "Roll-in shower 60x36, trench drain (Unit A)", "1.8 gpm", "Handheld on slide bar"),
        ("KS-1", "Double-bowl stainless, pull-down faucet", "1.8 gpm", "Unit A: removable base"),
        ("DW", "Dishwasher, ENERGY STAR", "—", "Air gap or high loop"),
        ("CW", "Washer box with hammer arrestors + pan", "—", "Pan drain"),
        ("WH", "50 gal heat pump water heater, UEF 3.3+", "—", "Pan, T&P to exterior"),
        ("HB", "Frost-free hose bib w/ vacuum breaker", "—", "On house water")])
    f.notes("PLUMBING GENERAL NOTES", [
        "Comply with the 2021 IPC and City of Scottsdale amendments. Licensed plumbing contractor (ROC).",
        "Materials: PVC/ABS Sch. 40 DWV (cast iron in chases as the quiet alternate); PEX-A water distribution with manifolds; copper Type L at the water service and in room 103.",
        "Water service: one City meter; backflow per Scottsdale; PRV if street pressure exceeds 80 psi; thermal expansion tank at each water heater.",
        "Unit submeters with remote read in room 103 (confirm Arizona and City submetering rules).",
        "All piping in W1 is prohibited; branches cross into chases with listed firestop systems and acoustic isolation sleeves.",
        "Insulate hot water piping R-3; insulate cold piping in exterior walls and the attic against condensation and solar heat gain.",
        "Pipe supports and isolation clips at every stud and truss crossing to limit noise transmission between units.",
        "Test DWV with water or air before cover; test water piping at 100 psi for 15 minutes min.",
        "Water heater: seismic strapping, drain pan to exterior, accessible shutoff, 10 ft clear of the electric panel working space.",
        "Accessible fixtures in Unit A per A117.1 Sec. 1003: lever controls, insulated drain and supply under lavs and the sink, handheld shower.",
    ])
    f.notes("GAS (ALTERNATE ONLY)", [
        "The base design is all-electric: no gas service. If the owner elects the gas alternate, see P-202 for meter, riser and appliance venting; combustion air per IFGC Ch. 3.",
    ])


# ===================================================================== E-001
def e001(f):
    f.table("SYMBOLS", [("SYMBOL", 1.0, "c"), ("DESCRIPTION", 5.0, "l")], [
        ("( || )", "Duplex receptacle, tamper-resistant, 18\" A.F.F."), ("GFCI", "Ground-fault circuit interrupter receptacle"),
        ("( X )", "LED ceiling fixture, surface mount"), ("S", "Single-pole switch, 44\" A.F.F. (48\" max. Unit A)"),
        ("S3", "Three-way switch"), ("SD / SC", "Smoke alarm / combination smoke-CO alarm"),
        ("[==]", "Panelboard"), ("MC-1", "Meter center"), ("EV", "EV-ready 40A 240V circuit, capped")])
    f.notes("ELECTRICAL GENERAL NOTES", [
        "Comply with the 2020 NEC (NFPA 70), IECC 2021 and City of Scottsdale amendments. Licensed electrical contractor (ROC). Utility: Arizona Public Service (APS) or SRP — confirm by parcel.",
        "Service: 400A, 120/240V, single-phase, underground from the utility transformer to meter center MC-1 with four 125A unit meters and one 60A house meter (E-201).",
        "Copper conductors for branch circuits; aluminum (AA-8000) permitted for the service and feeders if sized accordingly.",
        "AFCI protection for all 120V 15/20A branch circuits in dwelling units (210.12); GFCI per 210.8 incl. kitchen, baths, laundry, outdoors, garage and within 6 ft of sinks.",
        "Tamper-resistant receptacles (406.12); weather-resistant in-use covers outdoors.",
        "Surge protection at each unit panel (230.67).",
        "Wiring: NM cable in wood framing where permitted; MC cable or listed methods where required. No wiring or boxes in W1 walls.",
        "F1 ceilings: boxes listed for fire-rated ceilings or protected per the listing; surface fixtures only.",
        "Lighting: 100% high-efficacy LED (IECC R404.1); exterior fixtures full-cutoff, motion or photocell controlled.",
        "Smoke and CO alarms: hard-wired, interconnected, battery backup, per IFC 907.2.11 and 915.",
        "Label every panel and circuit; provide a typed directory.",
    ])
    f.notes("ACCESSIBILITY (UNIT A, TYPE A)", [
        "Switches, receptacles, thermostats and controls 15\" min. to 48\" max. A.F.F.",
        "Doorbell with visual signal; smoke alarm visual notification prewire in each bedroom and the living area (A117.1 1003.12).",
    ])


# ===================================================================== FP-001
def fp001(f):
    f.notes("FIRE SPRINKLER DESIGN CRITERIA", [
        "Standard: NFPA 13R (2019 edition or as adopted) with City of Scottsdale Fire Code amendments.",
        "Occupancy: residential, R-2, four dwelling units, two stories.",
        "Design: listed residential sprinklers, four-head design area (or as required by the listing), minimum 0.05 gpm/SF, plus 0 gpm hose (13R).",
        "Water supply: separate fire service from the street main, size per hydraulic calculation (2\" assumed), with backflow assembly as required by the water purveyor.",
        "Flow test: obtain a current City hydrant flow test before design.",
        "Riser: room 103 (door 102 from outside), with control valve, check, drain, pressure gauges, flow switch, and exterior waterflow bell.",
        "FDC: location and type per the Scottsdale Fire Marshal; within 100 ft of a hydrant.",
    ])
    f.notes("FIRE SPRINKLER NOTES", [
        "Deferred submittal: sprinkler shop drawings, hydraulic calculations and product data prepared by an Arizona-licensed fire sprinkler contractor (NICET III or as required) for City approval before installation.",
        "Sprinklers required in all rooms, closets over 24 SF, bathrooms over 55 SF, the shared entry, stair, storage 102, loft 202 and room 103.",
        "Attic protection: not required by NFPA 13R; provide if the Scottsdale amendments require it.",
        "Piping in the F1 assembly and through W1 uses listed firestop systems and listed escutcheons to maintain the ratings.",
        "Protect piping in the attic and exterior walls from heat above the CPVC listing; use steel in high-heat locations.",
        "Inspection, testing and maintenance per NFPA 25; provide the owner with the system manual and a maintenance schedule.",
    ])
    f.notes("RISER DIAGRAM (SCHEMATIC)", [
        "STREET MAIN → tap and valve → 2\" fire service → backflow assembly (DCVA) → room 103 riser: OS&Y control valve (supervised) → check → flow switch → gauges → main drain → 2\" main in the core ceiling → 1\" and 1-1/4\" branches to each unit.",
        "FDC connects on the system side of the check valve per NFPA 13R; waterflow bell on the exterior street face.",
    ])


# ===================================================================== EN-001
def en001(f):
    f.table("ENVELOPE — PRESCRIPTIVE (IECC 2021 TABLE R402.1.3, CZ 2B)", [("COMPONENT", 1.8, "l"), ("REQUIRED", 1.6, "c"), ("PROVIDED", 1.6, "c"), ("OK", 0.6, "c")], [
        ("Ceiling (attic)", "R-49", "R-38 + raised heel", "SEE NOTE"), ("Wood frame wall", "R-13 or 0+10ci", "R-21", "YES"),
        ("Slab edge", "None (CZ 2)", "None", "YES"), ("Fenestration U", "0.40", "0.30", "YES"), ("Fenestration SHGC", "0.25", "0.25", "YES"),
        ("Air leakage", "5.0 ACH50", "5.0 max., tested", "YES"), ("Duct leakage", "4 CFM25/100 SF", "Tested", "YES")])
    f.notes("COMPLIANCE PATH", [
        "Ceiling: IECC 2021 Table R402.1.3 lists R-49 for climate zone 2. R-38 is allowed where the full R-38 extends over the wall top plate at the eaves (R402.2.1), which the 14\" raised-heel trusses provide. Confirm Scottsdale's adopted IECC edition and amendments; if R-49 is required, increase the blown depth.",
        "Mechanical: heat pumps meeting federal minimums (SEER2 15.2 / HSPF2 7.8 split systems in the Southwest region) exceeded: SEER2 16 / HSPF2 8.1 specified.",
        "Water heating: heat pump water heaters, UEF 3.3+.",
        "Lighting: 100% high-efficacy (R404.1).",
        "Additional efficiency package (R408): option 1 (enhanced envelope) or option 3 (high-efficiency water heating) — heat pump water heaters selected; confirm local adoption.",
        "Alternative: performance path (R405) or ERI (R406) with a RESNET HERS rater; target HERS 55 or lower.",
    ])
    f.notes("TESTING + CERTIFICATES", [
        "Blower door test each unit after drywall (R402.4.1.2); duct leakage test each system (R403.3.5).",
        "Permanent energy certificate on the electrical panel of each unit (R401.3).",
        "Owner's manual with equipment efficiency, filter sizes and maintenance.",
    ])
    f.notes("ENERGY BEYOND CODE (OWNER GOALS)", [
        "All-electric building; solar-ready south roof plane kept clear of penetrations (A-103.1).",
        "EV-ready circuits at four stalls (E-401).",
        "ENERGY STAR appliances; WaterSense fixtures.",
    ])


# ===================================================================== A-602
def a602(f):
    f.table("ROOM FINISH SCHEDULE — TYPICAL ALL UNITS", [("ROOM", 1.3, "l"), ("FLOOR", 1.3, "l"), ("BASE", 0.9, "l"), ("WALLS", 1.4, "l"), ("CEILING", 1.1, "l")], [
        ("Living / dining", "LVP on mat", "4\" MDF", "GWB L4, PT-1", "GWB, PT-C"), ("Kitchen", "LVP on mat", "4\" MDF", "GWB L4, PT-1; tile backsplash", "GWB, PT-C"),
        ("Bedrooms", "LVP on mat", "4\" MDF", "GWB L4, PT-1", "GWB, PT-C"), ("Halls", "LVP on mat", "4\" MDF", "GWB L4, PT-1", "GWB, PT-C"),
        ("Baths", "Porcelain tile", "Tile cove", "MR GWB PT-2; tile wainscot / tub surround", "MR GWB, PT-2"),
        ("Roll-in bath (A)", "Slip-resistant tile, DCOF 0.42+", "Tile cove", "Cement board + tile full height at shower", "MR GWB, PT-2"),
        ("Laundry / WH", "Porcelain tile", "Tile", "MR GWB PT-2", "GWB, PT-C"),
        ("Closets", "LVP", "4\" MDF", "GWB PT-1", "GWB PT-C"),
        ("Shared entry 100", "Porcelain tile", "Tile", "GWB L5 PT-3; wainscot", "GWB PT-C"),
        ("Stair + landing", "Rubber treads / LVP", "Rubber", "GWB L5 PT-3", "GWB PT-C"),
        ("Storage 102 / 202", "Sealed concrete / OSB", "—", "GWB taped, PT-1", "GWB")])
    f.table("FINISH LEGEND", [("CODE", 0.7, "c"), ("PRODUCT (BASIS OF DESIGN OR EQUAL)", 5.3, "l")], [
        ("LVP", "Luxury vinyl plank, 20 mil wear layer, on 2 mm acoustic underlayment (IIC rated with F1)"),
        ("PT-1", "Interior latex, eggshell, low-VOC, warm white"), ("PT-2", "Interior latex, satin, mildew-resistant"),
        ("PT-3", "Scrubbable eggshell, accent color at entry"), ("PT-C", "Ceiling flat, white"),
        ("TILE", "Porcelain 12x24 floor, DCOF 0.42 wet; 3x12 wall at tub and backsplash"),
        ("CT", "Quartz or solid-surface counters; Unit A 34\" work surface section"),
        ("CAB", "Plywood-box shaker cabinets, soft-close, full-extension drawers; Unit A removable sink base")])
    f.notes("FINISH NOTES", [
        "Every unit receives identical finishes. No downgraded unit.",
        "Acoustic mat under all upper-unit flooring is part of the F1 STC/IIC 50 rating; do not substitute without test data.",
        "Paints and adhesives low-VOC (CARB / SCAQMD limits).",
        "Exterior: stucco color E-1 warm sand; trim E-2 off-white; shutters and doors E-3 deep green; clay tile blend, two tones (A-201.1).",
    ])


# ===================================================================== E-301
def e301(f):
    f.table("UNIT LOAD CALCULATION — NEC 220.82 (TYPICAL UNIT, 1,250 SF)", [("LOAD", 2.6, "l"), ("VA", 1.1, "c"), ("NOTE", 2.3, "l")], [
        ("General lighting 3 VA x 1,250 SF", "3,750", "220.82(B)(1)"), ("Small appliance (2) + laundry (1)", "4,500", "220.82(B)(2)"),
        ("Range (nameplate)", "12,000", ""), ("Dryer", "5,000", ""), ("Heat pump water heater", "4,500", ""), ("Dishwasher", "1,200", ""),
        ("Disposal / microwave / hood", "2,400", ""), ("Subtotal general loads", "33,350", ""), ("First 10 kVA at 100%", "10,000", ""),
        ("Remainder 23,350 at 40%", "9,340", ""), ("Heat pump + 5 kW strip (larger of heat/cool)", "7,500", "220.82(C)"),
        ("TOTAL", "26,840", "= 112 A at 240 V → 125 A panel")])
    f.table("SERVICE LOAD — NEC 220.84 (MULTIFAMILY OPTIONAL)", [("ITEM", 3.0, "l"), ("VA", 1.2, "c"), ("NOTE", 1.8, "l")], [
        ("4 units connected load (incl. HVAC)", "163,400", "4 x 40,850"), ("Demand factor, 4 units", "45%", "Table 220.84(B)"),
        ("Units after demand", "73,530", ""), ("House panel (site lights, EV, bell, irrigation)", "12,000", "at 100%"),
        ("SERVICE TOTAL", "85,530", "= 356 A → 400 A service")])
    f.table("PANEL A (TYPICAL UNIT) — 125A MAIN, 120/240V 1Ø 3W, 42 SP", [("CKT", 0.6, "c"), ("LOAD", 2.5, "l"), ("A/P", 0.8, "c"), ("TYPE", 0.9, "c"), ("CKT", 0.6, "c")], [
        ("1,3", "Range", "40/2", "—", "2,4"), ("5,7", "Dryer", "30/2", "—", "6,8"), ("9,11", "Water heater WH", "30/2", "—", "10,12"),
        ("13,15", "AHU (strip heat)", "40/2", "—", "14,16"), ("17,19", "Condenser CU", "25/2", "—", "18,20"),
        ("21", "Kitchen counter SA-1", "20", "GFCI/AFCI", "22"), ("23", "Kitchen counter SA-2", "20", "GFCI/AFCI", "24"),
        ("25", "Dishwasher", "20", "GFCI", "26"), ("27", "Disposal / hood", "20", "GFCI", "28"), ("29", "Microwave", "20", "AFCI", "30"),
        ("31", "Refrigerator", "20", "AFCI", "32"), ("33", "Laundry washer", "20", "GFCI/AFCI", "34"), ("35", "Bath receptacles", "20", "GFCI", "36"),
        ("37", "Bedrooms receptacles + lights", "15", "AFCI", "38"), ("39", "Living / dining", "15", "AFCI", "40"), ("41", "Smoke / CO, bath fans", "15", "AFCI", "42")], rowh=0.2)
    f.table("HOUSE PANEL HP — 60A (EXPAND TO 100A IF EV CIRCUITS ON HP)", [("CKT", 0.6, "c"), ("LOAD", 3.4, "l"), ("A/P", 0.8, "c"), ("NOTE", 1.2, "l")], [
        ("1", "Shared entry + stair lights", "15", "Photocell / timer"), ("2", "Site and parking lights", "20", "Dark-sky"), ("3", "Sprinkler bell + riser heat", "20", "Lock-on"),
        ("4", "Irrigation controller", "15", "GFCI"), ("5", "Exterior receptacles", "20", "GFCI WR"), ("6,8", "EV-ready (future)", "40/2", "Capped")])


if __name__ == "__main__":
    make("G-003", "Model1_General_Notes", "GENERAL\nCONSTRUCTION NOTES", g003)
    make("S-001", "Model1_Structural_General_Notes", "STRUCTURAL\nGENERAL NOTES", s001)
    make("M-001", "Model1_Mechanical_Notes_Schedules", "MECHANICAL NOTES\n+ SCHEDULES", m001)
    make("P-001", "Model1_Plumbing_Notes_Schedules", "PLUMBING NOTES\n+ SCHEDULES", p001)
    make("E-001", "Model1_Electrical_Notes_Symbols", "ELECTRICAL NOTES\n+ SYMBOLS", e001)
    make("FP-001", "Model1_Fire_Sprinkler_Notes", "FIRE SPRINKLER\nNOTES", fp001)
    make("EN-001", "Model1_Energy_Compliance", "ENERGY\nCOMPLIANCE", en001)
    make("A-602", "Model1_Finish_Schedule", "FINISH\nSCHEDULE", a602)
    make("E-301", "Model1_Panel_Schedules_Load_Calcs", "PANEL SCHEDULES\n+ LOAD CALCS", e301)
