"""Testing utilities."""

from functools import wraps
from pathlib import Path
import tempfile


def temp_folder():
    """Create a temporary folder."""

    def inner(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwds):
            with tempfile.TemporaryDirectory() as folder:
                return fn(self, folder, *args, **kwds)

        return wrapper

    return inner


def get_dataset_path(fname):
    """Return a data asset path."""
    return Path(__file__).parent / "tests" / "data" / fname
