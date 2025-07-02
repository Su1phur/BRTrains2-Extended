import os
import subprocess
import shutil
from pathlib import Path
from argparse import ArgumentParser

gorender_path = Path("../gorender/renderobject.exe").resolve()
gfx_directory = Path("gfx")
voxels_path = Path("voxels")
default_palette_path = Path("docs/ttd_palette.json")
default_manifest_path = Path("docs/manifest.json")

expected_endings = [
    "_1x_8bpp",
    "_1x_32bpp",
    "_1x_mask",
    "_2x_8bpp",
    "_2x_32bpp",
    "_2x_mask",
    "_4x_8bpp",
    "_4x_32bpp",
    "_4x_mask",
]

class GoRenderNotFoundError(FileNotFoundError):
    def __init__(self, path):
        message = (
            f"GoRender not found at '{path}'.\n"
            f"Make sure GoRender is compiled and accessible at the expected path."
        )
        super().__init__(message)


def validate_needed_files(find_file):
    if not find_file.exists():
        raise FileNotFoundError(f"{find_file} does not exist")


def move_files(rendered_path, output_path):
    for image in rendered_path.rglob("*.png"):
        shutil.move(str(image), output_path / image.name)


def display_progress(rendered, total):
    progress = "●" * rendered + "o" * (total - rendered)
    print(f"\r{progress} ({rendered}/{total})", end='', flush=True)


def expected_images_for(file_name):
    stem = file_name.stem
    relative = file_name.parent.relative_to(voxels_path)
    output_dir = gfx_directory / relative

    return [output_dir / f"{stem}{suffix}.png" for suffix in expected_endings]

def is_fully_rendered(file_name): 
    expected_images = expected_images_for(file_name)
    return all(image.exists() for image in expected_images)

def find_missing_files() -> list[Path]:
    return [
        f for f in voxels_path.rglob("*.vox")
        if "Non-Standard" not in f.parts and not is_fully_rendered(f)
    ]


def render_file(file_name, palette_path, manifest_path):
    command = [str(gorender_path),
               "-i", str(file_name),
               "-s", "1,2,4",
               "-palette", palette_path,
               "-m", manifest_path]
    
    subprocess.run(command, check=True)

def main(input_folder, 
         palette_path=default_palette_path,
         manifest_path=default_manifest_path,
         output=None, 
         all=False,
         missing=False):

    # validate if GoRender is installed
    if not gorender_path.is_file():
        raise GoRenderNotFoundError(gorender_path)
    
    validate_needed_files(palette_path)
    validate_needed_files(manifest_path)

    if all:
        input_folder = voxels_path

        vox_files = [x for x in input_folder.rglob("*.vox") if "Non-Standard" not in x.parts]

        total = len(vox_files)
        print(f"Total {total} .vox files to be rendered.")
        rendered_count = 0
        display_progress(rendered_count, total)

        for f in vox_files:
            relative_path = f.parent.relative_to(voxels_path)
            output_path = gfx_directory / relative_path
            output_path.mkdir(parents=True, exist_ok=True)

            render_file(f, palette_path, manifest_path)
            move_files(f.parent, output_path)

            rendered_count += 1
            display_progress(rendered_count, total)
        
    else:
        input_folder = Path(input_folder)
        if not input_folder.is_dir():
            raise ValueError(f"{input_folder} is not a valid directory.")
    
        if output == "" or output is None:
            output_path = gfx_directory / input_folder.relative_to(voxels_path)
        else:
            output_path = Path(output) 

        output_path.mkdir(parents=True, exist_ok=True)

        vox_files = {f for f in input_folder.iterdir() if f.suffix == ".vox"}

        total = len(vox_files)
        print(f"Total {total} .vox files to be rendered.")
        rendered_count = 0
        display_progress(rendered_count, total)

        for f in vox_files:
            render_file(f, palette_path, manifest_path)
            move_files(input_folder, output_path)

    if missing:
        vox_files = find_missing_files()

        total = len(vox_files)
        print(f"\nTotal {total} .vox files have missing gfx images.")
        rendered_count = 0
        display_progress(rendered_count, total)

        if total != 0:
            for f in vox_files:
                relative_path = f.parent.relative_to(voxels_path)
                output_path = gfx_directory / relative_path
                output_path.mkdir(parents=True, exist_ok=True)

                render_file(f, palette_path, manifest_path)
                move_files(f.parent, output_path)

                rendered_count += 1
                display_progress(rendered_count, total)
    

if __name__ == "__main__":
    # Parser arguments
    parser = ArgumentParser()
    parser.add_argument("--path",
                        type=str, 
                        help="Path to a folder containing all files to be rendered.")
    parser.add_argument("--output",
                        type=str,
                        help="Folder name/Destination folder to contain all rendered GFX")
    parser.add_argument("--all",
                        action="store_true",
                        help="Renders all .vox files, overrides --path and --output.")
    parser.add_argument("--palette",
                        type=str,
                        default=default_palette_path,
                        help="Specify a different palette from what is used by default.")
    parser.add_argument("--manifest",
                        type=str,
                        default=default_manifest_path,
                        help="Specify a different manifest from what is used by default.")
    parser.add_argument("--missing",
                        action="store_true",
                        help="Automatically looks for and renders any missing gfx.")
    args = parser.parse_args()

    main(args.path, args.palette, args.manifest, args.output, args.all, args.missing)