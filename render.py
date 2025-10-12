import os
import subprocess
import shutil
from pathlib import Path
from argparse import ArgumentParser

from generate import generate_pnml
from template.keywords import keyword_map
from template.endings import expected_endings

gorender_path = Path("../gorender/renderobject.exe").resolve()
gfx_directory = Path("gfx")
voxel_directory = Path("voxels")
default_palette_path = Path("docs/ttd_palette.json")
default_manifest_path = Path("docs/manifest.json")

ignore = keyword_map['ignore']

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

def display_progress(rendered, total):
    progress = "█" * rendered + "-" * (total - rendered)
    print(f"\r{progress} ({rendered}/{total})", end='', flush=True)

def expected_images_for(file_name):
    stem = file_name.stem
    relative = file_name.parent.relative_to(voxel_directory)
    output_dir = gfx_directory / relative

    return [output_dir / f"{stem}{suffix}.png" for suffix in expected_endings]

def is_fully_rendered(file_name): 
    expected_images = expected_images_for(file_name)
    return all(image.exists() for image in expected_images)


def render_file(file_name, palette_path, manifest_path):
    command = [str(gorender_path),
               "-i", str(file_name),
               "-s", "1,2,4",
               "-palette", palette_path,
               "-m", manifest_path]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Rendering failed for {file_name}:\n{e.stderr}")


def render_and_move(voxel_file, palette_path, manifest_path, output_path=None):
    relative_path = voxel_file.parent.relative_to(voxel_directory)

    if output_path is None or output_path == "":
        output_path = gfx_directory / relative_path

    output_path.mkdir(parents=True, exist_ok=True)

    render_file(voxel_file, palette_path, manifest_path)
    
    stem = voxel_file.stem
    for image in voxel_file.parent.glob(f"{stem}_*.png"):
        shutil.move(str(image), output_path / image.name)


def find_filter_vox_files(input_directory, only_missing=False):
    vox_list = []
    for f in input_directory.rglob("*.vox"):
        if "Non-Standard" not in f.parts and not any(k in f.stem.lower() for k in ignore):
            vox_list.append(f)
    
    if only_missing:
        vox_list = {f for f in vox_list if not is_fully_rendered(f)}

    return sorted(vox_list)
        

def process_vox_files(vox_files, palette_path, manifest_path, output_path=None):
    total = len(vox_files)
    print(f"Total {total} .vox files to be rendered.")
    rendered_count = 0
    display_progress(rendered_count, total)

    for f in vox_files:
        render_and_move(f, palette_path, manifest_path, output_path)
        rendered_count += 1
        display_progress(rendered_count, total)


def main(input_folder, 
         palette_path=default_palette_path,
         manifest_path=default_manifest_path,
         output=None, 
         all=False,
         missing=False,
         generate=False):

    # validate if GoRender is installed
    if not gorender_path.is_file():
        raise GoRenderNotFoundError(gorender_path)
    
    validate_needed_files(palette_path)
    validate_needed_files(manifest_path)

    if generate:
        input_folder = Path(input_folder)
        if not input_folder.is_dir():
            raise ValueError(f"{input_folder} is not a valid directory.")
        
        vox_files = find_filter_vox_files(input_folder)
        generate_pnml(vox_files)
        return
    
    elif all:
        input_folder = voxel_directory

        all_vox_files = find_filter_vox_files(input_folder)
        process_vox_files(all_vox_files, palette_path, manifest_path)
        
    else:
        input_folder = Path(input_folder)
        if not input_folder.is_dir():
            raise ValueError(f"{input_folder} is not a valid directory.")
    
        if output == "" or output is None:
            output_path = gfx_directory / input_folder.relative_to(voxel_directory)
        else:
            output_path = Path(output) 

        vox_files = find_filter_vox_files(input_folder)

        process_vox_files(vox_files, palette_path, manifest_path, output_path)

        generate_pnml(vox_files)

    if missing:
        missing_vox_files = find_filter_vox_files(voxel_directory, only_missing=True)
        total = len(missing_vox_files)

        if total != 0:
            print(f"\nTotal {total} .vox files have missing gfx images.")
            process_vox_files(missing_vox_files, palette_path, manifest_path, output)
    

if __name__ == "__main__":
    # Parser arguments
    parser = ArgumentParser()
    parser.add_argument("--path",
                        type=str, 
                        help="Path to a folder containing all files to be rendered.")
    parser.add_argument("--generate",
                        action="store_true",
                        help="Automatically generates pnml file within a folder.")
    parser.add_argument("--all",
                        action="store_true",
                        help="Renders all .vox files, overrides --path and --output.")
    parser.add_argument("--output",
                        type=str,
                        help="Folder name/Destination folder to contain all rendered GFX")
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

    main(args.path, args.palette, args.manifest, args.output, args.all, args.missing, args.generate)