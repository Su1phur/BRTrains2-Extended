from pathlib import Path
from sys import argv
from argparse import ArgumentParser
from importlib import util
from collections import OrderedDict

RED = "\033[91m"
YELLOW = "\033[93m" 
RESET = "\033[0m"   

KeyFiles = OrderedDict( [
    ("grf.pnml", "\"grf.pnml\" not found. It should be in \"src\" and contain the grf block."),
    ("railtypes.pnml", "\"railtypes.pnml\" not found. It should be in \"src\" and contain the railtypetable block."),
    ("sounds.pnml", "\"sounds.pnml\" not found.  Assuming no sounds are required"),
    ("templates_shared.pnml", "\"templates_shared.pnml\" not found.  Assuming no templates are required"),
    ("templates_trains.pnml", "\"templates_trains.pnml\" not found.  Assuming no templates are required"),
    # ("templates_trams.pnml", "\"templates_trams.pnml\" not found.  Assuming no templates are required"),
] )

SpecialOrderFiles = { 
    "BR_Mk3_TS.pnml": ["BR_Mk3_TSD.pnml", "BR43.pnml", "BR254.pnml"],
    "Containers_BR.pnml": ["BR_Conflat_A.pnml", "BR_Conflat_P.pnml"],
    "RCH_1907_graphics.pnml": ["1_Plank_Open_Wagons_Load.pnml", "RCH_1907.pnml", "RCH_1907_1_plank.pnml", "RCH_1907_3_plank.pnml", "RCH_1907_5_plank.pnml", "RCH_1907_7_plank.pnml", "RCH_1907_Van.pnml"],
    "60Long_Cont20_Side.pnml": ["60Long_Cont40_Side.pnml", "BR_FEA.pnml"]
}

def check_project_structure(src_directory: Path, gfx_directory: Path,
                            lang_directory: Path):
    has_lang_dir = True

    # Check that the project is properly structured
    if not src_directory.exists():
        raise FileNotFoundError("\"src\" directory not found.  Aborting")
    if not gfx_directory.exists():
        raise FileNotFoundError("\"gfx\" directory not found.  Aborting")
    if not lang_directory.exists():
        print("\"lang\" directory not found.  Assuming hard-coded strings (this is not best practice)")
        has_lang_dir = False

    # iterate over KeyFiles, and ensure they exist
    for file, error in KeyFiles.items():
        if not src_directory.joinpath(file).exists():
            if file == "grf.pnml" or file == "railtypes.pnml":
                raise FileNotFoundError(error)
            else:
                print(f"{YELLOW}WARNING: {error}{RESET}")

    print("Project structure is correct\n")
    return has_lang_dir


def find_special_file(filename:str, search_dir: Path):
    matches = list(search_dir.rglob(filename))
    
    if len(matches) == 0:
        raise FileNotFoundError(f"No file named '{filename}' found")
    elif len(matches) > 1:
        raise RuntimeError(f"Multiple files named '{filename}' found: {matches}")
    
    return matches[0]

def copy_file(filepath: Path, nml_file: str):
    # If the pnml filepath doesn't exist, exit
    if not filepath.exists():
        raise FileNotFoundError(f"The file <{filepath}> does not exist.")

    # Read the pnml file into the internal nml
    with open(str(filepath), "r") as file:
        nml_file += "// " + filepath.stem + filepath.suffix + "\n"
        for line in file:
            nml_file += line
    nml_file += "\n\n"
    return nml_file


def write_file(filename: str, nml_file: str):
    from os import makedirs
    # Generate the filepath and check if it exists
    filepath = Path("build/" + filename + ".nml")
    build_dir = Path("build/")
    if not build_dir.exists():
        makedirs("build")

    if filepath.exists():
        print("'%s.nml' already exists.  Overwriting" % filename)

    # Write the internal nml to the file
    with open(filepath, "w") as file_writer:
        for line in nml_file:
            file_writer.write(line)

    print("Written all files to '%s.nml' file\n" % filename)
    return 0


def compile_grf(has_lang_dir, grf_name, lang_dir):
    # Check if we have the nml package
    found_nml = util.find_spec("nml")
    if found_nml is not None:
        # Import nml's main module
        import nml.main # type: ignore
        parameters = []
        if has_lang_dir:
            # If we have a lang directory, add it to the parameters
            parameters = ["--lang", str(lang_dir), "build/" + grf_name + ".nml"]
        else:
            # If not, just the nml name
            parameters = ["build/" + grf_name + ".nml"]
        try:
            # Try to compile the nml file
            nml.main.main(parameters)
        except SystemExit:
            # nml uses sys.exit(), so catch this to stop the program exiting
            print("nml tried to exit but was stopped")
        print("Finished compiling grf file\n")
        return 1
    else:
        # nml isn't installed
        print("nml is not installed.  You can get it using 'pip install nml'")
        return -2


