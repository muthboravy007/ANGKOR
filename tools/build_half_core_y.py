import copy
import pathlib
import yaml


def build_half_core_y(src_path: pathlib.Path, dst_path: pathlib.Path):
    data = yaml.safe_load(src_path.read_text())
    Ly = float(data["geometry"]["domain_y"])  # 170

    def mirror_y(r):
        r = copy.deepcopy(r)
        r["y_min"], r["y_max"] = 2 * Ly - r["y_max"], 2 * Ly - r["y_min"]
        r["name"] += "_my"
        return r

    regions = []
    for r in data["regions"]:
        regions.append(r)
        regions.append(mirror_y(r))

    data["regions"] = regions
    data["geometry"]["domain_x"] = data["geometry"]["domain_x"]  # still 170
    data["geometry"]["domain_y"] = 2 * Ly  # 340
    data["boundary_conditions"] = {
        "left": "vacuum",
        "right": "vacuum",
        "top": "vacuum",
        "bottom": "reflective",
    }

    dst_path.write_text(yaml.dump(data, sort_keys=False))
    print(f"Wrote {dst_path} with {len(regions)} regions")


if __name__ == "__main__":
    src = pathlib.Path("input/iaea_2d.yaml")
    dst = pathlib.Path("input/iaea_2d_half_y.yaml")
    build_half_core_y(src, dst)
