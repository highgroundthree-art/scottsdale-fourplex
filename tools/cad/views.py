"""View configs for Models 2 and 3 (copied from gen_sheets.py) so other sheets can redraw the plans."""
from gen_floor import View

FP = "/home/claude/scottsdale-fourplex/drawings/floor-plans/"


def vc_m2(level):
    svg = FP + ("model2-ground.svg" if level == 1 else "model2-upper.svg")
    return dict(svg=svg, ppf=6.6, origin=(60, 40), W=28, D=102, rot="cw", west_type="EXT", type_a_unit="A",
                grids=([(0, "1"), (36, "2"), (58, "3"), (80, "4"), (102, "5")], [(0, "A"), (28, "B")]),
                wall_tags=[(36, 14.0, "W1"), (58, 14.0, "W1"), (80, 14.0, "W1"), (47, 0.3, "E1"), (91, 27.7, "E1")],
                group_rects=([((23, 16.5, 13, 3), "BS"), ((19, 0, 4, 28), "BS"), ((12, 8, 7, 4), "BS"), ((12, 12, 7, 16), "BS"), ((0, 12, 12, 16), "BS")] if level == 2 else []),
                door_edits=([lambda L: [d for d in L if not (d["o"] == "h" and abs(d["a"][1] - 19.5) < .01 and 37 < d["a"][0] < 41)]] if level == 2 else []))


def vc_m3(level):
    svg = FP + ("model3-main-ground.svg" if level == 1 else "model3-upper-owner.svg")
    return dict(svg=svg, ppf=12, origin=(70, 60), W=60, D=40, west_type="EXT", type_a_unit="A",
                grids=([(0, "1"), (26, "2"), (34, "3"), (60, "4")], [(0, "A"), (40, "B")]),
                unit_rects=([((26, 0, 8, 40), "K"), ((30, 16.5, 4, 13.5), "C")] if level == 1 else []),
                wall_tags=([(26, 22, "W1"), (34, 22, "W1"), (8, 0.3, "E1"), (59.7, 26, "E1")] if level == 1 else [(8, 0.3, "E1"), (59.7, 26, "E1")]))


def vc_m3c(n):
    g = ([(0, "1"), (24, "2"), (48, "3")], [(0, "A"), (24, "B")])
    tiers = (0.5, 0.85, None)
    if n == 1:
        return dict(svg=FP + "model3-carriage-ground.svg", ppf=12, origin=(70, 60), W=48, D=24, west_type="EXT", grids=g, tiers=tiers, grid_off=1.25,
                    unit_rects=[((0, 0, 24, 24), "G1"), ((24, 0, 24, 24), "G2")], pair_type=lambda a, b: "W3" if {a, b} == {"G1", "G2"} else None)
    if n == 2:
        return dict(svg=FP + "model3-casita-l2.svg", ppf=12, origin=(70, 60), W=48, D=24, west_type="EXT", grids=g, tiers=tiers, grid_off=1.25)
    return dict(svg=FP + "model3-casita-loft.svg", ppf=12, origin=(70, 60), shift=(12, 0), W=24, D=24, west_type="EXT",
                room_edits=[lambda rs: rs + [dict(x=22, y=0, w=2, h=8, fill="#fff", color="#1e5bd8", op=0.03)]],
                group_rects=[((0, 8, 24, 16), "open")], grids=([], []), tiers=(0.5, 0.85, None))
