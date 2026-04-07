# Plan: Legacy API Fixes

This plan addresses open GitHub issues affecting the legacy `TSPSolver`/Cython
API (`concorde.tsp`, `concorde._concorde`).

## Phase 1: Fix Build Failures

**Issues:** #84, #79, #22, #78 (PR), #85 (PR)

The Cython extension currently fails to compile on several platforms due to
problems in `setup.py`.

### 1.1 Revert the `-ansi` flag (PR #85)

The `-ansi` flag was added in commit 28500a2. On modern Linux (Debian 12,
Ubuntu 22.04+) it causes `concorde.h` to conflict with system headers
(`gethostname` signature mismatch). Reverting this flag unblocks Linux builds.

**Files:** `setup.py`
**Change:** Remove `-ansi` from `cflags` in `build_concorde()`.

```python
# Before
cflags = "-fPIC -O2 -g -ansi"
# After
cflags = "-fPIC -O2 -g"
```

### 1.2 Fix macOS ARM64 build (PR #78)

On Apple Silicon, the Concorde build needs explicit `-arch arm64` and the
correct SDK sysroot. Without this, compilation succeeds but linking fails
or produces an unusable binary.

**Files:** `setup.py`
**Change:** In `build_concorde()`, detect `Darwin` + `arm64` and set
appropriate `CFLAGS`/`LDFLAGS` including `-arch arm64`, `-std=gnu89`, and
`-isysroot` pointing to the Xcode SDK.

```python
if platform.system() == "Darwin" and platform.machine() == "arm64":
    sdk_path = subprocess.check_output(
        ["xcrun", "--show-sdk-path"], text=True
    ).strip()
    cflags = f"-arch arm64 -fPIC -O2 -g -std=gnu89 -isysroot {sdk_path}"
    ldflags = f"-arch arm64 -isysroot {sdk_path}"
    flags = "--host=darwin"
else:
    ...
```

### 1.3 Verify builds in CI

**Files:** `.github/workflows/run-unittests.yml`
**Change:** Extend the Python version matrix to include 3.12 and 3.13. Add a
macOS ARM64 runner (`macos-latest`) in addition to `ubuntu-latest`.

---

## Phase 2: Input Validation in `TSPSolver.from_data`

**Issues:** #29, #27, #63, #33, #35

These issues all stem from the same root cause: Concorde operates on integer
distances internally, but the legacy API passes user-supplied floating-point
coordinates through without validation. This causes:

- Coordinates in [0, 1] → truncated to 0 → `optimal_value = 0` (#29)
- Coordinates at 1e9 scale → integer overflow → segfault (#33, #35)
- Misleading results when using `GEO` norm with non-geographic data (#27, #63)

### 2.1 Add coordinate range warnings

**Files:** `concorde/tsp.py`
**Change:** In `TSPSolver.from_data`, check coordinate ranges and warn:

- If all coordinates fall within [-1, 1], emit a `UserWarning` advising to
  scale up (e.g. multiply by 1e6) since Concorde uses integer arithmetic.
- If any coordinate exceeds 1e7 in absolute value, emit a `UserWarning` about
  potential overflow and suggest scaling down.

```python
import warnings

@classmethod
def from_data(cls, xs, ys, norm, name=None):
    xs, ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    max_abs = max(np.max(np.abs(xs)), np.max(np.abs(ys)))
    min_abs = max(np.max(np.abs(xs)), np.max(np.abs(ys)))

    if max_abs <= 1.0:
        warnings.warn(
            "All coordinates are in [-1, 1]. Concorde uses integer "
            "distances internally, so small coordinates will be "
            "truncated to 0. Consider scaling your coordinates "
            "(e.g. multiply by 1e6).",
            UserWarning,
            stacklevel=2,
        )
    if max_abs > 1e7:
        warnings.warn(
            "Coordinates exceed 1e7. Large values may cause integer "
            "overflow in Concorde, leading to incorrect results or "
            "crashes. Consider scaling down.",
            UserWarning,
            stacklevel=2,
        )
    ...
```

### 2.2 Validate norm usage

**Files:** `concorde/tsp.py`
**Change:** When `norm="GEO"` or `norm="GEOM"`, check that coordinates are
plausible as geographic (latitude/longitude) values. Warn if they are not.

```python
if norm in ("GEO", "GEOM"):
    if np.any(np.abs(xs) > 180) or np.any(np.abs(ys) > 180):
        warnings.warn(
            f"norm={norm!r} expects geographic coordinates "
            "(latitude/longitude) but values exceed 180. "
            "Consider using 'EUC_2D' for Euclidean distances.",
            UserWarning,
            stacklevel=2,
        )
```

### 2.3 Add tests for validation

**Files:** `concorde/tests/test_concorde_datagroup.py` (or new file)
**Change:** Add tests verifying that warnings are emitted for small
coordinates, large coordinates, and misused geographic norms.

---

## Phase 3: Clean Up Temp Files

**Issue:** #44

### 3.1 Run solver in a temporary directory

**Files:** `concorde/tsp.py`
**Change:** In `TSPSolver.solve`, change into a temporary directory before
calling `_CCtsp_solve_dat`, then change back and clean up. This prevents
`.res` files from accumulating in the user's working directory.

The Cython function `_CCtsp_solve_dat` writes files relative to `cwd`, so
we need to `os.chdir` around the call.

```python
def solve(self, time_bound=-1, verbose=True, random_seed=0):
    name = str(uuid.uuid4().hex)[0:9]
    original_dir = os.getcwd()
    try:
        tmpdir = tempfile.mkdtemp()
        os.chdir(tmpdir)
        res = _CCtsp_solve_dat(
            self._ncount, self._data, name, time_bound,
            not verbose, random_seed
        )
    finally:
        os.chdir(original_dir)
        shutil.rmtree(tmpdir, ignore_errors=True)
    return ComputedTour(*res)
```

### 3.2 Add test for temp file cleanup

**Files:** `concorde/tests/test_concorde_datagroup.py`
**Change:** Add a test that runs `solver.solve()` and verifies no `.res`
files are left in the working directory afterward.

---

## Phase 4: Update CI Matrix

**Issue:** General maintenance to prevent regressions.

**Files:** `.github/workflows/run-unittests.yml`
**Changes:**
- Update Python matrix: `["3.9", "3.10", "3.11", "3.12", "3.13"]`
  (drop 3.7/3.8 which are EOL).
- Add `macos-latest` (ARM64) to the `runs-on` matrix.
- Update `actions/checkout` and `actions/setup-python` from `v2` to `v4`.

---

## Implementation Order

1. **Phase 1.1** — Revert `-ansi` flag. Smallest change, unblocks most users.
2. **Phase 3** — Temp file cleanup. Self-contained, no API changes.
3. **Phase 2** — Input validation. Addresses the largest cluster of issues.
4. **Phase 1.2** — macOS ARM64 fix. Requires testing on Apple Silicon.
5. **Phase 4** — CI updates. Do last so earlier changes can be validated.

Each phase should be a separate PR.

## Out of Scope

- **#4 (Windows support):** The legacy Cython API requires compiling C
  libraries with `./configure && make`, which is fundamentally incompatible
  with Windows. Windows support should come through the new subprocess API
  (issues #56–#58) instead.
- **#68 / #20 (distance matrix input):** Already supported by the new API
  (`Problem.from_matrix`). Not worth adding to the legacy API.
- **#72 (restrict to Lin-Kernighan):** Feature request for Concorde
  configuration, not a bug.
- **#73 (initial solution):** Feature request, not a bug.
