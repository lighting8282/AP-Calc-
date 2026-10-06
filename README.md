# AP Calc — Archipelago world

The [Archipelago](https://archipelago.gg) multiworld randomizer world for
**AP Calc**, a calculator puzzle game made in Unity. A target number appears
and you build an equation that equals it from the keys you have. In
Archipelago every key is an item: you start with three digits and one
operator, and the rest of the calculator — up to trig and calculus — comes
from the multiworld.

> **Status:** the world generates seeds and installs on Archipelago 0.6.7, and
> the game connects to servers (tested end to end against a live server with
> another game in the room). No public release of the game yet.

## Install

1. Build `apcalc.apworld` (see Development, below). Releases with a ready-made
   file will start alongside the first public build of the game.
2. Double-click it, or copy it into Archipelago's `custom_worlds` folder.
3. In the Archipelago Launcher, run **Generate Template Options** and edit
   `AP Calc.yaml`.

To play, the game's main menu has an **Archipelago** button on the save note:
enter the server, slot name and password and connect. The full steps are in
[the setup guide](apcalc/docs/setup_en.md).

## Options

| Option | Default | |
|---|---|---|
| `goal_count` | 50 | equations to solve (20–100) |
| `equation_checks` | every | `every_other` halves the equation checks |
| `tier_order` | sequential | logic expects Medium before Hard before AP; `any` drops the chain |
| `funny_number_chance` | 10 | % chance a target is an unsolved funny number |
| `trap_chance` | 15 | % of filler replaced by traps |

## Checks (about goal + 44)

- **Equation 1 … N**: every solve up to the goal (or every other one)
- **First Solve Using …**: the first correct answer using each of the 34 keys
- **First Hint / Skip / Freebie Used**
- **Funny Number 67, 69, 420, 666, 777, 1337, 80085**: excluded, filler and traps only

## Items

| | |
|---|---|
| Progression | Medium / Hard / AP Difficulty; the 34 keys (`Digit 7`, `Operator +`, `Function sin` …); the first Hint, Skip and Freebie |
| Useful | Progressive Magnitude ×6, Progressive Decimal ×2, Negative Numbers, Card Pack, Streak Saver, extra Freebies |
| Filler | 100 / 250 Extra Credit, Pep Talk, Confetti, extra Hints and Skips |
| Traps | Freeze, Dessert, Invisibility, Clear Equation, Locked Operator |

A key works once both its own item and its tier's item have arrived. Three
digits and one of `+ - *` are given at the start.

## Development

The game's `APItems.cs` and `APLocations.cs` are the source of truth for names
and ids. `apcalc/data.py` mirrors them, and `test_data` checks the mirror
against `apcalc/test/unity_tables.json`, exported from the game by running
`tools/export_unity_tables.cs` in the Unity editor.

Work from an Archipelago **source** checkout with this folder linked in as
`worlds/apcalc`, using that checkout's virtual environment:

    SKIP_REQUIREMENTS_UPDATE=1 python -m unittest discover -s worlds/apcalc/test -t . -p "test_*.py"
    python Generate.py --player_files_path "<this repo>/tests/yaml/multi" --spoiler 2
    python tools/build_apworld.py          # -> dist/apcalc.apworld

| | |
|---|---|
| `apcalc/` | the world: data, options, items, locations, rules, docs, tests |
| `tools/build_apworld.py` | packages a reproducible, verified `dist/apcalc.apworld` |
| `tools/export_unity_tables.cs` | refreshes `unity_tables.json` from the game |
| `tests/yaml/` | solo and 4-player yamls for real generations |

## License

[MIT](LICENSE)
