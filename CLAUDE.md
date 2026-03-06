# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyConcorde is a Python wrapper around the [Concorde TSP solver](http://www.math.uwaterloo.ca/tsp/concorde.html). It provides two APIs for solving Traveling Salesman Problems.

## Build & Development

```bash
# Install in editable mode (downloads and builds Concorde + QSOpt automatically on first run)
pip install -e .

# Run all tests
python -m unittest discover -v .

# Run a single test file
python -m unittest concorde.tests.test_concorde -v

# Run a single test
python -m unittest concorde.tests.test_concorde.TestConcorde.test_solve -v
```

No separate lint or type-check tooling is configured.

Set `CONCORDE_DIR` and `QSOPT_DIR` environment variables to use pre-installed Concorde/QSOpt instead of downloading.

## Architecture

There are two parallel APIs:

### New API (`concorde.concorde`, `concorde.problem`, `concorde.solution`)
- **`Concorde`** — invokes the Concorde binary as a subprocess
- **`Problem`** — wraps `tsplib95` to create TSP problems from coordinates, distance matrices, or `.tsp` files
- **`Solution`** — parses Concorde's `.sol` output files, extracts optimal value and running time
- The Concorde binary is located via `find_concorde_binary()` which checks `external/pyconcorde-build/binaries/` (git checkout) or falls back to a bundled binary (wheel install)

### Legacy API (`concorde.tsp`)
- **`TSPSolver`** — uses Cython bindings (`concorde/_concorde.pyx`) to call Concorde's C library directly
- Returns `ComputedTour` namedtuple with tour, optimal value, and status flags
- The Cython extension links against `concorde.a` and `qsopt.a` static libraries

### Key files
- `setup.py` — custom build that downloads QSOpt and compiles Concorde from source, then builds the Cython extension
- `concorde/_concorde.pyx` — Cython bridge to Concorde's C API
- `concorde/util.py` — TSP file writing utilities and `EDGE_WEIGHT_TYPES` constants
- `concorde/testing.py` — test helpers (`temp_folder` decorator, `get_dataset_path`)
- Test data lives in `concorde/tests/data/`
