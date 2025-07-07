import os
from pathlib import Path
from collections import defaultdict

from template.spriteset_template import *

gfx_directory = Path("gfx")
src_directory = Path("src")
voxel_directory = Path("voxels")

cargo = {"bulk", "steel", "wood", "bars"}
loading = {"loading"}
dual_mode = {"panto_up", "panto_down"}
anim = {"anim"}

def classify_vox_files(vox_files: set[Path]):
    groups = defaultdict(list)

    for f in vox_files:
        stem = f.stem.lower()

        if any(k in stem for k in anim):
            groups["anim"].append(f)
        elif any(k in stem for k in cargo):
            groups["cargo"].append(f)
        elif any(k in stem for k in dual_mode):
            groups["dual_mode"].append(f)
        elif any(k in stem for k in loading):
            groups["loading"].append(f)
        else:
            groups["default"].append(f)

    return groups

def generate_pnml(vox_files):
    stems = [v.stem for v in vox_files]
    unit_base_name = os.path.commonprefix(stems).rstrip("_")

    rel_path = next(iter(vox_files)).parent.relative_to(voxel_directory)

    output_dir = Path("template/autogen")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pnml_file = output_dir / f"{unit_base_name}.pnml"

    groups = classify_vox_files(vox_files)
    gfx_path = f"gfx\\{rel_path.as_posix().replace('/', '\\')}"

    with open(pnml_file, "w", encoding="utf-8") as p:
        for f_default in groups['default']:
            p.write(PNML_TEMPLATE.format(
                unit = f_default.stem,
                path = gfx_path
            ) + "\n")

            if Path(voxel_directory / rel_path / f"{f_default.stem}_Loading.vox").exists():
                p.write(LOADING_TEMPLATE.format(
                    unit = f_default.stem,
                    path = gfx_path
                ))

        if Path(voxel_directory / rel_path / f"{unit_base_name}_Loading.vox").exists():
            p.write(LOADING_TEMPLATE.format(
                unit = unit_base_name,
                path = gfx_path
            ) + "\n")

        if len(groups["dual_mode"]) == 2:
            p.write(DUAL_MODE_TEMPLATE.format(
                unit = unit_base_name,
                path = gfx_path
            ) + "\n")

        if len(groups["anim"]) == 4:
            p.write(ANIM_TEMPLATE.format(
                unit = unit_base_name,
                path = gfx_path
            ) + "\n")

        for f_cargo in groups["cargo"]:
            p.write(CARGO_TEMPLATE.format(
                unit = f_cargo.stem,
                base_unit = unit_base_name,
                path = gfx_path
            ) + "\n")
    
    print(f"\nGenerated: {pnml_file}")