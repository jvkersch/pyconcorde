"""Wrapper for the Concorde TSP solver."""

from pathlib import Path
import subprocess
import tempfile

from .solution import Solution


class ConcordeError(Exception):
    """Base class for errors that happen during Concorde invocations."""


class Concorde:
    """Main entrypoint for the Concorde TSP solver."""

    def solve(self, problem, concorde_exe="concorde", extra_args=None):
        """Solve a given TSP problem.

        Parameters
        ----------
        problem : Problem
            The TSP problem to be solved.
        concorde_exe : str
            The location of the Concorde solver.
        extra_args : list or None
            Optional arguments to be passed to the Concorde solver.

        Returns
        -------
        solution : Solution
            The optimal tour that Concorde found.
        """
        extra_args = extra_args or []

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