def run_game(grf_name):
    from sys import platform

    print("Detecting platform")

    # Change default paths depending on whether we use Linux or Windows (sorry OSX)
    if platform.startswith("linux"):
        newgrf_dir = Path.home().joinpath(".openttd", "newgrf")
        executable_path = "/usr/bin/openttd"
        kill_cmd = ["killall","openttd"]
        print("Detected as Linux")
    elif platform.startswith("win32"):
        newgrf_dir = Path.home().joinpath("Documents", "OpenTTD", "newgrf")
        executable_path = "C:/Program Files/OpenTTD/openttd.exe"
        kill_cmd = ["taskkill.exe" "/IM" "OpenTTD.exe"]
        print("Detected as Windows")
    else:
        print("Detected as Other.  Cannot run game.")
        return -3

    print("Attempting to read config")
    json_read_ok = False
    # Check that the config file exists
    if Path("build/build.json").exists():
        from json import load, decoder
        with open("build/build.json") as json_data:
            # Try to read the config file
            try:
                data = load(json_data)
            # Errors if the file in invalid
            except decoder.JSONDecodeError:
                print("The config file is invalid")
                json_read_ok = False
            else:
                # Read successfully
                # Try to read the keys from the json file
                try:
                    newgrf_dir = data["newgrf_dir"]
                    executable_path = data["executable"]
                # Errors if not all keys are found
                except KeyError:
                    print("The config json file is invalid")
                    json_read_ok = False
                # Read successfully, set read_ok to true
                else:
                    json_read_ok = True
                    print("Read config successfully")

    # If reading the json didn't work
    if not json_read_ok:
        from json import dump
        from os import access, X_OK

        print("No config, require user input")

        # Prompt the user for the "newgrf" directory until we get something like it
        while not Path(newgrf_dir).exists():
            newgrf_dir = input("Enter the newgrf directory: ")
            if len(newgrf_dir) > 6:
                newgrf_dir = "~/.openttd/newgrf"
                continue
            if newgrf_dir[-6:] != "newgrf":
                newgrf_dir = "~/.openttd/newgrf"

        # Prompt the user for the executable path until we get an executable
        while not Path(executable_path).exists():
            executable_path = input("Enter the OpenTTD executable path: ")
            if not (access(executable_path, X_OK)):
                executable_path = "/usr/bin/openttd"

        # Dump the two paths to a json file for next time
        with open("build/build.json", "w") as json_data:
            data = {
                "newgrf_dir": str(newgrf_dir),
                "executable": str(executable_path)
            }
            dump(data, json_data)

    from shutil import copy
    from subprocess import Popen
    from os import devnull

    # Kill existing processes
    print("Killing existing processes")
    try:
        kill_process = Popen(kill_cmd)
        kill_process.wait()
    except:
        print("Something went wrong when trying to kill processes")

    # Copy grf
    print("Copying grf")
    copy("build/" + grf_name + ".grf", Path(newgrf_dir))

    # Run the game in it's root directory
    print("Running game\n")
    # Redirect stdout and stderr
    null = open(devnull, "w")
    Popen([executable_path, "-t", "2050", "-g"], cwd=Path(executable_path).parent, stdout=null, stderr=null)
    return 2


