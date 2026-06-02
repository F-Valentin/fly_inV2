*This project has been created as part of the 42 curriculum by vafechte.*

# Fly-in — Drone Routing Simulation

## Description

Fly-in is a drone fleet routing system that navigates multiple drones through a network of connected zones, moving them all from a start hub to an end hub in the fewest possible simulation turns.

The network is defined in a plain-text map file: zones carry properties (normal, restricted, priority, blocked), connections between zones carry capacity limits, and both zones and connections can be given color metadata for visual output. The program parses that file, finds all viable paths using depth-first search, distributes drones across those paths to balance load, then runs a discrete turn-based simulation to completion.

The key challenge is not just finding paths — it is scheduling drone movement so that zone capacities (`max_drones`) and connection capacities (`max_link_capacity`) are never violated, restricted zones (which cost 2 turns to enter) are handled correctly, and the total number of turns is minimized.

## Instructions

### Requirements

- Python 3.10 or later
- No external graph libraries (networkx, graphlib, etc.)

### Installation

```bash
make install
```

This installs any project dependencies via pip.

### Running

```bash
make run
```

Executes `fly_in.py` with the map file configured inside it.

To change the active map, edit the `file_path` list in `fly_in.py` and uncomment the desired map path.

### Debug mode

```bash
make debug
```

Runs the simulation through Python's built-in `pdb` debugger.

### Lint

```bash
make lint
```

Runs `flake8 .` and `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`.

```bash
make lint-strict   # optional — runs mypy . --strict
```

### Clean

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, and other generated artifacts.

### Map file format

```
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
connection: hub-roof1
connection: hub-corridorA
connection: corridorA-goal [max_link_capacity=2]
```

Zone types: `normal` (cost 1), `restricted` (cost 2), `priority` (cost 1, preferred), `blocked` (impassable).  
All metadata fields are optional. Zone names may not contain dashes or spaces.

## Algorithm

### Pathfinding — DFS (Solver)

All paths from the start hub to the end hub are found using a recursive depth-first search. Blocked zones are pruned immediately. The visited-zone set is maintained per-branch (added on descent, removed on backtrack), so every simple path through the graph is enumerated without revisiting a zone within a single path. This exhaustive enumeration is deliberate: with the graph sizes in scope, completeness matters more than early termination.

### Path scoring and sorting

Each discovered path is scored by two criteria, applied in order:

1. **Cost** — the sum of zone traversal costs along the path (restricted zones contribute 2, all others 1). Lower cost paths move drones to the destination faster.
2. **Priority zone count** — among paths with equal cost, those passing through more `priority` zones are preferred (they are sorted by descending priority count as a tiebreaker).

Paths are sorted by `(cost, -nb_of_priority_zones)` before drone assignment.

### Drone distribution (Path)

Drones are distributed across sorted paths to balance throughput. The logic works left-to-right through the sorted path list: for each path, drones are appended until adding one more would make this path's effective cost exceed the next path's cost. This keeps the cheaper path from being overloaded while the more expensive path sits empty. Any remaining drones after the main pass are round-robined across all paths. A per-path bottleneck (`find_min_max_drones`) caps assignment at the tightest zone capacity on that path.

### Simulation (Simulation)

The simulation runs in discrete turns. Each turn has two phases, in order:

1. **Arrivals** — drones in transit have their `waiting_turn` decremented. Those that reach zero land at their destination zone (incrementing `nb_drones`) and are removed from their connection's transit list. Drones that land at the end hub are removed from the active set entirely.

2. **Departures** — ready drones (status `"move"`, path length > 1) attempt to move to their next zone. A move is blocked if: the destination zone is already at capacity (counting both occupants and in-transit drones heading there), or the connection between start and destination is at capacity. If the move is allowed, the drone enters `"waiting"` status, is placed on the connection, and its `waiting_turn` is set to the destination's traversal cost (1 for normal/priority, 2 for restricted). The source zone's `nb_drones` is decremented immediately, freeing space for other drones on the same turn.

This two-phase ordering (arrivals before departures) ensures that a zone a drone just vacated can be filled by another drone in the same turn, maximising throughput.

### Complexity notes

- DFS path enumeration is exponential in the worst case (all simple paths), but graph sizes in this project are small and the result is cached once before the simulation begins — there is no re-computation during the simulation loop.
- The simulation loop is O(T × D × P) where T is the number of turns, D the number of drones, and P the number of active connections, all of which are small in practice.
- Memory usage is proportional to the number of paths × average path length, which is manageable for the provided maps.

## Visual Representation

Terminal output is produced each turn in two layers:

**Movement line** — all drone departures for that turn are printed space-separated in the format `D<id>-<zone>` (normal moves) or `D<id>-<start>-<dest>` (moves toward restricted zones, where the connection is shown). This matches the required simulation output format exactly.

**Zone state block** — after the movement line, each zone that currently holds at least one non-waiting drone is printed with its occupants listed. Active connections with drones in transit are also printed (`start->dest (in transit): [D0, D1, ...]`).

**Colors** — when a zone has a `color` metadata field, its name and drone movements are wrapped in the corresponding ANSI escape code and reset. This makes it easy to visually distinguish zone types and paths at a glance in a color-capable terminal. The full set of supported color names is defined in `colors.py`.

## Resources

### Graph algorithms and pathfinding
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — DFS and graph traversal foundations
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### AI usage

Claude (Anthropic) was used during this project for the following:

- **Understanding the subject** — asking questions about the simulation rules, particularly around the two-phase turn model and restricted zone transit semantics.
- **Reviewing design decisions** — discussing the drone distribution algorithm and the tradeoffs between greedy assignment and round-robin fallback.
- **Writing this README** — the README was drafted with Claude's assistance based on the actual source code and subject document.

All AI-generated content was read, understood, and verified before being included. No code was copied from AI output without full comprehension.
