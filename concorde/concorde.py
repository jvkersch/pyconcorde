"""Wrapper for the Concorde TSP solver."""

from pathlib import Path
import platform
import subprocess
import tempfile

from .solution import Solution


class ConcordeError(Exception):
    """Base class for errors that happen during Concorde invocations."""


class Concorde:
    """Main entrypoint for the Concorde TSP solver."""

    def solve(self, problem, concorde_exe=None, extra_args=None):
        """Solve a given TSP problem.

        Parameters
        ----------
        problem : Problem
            The TSP problem to be solved.
        concorde_exe : str or None
            The location of the Concorde solver. If ``None``, use the
            Concorde binary provided with this package.
        extra_args : list or None
            Optional arguments to be passed to the Concorde solver.

        Returns
        -------
        solution : Solution
            The optimal tour that Concorde found.
        """
        extra_args = extra_args or []
        concorde_exe = concorde_exe or find_concorde_binary()

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            tsp_fname = tmp / "problem.tsp"
            problem.to_tsp(tsp_fname)

            cmd = [concorde_exe] + extra_args + [tsp_fname]
            try:
                res = subprocess.run(
                    cmd, cwd=tmp, capture_output=True, check=True, text=True
                )
            except subprocess.CalledProcessError as e:
                raise ConcordeError() from e

            solution = Solution.from_file(tmp / "problem.sol", output=res.stdout)
            return solution


_PLATFORM_MAP = {
    ("Linux", "x86_64"): "linux",
    ("Darwin", "x86_64"): "macos/x86_64",
    ("Darwin", "arm64"): "macos/arm64",
}


def find_concorde_binary():
    """Return location of concorde binary for the current platform."""
    project_dir = Path(__file__).parent.parent
    pyconcorde_binaries = project_dir / "external" / "pyconcorde-build" / "binaries"
    if pyconcorde_binaries.exists():
        # Git checkout, with pyconcorde-build as git subtree
        location = _PLATFORM_MAP[(platform.system(), platform.machine())]
        concorde_exe = pyconcorde_binaries / location / "concorde"
    else:
        # Not a Git checkout. Assume that we're working from a wheel, with a
        # platform-specific concorde located in the module.
        concorde_exe = project_dir / "concorde" / "concorde"
    return concorde_exe