def main(grf_name, src_dir, lang_dir, gfx_dir, b_compile_grf, b_run_game):
    src_directory = Path("src")
    lang_directory = Path("lang")
    gfx_directory = Path("gfx")

    nml_file = ""
    has_lang_dir = False

    # Check if the project is set up properly and we have a lang directory
    has_lang_dir = check_project_structure(src_directory, gfx_directory, lang_directory)

    # Add the special files to the internal nml file
    for files in KeyFiles.keys():
        result = copy_file(src_directory.joinpath(files), nml_file)
        
        if result == -1:
            return -1
        else:
            nml_file = result

    # Get a list of all the pnml files in src
    file_list = dict()
    pnml_files = OrderedDict( [ ("Top level", list()), ("Priority", list()), ("Normal", list()), ("Append", list()) ] )
    tender_files = dict()
    special_files = dict()
    in_chain = set()

    for file in src_directory.rglob("*.pnml"):
        relative_path = file.relative_to(src_directory)
        file_name = file.stem + file.suffix # e.g. BR43.pnml

        if file.parent not in file_list.keys():
            file_list[file.parent] = list()

        if (file_name) not in KeyFiles.keys():
            file_list[file.parent].append(file)

        if file_name in SpecialOrderFiles and file_name not in in_chain:
            chain = SpecialOrderFiles.get(file_name)
            file_chain = []
            if type(chain) is str:
                in_chain.add(chain)
                file_chain.append(find_special_file(chain, src_directory))
            elif type(chain) is list:
                for cf in chain:
                    in_chain.add(cf)
                    file_chain.append(find_special_file(cf, src_directory))
            elif chain is None:
                raise RuntimeError

            special_files[file_name] = file_chain

        # sort and add the pnml files to their correct location
        if len(relative_path.parts) == 1:
            if (file_name not in KeyFiles.keys()): # filter out the KeyFiles
                pnml_files["Top level"].append(file)
        elif "priority" in relative_path.parts:
            pnml_files["Priority"].append(file)
        elif "append" in relative_path.parts:
            pnml_files["Append"].append(file)
        elif "Tenders" in file.stem:
            company_name = file.stem.rsplit("_")[0]
            tender_files[company_name] = file
        elif file_name not in KeyFiles and file_name not in in_chain:
            pnml_files['Normal'].append(file)
  

    f = lambda a: "src" if a == src_directory else "/".join(directory.parts[1:])
    for directory in file_list.keys():
        print(f"Found in directory [{f(directory)}]:")
        print([str(file.stem + file.suffix) for file in file_list[directory]])

    print("Finished finding pnml files\n")

    # iterate over all pnml files in the dictionary, and append it to the nml file
    for key, file_list in pnml_files.items():
        print(f"Starting to read {key} files")
        
        for file in sorted(file_list):
            file_name = file.stem + file.suffix

            if file_name in in_chain:
                continue

            if "Locomotive_Steam" in file.parts:
                engine_company_name = file.stem.rsplit("_")[0]
                if engine_company_name in tender_files:
                    tender_file = tender_files.pop(engine_company_name)
                    print(f"Reading Tender file: {tender_file.stem + tender_file.suffix}")
                    nml_file = copy_file(tender_file, nml_file)

            print(f"Reading {key} file: {file_name}")
            nml_file = copy_file(file, nml_file)

            if file_name in SpecialOrderFiles.keys():
                chain = special_files.get(file_name)
                if chain is not None:
                    for chain_file in chain:
                        print(f"Reading Special Order file: {chain_file.stem + chain_file.suffix}")
                        nml_file = copy_file(chain_file, nml_file)

    print("Copied all files to internal buffer\n")

    # Try to write the internal nml to a file
    if write_file(grf_name, nml_file) != 0:
        print("The nml file failed to compile")
        return -1

    # If we're compiling or running the game
    if b_compile_grf or b_run_game:
        # Try to compile the GRF
        error = compile_grf(has_lang_dir, grf_name, lang_directory)
        if error == -2:
            return -2
        elif b_run_game == False:
            return 1

    # Optionally run the game
    if b_run_game:
        return run_game(grf_name)

    return 0


if __name__ == "__main__":
    # Parser arguments
    parser = ArgumentParser(description="Compile pnml files into one nml file")
    parser.add_argument("grf_name")
    parser.add_argument("--src", default="src", help="Source files directory")
    parser.add_argument("--lang",
                        default="lang",
                        help="Language files directory")
    parser.add_argument("--gfx",
                        default="gfx",
                        help="Graphics files directory")
    parser.add_argument("--compile",
                        action="store_true",
                        help="Compile the nml file with nmlc")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the game after compilation (will also compile the file.  Also kills existing instances)")
    args = parser.parse_args()

    # Reports any errors in the nml file compilation process
    error_code = main(args.grf_name, args.src, args.lang, args.gfx,
                      args.compile, args.run)
    if error_code == -1:
        print(
            "The nml file failed to compile properly.  Please consult the log")
    elif error_code == -2:
        print("The nml file compiled correctly, but nml failed to compile it")
    elif error_code == -3:
        print(
            "The grf file compiled successfully but the game failed to start")
    elif error_code == 1:
        print("The grf file was compiled successfully")
    elif error_code == 2:
        print(
            "The grf file was compiled successfully, and the game was started")
    else:
        print("The nml file was compiled successfully (this is the not grf)")
