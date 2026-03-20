import copy
import pathlib
import yaml


def build_full_core(src_path: pathlib.Path, dst_path: pathlib.Path):
    data = yaml.safe_load(src_path.read_text())
    Lx = float(data["geometry"]["domain_x"])
    Ly = float(data["geometry"]["domain_y"])
    assert abs(Lx - Ly) < 1e-6, "Geometry must be square for this mirroring."

    def shift_to_center(r):
        r = copy.deepcopy(r)
        r["x_min"] -= Lx / 2
        r["x_max"] -= Lx / 2
        r["y_min"] -= Ly / 2
        r["y_max"] -= Ly / 2
        return r

    def mirror(r, flip_x, flip_y):
        r = copy.deepcopy(r)
        if flip_x:
            r["x_min"], r["x_max"] = -r["x_max"], -r["x_min"]
        if flip_y:
            r["y_min"], r["y_max"] = -r["y_max"], -r["y_min"]
        r["name"] += f"_mx{int(flip_x)}my{int(flip_y)}"
        return r

    regions = []
    for reg in data["regions"]:
        c = shift_to_center(reg)
        regions.append(c)
        regions.append(mirror(c, True, False))
        regions.append(mirror(c, False, True))
        regions.append(mirror(c, True, True))

    # shift back to positive coordinates
    for r in regions:
        r["x_min"] += Lx
        r["x_max"] += Lx
        r["y_min"] += Ly
        r["y_max"] += Ly

    data["regions"] = regions
    data["geometry"]["domain_x"] = 2 * Lx
    data["geometry"]["domain_y"] = 2 * Ly
    data["boundary_conditions"] = {
        "left": "vacuum",
        "right": "vacuum",
        "top": "vacuum",
        "bottom": "vacuum",
    }

    # enforce benchmark fast fission = 0
    for mat_name in ("fuel1", "fuel2", "fuel_cr"):
        if mat_name in data["materials"]:
            data["materials"][mat_name]["nu_sigma_f"][0] = 0.0

    dst_path.write_text(yaml.dump(data, sort_keys=False))
    print(f"Wrote {dst_path} with {len(regions)} regions")


if __name__ == "__main__":
    src = pathlib.Path("input/iaea_2d.yaml")
    dst = pathlib.Path("input/iaea_2d_full.yaml")
    build_full_core(src, dst)
