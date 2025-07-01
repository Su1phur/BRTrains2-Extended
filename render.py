import os
import subprocess
import shutil
from pathlib import Path
from argparse import ArgumentParser

gorender_path = Path("../gorender/renderobject.exe").resolve()
gfx_directory = Path("gfx")
voxels_path = Path("voxels")
palette_path = Path("./docs/ttd_palette.json")
manifest_path = Path("./docs/manifest.json")

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

def render_file(file_name):
    command = [str(gorender_path),
               "-i",str(file_name),
               "-s", "1,2,4",
               "-palette", palette_path,
               "-m", manifest_path]
    
    subprocess.run(command, check=True)

def main(input_folder, output=None, all=False):
    output_path = ""
    print(input_folder)

    # validate if GoRender is installed
    if not gorender_path.is_file():
        raise GoRenderNotFoundError(gorender_path)
    
    if all == False:
        input_folder = Path(input_folder)
        if not input_folder.is_dir():
            raise ValueError(f"{input_folder} is not a valid directory.")
    else:
        input_folder = voxels_path
    
    if output == "" or output == None:
        output_path = gfx_directory / input_folder.relative_to(voxels_path).with_suffix('')
        output_path.mkdir(parents=True, exist_ok=True)
        print(output_path)
    else:
        output_path = Path(output) 
        print(output_path)

    validate_needed_files(palette_path)
    validate_needed_files(manifest_path)

    input_files = {f for f in input_folder.iterdir() if f.suffix == ".vox"}

    for f in input_files:
        render_file(f)
        move_files(input_folder, output_path)
    

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
                        help="Renders all .vox files, overrides all other arguments.")
    args = parser.parse_args()

    main(args.path, args.output, args.all)