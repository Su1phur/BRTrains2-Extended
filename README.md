# BR Extended Train Set
A UK Train Set addon (newGRF) for OpenTTD, featuring UK rail (train and tram) rolling stock from the entire history of the British Railway Network.

This is an 4x zoom, 32bpp, extra-long train set, designed with a focus on real-world consists and liveries first, and aim to be able to recreate the UK rail network in game. 

### Main Goals
- Extra length, 4x zoom, 32bpp train set with comprehensive unit selection across the ages (1850-modern day) (early versions may not support the entire age)
- Speed options (operation VS potential/achieved speeds)
- Customizable multiple unit consists

#### Potentially...
- 2CC Unit variants
- Unit bonuses (Passengers in express vehicles pay more)
- Coupling restrictions options (Brake vans, MU working)

## Tracking table
To track vehicles planned, current progress and other statistics, please refer to the following spreadsheet. Correcting or providing additional information and diagrams for tracked or new vehicles are welcome.
https://docs.google.com/spreadsheets/d/1RACfDDpuTNXPyaUC5tNg7-STm_maQqCuw_r31gAB8eU/edit?usp=sharing

### Credits (In no particular order)

### Developers
- Su1phur

### With special thanks to:
- Timberwolf, for creating and providing the Voxel-to-Sprite Toolchain.
- GarlicBread42 and the GETS Team, for their assistance, knowledge and models.
- Audigex and the BRTrainsV2 Team, for without their inspiration and support this set would not have started.

### To Build
Building from the source should be mostly automated using the `build.py` script, but it has a few requirements:
  - Python 3.8+
  - `nml` Python package (available through `pip`)
  
To build the grf completely, just run the following command in your terminal:
```bash
python build.py --compile brtrainsv2XL
```
This should first compile the `.nml` file, then compile that through to a `.grf` file using `nml`.  Install in the same manner as previously described, copying the generated `.grf` file into `OpenTTD/newGRF`.

Note, this method still requires the `nml` python package to be installed.

To build the grf, and initiate the game with the compiled `.grf`, run:
```bash
python build.py --compile brtrainsv2XL --run 
```
This moves the compiled `.grf` to your `Documents/OpenTTD/newgrf`, then looks for and executes `C:/Program Files/OpenTTD/openttd.exe"`.

You may be prompted to provide a path to any `openttd.exe`, if one is not located. After being provided, the configured path will be stored in `build/build.json`. Subsequent executions will be pathed to said stored `openttd.exe`.

### License
This project is licensed under the GPLv2 license
See [LICENSE](./LICENSE) for license details
