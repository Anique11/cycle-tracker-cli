#README file accompanying the cycle utility.

## Configuration
The script expects a cycle_config.json to exist in ~/.cycle/
This file should follow the structure of the example file provided.
The values in the config are:
- `cycles_file`: full path to the file where the cycle info is stored.    
  If this file does not exist, most functions of the script will throw an error.  
  However, setting a start day will work and this will create the file.
- `avg_cycle_length`: this controls the date that will be given for the expected next cycle.
- `locale`: this controls the language in which dates are displayed; the rest of the program text is still in English only.

## Usage
- `cycle.py` Outputs a simple count of the current cycle day as 'CD: nn'
- `cycle.py -s` or `cycle.py --start` Sets a new cycle start day, using today as date. You will be prompted to confirm.
- `cycle.py -s N` or `cycle.py --start N` Sets a new cycle start day, using N days ago as date. You will be prompted to confirm.
- `cycle.py -p` or `cycle.py --plan` Outputs the expected next cycle start day, based on the average cycle length.

## ToDo
- Enable 'calculate' as `avg_cycle_length` setting, which will calculate using the last full cycles available (max. 6 cycles).
- Build a backup function that will store the current values in cycles.txt in cycles.bak
- Build an archive function that will store all but the last 6 cycles in cycles.archive
- Extend automated archiving that will trigger archiving as soon as cycles.txt holds more than 6 cycles.
- (Wishlist) Enable flow tracking.
- (Wishlist) Enable Luteal Phase tracking and planning.
