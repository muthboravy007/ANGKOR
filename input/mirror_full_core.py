# tools/build_full_core_centered.py
import yaml, pathlib, copy

src = pathlib.Path("input/iaea_2d.yaml")           # current outer-corner quarter
dst = pathlib.Path("input/iaea_2d_full.yaml")

data = yaml.safe_load(src.read_text())
Lq = data["geometry"]["domain_x"]   # 170.0

def shift_to_center(reg):
    r = copy.deepcopy(reg)
    r["x_min"] -= Lq/2; r["x_max"] -= Lq/2
    r["y_min"] -= Lq/2; r["y_max"] -= Lq/2
    return r

def mirror(r, fx, fy):
    r = copy.deepcopy(r)
    if fx:
        r["x_min"], r["x_max"] = -r["x_max"], -r["x_min"]
    if fy:
        r["y_min"], r["y_max"] = -r["y_max"], -r["y_min"]
    r["name"] += f"_mx{int(fx)}my{int(fy)}"
    return r

regions = []
for reg in data["regions"]:
    c = shift_to_center(reg)
    regions += [
        c,
        mirror(c, True, False),
        mirror(c, False, True),
        mirror(c, True, True),
    ]

# shift entire full core to positive coordinates
for r in regions:
    r["x_min"] += Lq; r["x_max"] += Lq
    r["y_min"] += Lq; r["y_max"] += Lq

data["regions"] = regions
data["geometry"]["domain_x"] = 2 * Lq   # 340
data["geometry"]["domain_y"] = 2 * Lq   # 340
data["boundary_conditions"] = { "left":"vacuum","right":"vacuum","top":"vacuum","bottom":"vacuum" }

# enforce benchmark fast fission = 0
for m in ("fuel1","fuel2","fuel_cr"):
    data["materials"][m]["nu_sigma_f"][0] = 0.0

dst.write_text(yaml.dump(data, sort_keys=False))
print(f"Wrote {dst} with {len(regions)} regions")
